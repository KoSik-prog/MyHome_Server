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
except ImportError:
    print "Import error"

from lib.log import *
from lib.sqlDatabase import *
from lib.infoStrip import *


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

    def __init__(self):
        self.time = datetime.datetime.now()

    def add_record(self, data):
        if data[3] == "s":
            self.light = int(data[4:9])
            self.ir = int(data[9:14])
            self.power = int(data[14:18])
            sql.add_record_sensor_outdoor_light(self.light, self.ir)
            self.calculate_light()
            log.add_log("Calculated light: {}".format(lightingAutomation.calculatedBrightness))
            log.add_log("Sensor outside -> light: {}    lightIR: {}    power: {}".format(self.light, self.ir, self.power))
        if data[3] == "t":
            if(data[4] == "1"):
                tempVal = ('-' + data[5:7] + "." + data[7])
            else:
                tempVal = (data[5:7] + "." + data[7])
            self.temperature = float(tempVal)
            self.humi = float(data[8:10] + "." + data[10])

            sql.add_record_sensor_outdoor_temp(self.temperature, self.humi, self.windSpeed, self.windDirection)
            self.windSpeed = float(data[11:13]+'.'+data[13])
            self.windDirection = int(data[14:17])
            self.time = datetime.datetime.now()
            self.errorFlag = False
            infoStrip.set_error(0, False)
            log.add_log("Sensor outside -> temp: {}*C   humi: {}%   wind: {}m/s   dir:{}".format(self.temperature,
                                                                                                 self.humi, self.windSpeed, self.windDirection))

    def calculate_light(self):
        k = 3  # amplifier
        for i in range(4):
            lightingAutomation.LUXvalue[i] = lightingAutomation.LUXvalue[i+1]
        lightingAutomation.LUXvalue[4] = self.light
        lightingAutomation.calculatedBrightness = lightingAutomation.LUXvalue[0]
        for i in range(4):
            lightingAutomation.calculatedBrightness = lightingAutomation.calculatedBrightness + \
                lightingAutomation.LUXvalue[i+1]
        lightingAutomation.calculatedBrightness = (
            lightingAutomation.calculatedBrightness + ((lightingAutomation.LUXvalue[4]*k))) / (5+k)
        if lightingAutomation.calculatedBrightness < self.nightSetting:
            self.nightFlag = True
        else:
            self.nightFlag = False
        log.add_log("Calculated outside light: {}".format(lightingAutomation.calculatedBrightness) +
                    " / {}".format(lightingAutomation.LUXvalue))


sensorOutside = SensorOutside()
