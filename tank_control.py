# -*- coding: utf-8 -*-

import tank_measurement
import tank_alarm
import time


class TankControl:
    def __init__(self, buzzer, config=None):
        self._tank_measurement = tank_measurement.TankMeasurement()
        self._tank_alarm = tank_alarm.TankAlarm(config)
        self._buzzer_alarm = buzzer

    def update(self):
        status =  self._tank_measurement.get_tank_level()
        self._tank_alarm.set_status(status)
        self._buzzer_alarm.set_status(status)

    def run(self, scheduler, name):
        self.update()
        scheduler.add_to_schedule(name, time.time() + 5)
