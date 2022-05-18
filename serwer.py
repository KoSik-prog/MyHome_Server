 # -*- coding: utf-8 -*-
try:
    import time, traceback, datetime, random, threading, sys ,os, linecache, re, glob
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

from time import sleep
import RPi.GPIO as GPIO

from numpy.random import randint


kasowanieSQL_flaga=False

#+++++ZWLOKA CZASOWA +++++++++++++++++++
time.sleep(5)

swiatlo=0
flaga_odczyt_ustawien=False


def sprawdzCzujniki():
    minimalneNapiecieBaterii=2.55
    minimalnaWilgotnosc = 10
    if((datetime.datetime.now() - czujnikZew.czas)>(datetime.timedelta(minutes=18))):
        infoStrip.set_error(0,True)
    if((datetime.datetime.now() - czujnikPok1.czas)>(datetime.timedelta(minutes=23))):
        infoStrip.set_error(1,True)
    if((datetime.datetime.now() - czujnikPok2.czas)>(datetime.timedelta(minutes=23))):
        infoStrip.set_error(2,True)
    if((datetime.datetime.now() - czujnikKwiatek.czas)>(datetime.timedelta(minutes=63))):
        infoStrip.set_error(3,True)
    if((datetime.datetime.now() - czujnikKwiatek2.czas)>(datetime.timedelta(minutes=63))):
        infoStrip.set_error(4,True)
    if((datetime.datetime.now() - czujnikKwiatek3.czas)>(datetime.timedelta(minutes=63))):
        infoStrip.set_error(5,True)
    if((datetime.datetime.now() - czujnikKwiatek4.czas)>(datetime.timedelta(minutes=63))):
        infoStrip.set_error(6,True)
    if((datetime.datetime.now() - czujnikKwiatek5.czas)>(datetime.timedelta(minutes=63))):
        infoStrip.set_error(16,True)
    if((datetime.datetime.now() - czujnikKwiatek6.czas)>(datetime.timedelta(minutes=63))):
        infoStrip.set_error(19,True)
    #sprawdzenie budy
    if((datetime.datetime.now() - buda.czas)>(datetime.timedelta(minutes=2))):
        buda.temp1=0.0
        buda.temp2=0.0
        buda.temp3=0.0
        buda.czujnikZajetosciFlaga=0
        buda.czujnikZajetosciRaw=0
    #sprawdzenie stanu baterii
    if(czujnikKwiatek.zasilanie <= 5):
        infoStrip.set_error(7,True)
    else:
        infoStrip.set_error(7,False)
    if(czujnikKwiatek2.zasilanie <= minimalneNapiecieBaterii):
        infoStrip.set_error(8,True)
    else:
        infoStrip.set_error(8,False)
    if(czujnikKwiatek3.zasilanie <= minimalneNapiecieBaterii):
        infoStrip.set_error(9,True)
    else:
        infoStrip.set_error(9,False)
    if(czujnikKwiatek4.zasilanie <= minimalneNapiecieBaterii):
        infoStrip.set_error(10,True)
    else:
        infoStrip.set_error(10,False)
    if(czujnikKwiatek2.wilgotnosc <= minimalnaWilgotnosc and czujnikKwiatek2.slonce < 60):
        infoStrip.set_error(11,True)
    else:
        infoStrip.set_error(11,False)
    if(czujnikKwiatek3.wilgotnosc <= minimalnaWilgotnosc and czujnikKwiatek3.slonce < 60):
        infoStrip.set_error(12,True)
    else:
        infoStrip.set_error(12,False)
    if(czujnikKwiatek4.wilgotnosc <= minimalnaWilgotnosc and czujnikKwiatek4.slonce < 60):
        infoStrip.set_error(13,True)
    else:
        infoStrip.set_error(13,False)
    if(czujnikKwiatek5.zasilanie <= minimalneNapiecieBaterii):
        infoStrip.set_error(14,True)
    else:
        infoStrip.set_error(14,False)
    if(czujnikKwiatek5.wilgotnosc <= minimalnaWilgotnosc and czujnikKwiatek5.slonce < 60):
        infoStrip.set_error(15,True)
    else:
        infoStrip.set_error(15,False)
    if(czujnikKwiatek6.zasilanie <= minimalneNapiecieBaterii):
        infoStrip.set_error(17,True)
    else:
        infoStrip.set_error(17,False)
    if(czujnikKwiatek6.wilgotnosc <= minimalnaWilgotnosc and czujnikKwiatek6.slonce < 60):
        infoStrip.set_error(18,True)
    else:
        infoStrip.set_error(18,False)




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
        sprawdzCzujniki()
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
#--------------MAIN FUNKTION------------------------------
ready = udp.readStatus() #inicjalizacja zmiennej
while(1):
    if ready[0]:
        udp.server()
    ready = udp.readStatus()
