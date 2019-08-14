# -*- coding: utf-8 -*-
# pylint: disable=C0111

import gpiozero


class MockTankMeasurement:
    def __init__(self, calls_till_empty, start_level, end_level):
        self.calls_till_empty = calls_till_empty
        self.current_call = 0
        self.start_level = start_level
        self.end_level = end_level

    def get_tank_level(self):
        '''
        Return a value between 0 and 1 depending on how full,
        with 1 returned when full, and 0 when empty
        '''
        if (self.calls_till_empty == 0
                or self.current_call > self.calls_till_empty):
            return 0.0

        diff = self.end_level - self.start_level
        self.current_call += 1

        return self.start_level + (
            ((self.current_call - 1.0) / self.calls_till_empty) * diff)
