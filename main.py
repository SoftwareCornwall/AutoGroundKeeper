#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=C0111


import schedule_control

def main():
    schedule = schedule_control.Schedule()
    schedule.set_check_frequency(5)
    schedule.set_minimium_watering_frequency(10)
    schedule.set_moisture_level_threshold(800)
    schedule.run()


if __name__ == '__main__':
    main()
    
