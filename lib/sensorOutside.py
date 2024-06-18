#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:        sensorOutside
# Author:      KoSik
#
# Created:     29.05.2022
# Copyright:   (c) kosik 2022
# -------------------------------------------------------------------------------
# try:
from devicesList import *
import datetime
from lib.log import *
from lib.sqlDatabase import *
from lib.infoStrip import *
import numpy as np
# except ImportError:
#     print("Import error - sensor outside")


class SensorOutside:
    temperature = 0.0
    humidity = 0.0
    airPressure = 0
    power = 0.0
    light = 0
    windX = 0
    windY = 0
    windSpeed = 0
    windDirection = 0
    time = datetime.datetime.now()
    errorFlag = False
    nightFlag = False
    nightSetting = 60
    LUXvalue = [2000, 2000, 2000, 2000, 2000]
    calculatedBrightness = 2000
    directionOffset = 83

    def __init__(self):
        self.time = datetime.datetime.now()
        
    def get_json_data(self):
        retData = {
            "name": "sensorOutside",
            "temperature": self.temperature,
            "humidity": self.humidity,
            "airPressure": self.airPressure,
            "light": self.light,
            "power": self.power,
            "windspeed": self.windSpeed,
            "winddirection": self.windDirection,
            "directionOffset": self.directionOffset,
            } 
        return retData

    def add_record(self, data):
        if data[3] == "t":
            self.temperature = (float(data[4:8])) / 10
            self.humidity = int(data[8:11])
            self.airPressure = int(data[11:15])
            self.light = int(data[15:21])
            self.power = (float(data[21:24])) / 100 
            sql.add_record_sensor_outdoor_temp(self.temperature, self.humidity, self.airPressure, self.light, self.power)
            self.calculate_light()
            self.time = datetime.datetime.now()
            self.errorFlag = False
            infoStrip.set_error(0, False)
            log.add_log("Sensor outside -> temp: {}°C  humi: {}%   press: {}hPa  light: {}lux  power: {}V".format(self.temperature, self.humidity, self.airPressure, self.light, self.power))
        if data[3] == "w":
            self.windX = int(data[4:11])
            self.windY = int(data[11:18])
            calibrationCounter = int(data[18:21])
            cycleCounter = int(data[21:24])
            self.calculate_wind()
            sql.add_record_sensor_wind(self.windSpeed, self.windDirection)
            log.add_log("Sensor outside -> {}/{} direction:{:.0f}°  speed:{:.0f}kmh  calibCounter: {} cycleCounter: {}".format(self.windX, self.windY, self.windDirection, self.windSpeed, calibrationCounter, cycleCounter))

    def calculate_wind(self):
        self.windDirection = self.points_to_direction(self.windX, self.windY, self.directionOffset)
        self.windSpeed = self.points_to_speed(self.windX, self.windY)

    def points_to_direction(self, x, y, offset=0):
        directionRadians = np.arctan2(y, x)
        directionDegrees = np.degrees(directionRadians) + offset

        directionDegrees %= 360
        return int(directionDegrees)
    
    def points_to_speed(self, x, y):
        # data for wind calibration
        # 10kmh - 4500
        # 25kmh - 15000
        windForce = np.sqrt(x**2 + y**2)
        # forcesWind = np.array([0, 4500, 15000])
        # speedsWind = np.array([0, 10, 25])  # km/h
        # return int(np.interp(windForce, forcesWind, speedsWind))

        windSpeed = (0.001428 * windForce) + 3.57
        if(windSpeed < 0):
            windSpeed = 0
        return int(windSpeed)

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
