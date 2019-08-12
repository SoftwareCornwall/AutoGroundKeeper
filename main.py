#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=C0111

import scheduler
import time

import tank_control
import moisture_check


def main():
    schedule = scheduler.Scheduler()

    schedule.register_task('stop', schedule.stop_scheduler)
    schedule.add_to_schedule('stop', time.time() + 10)  # 86400)

    tank = tank_control.TankControl()
    schedule.register_task(
        'update_leds', tank.run, (schedule, 'update_leds'))
    schedule.add_to_schedule('update_leds', time.time())

    moisture = moisture_check.MoistureCheck()
    schedule.register_task(
        'check_moisture_level',
        moisture.run,
        (schedule,
         'check_moisture_level'))
    schedule.add_to_schedule('update_leds', time.time())

    schedule.run_scheduler()


if __name__ == '__main__':
    main()
