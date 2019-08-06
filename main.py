#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=C0111
import time

import pump_control

def main():
    pump = pump_control.Pump()
    for _ in range(8):
        pump.enable_pump_for_duration(2)
        time.sleep(3 * 3600)

if __name__ == '__main__':
    main()
