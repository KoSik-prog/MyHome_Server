#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      kosik
#
# Created:     21.05.2020
# Copyright:   (c) kosik 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from libraries.log import *


import xml.etree.cElementTree as ET
import time, os, sys

class WATCHDOG_CL:
    watchdogFlag=0
    path = 'Desktop/Home/watchdog.xml'

    def start(self):
        log.add_watchdog_log("Uruchamiam watchdog...")
        time.sleep(1200)
        log.add_watchdog_log("watchdog uruchomiony")
        while(1):
            self.watchdog_set()
            time.sleep(120)
            self.watchdog_read()
            log.add_watchdog_log('flaga watchdog = {}'.format(WATCHDOG_CL.watchdogFlag))
            sys.stdout.flush()
            if(WATCHDOG_CL.watchdogFlag == 0):
                log.add_watchdog_log('RESET!')
                os.system('sudo shutdown -r now')
        pass

    def read(self):
        tree = ET.ElementTree(file = WATCHDOG_CL.path)
        root = tree.getroot()
        WATCHDOG_CL.watchdogFlag = int(root.find("watchdogFlag").text)

    def set(self):
        setings = ET.Element("settings")
        ET.SubElement(setings, "watchdogFlag").text = str(0)
        tree2 = ET.ElementTree(setings)
        tree2.write(WATCHDOG_CL.path)

    def reset(self):
        setings = ET.Element("settings")
        ET.SubElement(setings, "watchdogFlag").text = str(1)
        tree2 = ET.ElementTree(setings)
        tree2.write(WATCHDOG_CL.path)
watchdog = WATCHDOG_CL()
