# -*- coding: utf-8 -*-
# pylint: disable=C0111

import json
import time
import os


class ConfigHandler:
    def __init__(self):
        self.load()

    def load(self):
        with open('config.json') as file:
            self.data = json.load(file)
        self.last_loaded = time.time()

    def reload_if_modified(self):
        if os.path.getmtime('config.json') > self.last_loaded:
            self.load()
