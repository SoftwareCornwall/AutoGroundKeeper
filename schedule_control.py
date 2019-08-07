# -*- coding: utf-8 -*-
# pylint: disable=C0111

import time

class Schedule:
    def __init__(self):
        self.gap = 1*3600
        pass

    def set_minimium_watering_frequency(self, gap):
        self.gap = gap
        
        

    def set_water_dispense_amount(self, amount):
        pass

    def set_moisture_level_threshold(self, moisture_level):
        pass
    
    def wait_watering_gap(self):
        time.sleep(self.gap)