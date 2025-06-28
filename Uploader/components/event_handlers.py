import logging
from watchdog.events import FileSystemEvent

logger = logging.getLogger(__name__)

def handle_created(event: FileSystemEvent):
    logger.info(f"Detected CREATED event: {event.src_path}")
    # Add your file creation logic here

def handle_modified(event: FileSystemEvent):
    logger.info(f"Detected MODIFIED event: {event.src_path}")
    # Add your file modification logic here

def handle_deleted(event: FileSystemEvent):
    logger.info(f"Detected DELETED event: {event.src_path}")
    # Add your file deletion logic here

def handle_moved(event: FileSystemEvent):
    logger.info(f"Detected MOVED event: From {event.src_path} to {event.dest_path}")
    # Add your file movement logic here