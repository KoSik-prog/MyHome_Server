 # -*- coding: utf-8 -*-
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


time.sleep(5) #+++++ time delay - for safety +++++++++++++++++++

class Server:
    def __init__(self):
        log.add_log("Uruchamiam serwer MyHome...")
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(22,GPIO.OUT)
        #-------------THREADS INIT--------------------------
        self.LCD_thread_init()
        self.NRF_thread_init()
        self.display_brightness_thread_init()
        self.settings_read_thread_init()
        self.timer_thread_init()
        self.check_sensors_thread_init()
        #--------------MAIN FUNCTION------------------------------
        self.start_server()

    def start_server(self):
        ready = udp.readStatus()
        while(1):
            if ready[0]:
                udp.server()
            ready = udp.readStatus()

    def LCD_thread_init(self):
        lcdTh = threading.Thread(target=gui.lcd)
        lcdTh.start()

    def NRF_thread_init(self):
        nrfTh = threading.Thread(target=nrf.server)
        nrfTh.start()

    def display_brightness_thread_init(self):
        nrfTh = threading.Thread(target=displayBrightness.set_brightness)
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

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#-----START-------------------------------------------------------------------------------------------------------------------------------------------
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
if __name__ == "__main__":
    server = Server()
