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
        self._keep_running = True

    def register_task(self, name, function, args=()):
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

    def run_scheduler(self):
        while self._keep_running:
            self.run_tasklist_once()
            time.sleep(0.5)

    def stop_scheduler(self):
        '''Schedule this function to time when program should stop'''
        self._keep_running = False