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
import schedule_control
import sensor_control
import tank_alarm

import csv_recording


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


class MockSensor():
    '''
    Mock moisture sencor.
    The moisture incresses after 't' amount of time since Init-ed

    '''

    def __init__(self, moisture_delay=2, start_level=500, incressed_level=900):
        self.incress_moisture_delay = moisture_delay
        self.start_time = time.time()
        self.start_moisture_level = start_level
        self.incressed_moisture_level = incressed_level

    def get_moisture_a2d(self):

        if self.waiting_for_moisture_incress():
            return self.start_moisture_level
        else:
            return self.incressed_moisture_level

    def waiting_for_moisture_incress(self):
        return time.time() < self.start_time + self.incress_moisture_delay


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

    def test_water_recived_by_sensor(self):
        moisture_sensor = MockSensor()
        start_moisture_level = moisture_sensor.get_moisture_a2d()
        self.pump.enable_pump_until_saturated_for_duration(
            2, moisture_sensor, start_moisture_level, 50, 5)
        self.assertTrue(moisture_sensor.get_moisture_a2d()
                        > start_moisture_level)


class TestTankAlarm(unittest.TestCase):
    def setUp(self):
        self.tank_alarm = tank_alarm.TankAlarm()

    def tearDown(self):
        del self.tank_alarm

    def test_full_enables_green_disables_red(self):
        self.tank_alarm.set_status(1)
        self.assertEqual(1, self.tank_alarm._green.value)
        self.assertEqual(0, self.tank_alarm._red.value)

    def test_empty_disables_green_enables_red(self):
        self.tank_alarm.set_status(0)
        self.assertEqual(0, self.tank_alarm._green.value)
        self.assertEqual(1, self.tank_alarm._red.value)


class TestSchedule(unittest.TestCase):
    def setUp(self):
        self.mock_time = MockTime()
        self.mock_sensor = MockSensor(0.1)
        schedule_control.time = self.mock_time
        schedule_control.pump_control.time = self.mock_time
        self.schedule = schedule_control.Schedule()
        self.schedule._moisture_interpreter = self.mock_sensor

    def tearDown(self):
        schedule_control.time = time
        schedule_control.pump_control.time = time
        del self.schedule

    def test_watering_duration_is_amount(self):
        return
        self.schedule._config.data['water_pumping_duration'] = 2
        self.schedule._water()
        self.assertEqual(2, sum(self.mock_time.sleep_history))

    def test_total_sleep_is_runtime(self):
        return
        self.schedule._config.data['run_duration'] = 24 * 3600
        self.schedule._config.data['check_frequency'] = 15 * 60

        self.schedule.run()
        self.assertEqual(24 * 3600, sum(self.mock_time.sleep_history))

    def test_should_water_returns_true_when_moisture_level_below_threshold(
            self):
        self.schedule._moisture_level = 600
        self.schedule._config.data['moisture_level_threshold'] = 800
        self.assertTrue(self.schedule._should_water())

    def test_should_water_returns_false_when_moisture_level_above_threshold(
            self):
        self.schedule._moisture_level = 900
        self.schedule._config.data['moisture_level_threshold'] = 800
        self.assertFalse(self.schedule._should_water())

    def test_should_water_false_when_recently_watered(self):
        self.schedule._config.data['interval'] = 3 * 3600
        self.schedule._moisture_level = 600
        self.schedule._config.data['moisture_level_threshold'] = 800
        self.schedule._water()
        self.assertFalse(self.schedule._should_water())

    def test_should_water_returns_true_when_not_recently_watered(self):
        self.schedule._config.data['interval'] = 3 * 3600
        self.schedule._moisture_level = 600
        self.schedule._config.data['moisture_level_threshold'] = 800
        self.mock_time.set_time(0)
        self.schedule._water()
        self.mock_time.set_time(3 * 3600 + 1)
        self.assertTrue(self.schedule._should_water())


class MockSPI():
    def xfer(self, transmitted_data):
        self.transmitted = transmitted_data
        return [0, 0]


class TestMoistureSensorInOut(unittest.TestCase):
    def setUp(self):
        self.interp = sensor_control.Sensor()
        self.interp.MCP3002 = MockSPI()

    def test_data_is_converted_correctly(self):
        mock_data = [0b00000010, 0b11101011]
        self.assertEqual(0b1011101011, self.interp.convert_data(mock_data))

    def test_moisture_reading_is_taken_from_channel_0(self):
        self.interp.get_moisture_a2d()
        self.assertEqual([0x60, 0x00], self.interp.MCP3002.transmitted)

    def test_light_reading_is_taken_from_channel_1(self):
        self.interp.get_light_a2d()
        self.assertEqual([0x70, 0x00], self.interp.MCP3002.transmitted)


class TestCSV(unittest.TestCase):
    def test_rows_ordered_by_time_from_CSV_data(self):
        # most recent readings at end of file
        CSV_handler = csv_recording.CSVRecording()
        list_of_datetimes = CSV_handler.read_data(1)
        self.assertEqual(sorted(list_of_datetimes[0]), list_of_datetimes[0])

    def test_moisture_values_are_in_range_of_0_to_1023(self):
        CSV_handler = csv_recording.CSVRecording()
        list_of_datetimes = CSV_handler.read_data(1)
        self.assertGreaterEqual(1023, sorted(list_of_datetimes[1])[0])
        self.assertLessEqual(0, sorted(list_of_datetimes[1])[-1])

    def test_light_levels_are_inrange_of_0_to_1023(self):
        CSV_handler = csv_recording.CSVRecording()
        list_of_datetimes = CSV_handler.read_data(2)
        self.assertGreaterEqual(1023, sorted(list_of_datetimes[1])[0])
        self.assertLessEqual(0, sorted(list_of_datetimes[1])[-1])


if __name__ == '__main__':
    unittest.main()
    doctest.testmod()
