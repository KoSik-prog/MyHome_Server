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
    from lib.infoStrip import *
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

    def handle_nrf(self, data):
        if data[1:3] == "12":  # kwiatek 2  addres 12
            self.add_record(data)
            infoStrip.set_error(4, False)  # poprawic - przeniesc do klasy urzadzenia
            return True
        # ------------------------------------------------------------------------------------------------------------
        elif data[1:3] == "13":  # kwiatek 3 adres 13
            self.add_record(data)
            infoStrip.set_error(5, False)
            return True
        # ------------------------------------------------------------------------------------------------------------
        elif data[1:3] == "14":  # kwiatek 5 adres 14
            self.add_record(data)
            infoStrip.set_error(16, False)
            return True
        return False

    def add_record(self, data): #12k 000 0998 306
        if data[3] == "k":
            if len(data) >= 14:
                self.light = int(data[4:7])
                self.humidity = self.get_val_from_min_max(self.humiMin, self.humiMax, data[7:11])
                self.power = data[11]+"."+data[12:14]

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
            
    def handle_socketService(self, message):
        return [0]

    def auto_timer(self):
        return
        
    def get_name(self):
        return self.name

    def to_dict(self):
        return self.__dict__

    def from_dict(self, data):
        self.__dict__.update(data)

    def set_param(self, param, setting):
        setattr(self, param, setting)

    def get_param(self, param):
        return getattr(self, param, None)
