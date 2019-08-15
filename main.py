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


def check_for_stop(schedule, name, config, start_time):
    if config['run_duration'] is not None:
        if time.time() > start_time + config['run_duration']:
            schedule.stop_scheduler()
    schedule.add_to_schedule('stop', time.time() + 5)


def main():
    schedule = scheduler.Scheduler()

    config = config_handler.ConfigHandler()
    sensors = sensor_control.Sensor()
    buzzer = buzzer_control.Buzzer()
    error_handler = error_control.ErrorControl(buzzer, sensors)
    tank = tank_control.TankControl(config, error_handler=error_handler)
    moisture = moisture_check.MoistureCheck(config, sensors, tank)
    recorder = record_data.RecordData(config, sensors)

    schedule.register_task('config_reload', config.run,
                           (), 0)

    schedule.register_task(
        'stop',
        check_for_stop,
        (schedule,
         'stop',
         config,
         time.time()))
    schedule.add_to_schedule('stop', 0)  # 86400)

    schedule.register_task(
        'update_leds', tank.run, (schedule, 'update_leds'), 0)

    schedule.register_task(
        'check_moisture_level',
        moisture.run,
        (schedule,
         'check_moisture_level'), 0)

    schedule.register_task(
        'update_csv', recorder.run, (schedule, 'update_csv'), 0)

    schedule.register_task(
        'check_for_errors',
        error_handler.run,
        (schedule,
         'check_for_errors'), 0)

    schedule.run_scheduler()


if __name__ == '__main__':
    main()
