# -*- coding: utf-8 -*-
import unittest
import sys

sys.path.append('.')

import tests_old
import pump_schedule_tests
import sensor_tests
import scheduler_test
import csv_tests

if __name__ == '__main__':
    unittest.main(defaultTest=['scheduler_test', 'sensor_tests', 'tests_old',
                               'csv_tests', 'pump_schedule_tests'])

