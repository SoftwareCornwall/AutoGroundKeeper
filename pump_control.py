#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  6 15:34:58 2019

@author: pi
"""
import time

import gpiozero

class Pump:
    def __init__(self):
        self.led = gpiozero.LED(17)
    

    def start_pump(self):
        self.led.on()

    def stop_pump(self):
        self.led.off()
        
    def enable_pump_for_duration(self, duration):
        self.start_pump()
        time.sleep(duration)
        self.stop_pump()
        
if __name__ == '__main__':
    pump = Pump()  
    pump.enable_pump_for_duration(2)