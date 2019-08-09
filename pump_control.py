# -*- coding: utf-8 -*-
# pylint: disable=C0111
"""
Created on Tue Aug  6 15:34:58 2019

@author: pi
"""
import time

import gpiozero


class Pump:
    def __init__(self):
        self.pump = gpiozero.LED(17)

    def start_pump(self):
        self.pump.on()

    def stop_pump(self):
        self.pump.off()

    def enable_pump_for_duration(self, duration):
        self.start_pump()
        time.sleep(duration)
        self.stop_pump()

    # Todo: change to has recive water ?? and apply to enable pump durarion.
    def enable_pump_until_moisture_sencor_is_saturated_for_duration(self, 
                                                                    duration,
                                                                    moisture_sencor, 
                                                                    start_moisture_value, 
                                                                    moisture_thresshold = 50,
                                                                    timeout = 5
                                                                    ):
        current_moisture_level = moisture_sencor.get_a2d_count()
        
        # start the pump and wait till the moisture sencor value goes above the
        # thresshold. -> continued by waiting for the duration and stoping the 
        # pump 
        
        
        self.start_pump()
        start_time = time.time();
        
        while moisture_sencor.get_a2d_count() <= start_moisture_value + moisture_thresshold:
            time.sleep(1)    # sleep for 1/4 of a second.
            current_moisture_level = moisture_sencor.get_a2d_count()
            
            if start_time + timeout < time.time():
                print( "Error: Moisture Not Detected within timeout :(" )
                break   # Error: we have not recived water with in the timeout :|
            
        
        print("End Mois Value:", moisture_sencor.get_a2d_count() )
        
        time.sleep(duration)
        
        self.stop_pump()
        
