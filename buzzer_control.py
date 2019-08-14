# -*- coding: utf-8 -*-
import gpiozero


class Buzzer:
    def __init__(self):
        self.buzzer_pin = gpiozero.DigitalOutputDevice(5)
        self.status = 0

    def buzzer_update(self):
        if self.status == 0:
            self.buzzer_pin.blink()
            # blink
        elif self.status == 1:
            # don't blink
            self.buzzer_pin.off()

    def set_status(self, status):
        self.status = status
        self.buzzer_update()
