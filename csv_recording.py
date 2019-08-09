# -*- coding: utf-8 -*-
# pylint: disable=C0111
import time
import csv


class CSVRecording:
    def __init__(self, name='data.csv'):
        self._csvfile = open(name, 'a')
        self._csvwriter = csv.writer(self._csvfile, delimiter=',', quotechar='"')

    def add_record(self, moisture, light_level):
        date = time.strftime('%Y/%m/%d %H:%M')
        self._csvwriter.writerow([date, moisture, light_level])

    def close(self):
        self._csvfile.close()