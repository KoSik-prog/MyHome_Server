 # -*- coding: utf-8 -*-
try:
    import time, datetime, threading
except ImportError:
    print "Blad importu"

from libraries.log import *
from libraries.gui import *
from devicesList import *
from libraries.infoStrip import *
from libraries.sqlDatabase import *
from libraries.nrfConnect import *
from libraries.webServices import *
from libraries.settings import *
from libraries.displayBrightness import *
from libraries.timer import *
from sensors import *

from time import sleep
import RPi.GPIO as GPIO


time.sleep(5) #+++++ZWLOKA CZASOWA +++++++++++++++++++

def LCD_thread_init():
    lcdTh = threading.Thread(target=gui.lcd)
    lcdTh.start()

def NRF_thread_init():
    nrfTh = threading.Thread(target=nrf.server)
    nrfTh.start()

def display_brightness_thread_init():
    nrfTh = threading.Thread(target=displayBrightness.set_brightness)
    nrfTh.start()

def settings_read_thread_init():
    nrfTh = threading.Thread(target=settings.start_read)
    nrfTh.start()

def timer_thread_init():
    nrfTh = threading.Thread(target=timer.timer_start)
    nrfTh.start()

def check_sensors_thread_init():
    nrfTh = threading.Thread(target=sensor.check_sensors)
    nrfTh.start()

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#-----START-------------------------------------------------------------------------------------------------------------------------------------------
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
if __name__ == "__main__":
    log.add_log("Uruchamiam serwer MyHome...")
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(22,GPIO.OUT)
    #-------------THREADS INIT--------------------------
    LCD_thread_init()
    NRF_thread_init()
    display_brightness_thread_init()
    settings_read_thread_init()
    timer_thread_init()
    check_sensors_thread_init()
    #--------------MAIN FUNCTION------------------------------
    ready = udp.readStatus() #inicjalizacja zmiennej
    while(1):
        if ready[0]:
            udp.server()
        ready = udp.readStatus()
