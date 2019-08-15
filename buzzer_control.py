# -*- coding: utf-8 -*-
import gpiozero


class Buzzer:
    def __init__(self, config):
        self.buzzer_pin = gpiozero.DigitalOutputDevice(5)
        self.status = 0
        self.old_status = 1
        self._config = config

    def buzzer_update(self):
        if self.status == 0 and self.old_status != self.status:
            self.buzzer_pin.blink(background=True,
                                  on_time=self._config['buzzer_on_time'],
                                  off_time=self._config['buzzer_off_time'])
            # blink
        elif self.status == 1:
            # don't blink
            self.buzzer_pin.off()
        self.old_status = self.status

    def set_status(self, status):
        self.status = status
        self.buzzer_update()
