# -*- coding: utf-8 -*-
# pylint: disable=C0111

import gpiozero


class TankAlarm:
    def __init__(self):
        self._green = gpiozero.DigitalOutputDevice(6)
        self._red = gpiozero.DigitalOutputDevice(26)
        self._status = 0
        self.set_status(1)

    def set_status(self, status):
        '''Status is current tank water level'''
        if status != self._status:
            self._status = status
            if status == 1:
                self._green.blink(background=True)
                self._red.off()
            else:
                self._red.blink(background=True)
                self._green.off()

    def __del__(self):
        try:
            self._red.off()
        except gpiozero.exc.GPIODeviceClosed:
            pass
        try:
            self._green.off()
        except gpiozero.exc.GPIODeviceClosed:
            pass