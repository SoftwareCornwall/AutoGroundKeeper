# -*- coding: utf-8 -*-
import time


class MoistureCheck:
    def __init__(self, config, sensors):
        self._config = config
        self._moisture_sensor = sensors
        self._last_water = time.time()
        self._moisture_level = 0

    def _should_water(self):
        self._moisture_level = self._moisture_sensor.get_moisture_a2d()
        if (self._moisture_level < self._config['moisture_level_threshold']):
            self._last_water = time.time()
            # call watering function
            return self._config['interval']
        else:
            return self._config['check_frequency']

    def run(self, scheduler, name):
        wait_time = self._should_water()

        scheduler.add_to_schedule(name, time.time() + wait_time)
