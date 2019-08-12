#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 12 12:42:41 2019

@author: pi
"""

import time


class Scheduler:
    def __init__(self):
        self.tasks = dict()
        self.schedule = set()

    def register_task(self, name, function, args):
        self.tasks[name] = (function, args)

    def add_to_schedule(self, name, next_run_time):
        self.schedule.add((name, next_run_time))

    def run_tasklist_once(self):
        tasks_to_remove = []
        for (name, next_run_time) in list(self.schedule):
            if next_run_time < time.time():
                (function, args) = self.tasks[name]
                function(*args)
                tasks_to_remove.append((name, next_run_time))
        for item in tasks_to_remove:
            self.schedule.remove(item)
