# -*- coding: utf-8 -*-
# pylint: disable=C0111
"""
Created on Tue Aug  6 15:34:58 2019

@author: pi
"""
import time

import gpiozero


class Pump:
    def __init__(self):
        self.pump = gpiozero.LED(17)

    def start_pump(self):
        self.pump.on()

    def stop_pump(self):
        self.pump.off()

    def enable_pump_for_duration(self, duration):
        self.start_pump()
        time.sleep(duration)
        self.stop_pump()
