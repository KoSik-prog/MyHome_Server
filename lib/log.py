#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:        log.py
# Purpose:
#
# Author:      KoSik
#
# Created:     26.08.2022
# Copyright:   (c) kosik 2022
# -------------------------------------------------------------------------------
try:
    import sys
    import os
    import datetime
    import time
except ImportError:
    print("Import error - log")


class Log:
    busyFlag = False

    def __init__(self, filePath):
        self.filePath = filePath
        self.delete_log()
        self.delete_watchdog_log()

    def actualTime(self):
        return str(time.strftime("%H:%M"))

    def actualDate(self):
        return str(time.strftime("%d-%m-%Y"))

    def add_log(self, information):
        while self.busyFlag == True:
            time.sleep(0.001)
        self.busyFlag = True
        actFile = open(self.filePath + '/log.txt', 'a+')
        actFile.write(self.actualTime() + ' ' + information+'\n')
        actFile.close()
        self.busyFlag = False
        print(self.actualTime() + ' ' + information)

    def delete_log(self):
        while self.busyFlag == True:
            time.sleep(0.001)
        self.busyFlag = True
        actFile = open(self.filePath + '/log.txt', 'w')
        actFile.write(self.actualDate() + "  " + self.actualTime() + " LOG:\n")
        actFile.close()
        self.busyFlag = False

    def add_watchdog_log(self, information):
        while self.busyFlag == True:
            time.sleep(0.001)
        self.busyFlag = True
        actFile = open(self.filePath + '/watchdog_log.txt', 'a+')
        actFile.write(self.actualTime() + ' ' + information + '\n')
        actFile.close()
        self.busyFlag = False

    def delete_watchdog_log(self):
        while self.busyFlag == True:
            time.sleep(0.001)
        self.busyFlag = True
        actFile = open(self.filePath + '/watchdog_log.txt', 'w')
        actFile.write(self.actualDate() + "  " + self.actualTime() + " LOG:\n")
        actFile.close()
        self.busyFlag = False

    def add_error_log(self, information):
        while self.busyFlag == True:
            time.sleep(0.001)
        self.busyFlag = True
        actFile = open(self.filePath + '/error.txt', 'a+')
        actFile.write(self.actualTime() + ' ' + information + '\n')
        actFile.close()
        self.busyFlag = False

log = Log('Desktop/Home')
