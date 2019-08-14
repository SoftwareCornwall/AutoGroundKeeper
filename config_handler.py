# -*- coding: utf-8 -*-
# pylint: disable=C0111

import json
import time
import os


class ConfigHandler:
    def __init__(self):
        self.file_location = self.get_user_preferences()
        self.load(self.file_location)
        self.disable_reload = False

    def load(self, config_file):
        with open(config_file) as file:
            self.data = json.load(file)
        self.last_loaded = time.time()

    def reload_if_modified(self):
        if not self.disable_reload and os.path.getmtime(
                self.file_location) > self.last_loaded:
            self.load(self.file_location)

    def __getitem__(self, key):
        try:
            return self.data[key]
        except KeyError:
            return None

    def run(self, scheduler, name):
        self.reload_if_modified()
        scheduler.add_to_schedule(name, time.time() + 5)

    def get_user_preferences(self):
        with open('user_preferences.json') as file:
            config = json.load(file)
        return config['Plant_Type']
