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
import time, os

watchdogFlag=0


def watchdog_read():
    global watchdogFlag
    tree = ET.ElementTree(file='Desktop/Home/watchdog.xml')
    root = tree.getroot()
    watchdogFlag = int(root.find("watchdogFlag").text)

def watchdog_set():
    global watchdogFlag
    setings = ET.Element("settings")
    ET.SubElement(setings, "watchdogFlag").text = str(0)
    tree2 = ET.ElementTree(setings)
    tree2.write('Desktop/Home/watchdog.xml')

def main():
    global watchdogFlag
    log.add_watchdog_log("Uruchamiam watchdog...")
    time.sleep(1200)
    log.add_watchdog_log("watchdog uruchomiony")
    while(1):
        watchdog_set()
        time.sleep(120)
        watchdog_read()
        log.add_watchdog_log('Flaga watchdog = {}'.format(watchdogFlag))
        sys.stdout.flush()
        if(watchdogFlag == 0):
            log.add_watchdog_log('RESET!')
            os.system('sudo shutdown -r now')
    pass

if __name__ == '__main__':
    main()
