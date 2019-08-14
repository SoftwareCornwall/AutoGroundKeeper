# -*- coding: utf-8 -*-
import unittest
import time


import pump_schedule


def enable_test_time_config(conf):
    '''
    disable reload ing config handler to prevent the settings from updateing :D
    @param conf:    config dict
    '''
    conf.data["interval"] = 1
    conf.data["water_pumping_duration"] = 0.05
    conf.data["water_not_detected_thresshold"] = 1
    conf.data["water_detected_timeout"] = 2


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


class TestPumpSchedule(unittest.TestCase):
    def test_water_recived_by_sensor(self):

        moisture_sensor = MockSensor(1)

        start_moisture_level = moisture_sensor.get_moisture_a2d()
        water_schedule = pump_schedule.Watering_Schedule(moisture_sensor)
        water_schedule.status_level = 1
        with water_schedule as pump_sch:
            pump_sch._config.disable_reload = True
            enable_test_time_config(pump_sch._config)
            (pump_sch.
             enable_pump_until_moisture_sencor_is_saturated_for_duration())

        self.assertTrue(moisture_sensor.get_moisture_a2d()
                        > start_moisture_level)

    def test_water_not_recived_by_sensor__timedout(self):

        moisture_sensor = MockSensor(10)

        start_moisture_level = moisture_sensor.get_moisture_a2d()

        with pump_schedule.Watering_Schedule(moisture_sensor) as pump_sch:
            pump_sch._config.disable_reload = True
            enable_test_time_config(pump_sch._config)
            pump_sch._config.data["water_detected_timeout"] = 0.1
            (pump_sch.
             enable_pump_until_moisture_sencor_is_saturated_for_duration())

        self.assertFalse(moisture_sensor.get_moisture_a2d()
                         > start_moisture_level)

    def test_pump_starts(self):
        moisture_sensor = MockSensor(1)

        water_schedule = pump_schedule.Watering_Schedule(moisture_sensor)
        water_schedule.status_level = 1
        with water_schedule as pump_sch:
            pump_sch._config.disable_reload = True
            enable_test_time_config(pump_sch._config)
            self.assertEqual(1, pump_sch.pump.pump.value)
            (pump_sch.
             enable_pump_until_moisture_sencor_is_saturated_for_duration())

    def test_pump_stops(self):
        moisture_sensor = MockSensor(1)

        with pump_schedule.Watering_Schedule(moisture_sensor) as pump_sch:
            pump_sch._config.disable_reload = True
            enable_test_time_config(pump_sch._config)
            pump = pump_sch.pump
            (pump_sch.
             enable_pump_until_moisture_sencor_is_saturated_for_duration())

        self.assertEqual(0, pump.pump.value)
