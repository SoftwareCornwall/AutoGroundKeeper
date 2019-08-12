#!/usr/bin/env python3
# -*- coding: utf-8 -*
# pylint: disable=C0111
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

    def convert_data(self, byte_array):
        '''Strips unneeded bits to avoid errors'''
        byte_1 = (byte_array[0] & 0x03) << 8
        byte_2 = byte_array[1]
        return byte_1 + byte_2

    def get_moisture_a2d(self):
        data = self.moisture_sensor.xfer([0x60, 0x00])
        moisture_level = self.convert_data(data)
        print(moisture_level)
        return moisture_level

    def get_light_a2d(self):
        data = self.moisture_sensor.xfer([0x70, 0x00])
        light_level = self.convert_data(data)
        print(light_level)
        return light_level
