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
    print "Import error - room sensor"


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

    def decode_data(self, rxData):
        if rxData[3] == "t":
            if(rxData[4] == "1"):
                bufTemp = ('-{}.{}'.format(rxData[5:7], rxData[7]))
            else:
                bufTemp = ('{}.{}'.format(rxData[5:7], rxData[7]))
            self.temp = float(bufTemp)
            self.humi = float('{}.{}'.format(rxData[8:10], rxData[10]))
            sql.add_record_sensor_temp(self.databaseName, self.temp, self.humi)
            self.batt = int(rxData[11:14])
            self.time = datetime.datetime.now()
            self.error = False
            infoStrip.set_error(1, False)
            log.add_log(("Sensor {}  temp: {}°C  humi: {}%  power: {}".format(self.sensorName, self.temp, self.humi, self.batt)))
        if rxData[3] == "y":  # for bedroom sensor
            bufTemp = ("{}.{}".format(rxData[4:6], rxData[6]))
            print("test ---> {}".format(rxData[7:10]))
            if(len(rxData) > 9):
                bufHumi = (rxData[7:10])
            else:
                bufHumi = (rxData[7:9])  # +'.0')
            self.temp = float(bufTemp)
            self.humi = float(bufHumi)
            sql.add_record_sensor_temp(self.sqlRoom, self.temp, self.humi)
            self.time = datetime.datetime.now()  # zapisanie czasu ostatniego odbioru
            self.error = False 
            infoStrip.set_error(2, False)
            log.add_log("Sensor {}  temp: {}°C humi: {}%".format(self.sensorName, sekf.temp, self.humi))
        if rxData[3] == "?":
            ledLightRoom2.brightness = int(rxData[4:7])
            if(ledLightRoom2.brightness == 0):
                ledLightRoom2.flag = 0
            else:
                ledLightRoom2.flag = 1
            ledLightRoom2.flagManualControl = True
            ledLightRoom2.error = 0
            log.add_log(("Led Bedroom ON/OFF:{}  PWM:{}".format(ledLightRoom2.flag, ledLightRoom2.brightness)))
