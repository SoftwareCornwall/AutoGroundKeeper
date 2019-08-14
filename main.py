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


def check_for_stop(schedule, name, config, start_time):
    if config['run_duration'] is not None:
        if time.time() > start_time + config['run_duration']:
            schedule.stop_scheduler()
    schedule.add_to_schedule('stop', time.time() + 5)


def main():
    schedule = scheduler.Scheduler()

    config = config_handler.ConfigHandler()
    schedule.register_task('config_reload', config.run,
                           (schedule, 'config_reload'))
    schedule.add_to_schedule('config_reload', time.time())

    sensors = sensor_control.Sensor()

    buzzer = buzzer_control.Buzzer()

    schedule.register_task(
        'stop',
        check_for_stop,
        (schedule,
         'stop',
         config,
         time.time()))
    schedule.add_to_schedule('stop', time.time())  # 86400)

    tank = tank_control.TankControl(buzzer, config)
    schedule.register_task(
        'update_leds', tank.run, (schedule, 'update_leds'))
    schedule.add_to_schedule('update_leds', time.time())

    moisture = moisture_check.MoistureCheck(config, sensors, buzzer)
    schedule.register_task(
        'check_moisture_level',
        moisture.run,
        (schedule,
         'check_moisture_level'))
    schedule.add_to_schedule('check_moisture_level', time.time())

    recorder = record_data.RecordData(config, sensors)
    schedule.register_task(
        'update_csv', recorder.run, (schedule, 'update_csv'))
    schedule.add_to_schedule('update_csv', time.time())
    schedule.run_scheduler()


if __name__ == '__main__':
    main()
