# -*- coding: utf-8 -*-
# pylint: disable=C0111

import gpiozero


class TankAlarm:
    def __init__(self, config=None):
        self._green = gpiozero.DigitalOutputDevice(6)
        self._red = gpiozero.DigitalOutputDevice(26)
        self._status = 0
        self._config = config
        self.set_status(1)

    def set_status(self, status):
        '''Status is current tank water level'''
        if status != self._status:
            self._status = status
            if status == 1:
                if self._config is not None:
                    self._green.blink(background=True,
                                      on_time=self._config['tank_led_blink'],
                                      off_time=self._config['tank_led_blink'])
                else:
                    self._green.blink(background=True)
                self._red.off()
            else:
                if self._config is not None:
                    self._red.blink(background=True,
                                    on_time=self._config['tank_led_blink'],
                                    off_time=self._config['tank_led_blink'])
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
