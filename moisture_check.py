# -*- coding: utf-8 -*-
import time
import pump_schedule


class MoistureCheck:
    def __init__(self, config, sensors, tank_control):
        self._config = config
        self._moisture_sensor = sensors
        self._last_water = time.time()
        self._moisture_level = 0
        self._tank_control = tank_control

    def _should_water(self):
        return (self._tank_control.tank_level_above_threshold()
                and (self._moisture_level
                     < self._config['moisture_level_threshold']))

    def get_next_interval(self):
        if (self._should_water()):
            self._last_water = time.time()
            # call watering function
            return self._config['interval']
        else:
            return self._config['check_frequency']

    def run(self):
        self._moisture_level = self._moisture_sensor.get_moisture_a2d()
        water_schedule = pump_schedule.Watering_Schedule
        if self._should_water():
            with water_schedule(self._moisture_sensor) as pump_sch:
                pump_sch._config = self._config
                (pump_sch.
                 enable_pump_until_moisture_sencor_is_saturated_for_duration())

        wait_time = self.get_next_interval()
        return time.time() + wait_time
