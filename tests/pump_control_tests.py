#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=C0111,W0212,R0902,R0903
"""
Created on Tue Aug  6 15:38:24 2019

@author: pi
"""
import unittest


import pump_control


class TestPumpControl(unittest.TestCase):
    def setUp(self):
        self.pump = pump_control.Pump()

    def tearDown(self):
        del self.pump

    def test_start_pump(self):
        self.pump.start_pump()
        self.assertEqual(1, self.pump.pump.value)
        self.pump.stop_pump()

    def test_stop_pump(self):
        self.pump.start_pump()
        self.pump.stop_pump()
        self.assertEqual(0, self.pump.pump.value)


if __name__ == '__main__':
    unittest.main()
