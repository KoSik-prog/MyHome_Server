#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:        sensorFlower
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
    print("Import error - sensor flower")


class SensorFlower:
    light = 0
    humidity = 0
    power = 0

    def __init__(self, nr,  address, name, humiMin, humiMax):
        self.nr = nr
        self.address = address
        self.name = name
        self.humiMin = humiMin
        self.humiMax = humiMax
        self.time = datetime.datetime.now()

    def add_record(self, data):
        if data[3] == "k":
            if len(data) >= 17:
                self.light = int(data[4:7])
                self.power = data[11]+"."+data[12:14]
                self.humidity = self.get_val_from_min_max(self.humiMin, self.humiMax, data[7:11])

                self.time = datetime.datetime.now()
                sql.add_record_flower(self.nr, self.humidity, self.light, self.power)
                log.add_log("   Flower {}({}) Sun: {}%   Humi: {}%   Power: {}V".format(
                    self.name, self.nr, self.light, self.humidity, self.power))
            else:
                log.add_log("   Flower {}({}) data error!".format(self.name, self.nr))

    def return_humiMin(self):
        return self.humiMin

    def return_humiMax(self):
        return self.humiMax

    def get_val_from_min_max(self, min, max, value):
        if(float(value) < min):
            return 0
        elif(float(value) > max):
            return 100
        else:
            diff = max - min
            result = ((100.0/diff)*float(value)) + ((-min)*(100.0/diff))
            return int(round(result))
        
    def get_name(self):
        return self.name
