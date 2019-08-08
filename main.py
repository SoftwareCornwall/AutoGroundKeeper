#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=C0111


import schedule_control

def main():
    schedule = schedule_control.Schedule()
    schedule.run()


if __name__ == '__main__':
    main()
    
