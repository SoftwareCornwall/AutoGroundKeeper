# -*- coding: utf-8 -*-
import csv_recording
import time


class RecordData:
    def __init__(self, config, sensor_control):
        self._config = config
        self._csv_file = csv_recording.CSVRecording()
        self._sensor = sensor_control

    def append_current_readings_to_csv(self):
        moisture_level = self._sensor.get_moisture_a2d()
        light_level = self._sensor.get_light_a2d()
        self._csv_file.add_record(moisture_level, light_level)

    def run(self):
        self.append_current_readings_to_csv()
        return time.time() + self._config["record_interval"]
