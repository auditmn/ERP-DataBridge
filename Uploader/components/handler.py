import logging
from watchdog.events import FileSystemEventHandler, FileSystemEvent, EVENT_TYPE_CREATED, EVENT_TYPE_MODIFIED, EVENT_TYPE_DELETED, EVENT_TYPE_MOVED
from components.event_handlers import handle_created, handle_modified, handle_deleted, handle_moved
from components.file_index import FileIndex

logger = logging.getLogger(__name__)

class MyHandler(FileSystemEventHandler):
    def __init__(self):
        super().__init__()
        self.index = FileIndex()
        self._handlers = {
            EVENT_TYPE_CREATED: handle_created,
            EVENT_TYPE_MODIFIED: handle_modified,
            EVENT_TYPE_DELETED: handle_deleted,
            EVENT_TYPE_MOVED: handle_moved
        }
        logger.info("MyHandler initialized with SQLite-based hash tracking")

    def on_any_event(self, event: FileSystemEvent):
        if event.is_directory:
            return

        handler = self._handlers.get(event.event_type)
        if not handler:
            return

        path = getattr(event, 'dest_path', event.src_path) if event.event_type == EVENT_TYPE_MOVED else event.src_path

        # Cleanup old events
        self.index.cleanup_old_entries()

        if event.event_type == EVENT_TYPE_DELETED:
            handler(event)
        else:
            if self.index.should_process(path):
                handler(event)
            else:
                logger.debug(f"Skipped duplicate event for: {path}")