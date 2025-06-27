from components.MyHandler import MyHandler
from watchdog.observers import Observer
import time
from watchdog.events import EVENT_TYPE_CREATED, EVENT_TYPE_MODIFIED



if __name__ == "__main__":
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path='demo', recursive=True, event_filter=[EVENT_TYPE_MODIFIED, EVENT_TYPE_CREATED])
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()