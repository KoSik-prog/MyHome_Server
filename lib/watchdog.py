#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:        watchdog
# Author:      KoSik
#
# Created:     21.05.2020
# Copyright:   (c) kosik 2020
# -------------------------------------------------------------------------------
try:
    from lib.log import *
    import xml.etree.cElementTree as ET
    import time
    import os
    import sys
except ImportError:
    print("Import error - watchdog")


class Watchdog:
    watchdogFlag = 0
    
    def __init__(self, path):
        self.path = path

    def start(self):
        log.add_watchdog_log("Uruchamiam watchdog...")
        time.sleep(1200)
        log.add_watchdog_log("watchdog uruchomiony")
        while(1):
            self.watchdog_set()
            time.sleep(120)
            self.watchdog_read()
            log.add_watchdog_log('flaga watchdog = {}'.format(self.watchdogFlag))
            sys.stdout.flush()
            if(self.watchdogFlag == 0):
                log.add_watchdog_log('RESET!')
                os.system('sudo shutdown -r now')

    def read(self):
        tree = ET.ElementTree(file=self.path + "/watchdog.xml")
        root = tree.getroot()
        self.watchdogFlag = int(root.find("watchdogFlag").text)

    def set(self):
        setings = ET.Element("settings")
        ET.SubElement(setings, "watchdogFlag").text = str(0)
        tree2 = ET.ElementTree(setings)
        tree2.write(self.path + "/watchdog.xml")

    def reset(self):
        setings = ET.Element("settings")
        ET.SubElement(setings, "watchdogFlag").text = str(1)
        tree2 = ET.ElementTree(setings)
        tree2.write(self.path + "/watchdog.xml")


watchdog = Watchdog('Desktop/Home')
