import time
import logging
from watchdog.observers import Observer
from components.handler import MyHandler
from components.logger_config import setup_logging

if __name__ == "__main__":
    setup_logging()
    logger = logging.getLogger(__name__)

    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path='demo', recursive=True)

    logger.info("Starting file system observer for directory 'demo'...")
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("KeyboardInterrupt received. Stopping observer...")
        observer.stop()
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
    finally:
        logger.info("Observer joining...")
        observer.join()
        logger.info("Observer stopped gracefully.")