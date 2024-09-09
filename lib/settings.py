#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:        settings
# Purpose:
#
# Author:      KoSik
#
# Created:     17.05.2022
# Copyright:   (c) kosik 2022
# -------------------------------------------------------------------------------
try:
    import xml.etree.cElementTree as ET
    from lib.log import *
    from lib.weatherForecast import *
    from devicesList import *
    from lib.watchdog import *
    import json
except ImportError:
    print("Import error - settings")
    

class Settings:
    def __init__(self, path):
        self.path = path

    def start_read(self):
        while(1):
            self.read()
            watchdog.reset()
            time.sleep(60)


    def save(self):
        print("SETTINGS SAVE!")
        dataToSave = []
        for device in deviceArray:
            dataToSave.append(device.to_dict())
        try:
            with open(self.path, 'w') as file:
                json.dump(dataToSave, file, default=self.json_serial, indent=4)
                log.add_log("Settings saved")
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False

    @staticmethod
    def json_serial(obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        raise TypeError(f"Type {type(obj)} not serializable")
        
    def read(self):
        allowed_keys = {"label", "autoOn", "autoOff", "autoLuxMin", "autoBrightness", "address", "nrfPower"}
        try:
            with open(self.path, 'r') as file:
                data = json.load(file)
                for device_data in data:
                    device_name = device_data.get("name")
                    matching_device = next((device for device in deviceArray if device.name == device_name), None)
                    if matching_device:
                        filtered_data = {key: device_data[key] for key in allowed_keys if key in device_data}
                        matching_device.from_dict(filtered_data)
                return True
        except Exception as e:
            print(f"Error: {e}")
            return False


settings = Settings("/var/www/html/settings.json")