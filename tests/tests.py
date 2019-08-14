# -*- coding: utf-8 -*-
import unittest
import sys

sys.path.append('.')

import tests_old
import scheduler_test
import sensor_tests


if __name__ == '__main__':
    unittest.main(defaultTest=['scheduler_test', 'sensor_tests', 'tests_old'])
