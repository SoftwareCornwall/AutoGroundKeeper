# -*- coding: utf-8 -*-

import tank_measurement
import tank_alarm
import time


class TankControl:
    def __init__(
            self,
            config=None,
            tank_measure=None,
            _tank_alarm=None,
            error_handler=None):

        if tank_measure is None:
            self._tank_measurement = tank_measurement.TankMeasurement()
        else:
            self._tank_measurement = tank_measure

        if _tank_alarm is None:
            self._tank_alarm = tank_alarm.TankAlarm(config)
        else:
            self._tank_alarm = _tank_alarm

        self._buzzer_alarm = error_handler

    def tank_level_above_threshold(self):
        return self._tank_measurement.get_tank_level() >= 0.2

    def update(self):
        status = self.tank_level_above_threshold()
        self._tank_alarm.set_status(status)
        if self._buzzer_alarm is not None:
            self._buzzer_alarm.set_tank_status(status)

    def run(self, scheduler, name):
        self.update()
        scheduler.add_to_schedule(name, time.time() + 5)
