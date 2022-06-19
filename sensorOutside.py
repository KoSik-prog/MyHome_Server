#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        sensorOutside
# Purpose:
#
# Author:      KoSik
#
# Created:     29.05.2022
# Copyright:   (c) kosik 2022
#-------------------------------------------------------------------------------
try:
    import datetime
except ImportError:
    print "Import error"

from libraries.log import *
from libraries.sqlDatabase import *

class SENSOR_OUTSIDE_CL:
    temperature=0.0
    humidity=0.0
    power=0.0
    light=0
    ir=0
    windSpeed=0
    windDirection=0
    time=datetime.datetime.now()
    errorFlag = False
    nightFlag = False
    noc_ustawienie=60  #ustawienie kiedy noc
    flaga_peirwszaPaczka=False

    def __init__(self, address):
        self.time = datetime.datetime.now()

    def add_record(self, data):
        if data[3]== "s":
            self.light=int(data[4:9])
            self.ir=int(data[9:14])
            self.power=int(data[14:18])
            sql.addRecordSensorOutdoorLight(self.light, self.ir)
            self.calculate_light()
            log.add_log("Obliczylem, ze swiatlo wynosci: {}".format(automatykaOswietlenia.swiatloObliczone))
            log.add_log("   Sensor1 zewnetrzny ->   light: {}    lightIR: {}    Bateria: {}".format(self.light, self.ir, self.power))
        if data[3]== "t":
            if(data[4]=="1"):
                tempVal=('-'+data[5:7]+"."+data[7])
            else:
                tempVal=(data[5:7]+"."+data[7])
            self.temperature=float(tempVal)
            self.humi=float(data[8:10]+"."+data[10])

            sql.add_record_sensor_outdoor_temp(self.temperature, self.humi, self.windSpeed, self.windDirection)
            self.windSpeed = float(data[11:13]+'.'+data[13])
            self.windDirection = int(data[14:17])
            self.time=datetime.datetime.now() #zapisanie czasu ostatniego odbioru
            self.errorFlag = False #kasowanie bledu
            infoStrip.set_error(0,False)
            log.add_log("   Sensor1 zewnetrzny Temp: {}*C   Wilg: {}%   Wiatr: {}m/s   Kier:{}".format(self.temperature, self.humi, self.windSpeed, self.windDirection))

    def calculate_light(self):
        k=3 #wzmocnienie
        for i in range(4):
            automatykaOswietlenia.wartosciLux[i]=automatykaOswietlenia.wartosciLux[i+1]
        automatykaOswietlenia.wartosciLux[4]=czujnikZew.lux
        automatykaOswietlenia.swiatloObliczone=automatykaOswietlenia.wartosciLux[0]
        for i in range(4):
            automatykaOswietlenia.swiatloObliczone=automatykaOswietlenia.swiatloObliczone+automatykaOswietlenia.wartosciLux[i+1]
        automatykaOswietlenia.swiatloObliczone=(automatykaOswietlenia.swiatloObliczone+((automatykaOswietlenia.wartosciLux[4]*k)))/(5+k)
        if automatykaOswietlenia.swiatloObliczone<czujnikZew.noc_ustawienie:
            czujnikZew.nightFlag = True
        else:
            czujnikZew.nightFlag = False
        log.add_log("Swiatlo obliczone=  {}".format(automatykaOswietlenia.swiatloObliczone) + " / {}".format(automatykaOswietlenia.wartosciLux))