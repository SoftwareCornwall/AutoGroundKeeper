# -*- coding: utf-8 -*-
# pylint: disable=C0111

import pump_control
import time


class Schedule:
    def __init__(self):
        self.gap = 1*3600
        self.timeslept = 0
        self.runtime = None
        self.moisture_level = 0.4
        self.moisture_level_threshold = 0.5
        self.pump = pump_control.Pump()
        self.amount = 2
        self.check_frequency = 5 *60

    def set_minimium_watering_frequency(self, gap):
        self.gap = gap

    def set_water_dispense_amount(self, amount):
        self.amount = amount

    def set_moisture_level_threshold(self, moisture_level):
        self.moisture_level_threshold = moisture_level
    
    def set_maximium_runtime(self, runtime):
        self.runtime = runtime
        
        
    def set_check_frequency(self, check_frequency):
        self.check_frequency = check_frequency
        
    def run(self):
        while (self.timeslept < self.runtime or self.runtime is None):
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
        if self.moisture_level < self.moisture_level_threshold:
            return True
        else:
            return False
    
    

    def _water(self):
        self.pump.enable_pump_for_duration(self.amount)
        if self.runtime is not None:
            self.timeslept += self.amount
            time.sleep(min(self.gap, self.runtime - self.timeslept))
            self.timeslept += min(self.gap, self.runtime - self.timeslept)
                
        else:
            time.sleep(self.gap)