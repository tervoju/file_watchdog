import logging
import time
import os
import json

from pathlib import Path

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from watchdog.events import RegexMatchingEventHandler

# config_file modification

# counter for triggers - just for noting the duplicated triggering
cnt = 0

# check if there is "create" True in config file
def checkCreeteHydro(config_file):
    create = False
    samples = 0
    pause = 0
    count = 0
    config = {"create": False, "samples":200000, "pause":0, "count":0}
    try:
        # Opening JSON file
        f = open(config_file)
        # returns JSON object as  a dictionary
        data = json.load(f)
        if data['create'] == True:
            ret = True
            config = data
        # Closing file
        f.close()
    except:
        logging.info("fails to read config file")

    return config


class FileChangeHandler(RegexMatchingEventHandler):

    def on_modified(self, event):
        global cnt 
        print(f'event type: {event.event_type}  path : {event.src_path}, cnt: {cnt}')
        # this should trigger the event for configuration change
        cnt = cnt + 1
        # read file 
        to_be_recorded = checkCreeteHydro(event.src_path)
        print(f'create: {toberecorded}')
        # check if create 
        if to_be_recorded['create']:
            logging.info("to be recorded")

class Watcher:
    def __init__(self, basepath, patterns):
        self.dir = basepath
        self.paths = [os.path.join(self.dir, p) for p in patterns]
        self.observer = Observer()

    def run(self):
        logging.info(f"Starting watcher on {self.dir}")
        event_handler = FileChangeHandler(regexes=['.*/hydro_config.json'])
        self.observer.schedule(event_handler, path=self.dir, recursive=False)
        self.observer.start()

        try:
            while self.observer.is_alive():
                self.observer.join()
        finally:
            self.observer.stop()
            self.observer.join()

if __name__ == "__main__":
    CONFIG_FOLDER = "/home/jte/Development/filechange"
    watcher = Watcher(CONFIG_FOLDER, ["hydro_config.json"])
    watcher.run()
