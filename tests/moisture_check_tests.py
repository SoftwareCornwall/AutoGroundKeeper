# -*- coding: utf-8 -*-
import unittest
import moisture_check
import mock_config
import mock_sensor_control
import mock_error_controle
import mock_tank_control

class TestMoistureCheck(unittest.TestCase):
    def setUp(self):
        self._config = mock_config.MockConfig()
        self._sensor = mock_sensor_control.MockSensorControl()
        self._error = mock_error_controle.MockErrorContr()
        self._tank = mock_tank_control.MockTankControl()
        self._moisture_check = moisture_check.MoistureCheck(
                self._config, self._sensor, self._tank, self._error)
        
        self._moisture_check._config = self._config
        self._moisture_check._moisture_sensor = self._sensor
        self._moisture_check.error_controler = self._error
        
    def tearDown(self):
        del self._config
        del self._sensor
        del self._error
        del self._moisture_check
        
    def test_current_threshold_changes_to_max_when_watering_starts(self):
        self._config.data["moisture_level_threshold"] = 500
        self._config.data["max_moisture_level"] = 800
        
        self._sensor.moisture_value = 600
        self._moisture_check.run()
        self.assertEqual(500, self._moisture_check._config[self._moisture_check.current_threshold])
        
        self._sensor.moisture_value = 400
        self._moisture_check.run()
        self.assertEqual(800, self._moisture_check._config[self._moisture_check.current_threshold])
        
        
