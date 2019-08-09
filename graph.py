#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  9 12:00:53 2019

@author: pi
"""
import matplotlib.pyplot as plt
import datetime
import random

class GraphDrawer:
    
    '''def __init__(self):
        
        pass'''
        
    def fake_data(self):
        x_fake_data = []
        y_fake_data = []
                
        for day in range(1,28):
            for hour in range(1,24):
                x_fake_data.append(datetime.datetime(2016, 1, day, hour, 0, 0))
                if 0<hour<12:                 
                    y_fake_data.append(random.randrange(20*hour -20,20*hour))
                else:
                    y_fake_data.append(random.randrange(240 - (20*(hour-12)+20),240 - 20*(hour-12)))

        return [x_fake_data,y_fake_data]
    
    def read_data(self, file_location):
        #xLine=[63.3,57,64.3,63,71,61.8,62.9,65.6,64.8,63.1,68.3,69.7,65.4,66.3,60.7]
        #xLine = [datetime.datetime(2016, 1, 1, 16, 0, 0),datetime.datetime(2016, 1, 3, 13, 3),datetime.datetime(2016, 1, 4, 16, 0, 0),datetime.datetime(2016, 1, 8, 13, 3),datetime.datetime(2016, 1, 19, 16, 0, 0),datetime.datetime(2016, 1, 21, 13, 3)]
        #yLine = [156.3,100.7,114.8,156.3,237.1,123.9]
        #yLine=[156.3,100.7,114.8,156.3,237.1,123.9,151.8,164.7,105.4,136.1,175.2,137.4,164.2,151,124.3]
        fake_data = self.fake_data()
        xLine = fake_data[0]
        yLine = fake_data[1]
        
        return [xLine, yLine]
    
    def draw_graph(self):             
        plant_data = self.read_data("") 
        plt.figure(figsize=(14,5))
        plt.plot(plant_data[0],plant_data[1],c='b',marker='*')
        plt.xlabel('Time', fontsize=16)
        plt.ylabel('Light', fontsize=16)
        plt.title('scatter plot - Light vs Time',fontsize=20)
        plt.gcf().autofmt_xdate()
        plt.grid(True)
        plt.savefig("GraphImage.png", dpi=300)
        plt.show()





Graph = GraphDrawer()
Graph.draw_graph()