# -*- coding: utf-8 -*-

class MockErrorContr():
    
    def __init__(self, has_error=False):
        self._has_error = has_error
        pass
    
    def has_error(self):
        return self._has_error
    
    