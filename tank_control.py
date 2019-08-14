# -*- coding: utf-8 -*-

import tank_measurement
import tank_alarm
import time


class TankControl:
    def __init__(self, config=None, tank_measure=None, _tank_alarm=None):

        if self.tank_measure is not None:
            self._tank_measurement = tank_measurement.TankMeasurement()
        else:
            self._tank_measurement = tank_measure

        if self._tank_alarm is not None:
            self._tank_alarm = tank_alarm.TankAlarm(config)
        else:
            self._tank_alarm = _tank_alarm



    def tank_level_above_threshold(self):
        return self._tank_measurement.get_tank_level() >= 0.2

    def update(self):
        self._tank_alarm.set_status(self.tank_level_above_threshold())

    def run(self, scheduler, name):
        self.update()
        scheduler.add_to_schedule(name, time.time() + 5)
