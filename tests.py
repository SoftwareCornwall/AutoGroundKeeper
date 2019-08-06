#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  6 15:38:24 2019

@author: pi
"""

import unittest
import pump_control
import time

class TestPumpControl(unittest.TestCase):
    def test_enable_pump_for_duration(self):
        start = time.time()
        pump_control.enable_pump_for_duration(2)
        duration = time.time() - start
        self.assertTrue(1.9 < duration < 2.1)
        
if __name__ == '__main__':
    unittest.main()