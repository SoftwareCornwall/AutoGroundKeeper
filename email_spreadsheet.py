#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 14 15:54:13 2019

@author: pi
"""

import email_handler
import graph
import time



class Email_Spreadsheet:

    def __init__(self, config):
        self._config = config
        pass

    def send_spreadsheet_and_graph(self, file_name):
        Graph = graph.GraphDrawer()
        email = email_handler.EmailHandler(self._config)
        Graph.draw_light_level_graph(file_name)
        Graph.draw_moisture_level_graph(file_name)
        email.send_email("Info", "Data on light and moisture of plant", [file_name, "LightGraph.png", "MoistureGraph.png"])
    def send_email_every_week(self, file_name):
        self.send_spreadsheet_and_graph(file_name)
        return time.time() + 10

