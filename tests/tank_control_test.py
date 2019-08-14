# -*- coding: utf-8 -*-
import unittest
import mock_tank_measurement
import tank_control


class TestTankControl(unittest.TestCase):

    def test_tank_starts_with_water(self):

        _mock_tank_measurement = mock_tank_measurement.MockTankMeasurement(
            5, 1, 0)
        _tank_control = tank_control.TankControl(
            tank_measure=_mock_tank_measurement)

        self.assertEqual(_tank_control.tank_level_above_threshold(), True)

    def test_tank_stop_when_water_is_low(self):
        _mock_tank_measurement = mock_tank_measurement.MockTankMeasurement(
            1, 1, 0)
        _tank_control = tank_control.TankControl(
            tank_measure=_mock_tank_measurement)

        self.assertEqual(_tank_control.tank_level_above_threshold(), True)

        _tank_control._tank_measurement.get_tank_level()

        self.assertEqual(_tank_control.tank_level_above_threshold(), False)
