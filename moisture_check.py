# -*- coding: utf-8 -*-
import time
import sensor_control


class MoistureCheck:
    def __init__(self, config):
        self._config = config
        self._moisture_sensor = sensor_control.Sensor()
        self._last_water = time.time()
        self._moisture_level = 0

    def _should_water(self):
        self._moisture_level = self._moisture_sensor.get_moisture_a2d()
        if (self._moisture_level < self._config['moisture_level_threshold']):
            self._last_water = time.time()
            # call watering function
            return 1
        else:
            return 0

    def run(self, scheduler, name):
        if self._should_water() == 1:
            wait_time = self._config['interval']
        else:
            wait_time = self._config['check_frequency']
        scheduler.add_to_schedule(name, time.time() + wait_time)
