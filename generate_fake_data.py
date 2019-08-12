# -*- coding: utf-8 -*-
import random
import datetime


class GenerateFakeData:
    def generate_fake_data(self):
        x_fake_data = []
        y_fake_data = []
        for day in range(1, 28):
            for hour in range(1, 24):
                for minute in range(0, 60, 15):
                    x_fake_data.append(
                        datetime.datetime(
                            2016, 1, day, hour, minute, 0))
                    if 0 < hour < 12:
                        y_fake_data.append(
                            random.randrange(
                                20 * hour - 20, 20 * hour))
                    else:
                        y_fake_data.append(random.randrange(
                            240 - (20 * (hour - 12) + 20), 240 - 20 * (hour - 12)))
        return [x_fake_data, y_fake_data]
