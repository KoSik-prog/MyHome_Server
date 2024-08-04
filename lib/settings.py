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
        dataToSave = [ledStripRoom1.to_dict(), kitchenLight.to_dict(), ledLego.to_dict(), ledPhotosHeart.to_dict()]
        try:
            with open(self.path, 'w') as file:
                json.dump(dataToSave, file)
                log.add_log("Settings saved")
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False
        
    def read(self):
        try:
            with open(self.path, 'r') as file:
                data = json.load(file)
                ledStripRoom1.from_dict(data[0])
                kitchenLight.from_dict(data[1])
                ledLego.from_dict(data[2])
                ledPhotosHeart.from_dict(data[4])
            return True
        except Exception as e:
            print(f"bleble Error: {e}")
            return False

    # def save(self):
    #     setings = ET.Element("settings")

    #     ET.SubElement(setings, "ledStripRoom1autoLuxMin").text = str(ledStripRoom1.autoLuxMin)
    #     ET.SubElement(setings, "ledStripRoom1AutoOff").text = str(ledStripRoom1.autoOff)
    #     ET.SubElement(setings, "ledStripRoom1AutoOn").text = str(ledStripRoom1.autoOn)
    #     ET.SubElement(setings, "ledStripRoom1Jasnosc").text = str(ledStripRoom1.brightness)
    #     ET.SubElement(setings, "ledStripRoom1Ustawienie").text = str(ledStripRoom1.setting)

    #     ET.SubElement(setings, "kitchenLightautoLux_min").text = str(kitchenLight.autoLuxMin)
    #     ET.SubElement(setings, "kitchenLightAutoOFF").text = str(kitchenLight.autoOff)
    #     ET.SubElement(setings, "kitchenLightAutoON").text = str(kitchenLight.autoOn)

    #     ET.SubElement(setings, "spootLightRoom1Jasnosc").text = str(spootLightRoom1.brightness)

    #     ET.SubElement(setings, "ledPhotosHeartAutoBrightness").text = str(ledPhotosHeart.autoBrightness)
    #     ET.SubElement(setings, "ledPhotosHeartAutoLux_min").text = str(ledPhotosHeart.autoLuxMin)
    #     ET.SubElement(setings, "ledPhotosHeartAutoOFF").text = str(ledPhotosHeart.autoOff)
    #     ET.SubElement(setings, "ledPhotosHeartAutoON").text = str(ledPhotosHeart.autoOn)

    #     fileRaw = ET.ElementTree(setings)
    #     fileRaw.write(self.path)
    #     log.add_log("Settings saved")

    # def read(self):
    #     fileRaw = ET.ElementTree(file=self.path)
    #     root = fileRaw.getroot()

    #     ledStripRoom1.autoLuxMin = int(root.find('ledStripRoom1autoLuxMin').text)
    #     ledStripRoom1.AutoOff = root.find('ledStripRoom1AutoOff').text
    #     ledStripRoom1.AutoOn = root.find('ledStripRoom1AutoOn').text
    #     ledStripRoom1.brightness = int(root.find('ledStripRoom1Jasnosc').text)
    #     ledStripRoom1.setting = root.find('ledStripRoom1Ustawienie').text

    #     kitchenLight.autoLuxMin = int(root.find('kitchenLightautoLux_min').text)
    #     kitchenLight.autoOff = root.find('kitchenLightAutoOFF').text
    #     kitchenLight.autoOn = root.find('kitchenLightAutoON').text

    #     spootLightRoom1.brightness = int(root.find('spootLightRoom1Jasnosc').text)

    #     ledPhotosHeart.autoBrightness = int(root.find('ledPhotosHeartAutoBrightness').text)
    #     ledPhotosHeart.autoLuxMin = int(root.find('ledPhotosHeartAutoLux_min').text)
    #     ledPhotosHeart.autoOff = root.find('ledPhotosHeartAutoOFF').text
    #     ledPhotosHeart.autoOn = root.find('ledPhotosHeartAutoON').text


# settings = Settings('/var/www/html/settings.xml')
settings = Settings("/var/www/html/settings.json")