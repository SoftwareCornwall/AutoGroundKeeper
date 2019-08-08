# -*- coding: utf-8 -*-
# pylint: disable=C0111


import time

import pump_control
import sensor_control
import config_handler


class Schedule:
    def __init__(self):
        self.config = config_handler.ConfigHandler()
        self.timeslept = 0
        self.moisture_level = 0
        self.pump = pump_control.Pump()
        self.last_watered = 0  # Unix time
        self.moisture_interpreter = sensor_control.Sensor()

    def run(self):
        while (self.config.data['run_duration'] is None
                or self.timeslept < self.config.data['run_duration']):
            self.moisture_level = self.moisture_interpreter.get_a2d_count()
            self.config.reload_if_modified()
            if self._should_water():
                self._water()

            if self.config.data['run_duration'] is not None:
                amount_to_sleep = min(self.config.data['check_frequency'],
                                      self.config.data['run_duration'] - self.timeslept)
                time.sleep(amount_to_sleep)
                self.timeslept += amount_to_sleep
            else:
                time.sleep(self.config.data['check_frequency'])

    def _should_water(self):
        low_water = self.moisture_level < self.config.data['moisture_level_threshold']
        exceeded_interval = time.time() - self.last_watered > self.config.data['interval']
        print( low_water and exceeded_interval )
        return low_water and exceeded_interval

    def _water(self):
        self.pump.enable_pump_for_duration(self.config.data['water_pumping_duration'])
        self.last_watered = time.time()
        if self.config.data['run_duration'] is not None:
            self.timeslept += self.config.data['water_pumping_duration']
