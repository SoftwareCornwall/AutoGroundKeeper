# -*- coding: utf-8 -*-
import time
import email_handler


class ErrorControl:
    def __init__(self, buzzer, sensor, config_file, schedule):
        self.config = config_file
        self._sensor = sensor
        self.buzzer_control = buzzer
        self.tank_status = 1
        self.moisture_sensor_has_failed = False
        self.time_moisture_sensor_failed = None
        self.time_light_sensor_failed = None
        self.it_is_dark = False
        self.schedule = schedule
        self.last_email_warning = 0

    def check_current_moisture_status(self):
        moisture_level = self._sensor.get_moisture_a2d()

        if moisture_level < 50:
            if self.time_moisture_sensor_failed is None:
                self.time_moisture_sensor_failed = time.time()
                #Change number to change amount of time moisture sensor reads 0 error
            elif time.time() > self.time_moisture_sensor_failed + 10:
                self.moisture_sensor_has_failed = True

        else:
            self.time_moisture_sensor_failed = None
            self.moisture_sensor_has_failed = False

    def check_current_light_status(self):
        light_level = self._sensor.get_light_a2d()
        if light_level < 350:
            if self.time_light_sensor_failed is None:
                self.time_light_sensor_failed = time.time()
                #Change number to change amount of time LDR needs to be dark
            elif time.time() > self.time_light_sensor_failed + 5:
                self.it_is_dark = True

        else:
            self.time_light_sensor_failed = None
            self.it_is_dark = False
    
    def set_tank_status(self, status):
        self.tank_status = status

    def error_update(self):
        if self.has_error():
            self.buzzer_control.set_status(0)
            #Does not send email more than once every 6 hours
            if time.time() > self.last_email_warning + 6 * 3600:
                self.last_email_warning = time.time()
                print('Sending email due to error:', self.check_error())
                email = email_handler.EmailHandler(self.config)
                email.send_email("Error", self.check_error(), [], self.schedule, True)
        else:
            self.buzzer_control.set_status(1)

    def has_error(self):
        return self.moisture_sensor_has_failed or self.tank_status == 0 or self.it_is_dark

    def run(self):
        self.check_current_moisture_status()
        self.check_current_light_status()
        self.error_update()
        return time.time() + 5

    def check_error(self):
        error_string = "The errors are; "
        if self.tank_status == 0:
            error_string += "the water level in the tank is low, "
        if self.moisture_sensor_has_failed:
            error_string += "there is an error with the moister sensor, "
        if self.it_is_dark:
            error_string += "there is no light for the plant"
            
        return error_string 

