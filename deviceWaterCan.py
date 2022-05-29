#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        deviceWaterCan
# Purpose:
#
# Author:      KoSik
#
# Created:     29.05.2022
# Copyright:   (c) kosik 2022
#-------------------------------------------------------------------------------
try:
    import datetime
except ImportError:
    print "Import error"

from libraries.log import *
from libraries.sqlDatabase import *


class DEVICE_WATER_CAN_CL:
    humidity = 0
    light = 0
    water = 0
    power = 0
    watering = 0

    def __init__(self, address, name):
        self.address = address
        self.name = name
        self.time = datetime.datetime.now()

    def add_record(self, data):
        if data[3]== "k":
            if len(data) >= 17:
                self.light = data[4:7]
                self.humidity = data[7:10]
                self.water = data[10:13]
                self.power = data[13:16]
                self.watering = data[17]

                sql.addRecordWateringCan(self.humidity, self.light, self.woda, self.power, 0, 0) #ostatni parametr to podlanie poprawic!!!
                self.time=datetime.datetime.now() #zapisanie czasu ostatniego odbioru
                infoStrip.set_error(3,False)

                if(czujnikKwiatek.woda < 10):
                    infoStrip.set_error(20,False)
                log.add_log("   Kwiatek AutoKonewka swiatlo:{}%  wilgotnosc:{}  woda:{}x10ml  zas:{}%  podlanie:{}".format(self.light, self.humidity, self.water, self.power, self.watering))
            else:
                log.add_log("   Kwiatek AutoKonewka blad skladni")