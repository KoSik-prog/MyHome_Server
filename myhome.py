#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        myHome main program
#
# Author:      KoSik
#
# Created:     18.09.2021
# Copyright:   (c) kosik 2021
#-------------------------------------------------------------------------------

try:
    import time, datetime, threading
except ImportError:
    print "Blad importu"

from lib.log import *
from lib.gui import *
from devicesList import *
from lib.infoStrip import *
from lib.sqlDatabase import *
from lib.nrfConnect import *
from lib.webServices import *
from lib.settings import *
from lib.displayBrightness import *
from lib.timer import *
from sensors import *

from time import sleep
import RPi.GPIO as GPIO

class MyHome:
    def __init__(self):
        log.add_log("Uruchamiam serwer MyHome...")
        time.sleep(5) #+++++ time delay - for safety +++++++++++++++++++
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(22,GPIO.OUT)
        #-------------THREADS INIT--------------------------
        self.lcd_thread_init()
        self.nrf_thread_init()
        self.display_brightness_thread_init()
        self.settings_read_thread_init()
        self.timer_thread_init()
        self.check_sensors_thread_init()
        self.check_weatherForecast_thread_init()
        #--------------MAIN FUNCTION------------------------
        self.start_server()

    def start_server(self):
        ready = udp.readStatus()
        while(1):
            if ready[0]:
                udp.server()
            ready = udp.readStatus()

    def lcd_thread_init(self):
        lcdTh = threading.Thread(target=gui.lcd)
        lcdTh.start()

    def nrf_thread_init(self):
        nrfTh = threading.Thread(target=nrf.nrf24l01_thread)
        nrfTh.start()

    def display_brightness_thread_init(self):
        nrfTh = threading.Thread(target=displayBrightness.set_brightness_thread)
        nrfTh.start()

    def settings_read_thread_init(self):
        nrfTh = threading.Thread(target=settings.start_read)
        nrfTh.start()

    def timer_thread_init(self):
        nrfTh = threading.Thread(target=timer.timer_start)
        nrfTh.start()

    def check_sensors_thread_init(self):
        nrfTh = threading.Thread(target=sensor.check_sensors)
        nrfTh.start()

    def check_weatherForecast_thread_init(self):
        nrfTh = threading.Thread(target=weather.weather_thread)
        nrfTh.start()


#-----START-------------------------------------
if __name__ == "__main__":
    myHome = MyHome()
