# -*- coding: utf-8 -*-
# pylint: disable=C0111

import gpiozero

class TankMeasurement:
    def __init__(self):
        self._float_switch = gpiozero.DigitalInputDevice(16)

    def get_tank_level(self):
        '''
        Return a value between 0 and 1 depending on how full,
        with 1 returned when full, and 0 when empty
        '''
        return self._float_switch.value
    