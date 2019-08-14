# -*- coding: utf-8 -*-
import unittest
import sys

sys.path.append('.')

import pump_control_tests
import pump_schedule_tests
import sensor_tests
import scheduler_test
import csv_tests
import tank_control_test

if __name__ == '__main__':
    unittest.main(defaultTest=['scheduler_test', 'sensor_tests',
                               'pump_control_tests',
                               'csv_tests', 'pump_schedule_tests',
                               'tank_control_test'])

