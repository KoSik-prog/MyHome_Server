# -------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      kosik
#
# Created:     21.05.2020
# Copyright:   (c) kosik 2020
# Licence:     <your licence>
# -------------------------------------------------------------------------------
from lib.log import *


import xml.etree.cElementTree as ET
import time
import os
import sys


class Watchdog:
    watchdogFlag = 0
    path = 'Desktop/Home/watchdog.xml'

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
        tree = ET.ElementTree(file=self.path)
        root = tree.getroot()
        self.watchdogFlag = int(root.find("watchdogFlag").text)

    def set(self):
        setings = ET.Element("settings")
        ET.SubElement(setings, "watchdogFlag").text = str(0)
        tree2 = ET.ElementTree(setings)
        tree2.write(self.path)

    def reset(self):
        setings = ET.Element("settings")
        ET.SubElement(setings, "watchdogFlag").text = str(1)
        tree2 = ET.ElementTree(setings)
        tree2.write(self.path)


watchdog = Watchdog()
