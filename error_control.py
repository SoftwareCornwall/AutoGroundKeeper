# -*- coding: utf-8 -*-
import time


class ErrorControl:
    def __init__(self, buzzer, sensor):
        self.moisture_sensor = sensor
        self.buzzer_control = buzzer
        self.tank_status = 1
        self.sensor_has_failed = False
        self.time_sensor_failed = None

    def check_current_moisture_status(self):
        moisture_level = self.moisture_sensor.get_moisture_a2d()

        if moisture_level < 50:
            if self.time_sensor_failed is None:
                self.time_sensor_failed = time.time()
            elif time.time() > self.time_sensor_failed + 10:
                self.sensor_has_failed = True

        else:
            self.time_sensor_failed = None
            self.sensor_has_failed = False

    def set_tank_status(self, status):
        self.tank_status = status

    def error_update(self):
        if self.has_error():
            self.buzzer_control.set_status(0)
        else:
            self.buzzer_control.set_status(1)

    def has_error(self):
        return self.sensor_has_failed or self.tank_status == 0

    def run(self):
        self.check_current_moisture_status()
        self.error_update()
        return time.time() + 5
