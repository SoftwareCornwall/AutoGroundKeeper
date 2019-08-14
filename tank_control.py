# -*- coding: utf-8 -*-

import tank_measurement
import tank_alarm
import time


class TankControl:
    def __init__(self, config=None):
        self._tank_measurement = tank_measurement.TankMeasurement()
        self._tank_alarm = tank_alarm.TankAlarm(config)

    def tank_level_above_threshold(self):
        return self._tank_measurement.get_tank_level() >= 0.2

    def update(self):
        self._tank_alarm.set_status(self.tank_level_above_threshold())

    def run(self, scheduler, name):
        self.update()
        scheduler.add_to_schedule(name, time.time() + 5)
