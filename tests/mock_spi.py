# -*- coding: utf-8 -*-

class MockSPI():        
    def xfer(self, transmitted_data):
        self.transmitted = transmitted_data
        return [0, 0]
    