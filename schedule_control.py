# -*- coding: utf-8 -*-
# pylint: disable=C0111,R0902,R0903


import time

import pump_control
import sensor_control
import config_handler
import tank_measurement
import tank_alarm


class Schedule:
    def __init__(self):
        self._config = config_handler.ConfigHandler()
        self._timeslept = 0
        self._moisture_level = 0
        self._pump = pump_control.Pump()
        self._last_watered = 0  # Unix time
        self._moisture_interpreter = sensor_control.Sensor()
        self._tank_measurement = tank_measurement.TankMeasurement()
        self._tank_alarm = tank_alarm.TankAlarm()

    def run(self):
        while (self._config.data['run_duration'] is None
               or self._timeslept < self._config.data['run_duration']):

            self._tank_alarm.set_status(self._tank_measurement.get_tank_level())

            self._moisture_level = self._moisture_interpreter.get_a2d_count()
            self._config.reload_if_modified()
            if self._should_water():
                self._water()

            if self._config.data['run_duration'] is not None:
                amount_to_sleep = min(self._config.data['check_frequency'],
                                      self._config.data['run_duration']
                                      - self._timeslept)
                time.sleep(amount_to_sleep)
                self._timeslept += amount_to_sleep
            else:
                time.sleep(self._config.data['check_frequency'])

    def _should_water(self):
        low_water = (self._moisture_level
                     < self._config.data['moisture_level_threshold'])
        exceeded_interval = ((time.time() - self._last_watered)
                             > self._config.data['interval'])
        print(low_water and exceeded_interval)                  # Todo: removed
        return low_water and exceeded_interval

    def _water(self):

        self._pump.enable_pump_until_moisture_sencor_is_saturated_for_duration(
            self._config.data['water_pumping_duration'],
            self._moisture_interpreter,
            self._moisture_level,
        )

        self._last_watered = time.time()
        if self._config.data['run_duration'] is not None:
            self._timeslept += self._config.data['water_pumping_duration']
