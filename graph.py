#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  9 12:00:53 2019

@author: pi
"""
import matplotlib.pyplot as plt
import csv_recording
from matplotlib.dates import DateFormatter


class GraphDrawer:

    def __init__(self):
        self.point_shape = "."
        self.formatter = DateFormatter('%d/%m/%Y\n%H:%M')
        # Point shape options
        # "." = point
        # "," = pixel
        # "o" = circle
        # "^" = triangle_up
        # "v" = triangle_down
        # "8" = octagon
        # "s" = square
        # "p" = pentagon
        # "*" = star
        # "h" = hexagon
        # "+" = plus
        # "D" = diamond

    def draw_light_level_graph(self, name="data.csv"):
        CSV_handler = csv_recording.CSVRecording(name)
        plant_data = CSV_handler.read_data(2)
        plt.figure(figsize=(14, 5))
        plt.plot(plant_data[0], plant_data[1], c='b', marker=self.point_shape) #linewidth = 0
        plt.xlabel('Time', fontsize=16)
        plt.ylabel('Light', fontsize=16)
        plt.title('scatter plot - Light vs Time', fontsize=20)
        plt.gcf().axes[0].xaxis.set_major_formatter(self.formatter)
        plt.grid(True)
        plt.savefig("LightLevelGraphImage.png", dpi=300)
        plt.show()

    def draw_moisture_level_graph(self, name="data.csv"):
        CSV_handler = csv_recording.CSVRecording(name)
        plant_data = CSV_handler.read_data(1)
        plt.figure(figsize=(14, 5))
        plt.plot(plant_data[0], plant_data[1], c='r', marker=self.point_shape)
        plt.xlabel('Time', fontsize=16)
        plt.ylabel('Moisture Level', fontsize=16)
        plt.title('scatter plot - Moisture Level vs Time', fontsize=20)
        plt.gcf().axes[0].xaxis.set_major_formatter(self.formatter)
        plt.grid(True)
        plt.savefig("MoistureLevelGraphImage.png", dpi=300)
        plt.show()


Graph = GraphDrawer()
Graph.draw_light_level_graph("data.csv")
Graph.draw_moisture_level_graph("data.csv")
