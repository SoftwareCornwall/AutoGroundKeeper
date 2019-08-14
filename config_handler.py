# -*- coding: utf-8 -*-
# pylint: disable=C0111

import json
import time
import os


class ConfigHandler:
    def __init__(self, config_file='succulent.json'):
        self.file_location = config_file
        self.load(self.file_location)
        self.disable_reload = False

    def load(self, config_file):
        with open(self.file_location) as file:
            self.data = json.load(file)
        self.last_loaded = time.time()

    def reload_if_modified(self):
        if not self.disable_reload and os.path.getmtime(
                self.file_location) > self.last_loaded:
            self.load()

    def __getitem__(self, key):
        try:
            return self.data[key]
        except KeyError:
            return None

    def run(self, scheduler, name):
        self.reload_if_modified()
        scheduler.add_to_schedule(name, time.time() + 5)
