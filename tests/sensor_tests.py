# -*- coding: utf-8 -*-
import unittest
import sensor_control


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
