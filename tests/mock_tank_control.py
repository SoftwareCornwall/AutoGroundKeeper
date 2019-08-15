# -*- coding: utf-8 -*-

class MockTankControl:
    def __init__(self):
        self.level_above_threshold_return = 1
    
    def tank_level_above_threshold(self):
        return self.level_above_threshold_return
