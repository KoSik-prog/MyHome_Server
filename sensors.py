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
    minimalneNapiecieBaterii=2.55
    minimalnaWilgotnosc = 10

    def checkSensors(self): #watek
        while(1):
            self.checkSensor()
            time.sleep(10)

    def checkSensor(self):
        if((datetime.datetime.now() - czujnikZew.czas)>(datetime.timedelta(minutes=18))):
            infoStrip.set_error(0,True)
        if((datetime.datetime.now() - czujnikPok1.czas)>(datetime.timedelta(minutes=23))):
            infoStrip.set_error(1,True)
        if((datetime.datetime.now() - czujnikPok2.czas)>(datetime.timedelta(minutes=23))):
            infoStrip.set_error(2,True)
        if((datetime.datetime.now() - czujnikKwiatek.czas)>(datetime.timedelta(minutes=63))):
            infoStrip.set_error(3,True)
        if((datetime.datetime.now() - czujnikKwiatek2.czas)>(datetime.timedelta(minutes=63))):
            infoStrip.set_error(4,True)
        if((datetime.datetime.now() - czujnikKwiatek3.czas)>(datetime.timedelta(minutes=63))):
            infoStrip.set_error(5,True)
        if((datetime.datetime.now() - czujnikKwiatek4.czas)>(datetime.timedelta(minutes=63))):
            infoStrip.set_error(6,True)
        if((datetime.datetime.now() - czujnikKwiatek5.czas)>(datetime.timedelta(minutes=63))):
            infoStrip.set_error(16,True)
        if((datetime.datetime.now() - czujnikKwiatek6.czas)>(datetime.timedelta(minutes=63))):
            infoStrip.set_error(19,True)
        #sprawdzenie budy
        if((datetime.datetime.now() - buda.czas)>(datetime.timedelta(minutes=2))):
            buda.temp1=0.0
            buda.temp2=0.0
            buda.temp3=0.0
            buda.czujnikZajetosciFlaga=0
            buda.czujnikZajetosciRaw=0
        #sprawdzenie stanu baterii
        if(czujnikKwiatek.zasilanie <= 5):
            infoStrip.set_error(7,True)
        else:
            infoStrip.set_error(7,False)
        if(czujnikKwiatek2.zasilanie <= SENSORS_CL.minimalneNapiecieBaterii):
            infoStrip.set_error(8,True)
        else:
            infoStrip.set_error(8,False)
        if(czujnikKwiatek3.zasilanie <= SENSORS_CL.minimalneNapiecieBaterii):
            infoStrip.set_error(9,True)
        else:
            infoStrip.set_error(9,False)
        if(czujnikKwiatek4.zasilanie <= SENSORS_CL.minimalneNapiecieBaterii):
            infoStrip.set_error(10,True)
        else:
            infoStrip.set_error(10,False)
        if(czujnikKwiatek2.wilgotnosc <= SENSORS_CL.minimalnaWilgotnosc and czujnikKwiatek2.slonce < 60):
            infoStrip.set_error(11,True)
        else:
            infoStrip.set_error(11,False)
        if(czujnikKwiatek3.wilgotnosc <= SENSORS_CL.minimalnaWilgotnosc and czujnikKwiatek3.slonce < 60):
            infoStrip.set_error(12,True)
        else:
            infoStrip.set_error(12,False)
        if(czujnikKwiatek4.wilgotnosc <= SENSORS_CL.minimalnaWilgotnosc and czujnikKwiatek4.slonce < 60):
            infoStrip.set_error(13,True)
        else:
            infoStrip.set_error(13,False)
        if(czujnikKwiatek5.zasilanie <= SENSORS_CL.minimalneNapiecieBaterii):
            infoStrip.set_error(14,True)
        else:
            infoStrip.set_error(14,False)
        if(czujnikKwiatek5.wilgotnosc <= SENSORS_CL.minimalnaWilgotnosc and czujnikKwiatek5.slonce < 60):
            infoStrip.set_error(15,True)
        else:
            infoStrip.set_error(15,False)
        if(czujnikKwiatek6.zasilanie <= SENSORS_CL.minimalneNapiecieBaterii):
            infoStrip.set_error(17,True)
        else:
            infoStrip.set_error(17,False)
        if(czujnikKwiatek6.wilgotnosc <= SENSORS_CL.minimalnaWilgotnosc and czujnikKwiatek6.slonce < 60):
            infoStrip.set_error(18,True)
        else:
            infoStrip.set_error(18,False)
sensor = SENSORS_CL()