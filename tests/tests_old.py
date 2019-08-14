#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=C0111,W0212,R0902,R0903
"""
Created on Tue Aug  6 15:38:24 2019

@author: pi
"""
import unittest
import doctest
import time


import pump_control



class MockTime():
    '''
    Mock sleep function that records duration of all time.sleep calls.
    Example:
        >>> old_sleep = time.sleep
        >>> mock_time = MockTime()
        >>> time.sleep = mock_time.sleep
        >>> time.sleep(10)
        >>> time.sleep(3.2)
        >>> mock_time.sleep_history
        [10, 3.2]
        >>> time.sleep = old_sleep
    '''

    def __init__(self):
        self.sleep_history = []
        self._time_is_locked = False
        self._fixed_time = time.time()

    def sleep(self, duration):
        self.sleep_history.append(duration)

    def time(self):
        if self._time_is_locked:
            return self._fixed_time
        return time.time()

    def set_time(self, desired):
        self._time_is_locked = True
        self._fixed_time = desired


class TestPumpControl(unittest.TestCase):
    def setUp(self):
        self.mock_time = MockTime()
        pump_control.time = self.mock_time
        self.pump = pump_control.Pump()

    def tearDown(self):
        pump_control.time = time
        del self.pump

    def test_enable_pump_for_duration(self):
        self.pump.enable_pump_for_duration(2)
        self.assertEqual([2], self.mock_time.sleep_history)

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
    doctest.testmod()
