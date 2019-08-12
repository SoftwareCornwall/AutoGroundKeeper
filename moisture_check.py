# -*- coding: utf-8 -*-
import config_handler
import sensor_control

class MoistureCheck:
    def __init__(self, config):
        self._config = config
        self._moisture_sensor = sensor_control.Sensor()
        self._moisture_level = 0
        
    def _should_water(self):
        self._moisture_level = self._moisture_sensor.get_moisture_a2d()        
        if (self._moisture_level < self._config['moisture_level_threshold'])
            #call pump schedule
            pass
    
    def run(self, scheduler, name):
        self._should_water()
        scheduler.add_to_schedule(name, time.time() + _config["check_frequency"])
        
