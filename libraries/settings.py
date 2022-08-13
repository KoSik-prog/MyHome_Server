#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        settings
# Purpose:
#
# Author:      KoSik
#
# Created:     17.05.2022
# Copyright:   (c) kosik 2022
#-------------------------------------------------------------------------------
import xml.etree.cElementTree as ET
from libraries.log import *
from libraries.weatherForecast import *
from devicesList import *
from libraries.watchdog import *


class SETTINGS_CL:
    path = '/var/www/html/ustawienia.xml'
    i=0

    def start_read(self):
        while(1):
            if SETTINGS_CL.i>5:
                SETTINGS_CL.i=0
            if SETTINGS_CL.i==0:
                weather.get_forecast('Rodgau')
            self.read()
            watchdog.reset()
            time.sleep(60)
            SETTINGS_CL.i += 1
    
    def save(self):
        setings = ET.Element("settings")

        ET.SubElement(setings, "ledStripRoom1autoLux_min").text = str(ledStripRoom1.autoLux_min)
        ET.SubElement(setings, "ledStripRoom1AutoOff").text = str(ledStripRoom1.AutoOFF)
        ET.SubElement(setings, "ledStripRoom1AutoOn").text = str(ledStripRoom1.AutoON)
        ET.SubElement(setings, "ledStripRoom1Jasnosc").text = str(ledStripRoom1.Jasnosc)
        ET.SubElement(setings, "ledStripRoom1Ustawienie").text = str(ledStripRoom1.setting)

        ET.SubElement(setings, "kitchenLightautoLux_min").text = str(kitchenLight.autoLux_min)
        ET.SubElement(setings, "kitchenLightAutoOFF").text = str(kitchenLight.AutoOFF)
        ET.SubElement(setings, "kitchenLightAutoON").text = str(kitchenLight.AutoON)

        ET.SubElement(setings, "spootLightRoom1Jasnosc").text = str(spootLightRoom1.Jasnosc)

        ET.SubElement(setings, "ledLightRoom2autoBrightness").text = str(ledLightRoom2.autoBrightness)
        ET.SubElement(setings, "ledLightRoom2autoLux_min").text = str(ledLightRoom2.autoLux_min)
        ET.SubElement(setings, "ledLightRoom2AutoOFF").text = str(ledLightRoom2.AutoOFF)
        ET.SubElement(setings, "ledLightRoom2AutoON").text = str(ledLightRoom2.AutoON)

        tree2 = ET.ElementTree(setings)
        tree2.write(SETTINGS_CL.path)
        log.add_log("Zapisano ustawienia")

    def read(self):
        tree = ET.ElementTree(file=SETTINGS_CL.path)
        root = tree.getroot()

        ledStripRoom1.autoLux_min = int(root.find('ledStripRoom1autoLux_min').text)
        ledStripRoom1.AutoOff = root.find('ledStripRoom1AutoOff').text
        ledStripRoom1.AutoOn = root.find('ledStripRoom1AutoOn').text
        ledStripRoom1.Jasnosc = int(root.find('ledStripRoom1Jasnosc').text)
        ledStripRoom1.setting = root.find('ledStripRoom1Ustawienie').text

        kitchenLight.autoLux_min = int(root.find('kitchenLightautoLux_min').text)
        kitchenLight.AutoOFF = root.find('kitchenLightAutoOFF').text
        kitchenLight.AutoON = root.find('kitchenLightAutoON').text

        spootLightRoom1.Jasnosc = int(root.find('spootLightRoom1Jasnosc').text)

        ledLightRoom2.autoBrightness = int(root.find('ledLightRoom2autoBrightness').text)
        ledLightRoom2.autoLux_min = int(root.find('ledLightRoom2autoLux_min').text)
        ledLightRoom2.AutoOFF = root.find('ledLightRoom2AutoOFF').text
        ledLightRoom2.AutoON = root.find('ledLightRoom2AutoON').text
settings = SETTINGS_CL()