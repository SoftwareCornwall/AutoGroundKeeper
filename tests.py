#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=C0111
"""
Created on Tue Aug  6 15:38:24 2019

@author: pi
"""

import unittest
import time

import pump_control

class TestPumpControl(unittest.TestCase):
    def test_enable_pump_for_duration(self):
        start = time.time()
        pump = pump_control.Pump()
        pump.enable_pump_for_duration(2)
        duration = time.time() - start
        self.assertTrue(1.9 < duration < 2.1)

    def test_start_pump(self):
        pump = pump_control.Pump()
        pump.start_pump()
        self.assertEqual(1, pump.pump.value)
        pump.stop_pump()

    def test_stop_pump(self):
        pump = pump_control.Pump()
        pump.start_pump()
        pump.stop_pump()
        self.assertEqual(0, pump.pump.value)

if __name__ == '__main__':
    unittest.main()
