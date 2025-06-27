import threading
from watchdog.events import FileSystemEventHandler, FileSystemEvent

class MyHandler(FileSystemEventHandler):
    def __init__(self, debounce_delay: float = 1.0):
        super().__init__()
        self._delay = debounce_delay
        self._timers: dict[str|bytes, threading.Timer] = {}

        # Mapping event type string to handler methods
        self._handlers = {
            "created": self._handle_created,
            "modified": self._handle_modified,
            "deleted": self._handle_deleted,
            "moved": self._handle_moved
        }

    def _handle_created(self, event: FileSystemEvent):
        pass

    def _handle_modified(self, event: FileSystemEvent):
        pass

    def _handle_deleted(self, event: FileSystemEvent):
        pass

    def _handle_moved(self, event: FileSystemEvent):
        pass

    def on_any_event(self, event: FileSystemEvent):
        if event.is_directory:
            return

        handler = self._handlers.get(event.event_type)
        if not handler:
            return

        path = getattr(event, 'dest_path', event.src_path) if event.event_type == "moved" else event.src_path

        if path in self._timers:
            self._timers[path].cancel()

        def run_and_cleanup():
            handler(event)
            self._timers.pop(path, None)

        timer = threading.Timer(self._delay, run_and_cleanup)
        self._timers[path] = timer
        timer.start()