# -*- coding: utf-8 -*-
import random
import datetime
import csv_recording


class GenerateFakeData:
    def generate_fake_data_for_graph(self):
        x_fake_data = []
        y_fake_data = []
        for day in range(1, 28):
            for hour in range(1, 24):
                for minute in range(0, 60, 15):
                    x_fake_data.append(
                        datetime.datetime(
                            2019, 7, day, hour, minute, 0))
                    if 0 < hour < 12:
                        y_fake_data.append(
                            random.randrange(
                                20 * hour - 20,
                                20 * hour))
                    else:
                        y_fake_data.append(random.randrange(
                            240 - (20 * (hour - 12) + 20),
                            240 - 20 * (hour - 12)))
        return [x_fake_data, y_fake_data]

    def generate_fake_data_for_file(self, name):
        time_fake_data = []
        light_fake_data = []
        moisture_fake_data = []
        for month in range(7, 9):
            for day in range(1, 32):
                for hour in range(1, 24):
                    for minute in range(0, 60, 15):
                        time_fake_data.append(
                            datetime.datetime(
                                2019, month, day, hour, minute, 0))
                        if 0 < hour < 12:
                            light_fake_data.append(
                                random.randrange(
                                    20 * hour - 20, 20 * hour))
                            moisture_fake_data.append(
                                random.randrange(
                                    20 * hour - 20, 20 * hour))
                        else:
                            light_fake_data.append(random.randrange(
                                240 - (20 * (hour - 12) + 20),
                                240 - 20 * (hour - 12)))
                            moisture_fake_data.append(random.randrange(
                                240 - (20 * (hour - 12) + 20),
                                240 - 20 * (hour - 12)))

        fake_data_file = csv_recording.CSVRecording(name)
        for row in range(0, len(time_fake_data)):
            fake_data_file.add_record(
                moisture_fake_data[row],
                light_fake_data[row],
                time_fake_data[row])
        fake_data_file.close()


fake_data = GenerateFakeData()

fake_data.generate_fake_data_for_file("fake_data.csv")
