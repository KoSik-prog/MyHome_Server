#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:        deviceWaterCan
# Purpose:
#
# Author:      KoSik
#
# Created:     29.05.2022
# Copyright:   (c) kosik 2022
# -------------------------------------------------------------------------------
try:
    import datetime
    from lib.log import *
    from lib.sqlDatabase import *
except ImportError:
    print "Import error - water can"


class WaterCan:
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
        if data[3] == "k":
            if len(data) >= 17:
                self.light = data[4:7]
                self.humidity = data[7:10]
                self.water = data[10:13]
                self.power = data[13:16]
                self.watering = data[17]

                sql.add_record_watering_can(self.humidity, self.light, self.water, self.power,
                                            0, 0)  # ostatni parametr to podlanie poprawic!!!
                self.time = datetime.datetime.now()  # zapisanie czasu ostatniego odbioru

                log.add_log("   Kwiatek AutoKonewka wilgotnosc:{}  swiatlo:{}%  woda:{}x10ml  zas:{}%  podlanie:{}".format(
                    self.humidity, self.light, self.water, self.power, self.watering))
            else:
                log.add_log("   Kwiatek AutoKonewka blad skladni")
