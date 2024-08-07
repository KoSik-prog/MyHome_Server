#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:        timer
# Purpose:
#
# Author:      KoSik
#
# Created:     18.05.2022
# Copyright:   (c) kosik 2022
# -------------------------------------------------------------------------------
try:
    import time
    from lib.log import *
    from lib.sqlDatabase import *
    from lights import *
    from devicesList import *
except ImportError:
    print("Import error - timer")


class Timer:
    def timer_thread(self):
        while server.read_server_active_flag() == True:
            self.check_timer()
            time.sleep(10)

    def check_timer(self):
        # ----------------------SQL records check -------------------------------------------------
        if (str(time.strftime("%d")) == "01") and (str(time.strftime("%H:%M")) == "01:00") and Sql.flagSqlRecordsDelete == False:
            sql.delete_records(30)  # delete old records
            Sql.flagSqlRecordsDelete = True
            log.add_log("Skasowano stare dane z SQL")
        if (str(time.strftime("%d")) == "01") and (str(time.strftime("%H:%M")) == "01:01") and Sql.flagSqlRecordsDelete == True:
            Sql.flagSqlRecordsDelete = False
        # ------------------------------------------------------------------------------------------
        self.auto_timer(ledStripRoom1)
        self.auto_timer(decorationRoom1)
        self.auto_timer(decoration2Room1)
        self.auto_timer(decorationFlamingo)
        self.auto_timer(ledLego)
        self.auto_timer(ledLightRoom2Tradfri)
        self.auto_timer(ledPhotosHeart)#---- LED SYPIALNI - serce ze zdjęciami
        self.auto_timer(hydroponics)
        self.auto_timer(kitchenLight)
        self.auto_timer(usbPlug)#----USB Stick
        self.auto_timer(ledTerrace)

    def auto_timer(self, deviceClass):
        format = '%H:%M:%S.%f'
        aktual = datetime.datetime.now().time()
        try:
            stampOn = datetime.datetime.strptime(
                str(aktual), format) - datetime.datetime.strptime(deviceClass.autoOn, format)
        except ValueError as e:
            print('stamp error:', e)
        try:
            stampOff = datetime.datetime.strptime(
                str(aktual), format) - datetime.datetime.strptime(deviceClass.autoOff, format) 
        except ValueError as e:
            print('stamp error:', e)
        if(int(stampOn.total_seconds()) > (-15) and int(stampOn.total_seconds()) < 0 and deviceClass.flagManualControl == True):
            deviceClass.flagManualControl = False
        if(int(stampOff.total_seconds()) > (-15) and int(stampOff.total_seconds()) < 0 and deviceClass.flagManualControl == True):
            deviceClass.flagManualControl = False
        # ------CHECK------------------------
        if(deviceClass.flag == 0 and sensorOutside.get_calulated_brightness() < deviceClass.autoLuxMin and (int(stampOn.total_seconds()) > 0) and (int(stampOff.total_seconds()) < (-60)) and deviceClass.flagManualControl == False and deviceClass.error < 20):
            log.add_log("AUTO {} -> ON".format(deviceClass.label))
            log.add_log("AUTO {} -> ON / brightnessCalc: {} / setting: {}".format(deviceClass.label, sensorOutside.get_calulated_brightness(), deviceClass.autoLuxMin))
            light.set_light(deviceClass.address, deviceClass.autoBrightness)
            deviceClass.flag = 1
            time.sleep(20)
        if(deviceClass.flag == 1 and (int(stampOff.total_seconds()) > 0) and (int(stampOff.total_seconds()) < 60) and deviceClass.flagManualControl == False and deviceClass.error < 20):
            log.add_log("AUTO {} -> OFF".format(deviceClass.label))
            light.set_light(deviceClass.address, 0)
            deviceClass.flag = 0
            time.sleep(20)


timer = Timer()
