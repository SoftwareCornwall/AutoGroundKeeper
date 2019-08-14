# -*- coding: utf-8 -*-

import tank_measurement
import tank_alarm
import time


class TankControl:
    def __init__(self, config=None):
        self._tank_measurement = tank_measurement.TankMeasurement()
        self._tank_alarm = tank_alarm.TankAlarm(config)

    def is_too_low(self):
        return bool(self._tank_measurement.get_tank_level())

    def update(self):
        self._tank_alarm.set_status(self.is_too_low())

    def run(self, scheduler, name):
        self.update()
        scheduler.add_to_schedule(name, time.time() + 5)
