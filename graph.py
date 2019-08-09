#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  9 12:00:53 2019

@author: pi
"""
import matplotlib.pyplot as plt
import datetime
import random
import csv
import dateutil.relativedelta

class GraphDrawer:

    def __init__(self):
        self.file_location = "data.csv"
        self.max_time = datetime.datetime.now()
        self.min_time = datetime.datetime.now() - dateutil.relativedelta.relativedelta(months=1)
        self.point_shape = "*"
        #Point shape options
        #"." = point
        #"," = pixel
        #"o" = circle
        #"^" = triangle_up
        #"v" = triangle_down
        #"8" = octagon
        #"s" = square
        #"p" = pentagon
        #"*" = star
        #"h" = hexagon
        #"+" = plus
        #"D" = diamond


    def fake_data(self):
        x_fake_data = []
        y_fake_data = []
        for day in range(1,28):
            for hour in range(1,24):
                for minute in range(0,60,15):
                    x_fake_data.append(datetime.datetime(2016, 1, day, hour, minute, 0))
                    if 0<hour<12:
                        y_fake_data.append(random.randrange(20*hour -20,20*hour))
                    else:
                        y_fake_data.append(random.randrange(240 - (20*(hour-12)+20),240 - 20*(hour-12)))
        return [x_fake_data,y_fake_data]

    def read_data(self, Setting):
        """Setting: 1 for Moisture, 2 for Light Level """
        xLine = []
        yLine = []
        with open(self.file_location) as csvDataFile:
            csvReader = csv.reader(csvDataFile)
            for row in csvReader:
                date_time_of_row = datetime.datetime.strptime(row[0], "%Y/%m/%d %H:%M")
                if self.min_time < date_time_of_row < self.max_time:
                    xLine.append(date_time_of_row)
                    yLine.append(float(row[Setting]))
        return [xLine, yLine]



    def draw_light_level_graph(self):
        plant_data = self.read_data(2)
        plt.figure(figsize=(14,5))
        plt.plot(plant_data[0],plant_data[1],c='b',marker= self.point_shape)
        plt.xlabel('Time', fontsize=16)
        plt.ylabel('Light', fontsize=16)
        plt.title('scatter plot - Light vs Time',fontsize=20)
        plt.gcf().autofmt_xdate()
        plt.grid(True)
        plt.savefig("LightLevelGraphImage.png", dpi=300)
        plt.show()

    def draw_moisture_level_graph(self):
        plant_data = self.read_data(1)
        plt.figure(figsize=(14,5))
        plt.plot(plant_data[0],plant_data[1],c='r',marker=self.point_shape)
        plt.xlabel('Time', fontsize=16)
        plt.ylabel('Moisture Level', fontsize=16)
        plt.title('scatter plot - Moisture Level vs Time',fontsize=20)
        plt.gcf().autofmt_xdate()
        plt.grid(True)
        plt.savefig("MoistureLevelGraphImage.png", dpi=300)
        plt.show()



Graph = GraphDrawer()
Graph.draw_light_level_graph()
Graph.draw_moisture_level_graph()