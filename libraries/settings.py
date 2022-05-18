#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        nrf_connect
# Purpose:
#
# Author:      KoSik
#
# Created:     17.05.2022
# Copyright:   (c) kosik 2022
#-------------------------------------------------------------------------------
import xml.etree.cElementTree as ET
from libraries.log import *
from devicesList import *


class SETTINGS_CL:
    path = '/var/www/html/ustawienia.xml'

    
    def zapis_ustawien_xml(self):
        setings = ET.Element("settings")

        ET.SubElement(setings, "lampaTVAutoLux_min").text = str(lampaTV.AutoLux_min)
        ET.SubElement(setings, "lampaTVAutoOff").text = str(lampaTV.AutoOFF)
        ET.SubElement(setings, "lampaTVAutoOn").text = str(lampaTV.AutoON)
        ET.SubElement(setings, "lampaTVJasnosc").text = str(lampaTV.Jasnosc)
        ET.SubElement(setings, "lampaTVUstawienie").text = str(lampaTV.Ustawienie)

        ET.SubElement(setings, "lampaKuchAutoLux_min").text = str(lampaKuch.AutoLux_min)
        ET.SubElement(setings, "lampaKuchAutoOFF").text = str(lampaKuch.AutoOFF)
        ET.SubElement(setings, "lampaKuchAutoON").text = str(lampaKuch.AutoON)

        ET.SubElement(setings, "lampa1Pok1Jasnosc").text = str(lampa1Pok1.Jasnosc)

        ET.SubElement(setings, "lampaPok2AutoJasnosc").text = str(lampaPok2.AutoJasnosc)
        ET.SubElement(setings, "lampaPok2AutoLux_min").text = str(lampaPok2.AutoLux_min)
        ET.SubElement(setings, "lampaPok2AutoOFF").text = str(lampaPok2.AutoOFF)
        ET.SubElement(setings, "lampaPok2AutoON").text = str(lampaPok2.AutoON)

        tree2 = ET.ElementTree(setings)
        tree2.write(self.path)
        log.add_log("Zapisano ustawienia")

    def read(self):
        tree = ET.ElementTree(file=self.path)
        root = tree.getroot()

        lampaTV.AutoLux_min = int(root.find('lampaTVAutoLux_min').text)
        lampaTV.AutoOff = root.find('lampaTVAutoOff').text
        lampaTV.AutoOn = root.find('lampaTVAutoOn').text
        lampaTV.Jasnosc = int(root.find('lampaTVJasnosc').text)
        lampaTV.Ustawienie = root.find('lampaTVUstawienie').text

        lampaKuch.AutoLux_min = int(root.find('lampaKuchAutoLux_min').text)
        lampaKuch.AutoOFF = root.find('lampaKuchAutoOFF').text
        lampaKuch.AutoON = root.find('lampaKuchAutoON').text

        lampa1Pok1.Jasnosc = int(root.find('lampa1Pok1Jasnosc').text)

        lampaPok2.AutoJasnosc = int(root.find('lampaPok2AutoJasnosc').text)
        lampaPok2.AutoLux_min = int(root.find('lampaPok2AutoLux_min').text)
        lampaPok2.AutoOFF = root.find('lampaPok2AutoOFF').text
        lampaPok2.AutoON = root.find('lampaPok2AutoON').text
settings = SETTINGS_CL()