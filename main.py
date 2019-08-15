#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=C0111

import scheduler
import time

import config_handler
import tank_control
import moisture_check
import record_data
import sensor_control
import buzzer_control
import error_control
import email_spreadsheet


def check_for_stop(schedule, config, start_time):
    if config['run_duration'] is not None:
        if time.time() > start_time + config['run_duration']:
            schedule.stop_scheduler()
    return time.time() + 5


def main():
    schedule = scheduler.Scheduler()

    config = config_handler.ConfigHandler()
    sensors = sensor_control.Sensor()
    buzzer = buzzer_control.Buzzer(config)
    error_handler = error_control.ErrorControl(buzzer, sensors)
    tank = tank_control.TankControl(config, error_handler=error_handler)
    moisture = moisture_check.MoistureCheck(
        config, sensors, tank, error_handler)
    recorder = record_data.RecordData(config, sensors)
    email_spread = email_spreadsheet.Email_Spreadsheet()

    schedule.register_task('config_reload', config.run,
                           (), 0)

    schedule.register_task(
        'stop',
        check_for_stop,
        (schedule,
         config,
         time.time()))
    schedule.add_to_schedule('stop', 0)  # 86400)

    schedule.register_task(
        'update_leds', tank.run, (), 0)

    schedule.register_task(
        'check_for_errors',
        error_handler.run,
        (), 0)

    schedule.register_task(
        'check_moisture_level',
        moisture.run,
        (), 0)

    schedule.register_task(
        'update_csv', recorder.run, (), 0)

    schedule.register_task(
        'email_spreadsheet',
        email_spread.send_email_every_week,
        ("data.csv", ),
        time.time() + 10)
    # all tasks need to be before run scheduler

    schedule.run_scheduler()


if __name__ == '__main__':
    main()
