
from mmap import mmap
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from time import time
import numpy as np
import os
import logging



class Watcher:
    def __init__(self, basepath, patterns):
        self.dir = basepath
        self.paths = [os.path.join(self.dir, p) for p in patterns]
        self.observer = Observer()

    def run(self):
        logging.info(f"Starting watcher on {self.dir}")
        event_handler = Handler(patterns=self.paths)
        self.observer.schedule(event_handler, path=self.dir, recursive=True)
        self.observer.start()

        try:
            while self.observer.is_alive():
                self.observer.join()
        finally:
            self.observer.stop()
            self.observer.join()


class Handler(PatternMatchingEventHandler):
    @staticmethod
    def on_created(event):
        file_path = event.src_path
        logging.info("{}:{}".format("file created", file_path))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    CONFIG_FOLDER = "/home/jte/Development/filechange"
    watcher = Watcher(CONFIG_FOLDER, ["*"])
    watcher.run()




