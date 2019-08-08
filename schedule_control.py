# -*- coding: utf-8 -*-
# pylint: disable=C0111


import time

import pump_control
import sensor_control


class Schedule:
    def __init__(self):
        self.interval = 1*3600
        self.timeslept = 0
        self.runtime = None
        self.moisture_level = 0
        self.moisture_level_threshold = 500
        self.pump = pump_control.Pump()
        self.amount = 2
        self.check_frequency = 5 * 60
        self.last_watered = 0  # Unix time
        self.moisture_interpreter = sensor_control.Sensor()

    def set_minimium_watering_frequency(self, interval):
        self.interval = interval

    def set_water_dispense_amount(self, amount):
        self.amount = amount

    def set_moisture_level_threshold(self, moisture_level):
        self.moisture_level_threshold = moisture_level

    def set_maximium_runtime(self, runtime):
        self.runtime = runtime

    def set_check_frequency(self, check_frequency):
        self.check_frequency = check_frequency

    def run(self):
        while (self.runtime is None or self.timeslept < self.runtime):
            self.moisture_level = self.moisture_interpreter.get_a2d_count()
            if self._should_water():
                self._water()

            if self.runtime is not None:
                amount_to_sleep = min(self.check_frequency,
                                      self.runtime - self.timeslept)
                time.sleep(amount_to_sleep)
                self.timeslept += amount_to_sleep
            else:
                time.sleep(self.check_frequency)

    def _should_water(self):
        low_water = self.moisture_level < self.moisture_level_threshold
        exceeded_interval = time.time() - self.last_watered > self.interval
        print( low_water and exceeded_interval )
        return low_water and exceeded_interval

    def _water(self):
        self.pump.enable_pump_for_duration(self.amount)
        self.last_watered = time.time()
        if self.runtime is not None:
            self.timeslept += self.amount
