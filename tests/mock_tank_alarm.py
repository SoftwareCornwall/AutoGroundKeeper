# -*- coding: utf-8 -*-


class MockTankAlarm():

    def __init__(self):
        self._status = False

    def set_status(self, status):
        self._status = status
