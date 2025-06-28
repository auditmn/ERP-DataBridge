
import sqlite3
import hashlib
import os
import logging

logger = logging.getLogger(__name__)

_HASH_READ_LIMIT_BYTES = 1024 * 1024  # 1 MB

class FileIndex:
    def __init__(self, db_path: str ='file_index.db'):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self._create_table()
        logger.info(f"FileIndex initialized with database: {db_path}")

    def _create_table(self):
        with self.conn:
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS file_events (
                    path TEXT,
                    last_hash TEXT,
                    last_processed_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')

    def _calculate_hash(self, filepath: str) -> str | None:
        """
        Calculates a SHA256 hash of the file content.

        To optimize for large files, this method uses a sampling strategy:
        - For files > 2MB, it hashes the first 1MB and the last 1MB.
        - For files <= 2MB, it hashes the entire content.

        This is a performance trade-off: it's very fast but may not detect
        changes made exclusively in the middle of very large files.

        Returns the hex digest of the hash, or None if the file cannot be read.
        """
        hasher = hashlib.sha256()
        try:
            file_size = os.path.getsize(filepath)
            with open(filepath, 'rb') as f:
                first_part = f.read(_HASH_READ_LIMIT_BYTES)
                hasher.update(first_part)

                # If the file is larger than 2MB, sample the end. Otherwise, hash the rest.
                if file_size > 2 * _HASH_READ_LIMIT_BYTES:
                    f.seek(-_HASH_READ_LIMIT_BYTES, os.SEEK_END)
                    last_part = f.read(_HASH_READ_LIMIT_BYTES)
                    hasher.update(last_part)
                elif file_size > _HASH_READ_LIMIT_BYTES:
                    hasher.update(f.read())
        except IOError as e:
            logger.error(f"Error reading file {filepath} for hashing: {e}")
            return None # Or raise an exception, depending on desired error handling
        return hasher.hexdigest()

    def should_process(self, path: str) -> bool:
        if not os.path.exists(path):
            return True # Always process if file doesn't exist (e.g., deleted event)

        current_hash = self._calculate_hash(path)
        cur = self.conn.cursor()
        cur.execute('''
            SELECT last_hash FROM file_events WHERE path = ?
        ''', (path,))
        result = cur.fetchone()

        if result is None:
            # First time seeing this file, record and process
            with self.conn:
                self.conn.execute('''
                    INSERT INTO file_events (path, last_hash) VALUES (?, ?)
                ''', (path, current_hash))
            logger.debug(f"New file detected: {path}. Processing.")
            return True
        else:
            last_hash = result[0]
            if last_hash == current_hash:
                # Hash hasn't changed, skip processing
                logger.debug(f"File {path} hash unchanged. Skipping.")
                return False
            else:
                # Hash changed, update and process
                with self.conn:
                    self.conn.execute('''
                        UPDATE file_events SET last_hash = ?, last_processed_timestamp = CURRENT_TIMESTAMP WHERE path = ?
                    ''', (current_hash, path))
                logger.debug(f"File {path} hash changed. Processing.")
                return True

    def remove_entry(self, path: str):
        with self.conn:
            self.conn.execute('DELETE FROM file_events WHERE path = ?', (path,))
            logger.debug(f"Removed entry for {path} from index.")

    def cleanup_old_entries(self, max_age_minutes: int = 1440): # Default to 24 hours
        with self.conn:
            self.conn.execute(f'''
                DELETE FROM file_events
                WHERE last_processed_timestamp < datetime('now', '-{max_age_minutes} minutes')
            ''')
            logger.debug(f"Cleaned up entries older than {max_age_minutes} minutes.")
