 # -*- coding: utf-8 -*-
try:
    import time, traceback, smbus, datetime, random, threading, sys ,os, linecache, re, glob
except ImportError:
    print "Blad importu"

from libraries.log import *
from libraries.gui import *
from devicesList import *
from libraries.infoStrip import *
from libraries.weatherForecast import *
from libraries.ikea import *
from libraries.sqlDatabase import *
from libraries.nrfConnect import *
from libraries.udpServer import *

from time import sleep
import rpi_backlight as bl
import RPi.GPIO as GPIO
import xml.etree.cElementTree as ET

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



def zapis_danych_xml():
    root = ET.Element("data")

    ET.SubElement(root, "czujnikZewtemp").text = str(czujnikZew.temp)
    ET.SubElement(root, "czujnikZewhumi").text = str(czujnikZew.humi)
    ET.SubElement(root, "czujnikZewlux").text = str(czujnikZew.lux)
    ET.SubElement(root, "czujnikZewbatt").text = str(czujnikZew.batt)
    ET.SubElement(root, "czujnikPok1temp").text = str(czujnikPok1.temp)
    ET.SubElement(root, "czujnikPok1humi").text = str(czujnikPok1.humi)
    ET.SubElement(root, "czujnikPok1batt").text = str(czujnikPok1.batt)
    ET.SubElement(root, "czujnikPok2temp").text = str(czujnikPok2.temp)
    ET.SubElement(root, "czujnikPok2humi").text = str(czujnikPok2.humi)

    ET.SubElement(root, "czujnikKwiatekSlonce").text = str(czujnikKwiatek.slonce)
    ET.SubElement(root, "czujnikKwiatekWilgotnosc").text = str(czujnikKwiatek.wilgotnosc)
    ET.SubElement(root, "czujnikKwiatekWoda").text = str(czujnikKwiatek.woda)
    ET.SubElement(root, "czujnikKwiatekZasilanie").text = str(czujnikKwiatek.zasilanie)

    ET.SubElement(root, "lampaTVFlaga").text = str(lampaTV.Flaga)
    ET.SubElement(root, "lampaTVUstawienie").text = str(lampaTV.Ustawienie)
    ET.SubElement(root, "lampaTVJasnosc").text = str(lampaTV.Jasnosc)

    ET.SubElement(root, "dekoracje1Flaga").text = str(dekoPok1.Flaga)
    ET.SubElement(root, "dekoracje2Flaga").text = str(deko2Pok1.Flaga)

    ET.SubElement(root, "dekoracjeUSB").text = str(dekoUsb.Flaga)

    ET.SubElement(root, "dekoracjeFlaming").text = str(dekoFlaming.Flaga)

    ET.SubElement(root, "lampaPrzedpokoj").text = str(lampaPrzedpokojTradfri.Status)

    ET.SubElement(root, "lampaKuchFlaga").text = str(lampaKuch.Flaga)

    ET.SubElement(root, "lampaPok2Flaga").text = str(lampaPok2.Flaga)
    ET.SubElement(root, "lampaPok2Jasnosc").text = str(lampaPok2.Jasnosc)

    ET.SubElement(root, "budaTemp1").text = str(buda.temp1)
    ET.SubElement(root, "budaTemp2").text = str(buda.temp2)
    ET.SubElement(root, "budaTemp3").text = str(buda.temp3)
    ET.SubElement(root, "budaCzujnikFlaga").text = str(buda.czujnikZajetosciFlaga)
    ET.SubElement(root, "budaCzujnikRaw").text = str(buda.czujnikZajetosciRaw)

    tree = ET.ElementTree(root)
    tree.write('/var/www/html/homevariables.xml')
    #log.add_log("Zapisano dane")

