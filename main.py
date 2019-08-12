#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=C0111

import scheduler
import time

import config_handler
import tank_control
import moisture_check


def main():
    schedule = scheduler.Scheduler()

    schedule.register_task('stop', schedule.stop_scheduler)
    schedule.add_to_schedule('stop', time.time() + 10)  # 86400)

    config = config_handler.ConfigHandler()
    schedule.register_task('config_reload', config.run,
                           (schedule, 'config_reload'))
    schedule.add_to_schedule('config_reload', time.time())

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
    schedule.add_to_schedule('check_moisture_level', time.time())

    schedule.run_scheduler()


if __name__ == '__main__':
    main()
