# -*- coding: utf-8 -*-

class MockSensorControl:
    def __init__(self):
        self.moisture_value = 100
        self.light_value = 100
        
    def get_moisture_a2d(self):
        return self.moisture_value
    
    def get_light_a2d(self):
        return self.lght_value
