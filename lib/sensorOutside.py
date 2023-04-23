#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:        sensorOutside
# Author:      KoSik
#
# Created:     29.05.2022
# Copyright:   (c) kosik 2022
# -------------------------------------------------------------------------------
try:
    import datetime
    from devicesList import *
    from lib.log import *
    from lib.sqlDatabase import *
    from lib.infoStrip import *
except ImportError:
    print("Import error - sensor outside")


class SensorOutside:
    temperature = 0.0
    humidity = 0.0
    power = 0.0
    light = 0
    ir = 0
    windSpeed = 0
    windDirection = 0
    time = datetime.datetime.now()
    errorFlag = False
    nightFlag = False
    nightSetting = 60
    LUXvalue = [2000, 2000, 2000, 2000, 2000]
    calculatedBrightness = 2000

    def __init__(self):
        self.time = datetime.datetime.now()
        
    def get_json_data(self):
        retData = {
            "name": "sensorOutside",
            "temperature": self.temperature,
            "humidity": self.humidity,
            "power": self.power,
            "light": self.light,
            "ir": self.ir,
            "windspeed": self.windSpeed
            } 
        return retData

    def add_record(self, data):
        if data[3] == "s":
            self.light = int(data[4:9])
            self.ir = int(data[9:14])
            self.power = int(data[14:18])
            sql.add_record_sensor_outdoor_light(self.light, self.ir)
            self.calculate_light()
            log.add_log("Sensor outside -> light: {}    lightIR: {}    power: {}".format(self.light, self.ir, self.power))
        if data[3] == "t":
            if(data[4] == "1"):
                tempVal = ('-' + data[5:7] + "." + data[7])
            else:
                tempVal = (data[5:7] + "." + data[7])
            self.temperature = float(tempVal)
            self.humidity = float(data[8:10] + "." + data[10])

            sql.add_record_sensor_outdoor_temp(self.temperature, self.humidity, self.windSpeed, self.windDirection)
            self.windSpeed = float(data[11:13]+'.'+data[13])
            self.windDirection = int(data[14:17])
            self.time = datetime.datetime.now()
            self.errorFlag = False
            infoStrip.set_error(0, False)
            log.add_log("Sensor outside -> temp: {}°C   humi: {}%   wind: {}m/s   dir:{}".format(self.temperature,
                                                                                                 self.humidity, self.windSpeed, self.windDirection))

    def calculate_light(self):
        k = 3  # amplifier
        for i in range(4):
            self.LUXvalue[i] = self.LUXvalue[i+1]
        self.LUXvalue[4] = self.light
        self.calculatedBrightness = self.LUXvalue[0]
        for i in range(4):
            self.calculatedBrightness = self.calculatedBrightness + \
                self.LUXvalue[i+1]
        self.calculatedBrightness = (
            self.calculatedBrightness + ((self.LUXvalue[4]*k))) / (5+k)
        if self.calculatedBrightness < self.nightSetting:
            self.nightFlag = True
        else:
            self.nightFlag = False
        log.add_log("Calculated outside light: {} / {}".format(self.calculatedBrightness, self.LUXvalue))
        
    def get_calulated_brightness(self):
        return self.calculatedBrightness
