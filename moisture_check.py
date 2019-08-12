# -*- coding: utf-8 -*-
import time
import config_handler
import sensor_control

class MoistureCheck:
    def __init__(self, config):
        self._config = config
        self._moisture_sensor = sensor_control.Sensor()
        self._last_water = time.time()
        self._moisture_level = 0
        
    def _should_water(self):
        self._moisture_level = self._moisture_sensor.get_moisture_a2d()
        moisture_low = (self._moisture_level < self._config['moisture_level_threshold'])
        interval_exceeded = ((time.time() - self._last_water) > self._config.data['interval'])        
        if moisture_low and interval_exceeded
            _last_water = time.time()
            #call watering function
            
    
    def run(self, scheduler, name):
        self._should_water()
        scheduler.add_to_schedule(name, time.time() + _config["check_frequency"])
        
