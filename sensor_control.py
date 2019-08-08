#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  7 11:14:55 2019

@author: pi
"""

import spidev


class Sensor:
    def __init__(self):
        self.moisture_sensor = spidev.SpiDev()
        self.moisture_sensor.open(0, 0)
        self.moisture_sensor.max_speed_hz = 5000

    def read_from_chip(self):
        return self.moisture_sensor.xfer([0x60, 0x00])

    def convert_data(self, data_array):
        return (data_array[0] * 256) + (data_array[1])

    def get_a2d_count(self):
        result = self.convert_data(self.read_from_chip())
        print(result)
        return result

        # convert from binary to int
