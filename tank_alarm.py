# -*- coding: utf-8 -*-
# pylint: disable=C0111

import gpiozero


class TankAlarm:
    def __init__(self):
        self._green = gpiozero.DigitalOutputDevice(6)
        self._red = gpiozero.DigitalOutputDevice(26)
        self.set_status(1)

    def set_status(self, status):
        '''Status is current tank water level'''
        if status == 1:
            self._green.blink(n=20, background=True)
            self._red.off()
        else:
            self._red.blink(n=20, background=True)
            self._green.off()

    def __del__(self):
        self._red.off()
        self._green.off()