#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=C0111
"""
Created on Tue Aug  6 15:38:24 2019

@author: pi
"""

import unittest
import doctest
import time

import pump_control
import schedule_control


class MockSleep():
    '''
    Mock sleep function that records duration of all time.sleep calls.
    Example:
        >>> old_sleep = time.sleep
        >>> mock_sleep = MockSleep()
        >>> time.sleep = mock_sleep.sleep
        >>> time.sleep(10)
        >>> time.sleep(3.2)
        >>> mock_sleep.sleep_history
        [10, 3.2]
        >>> time.sleep = old_sleep
    '''
    def __init__(self):
        self.sleep_history = []

    def sleep(self, duration):
        self.sleep_history.append(duration)


class TestPumpControl(unittest.TestCase):
    def test_enable_pump_for_duration(self):
        mock_sleep = MockSleep()
        pump_control.time.sleep = mock_sleep.sleep
        pump = pump_control.Pump()
        pump.enable_pump_for_duration(2)
        pump_control.time.sleep = time.sleep
        self.assertEqual([2], mock_sleep.sleep_history)

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


class TestSchedule(unittest.TestCase):
    def test_watering_duration_is_amount(self):
        mock_sleep = MockSleep()
        schedule_control.time.sleep = mock_sleep.sleep
        schedule = schedule_control.Schedule()
        schedule.set_water_dispense_amount(2)
        schedule.set_minimium_watering_frequency(5)
        schedule._water()
        self.assertEqual(7, sum(mock_sleep.sleep_history))
        
    def test_total_sleep_is_runtime(self):
        mock_sleep = MockSleep()
        schedule_control.time.sleep = mock_sleep.sleep
        schedule_control.pump_control.time.sleep = mock_sleep.sleep
        schedule = schedule_control.Schedule()
        schedule.set_maximium_runtime(24 * 3600)
        
        schedule.run()
        self.assertEqual(24 * 3600, sum(mock_sleep.sleep_history))
        
        schedule_control.time.sleep = time.sleep
        schedule_control.pump_control.time.sleep = time.sleep


if __name__ == '__main__':
    unittest.main()
    doctest.testmod()
