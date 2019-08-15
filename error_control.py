# -*- coding: utf-8 -*-
import time


class ErrorControl:
    def __init__(self, buzzer, sensor):
        self.moisture_sensor = sensor
        self.buzzer_control = buzzer
        self.moisture_status = 1
        self.tank_status = 1
        self.sensor_has_failed = False
        self.time_sensor_failed = time.time()

    def check_current_moisture_status(self):
        moisture_level = self.moisture_sensor.get_moisture_a2d()
        if moisture_level < 50 and self.sensor_has_failed is False:
            self.sensor_has_failed = True
            self.time_sensor_failed = time.time()
        elif moisture_level < 50 and self.sensor_has_failed and time.time() - 10 > self.time_sensor_failed:
            self.moisture_status = 0

        if moisture_level > 50:
            self.moisture_status = 1
            self.time_sensor_failed = time.time()
            self.sensor_has_failed = True

    def set_tank_status(self, status):
        self.tank_status = status

    def error_update(self):
        if self.moisture_status == 0 or self.tank_status == 0:
            self.buzzer_control.set_status(0)
        else:
            self.buzzer_control.set_status(1)

    def get_error_status(self):
        if self.moisture_status == 0 or self.tank_status == 0:
            return 0
        else:
            return 1

    def run(self, scheduler, name):
        self.check_current_moisture_status()
        self.error_update()
        scheduler.add_to_schedule(name, time.time() + 5)
