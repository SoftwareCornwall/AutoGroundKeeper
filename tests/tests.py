# -*- coding: utf-8 -*-
import unittest
import sys

sys.path.append('.')

import scheduler_test
import tests_old

if __name__ == '__main__':
    unittest.main(defaultTest=['scheduler_test', 'tests_old'])
