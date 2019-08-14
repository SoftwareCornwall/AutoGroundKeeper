# -*- coding: utf-8 -*-
# pylint: disable=C0111
import datetime
import csv


class CSVRecording:
    def __init__(self, name='data.csv'):
        self.file_location = name
        self._csvfile = open(self.file_location, 'a')
        self._csvwriter = csv.writer(
            self._csvfile, delimiter=',', quotechar='"')
        self.max_time = now = datetime.datetime.now()
        self.min_time = datetime.datetime(
            now.year if now.month != 1 else now.year - 1,
            now.month - 1 if now.month != 1 else 12,
            now.day,
            now.hour,
            now.minute,
            now.second,
            now.microsecond,
            now.tzinfo)

    def add_record(self, moisture, light_level, date=None):
        if date is None:
            date = datetime.datetime.now()
        date = date.strftime('%Y/%m/%d %H:%M')
        self._csvwriter.writerow([date, moisture, light_level])

    def close(self):
        self._csvfile.close()

    def read_data(self, Setting):
        """Setting: 1 for Moisture, 2 for Light Level """
        xLine = []
        yLine = []
        with open(self.file_location) as csvDataFile:
            csvReader = csv.reader(csvDataFile)
            for row in csvReader:
                date_time_of_row = datetime.datetime.strptime(
                    row[0], "%Y/%m/%d %H:%M")
                if self.min_time < date_time_of_row < self.max_time:
                    xLine.append(date_time_of_row)
                    yLine.append(float(row[Setting]))
        self.close()
        return [xLine, yLine]
