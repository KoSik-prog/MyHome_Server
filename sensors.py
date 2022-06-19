#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        sensors
# Purpose:
#
# Author:      KoSik
#
# Created:     18.05.2022
# Copyright:   (c) kosik 2022
#-------------------------------------------------------------------------------
try:
    import datetime
except ImportError:
    print "Blad importu"

from libraries.log import *
from devicesList import *
from libraries.infoStrip import *

class SENSORS_CL:
    minBatteryVoltage=2.55
    minHumidity = 10

    def check_sensors(self): #watek
        while(1):
            self.check_sensor()
            time.sleep(10)

    def set_receive_error_on_strip(self, myClass, time, errorNumber):
        if((datetime.datetime.now() - myClass.time) > (datetime.timedelta(minutes = time))):
            infoStrip.set_error(errorNumber,True)

    def set_power_error_on_strip(self, myClass, minPower, errorNumber):
        if(myClass.power <= minPower):
            infoStrip.set_error(errorNumber, True)
        else:
            infoStrip.set_error(errorNumber, False)

    def set_min_humidity_error_on_strip(self, myClass, errorNumber):
        if(myClass.humidity <= SENSORS_CL.minHumidity and myClass.light < 60):
            infoStrip.set_error(errorNumber, True)
        else:
            infoStrip.set_error(errorNumber, False)

    def check_sensor(self):
        self.set_receive_error_on_strip(czujnikZew, 18, 0)
        self.set_receive_error_on_strip(czujnikPok1, 23, 1)
        self.set_receive_error_on_strip(czujnikPok2, 23, 2)
        self.set_receive_error_on_strip(automatycznaKonewka, 63, 3)
        self.set_receive_error_on_strip(czujnikKwiatek2, 63, 4)
        self.set_receive_error_on_strip(czujnikKwiatek3, 63, 5)
        self.set_receive_error_on_strip(czujnikKwiatek4, 63, 6)
        self.set_receive_error_on_strip(czujnikKwiatek5, 63, 16)
        self.set_receive_error_on_strip(czujnikKwiatek6, 63, 19)
        #sprawdzenie stanu baterii
        self.set_power_error_on_strip(automatycznaKonewka, 5, 7)
        self.set_power_error_on_strip(czujnikKwiatek2, SENSORS_CL.minBatteryVoltage, 8)
        self.set_power_error_on_strip(czujnikKwiatek3, SENSORS_CL.minBatteryVoltage, 9)
        self.set_power_error_on_strip(czujnikKwiatek4, SENSORS_CL.minBatteryVoltage, 10)
        self.set_power_error_on_strip(czujnikKwiatek5, SENSORS_CL.minBatteryVoltage, 14)
        self.set_power_error_on_strip(czujnikKwiatek6, SENSORS_CL.minBatteryVoltage, 17)
        #sprawdzenie wilgotnosci
        self.set_min_humidity_error_on_strip(czujnikKwiatek2, 11)
        self.set_min_humidity_error_on_strip(czujnikKwiatek3, 12)
        self.set_min_humidity_error_on_strip(czujnikKwiatek4, 13)
        self.set_min_humidity_error_on_strip(czujnikKwiatek5, 15)
        self.set_min_humidity_error_on_strip(czujnikKwiatek6, 18)
        #sprawdzenie budy
        if((datetime.datetime.now() - buda.time)>(datetime.timedelta(minutes=2))):
            buda.temp1=0.0
            buda.temp2=0.0
            buda.temp3=0.0
            buda.czujnikZajetosciFlaga=0
            buda.czujnikZajetosciRaw=0
sensor = SENSORS_CL()