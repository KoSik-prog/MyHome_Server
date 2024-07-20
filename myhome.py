#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:        myHome main program
#
# Author:      KoSik
#
# Created:     18.09.2021
# Copyright:   (c) kosik 2021
# -------------------------------------------------------------------------------

# try:
import time
import threading
from time import sleep
import RPi.GPIO as GPIO
from lib.log import *
from lib.gui import *
from devicesList import *
from lib.infoStrip import *
from lib.sqlDatabase import *
from lib.nrfConnect import *
from lib.socketServices import *
from lib.settings import *
from lib.displayBrightness import *
from lib.timer import *
from lib.tasmota import *
from sensors import *
# except ImportError:
#     print("Import error - My Home")


class MyHome:
    def __init__(self):
        log.add_log("Uruchamiam serwer MyHome...")
        time.sleep(2)  # +++++ time delay - for safety +++++++++++++++++++
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(22, GPIO.OUT)
        # -------------THREADS INIT--------------------------
        self.lcd_thread_init()
        self.nrf_thread_init()
        self.display_brightness_thread_init()
        self.settings_read_thread_init()
        self.timer_thread_init()
        self.check_sensors_thread_init()
        self.check_weatherForecast_thread_init()
        self.socket_thread_init()
        self.tasmota_thread_init()

    # def __del__(self):
    #     self.socketTh.close()

    def lcd_thread_init(self):
        lcdTh = threading.Thread(target=gui.gui_thread)
        lcdTh.start()

    def nrf_thread_init(self):
        self.nrfTh = threading.Thread(target=nrf.nrf24l01_thread)
        self.nrfTh.start()
        
    def socket_thread_init(self):
        self.socketTh = threading.Thread(target=socket_server.server_thread)
        self.socketTh.start()
        
    def tasmota_thread_init(self):
        self.tasmotaTh = threading.Thread(target=tasmota.tasmota_thread)
        self.tasmotaTh.start()

    def display_brightness_thread_init(self):
        self.lcdBrightnessTh = threading.Thread(target=displayBrightness.set_brightness_thread)
        self.lcdBrightnessTh.start()

    def settings_read_thread_init(self):
        self.settingsTh = threading.Thread(target=settings.start_read)
        self.settingsTh.start()

    def timer_thread_init(self):
        self.timerTh = threading.Thread(target=timer.timer_thread)
        self.timerTh.start()

    def check_sensors_thread_init(self):
        self.sensorsTh = threading.Thread(target=sensor.check_sensors_thread)
        self.sensorsTh.start()

    def check_weatherForecast_thread_init(self):
        self.weatherTh = threading.Thread(target=weather.weather_thread)
        self.weatherTh.start()
    
    def watchdog_thread_init(self):
        self.wtdTh = threading.Thread(target=self.watchdog_thread)
        self.wtdTh.start()

    def watchdog_thread(self):
        while True:
            time.sleep(5)
            if not self.nrfTh.is_alive():
                print("nrfTh is not active. Restarting...")
                self.nrf_thread_init()


# -----START-------------------------------------
if __name__ == "__main__":
    myHome = MyHome()
