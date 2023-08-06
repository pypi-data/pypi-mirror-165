import time

import watchdog.events
import watchdog.observers


class Handler(watchdog.events.PatternMatchingEventHandler):
    def __init__(self):
        # Set the patterns for PatternMatchingEventHandler
        patterns = [
            '*NavCam*',
            '*/*.tif*',
            '*.pdf'
        ]
        watchdog.events.PatternMatchingEventHandler.__init__(self, patterns=patterns,
                                                             ignore_directories=False, case_sensitive=False)

    def on_created(self, event):
        print("Watchdog received created event - % s." % event.src_path)
        # Event is created, you can process it now

    def on_modified(self, event):
        print("Watchdog received modified event - % s." % event.src_path)
        # vent is modified, you can process it now

    def on_moved(self, event):
        print("Watchdog received a moved event from {} to {}".format(
            event.src_path, event.dest_path))

    def on_deleted(self, event):
        print('Watchdog received a delete event from {}'.format(event.src_path))


if __name__ == "__main__":
    src_path = r"S:\autologbook-dev\autologbook-watchdog-dev\examples"
    event_handler = Handler()
    observer = watchdog.observers.Observer()
    observer.schedule(event_handler, path=src_path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
