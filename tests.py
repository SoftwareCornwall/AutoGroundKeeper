#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=C0111,W0212
"""
Created on Tue Aug  6 15:38:24 2019

@author: pi
"""

import unittest
import doctest
import time

import pump_control
import schedule_control
import sensor_control


class MockTime():
    '''
    Mock sleep function that records duration of all time.sleep calls.
    Example:
        >>> old_sleep = time.sleep
        >>> mock_time = MockSleep()
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

    def tearDown(self):
        pump_control.time = time

    def test_enable_pump_for_duration(self):
        pump = pump_control.Pump()
        pump.enable_pump_for_duration(2)
        self.assertEqual([2], self.mock_time.sleep_history)

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
    def setUp(self):
        self.mock_time = MockTime()
        schedule_control.time = self.mock_time
        schedule_control.pump_control.time = self.mock_time

    def tearDown(self):
        schedule_control.time = time
        schedule_control.pump_control.time = time

    def test_watering_duration_is_amount(self):
        schedule = schedule_control.Schedule()
        schedule.set_water_dispense_amount(2)
        schedule._water()
        self.assertEqual(2, sum(self.mock_time.sleep_history))

    def test_total_sleep_is_runtime(self):
        schedule = schedule_control.Schedule()
        schedule.set_maximium_runtime(24 * 3600)

        schedule.run()
        self.assertEqual(24 * 3600, sum(self.mock_time.sleep_history))

    def test_should_water_returns_true_when_moisture_level_below_threshold(self):
        schedule = schedule_control.Schedule()
        schedule.moisture_level = 0.2
        schedule.moisture_level_threshold = 0.3
        self.assertTrue(schedule._should_water())

    def test_should_water_returns_false_when_moisture_level_above_threshold(self):
        schedule = schedule_control.Schedule()
        schedule.moisture_level = 0.4
        schedule.moisture_level_threshold = 0.3
        self.assertFalse(schedule._should_water())

    def test_should_water_false_when_recently_watered(self):
        schedule = schedule_control.Schedule()
        schedule.set_minimium_watering_frequency(3*3600)
        schedule.moisture_level = 0.2
        schedule.moisture_level_threshold = 0.3
        schedule._water()
        self.assertFalse(schedule._should_water())

    def test_should_water_returns_true_when_not_recently_watered(self):
        schedule = schedule_control.Schedule()
        schedule.set_minimium_watering_frequency(3*3600)
        schedule.moisture_level = 0.2
        schedule.moisture_level_threshold = 0.3
        self.mock_time.set_time(0)
        schedule._water()
        self.mock_time.set_time(3*3600 + 1)
        self.assertTrue(schedule._should_water())


class MockSPI():
    def xfer(self, transmitted_data):
        self.transmitted = transmitted_data
        return [0, 0]


class TestMoistureSensorInOut(unittest.TestCase):
    def test_data_is_converted_correctly(self):
        mockData = [0b00000010, 0b11101011]
        interp = sensor_control.Sensor()
        self.assertEqual(0b1011101011, interp.convert_data(mockData))

    def test_moisture_reading_is_taken_from_channel_0(self):
        interp = sensor_control.Sensor()
        interp.moisture_sensor = MockSPI()
        interp.read_from_chip()
        self.assertEqual([0x60, 0x00], interp.moisture_sensor.transmitted)


if __name__ == '__main__':
    unittest.main()
    doctest.testmod()
