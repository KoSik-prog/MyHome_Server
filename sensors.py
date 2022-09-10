#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:        sensors
# Purpose:
#
# Author:      KoSik
#
# Created:     18.05.2022
# Copyright:   (c) kosik 2022
# -------------------------------------------------------------------------------
try:
    import datetime
except ImportError:
    print "Blad importu"

from lib.log import *
from devicesList import *
from lib.infoStrip import *
from sensorOutside import *


class Sensors:
    minBatteryVoltage = 2.55
    minHumidity = 10

    def check_sensors_thread(self):
        while(1):
            self.check_sensor()
            time.sleep(10)

    def set_receive_error_on_strip(self, myClass, time, errorNumber):
        if((datetime.datetime.now() - myClass.time) > (datetime.timedelta(minutes=time))):
            infoStrip.set_error(errorNumber, True)

    def set_power_error_on_strip(self, myClass, minPower, errorNumber):
        if(myClass.power <= minPower):
            infoStrip.set_error(errorNumber, True)
        else:
            infoStrip.set_error(errorNumber, False)

    def set_min_humidity_error_on_strip(self, myClass, errorNumber):
        if(myClass.humidity <= Sensors.minHumidity and myClass.light < 60):
            infoStrip.set_error(errorNumber, True)
        else:
            infoStrip.set_error(errorNumber, False)

    def check_sensor(self):
        self.set_receive_error_on_strip(sensorOutside, 18, 0)
        self.set_receive_error_on_strip(sensorRoom1Temperature, 23, 1)
        self.set_receive_error_on_strip(sensorRoom2Temperature, 23, 2)
        self.set_receive_error_on_strip(sensorFlower2, 63, 4)
        self.set_receive_error_on_strip(sensorFlower3, 63, 5)
        self.set_receive_error_on_strip(sensorFlower4, 63, 6)
        self.set_receive_error_on_strip(sensorFlower5, 63, 16)
        self.set_receive_error_on_strip(sensorFlower6, 63, 19)
        # sprawdzenie stanu baterii
        self.set_power_error_on_strip(sensorFlower2, Sensors.minBatteryVoltage, 8)
        self.set_power_error_on_strip(sensorFlower3, Sensors.minBatteryVoltage, 9)
        self.set_power_error_on_strip(sensorFlower4, Sensors.minBatteryVoltage, 10)
        self.set_power_error_on_strip(sensorFlower5, Sensors.minBatteryVoltage, 14)
        self.set_power_error_on_strip(sensorFlower6, Sensors.minBatteryVoltage, 17)
        # sprawdzenie wilgotnosci
        self.set_min_humidity_error_on_strip(sensorFlower2, 11)
        self.set_min_humidity_error_on_strip(sensorFlower3, 12)
        self.set_min_humidity_error_on_strip(sensorFlower4, 13)
        self.set_min_humidity_error_on_strip(sensorFlower5, 15)
        self.set_min_humidity_error_on_strip(sensorFlower6, 18)
        # sprawdzenie budy
        if((datetime.datetime.now() - dogHouse.time) > (datetime.timedelta(minutes=2))):
            dogHouse.temp1 = 0.0
            dogHouse.temp2 = 0.0
            dogHouse.temp3 = 0.0
            dogHouse.czujnikZajetosciflaga = 0
            dogHouse.czujnikZajetosciRaw = 0


sensor = Sensors()
