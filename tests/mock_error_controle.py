# -*- coding: utf-8 -*-

class MockErrorContr():
    
    def __init__(self, has_error=False):
        self.has_error = has_error
        pass
    
    def get_error_status(self):
        return self.has_error
    
    