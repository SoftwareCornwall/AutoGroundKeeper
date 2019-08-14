# -*- coding: utf-8 -*-
import unittest
import sys

sys.path.append('.')

import tests_old
import scheduler_test


if __name__ == '__main__':
    unittest.main(defaultTest=['scheduler_test', 'tests_old'])
