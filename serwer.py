 # -*- coding: utf-8 -*-
try:
    import time, datetime, threading, sys ,os, re, glob
except ImportError:
    print "Blad importu"

from libraries.log import *
from libraries.gui import *
from devicesList import *
from libraries.infoStrip import *
from libraries.sqlDatabase import *
from libraries.nrfConnect import *
from libraries.udpServer import *
from libraries.settings import *
from libraries.displayBrightness import *
from sensors import *

from time import sleep
import RPi.GPIO as GPIO


time.sleep(5) #+++++ZWLOKA CZASOWA +++++++++++++++++++

swiatlo=0
flaga_odczyt_ustawien=False
kasowanieSQL_flaga=False




def sprawdzTimer():  #SPRAWDZENIE CO WYKONAC O DANEJ PORZE
    #----------------------SPRAWDZENIE BAZY DANYCH SQL-----------------------kasowanie starych rekordow------------
    if (str(time.strftime("%d"))=="01") and (str(time.strftime("%H:%M"))=="01:00") and kasowanieSQL_flaga==False:
        sql.delete_records(30) #kasowanie starych rekordow z bazy danych
        kasowanieSQL_flaga=True
        log.add_log("Skasowano stare dane z SQL")
    if (str(time.strftime("%d"))=="01") and (str(time.strftime("%H:%M"))=="01:01") and kasowanieSQL_flaga==True:
        kasowanieSQL_flaga=False
    #------------------------------------------------------------------------------------------
    autoCzas(lampaTV)
    autoCzas(dekoPok1)
    autoCzas(deko2Pok1)
    autoCzas(dekoFlaming)
    autoCzas(lampaPok2Tradfri)
    autoCzas(lampaPok2)#---- LED SYPIALNI
    #autoCzas(lampaKuch)#-----LED KUCHNI
    #autoCzas(dekoUsb)#----USB Stick
    autoCzas(hydroponika)#----Hydroponika


def autoCzas(klasa):
    format = '%H:%M:%S.%f'
    aktual=datetime.datetime.now().time()
    try:
        zmiennaON = datetime.datetime.strptime(str(aktual), format) - datetime.datetime.strptime(klasa.AutoON, format) # obliczenie roznicy czasu
    except ValueError as e:
        print('Blad czasu wł:', e)
    try:
        zmiennaOFF = datetime.datetime.strptime(str(aktual), format) - datetime.datetime.strptime(klasa.AutoOFF, format) # obliczenie roznicy czasu
    except ValueError as e:
        print('Blad czasu wył:', e)
    #-----skasowanie flag ----------
    if(int(zmiennaON.total_seconds())>(-15) and int(zmiennaON.total_seconds())<0 and  klasa.FlagaSterowanieManualne==True):
        klasa.FlagaSterowanieManualne=False
    if(int(zmiennaOFF.total_seconds())>(-15) and int(zmiennaOFF.total_seconds())<0 and klasa.FlagaSterowanieManualne==True):
        klasa.FlagaSterowanieManualne=False
    #------SPRAWDZENIE------------------------
    if(klasa.Flaga==0 and automatykaOswietlenia.swiatloObliczone<klasa.AutoLux_min and (int(zmiennaON.total_seconds())>0) and (int(zmiennaOFF.total_seconds())<(-60)) and klasa.FlagaSterowanieManualne==False and klasa.blad<20):
        log.add_log("AUTO {} -> ON".format(klasa.Opis))
        sterowanieOswietleniem(klasa.Adres,klasa.AutoJasnosc)
        time.sleep(20)
    if(klasa.Flaga==1 and (int(zmiennaOFF.total_seconds())>0) and (int(zmiennaOFF.total_seconds())<60) and klasa.FlagaSterowanieManualne==False and klasa.blad<20):
        log.add_log("AUTO {} -> OFF".format(klasa.Opis))
        sterowanieOswietleniem(klasa.Adres,0)
        time.sleep(20)

def watchdog_reset():
    setings = ET.Element("settings")
    ET.SubElement(setings, "watchdogFlag").text = str(1)
    tree2 = ET.ElementTree(setings)
    tree2.write('Desktop/Home/watchdog.xml')



#=====================================================
#Adresy  ==>>
AdresLedTV = 1
AdresSypialnia = 2
AdresLampa1 = 3
AdresKuchnia = 4
AdresLampa2 = 5 #Dekoracje 1 REKA
AdresLampa3 = 6 #Dekoracje 2 Eifla
AdresFlaming = 7 #Dekoracje Flaming
AdresUsb = 8 #Modul uniwersalny USB
AdresCzujnikKwiatka1 = 9
AdresCzujnikKwiatka2 = 10
AdresCzujnikKwiatka3 = 11
AdresBuda = 12
AdresCzujnikKwiatka4 = 13
AdresHydroponika = 15
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def ODCZYT_USTAWIEN_WATEK():  #------WATEK ODCZYTUJACY USTAWIENIA Z XML
    q=0
    while(1):
        if q>5:
            q=0
        if q==0:
            weather.get_forecast('Rodgau')
        settings.read()
        watchdog_reset()
        time.sleep(60)
        q=q+1

def SPRAWDZENIE_TIMERA_WATEK():  #------WATEK SPRAWDZAJACY TIMER
    while(1):
        sprawdzTimer()
        time.sleep(10)

#++++++++++++++++++++++++++++++ funkcje dla watkow +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def LCD_thread_init():
    lcdTh = threading.Thread(target=gui.lcd)
    lcdTh.start()

def NRF_thread_init():
    nrfTh = threading.Thread(target=nrf.server)
    nrfTh.start()

def display_brightness_thread_init():
    nrfTh = threading.Thread(target=displayBrightness.set_brightness)
    nrfTh.start()

def check_sensors_thread_init():
    nrfTh = threading.Thread(target=sensor.checkSensors)
    nrfTh.start()
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#-----START-------------------------------------------------------------------------------------------------------------------------------------------
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
log.add_log("Uruchamiam serwer MyHome...")
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(22,GPIO.OUT)
#-------------WATKI--------------------------
LCD_thread_init()
NRF_thread_init()
display_brightness_thread_init()

o=threading.Thread(target=ODCZYT_USTAWIEN_WATEK)
o.start()
ti=threading.Thread(target=SPRAWDZENIE_TIMERA_WATEK)
ti.start()

check_sensors_thread_init()
#--------------MAIN FUNKTION------------------------------
ready = udp.readStatus() #inicjalizacja zmiennej
while(1):
    if ready[0]:
        udp.server()
    ready = udp.readStatus()
