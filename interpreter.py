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
        self.moistureSensor.max_speed_hz = 5000

    def ReadFromChip(self):
        return self.moistureSensor.xfer([0x60, 0x00])

    def ConvertData(self, data_array):
        return (data_array[0] * 256) + (data_array[1])

    def get_a2d_count(self):
        result = self.ConvertData(self.ReadFromChip())
        print(result)
        return result

        #convert from binary to int