def zapis_ustawien_xml():
    setings = ET.Element("settings")

    ET.SubElement(setings, "lampaTVAutoLux_min").text = str(lampaTV.AutoLux_min)
    ET.SubElement(setings, "lampaTVAutoOff").text = str(lampaTV.AutoOFF)
    ET.SubElement(setings, "lampaTVAutoOn").text = str(lampaTV.AutoON)
    ET.SubElement(setings, "lampaTVJasnosc").text = str(lampaTV.Jasnosc)
    ET.SubElement(setings, "lampaTVUstawienie").text = str(lampaTV.Ustawienie)

    ET.SubElement(setings, "lampaKuchAutoLux_min").text = str(lampaKuch.AutoLux_min)
    ET.SubElement(setings, "lampaKuchAutoOFF").text = str(lampaKuch.AutoOFF)
    ET.SubElement(setings, "lampaKuchAutoON").text = str(lampaKuch.AutoON)

    ET.SubElement(setings, "lampa1Pok1Jasnosc").text = str(lampa1Pok1.Jasnosc)

    ET.SubElement(setings, "lampaPok2AutoJasnosc").text = str(lampaPok2.AutoJasnosc)
    ET.SubElement(setings, "lampaPok2AutoLux_min").text = str(lampaPok2.AutoLux_min)
    ET.SubElement(setings, "lampaPok2AutoOFF").text = str(lampaPok2.AutoOFF)
    ET.SubElement(setings, "lampaPok2AutoON").text = str(lampaPok2.AutoON)

    tree2 = ET.ElementTree(setings)
    tree2.write('/var/www/html/ustawienia.xml')
    log.add_log("Zapisano ustawienia")

def odczyt_ustawien_xml():
    tree = ET.ElementTree(file='/var/www/html/ustawienia.xml')
    root = tree.getroot()

    lampaTV.AutoLux_min = int(root.find('lampaTVAutoLux_min').text)
    lampaTV.AutoOff = root.find('lampaTVAutoOff').text
    lampaTV.AutoOn = root.find('lampaTVAutoOn').text
    lampaTV.Jasnosc = int(root.find('lampaTVJasnosc').text)
    lampaTV.Ustawienie = root.find('lampaTVUstawienie').text

    lampaKuch.AutoLux_min = int(root.find('lampaKuchAutoLux_min').text)
    lampaKuch.AutoOFF = root.find('lampaKuchAutoOFF').text
    lampaKuch.AutoON = root.find('lampaKuchAutoON').text

    lampa1Pok1.Jasnosc = int(root.find('lampa1Pok1Jasnosc').text)

    lampaPok2.AutoJasnosc = int(root.find('lampaPok2AutoJasnosc').text)
    lampaPok2.AutoLux_min = int(root.find('lampaPok2AutoLux_min').text)
    lampaPok2.AutoOFF = root.find('lampaPok2AutoOFF').text
    lampaPok2.AutoON = root.find('lampaPok2AutoON').text

def watchdog_reset():
    setings = ET.Element("settings")
    ET.SubElement(setings, "watchdogFlag").text = str(1)
    tree2 = ET.ElementTree(setings)
    tree2.write('Desktop/Home/watchdog.xml')

def czujnik_swiatla():
    bus = smbus.SMBus(1)
    bus.write_byte_data(0x39, 0x00 | 0x80, 0x03)
    bus.write_byte_data(0x39, 0x01 | 0x80, 0x02)
    time.sleep(0.5)
    data = bus.read_i2c_block_data(0x39, 0x0C | 0x80, 2)
    ch0 = data[1] * 256 + data[0]
    return int(ch0)

def jasnosc_wyswietlacza(): #----STEROWANIE WYSWIETLACZEM - WATEK!!!!!!!!!! ----------------------------------------------------
    global swiatlo
    swiatlo_old=0
    while(1):
        swiatlo=czujnik_swiatla() #poprawic
        gui.swiatlo = swiatlo
        if swiatlo>(swiatlo_old+15) or swiatlo<(swiatlo_old-15): 
            if swiatlo<7:
                jasnoscwysw=11
            elif swiatlo>=7 and swiatlo<100:
                jasnoscwysw=int(((0.645*swiatlo)+5.4838)+11)
            elif swiatlo>=100 and swiatlo<1000:
                jasnoscwysw=int(((0.193*swiatlo) + 50.67)+11)
            elif swiatlo>=1000:
                jasnoscwysw=255
            bl.set_brightness(jasnoscwysw, smooth=True, duration=2)  # ustawienie jasnosci LCD
            #log.add_log("Jasnosc wyswietlacza:{}   / old:{}, new:{}".format(jasnoscwysw,swiatlo_old,swiatlo))
            swiatlo_old=swiatlo
        time.sleep(5)

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
        odczyt_ustawien_xml()
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
l=threading.Thread(target=jasnosc_wyswietlacza)
l.start()
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
