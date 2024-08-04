#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:        sensor room
# Author:      KoSik
#
# Created:     29.05.2022
# Copyright:   (c) kosik 2022
# -------------------------------------------------------------------------------
try:
    import datetime
    from devicesList import *
    from lib.sqlDatabase import *
    from lib.log import *
    from lib.infoStrip import *
except ImportError:
    print("Import error - room sensor")


class SensorRoom:
    temp = 0.0
    humi = 0.0
    batt = 0.0
    time = datetime.datetime.now()
    error = False

    def __init__(self, sensorName, databaseName):
        self.sensorName = sensorName
        self.databaseName = databaseName
        self.time = datetime.datetime.now()
        self.temp = 0.0
        self.humi = 0.0
        self.batt = 0.0
        self.error = False
        
    def get_json_data(self):
        retData = {
            "name": self.sensorName,
            "temperature": self.temp,
            "humidity": self.humi,
            "power": self.batt
            } 
        return retData

    def handle_nrf(self, data):
        if data[1:3] == "04":  # for room sensor
            if data[3] == "t":
                if(data[4] == "1"):
                    bufTemp = ('-{}.{}'.format(data[5:7], data[7]))
                else:
                    bufTemp = ('{}.{}'.format(data[5:7], data[7]))
                self.temp = float(bufTemp)
                self.humi = float('{}.{}'.format(data[8:10], data[10]))
                sql.add_record_sensor_temp(self.databaseName, self.temp, self.humi)
                self.batt = int(data[11:14])
                self.time = datetime.datetime.now()
                self.error = False
                infoStrip.set_error(1, False)
                log.add_log(("Sensor {}  temp: {}°C  humi: {}%  power: {}".format(self.sensorName, self.temp, self.humi, self.batt)))
        if data[1:3] == "02":  # for bedroom sensor
            if data[3] == "t":
                bufTemp = ("{}.{}".format(data[5:7], data[7]))
                bufHumi = (data[7:9])  # +'.0')
                self.temp = float(bufTemp)
                self.humi = float(bufHumi)
                sql.add_record_sensor_temp(self.databaseName, self.temp, self.humi)
                self.time = datetime.datetime.now()
                self.error = False 
                infoStrip.set_error(2, False)
                log.add_log("Sensor {}  temp: {}°C humi: {}%".format(self.sensorName, self.temp, self.humi))

    def handle_socketService(self, message):
        return [0]

    def auto_timer(self):
        return
    
    def to_dict(self):
        return self.__dict__

    def from_dict(self, data):
        self.__dict__.update(data)

    def set_param(self, param, setting):
        setattr(self, param, setting)

    def get_param(self, param):
        return getattr(self, param, None)

    def get_address_value(self):
        addrStr = f"{self.address[-2]:02x}{self.address[-1]:02x}"
        return addrStr[1:3]