#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  7 11:14:55 2019

@author: pi
"""

import spidev

class MoistureInterpreter:
    
    def __init__(self):
        self.moistureSensor = spidev.SpiDev()
        self.moistureSensor.open(0, 0)
        self.moistureSensor.bits_per_word = 10

    def ReadFromChip(self, nBytes):
        dataArray = self.moistureSensor.xfer([0x60,0x00])
        print(dataArray)

    def ConvertData(self, input):
        pass
        #convert from binary to int