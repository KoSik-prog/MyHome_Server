#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:        tasmota
# Purpose:
#
# Author:      KoSik
#
# Created:     23.11.2022
# Copyright:   (c) kosik 2022
# -------------------------------------------------------------------------------
# try:
from urllib.request import urlopen
from devicesList import *
from lib.log import *
from time import gmtime, localtime, strftime
import json
import time
# except ImportError:
#     print("Import error - tasmota")


class Tasmota:
    name = ""
    power = 0
    current = 0
    voltage = 0
    energyArray = []
    energyTotal = 0
    
    def __init__(self, address):
        self.address = address

    def tasmota_thread(self):
        while server.read_server_active_flag() == True:
            self.get_data_from_device(self.address)
            time.sleep(120)
            
    def get_data_from_device(self, address):
        url = "http://{}/cm?cmnd=status0".format(address)
        try:
            response = urlopen(url)
            contents = response.read()
            tasmotaStatus = json.loads(contents)
            log.add_log("Tasmota -> data received")

            part = tasmotaStatus["Status"]
            self.name = part["DeviceName"]

            snsStatus = tasmotaStatus["StatusSNS"]
            energyStatus = snsStatus["ENERGY"]
            self.energyTotal = float(energyStatus["Total"])
            self.power = energyStatus["Power"]
            self.voltage = energyStatus["Voltage"]
            
            while len(self.energyArray) > 60:
                self.energyArray.pop(0)
            self.energyArray.append([strftime("%H:%M", localtime()), self.power])
        except:
            log.add_log("Tasmota -> can't read device")
        
    def get_json_data(self):
        jsonData = {
            "name": self.name,
            "voltage": self.voltage,
            "power": self.power,
            "energyTotal": self.energyTotal,
            "energyArray": self.energyArray,
        }
        return jsonData
        
tasmota = Tasmota("192.168.0.101")
        
