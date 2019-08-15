#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 14 15:54:13 2019

@author: pi
"""

import email_handler
import datetime


class Email_Spreadsheet:

    def __init__(self):
        #self.email = email_handler.EmailHandler()
        #self.date = datetime.datetime()
        pass

    def send_email_every_friday(self):
        email_handler.EmailHandler.send_email(["mo214885@falmouth.ac.uk"],
                                              "someone@hotmail.com",
                                              "someone",
                                              "test",
                                              "This is a test",
                                              ["data.csv",
                                               "LightLevelGraphImage.png",
                                               "MoistureLevelGraphImage.png"])


if __name__ == '__main__':
    Email_Spreadsheet().send_email_every_friday()
