 # -*- coding: utf-8 -*-
from time import sleep

print("Uruchamiam serwer MyHome...")

try:
    import select, time, socket, traceback, sqlite3, spidev, smbus, datetime, random, ikea, wysw, threading, sys ,os, linecache, pogoda, re, sql_baza, dziennik
except ImportError:
    print "Blad importu"

import rpi_backlight as bl
import RPi.GPIO as GPIO
from lib_nrf24 import NRF24
import xml.etree.cElementTree as ET

import pygame, pygame.mixer, pygame.gfxdraw, glob
from pygame.locals import *
from pygame.compat import unichr_, unicode_
from pygame.locals import *
from pygame.compat import geterror
from numpy.random import randint


# my libraries
from libraries/webServices import *

AddrOut = 2222
kasowanieSQL_flaga=False

#+++++ZWLOKA CZASOWA +++++++++++++++++++
time.sleep(15)

class czujnikZewCl:   #CZUJNIK TEMPERATURY ZEWNETRZNEJ
    temp=1.1
    humi=1.1
    batt=1.1
    lux=0
    ir=0
    predkoscWiatru=0
    kierunekWiatru=0
    czas=datetime.datetime.now()
    blad=False
    noc_flaga=False
    noc_ustawienie=60  #ustawienie kiedy noc
    flaga_peirwszaPaczka=False
czujnikZew=czujnikZewCl

class czujnikPok1Cl:  #SALON
    temp=2.2
    humi=2.2
    batt=2.2
    czas=datetime.datetime.now()
    blad=False
czujnikPok1=czujnikPok1Cl

class czujnikPok2Cl:   #SYPIALNIA
    temp=3.3
    humi=3.3
    batt=3.3
    czas=datetime.datetime.now()
    blad=False
czujnikPok2=czujnikPok2Cl

class czujnikKwiatekCl:   #KWIATEK
    woda=0
    slonce=0
    wilgotnosc=100
    zasilanie=100
    czas=datetime.datetime.now()
czujnikKwiatek=czujnikKwiatekCl

class czujnikKwiatek2Cl:   #adres 12  KWIATEK _maly czujnik PALMA
    slonce=0
    wilgotnosc=100
    wilgotnosc_raw=0
    zasilanie=5.0
    wartoscMin=120.0
    wartoscMax=500.0
    czas=datetime.datetime.now()
    nazwa = "Palma"
czujnikKwiatek2=czujnikKwiatek2Cl

class czujnikKwiatek3Cl:   #adres 13  KWIATEK _maly czujnik PACHIRA
    slonce=0
    wilgotnosc=100
    wilgotnosc_raw=0
    zasilanie=5.0
    wartoscMin=380.0
    wartoscMax=500.0
    czas=datetime.datetime.now()
czujnikKwiatek3=czujnikKwiatek3Cl

class czujnikKwiatek4Cl:   #adres 14  KWIATEK _maly czujnik POKRZYWA
    slonce=0
    wilgotnosc=100
    wilgotnosc_raw=0
    zasilanie=5.0
    wartoscMin=280.0#250.0
    wartoscMax=580.0
    czas=datetime.datetime.now()
czujnikKwiatek4=czujnikKwiatek4Cl

class czujnikKwiatek5Cl:   #adres 16  KWIATEK _maly czujnik BENJAMIN
    slonce=0
    wilgotnosc=100
    wilgotnosc_raw=0
    zasilanie=5.0
    wartoscMin=400.0
    wartoscMax=550.0
    czas=datetime.datetime.now()
czujnikKwiatek5=czujnikKwiatek5Cl

class czujnikKwiatek6Cl:   #adres 17  KWIATEK _maly czujnik  SZEFLERA
    slonce=0
    wilgotnosc=100
    wilgotnosc_raw=0
    zasilanie=5.0
    wartoscMin=260.0
    wartoscMax=500.0
    czas=datetime.datetime.now()
czujnikKwiatek6=czujnikKwiatek6Cl

class terrariumCl:   #TERRARIUM
    temp1=0.0
    wilg1=0.0
    temp2=0.0
    wilg2=0.0
    UVI=0.0
terrarium=terrariumCl

class budaCl:   #BUDA
    Adres=12
    temp1=0.0
    temp2=0.0
    temp3=0.0
    czujnikZajetosciFlaga=False
    czujnikZajetosciRaw=0
    tryb=0
    czas=datetime.datetime.now()
buda=budaCl

class dekoPok1Cl:     #Dekoracje w salonie Reka
    Adres=5
    Flaga=0
    AutoON='15:50:00.0000'
    AutoOFF='23:05:00.0000'
    AutoLux_min=700 #ustawienie minimum oswietlenia przy ktorym zalaczy sie swiatlo
    FlagaSterowanieManualne=False
    AutoJasnosc=1
    blad=0
    Opis="Lampa-reka"
dekoPok1=dekoPok1Cl

class deko2Pok1Cl:     #Dekoracje 2 w salonie  Eifla i inne
    Adres=6
    Flaga=0
    AutoON='15:50:00.0000'
    AutoOFF='23:04:00.0000'
    AutoLux_min=800 #ustawienie minimum oswietlenia przy ktorym zalaczy sie swiatlo
    FlagaSterowanieManualne=False
    AutoJasnosc=1
    blad=0
    Opis="Dekoracje szafka"
deko2Pok1=deko2Pok1Cl

class dekoFlamingCl:     #Dekoracje w sypialni
    Flaga=0
    AutoON='20:00:00.0000'
    AutoOFF='23:59:00.0000'
    FlagaSterowanieManualne=False
    AutoJasnosc=1
    AutoLux_min=400 #ustawienie minimum oswietlenia przy ktrym zalaczy sie swiatlo
    blad=0
    Adres=7
    Opis='Flaming'
dekoFlaming=dekoFlamingCl

class dekoUsbCl:     #USB Stick
    AutoON='17:00:00.0000'
    AutoOFF='23:00:00.0000'
    AutoLux_min=1100
    AutoJasnosc=1
    Flaga=0
    blad=0
    FlagaSterowanieManualne=False
    Adres=8
    Opis='USB-Stick'
dekoUsb=dekoUsbCl

class hydroponikaCl:     #Hydroponika
    AutoON='08:00:00.0000'
    AutoOFF='19:00:00.0000'
    AutoLux_min=65000
    Flaga=0
    blad=0
    AutoJasnosc=1
    FlagaSterowanieManualne=False
    Adres=15
    Opis='Hyroponika'
hydroponika=hydroponikaCl

class lampaTVCl:     #LED TV
    Ustawienie="255255255"
    Bialy=000
    Jasnosc=70
    Flaga=0
    AutoON='16:00:00.0000'
    AutoOFF='23:00:00.0000'
    AutoLux_min=1000 #ustawienie minimum oswietlenia przy ktrym zalaczy sie swiatlo
    FlagaSterowanieManualne=False
    AutoJasnosc=70
    blad=0
    Adres=1
    Opis="LED TV"
lampaTV=lampaTVCl

class lampaPok2Cl:  # OSWIETLENIE SYPIALNI
    Jasnosc=0
    Flaga=0
    AutoON='21:00:00.0000'
    AutoOFF='23:50:00.0000'
    AutoLux_min=400 #ustawienie minimum oswietlenia przy ktrym zalaczy sie swiatlo
    FlagaSterowanieManualne=False
    AutoJasnosc=5
    blad=0
    Adres=2
    Opis='Sypialnia'
lampaPok2=lampaPok2Cl

class lampa1Pok1Cl:  # REFLEKTOR W SALONIE
    Ustawienie="000000000100"
    Jasnosc=0
    Flaga=0
    blad=0
    Adres=3
    Opis='Reflektor 1'
lampa1Pok1=lampa1Pok1Cl

class lampaKuchCl:  # OSWIETLENIE KUCHNI
    Flaga=0
    AutoON='15:00:00.0000'
    AutoOFF='23:58:00.0000'
    FlagaSterowanieManualne=False
    AutoJasnosc=1
    AutoLux_min=1300 #ustawienie minimum oswietlenia przy ktrym zalaczy sie swiatlo
    blad=0
    Adres=4
    Opis='Kuchnia'
lampaKuch=lampaKuchCl

class lampaDuzaTradfriCl:
    Adres="65537" #Adres="131079"  -> grupa
    Status=False
lampaDuzaTradfri=lampaDuzaTradfriCl

class lampaPok1TradfriCl:
    Zarowka="65559"
    Adres="131074"
    Status=False
lampaPok1Tradfri=lampaPok1TradfriCl

class lampaJadalniaTradfriCl:
    Adres="131075"
    Status=False
lampaJadalniaTradfri=lampaJadalniaTradfriCl

class lampaPok2TradfriCl:  #SYPIALNIA
    Adres="131082"
    Flaga=0
    AutoON='21:10:00.0000'
    AutoOFF='23:50:00.0000'
    AutoLux_min=600 #ustawienie minimum oswietlenia przy ktrym zalaczy sie swiatlo
    FlagaSterowanieManualne=False
    AutoJasnosc=5
    blad=0
    Opis="Lampy sypialnia"
lampaPok2Tradfri=lampaPok2TradfriCl

class lampaPrzedpokojTradfriCl:
    Adres="131077"
    Status=False
    Opis="Oswietlenie przedpokoj"
lampaPrzedpokojTradfri=lampaPrzedpokojTradfriCl

class automatykaOswietleniaCl:
    wartosciLux=[2000,2000,2000,2000,2000]
    swiatloObliczone=2000
    flagaSwiatloWlaczone=False
automatykaOswietlenia=automatykaOswietleniaCl()

swiatlo=0
flaga_odczyt_ustawien=False
obraz=0

def sprawdzCzujniki():
    minimalneNapiecieBaterii=2.55
    minimalnaWilgotnosc = 10
    if((datetime.datetime.now() - czujnikZew.czas)>(datetime.timedelta(minutes=18))):
        dodajUsunBlad(0,True)
    if((datetime.datetime.now() - czujnikPok1.czas)>(datetime.timedelta(minutes=23))):
        dodajUsunBlad(1,True)
    if((datetime.datetime.now() - czujnikPok2.czas)>(datetime.timedelta(minutes=23))):
        dodajUsunBlad(2,True)
    if((datetime.datetime.now() - czujnikKwiatek.czas)>(datetime.timedelta(minutes=63))):
        dodajUsunBlad(3,True)
    if((datetime.datetime.now() - czujnikKwiatek2.czas)>(datetime.timedelta(minutes=63))):
        dodajUsunBlad(4,True)
    if((datetime.datetime.now() - czujnikKwiatek3.czas)>(datetime.timedelta(minutes=63))):
        dodajUsunBlad(5,True)
    if((datetime.datetime.now() - czujnikKwiatek4.czas)>(datetime.timedelta(minutes=63))):
        dodajUsunBlad(6,True)
    if((datetime.datetime.now() - czujnikKwiatek5.czas)>(datetime.timedelta(minutes=63))):
        dodajUsunBlad(16,True)
    if((datetime.datetime.now() - czujnikKwiatek6.czas)>(datetime.timedelta(minutes=63))):
        dodajUsunBlad(19,True)
    #sprawdzenie budy
    if((datetime.datetime.now() - buda.czas)>(datetime.timedelta(minutes=2))):
        buda.temp1=0.0
        buda.temp2=0.0
        buda.temp3=0.0
        buda.czujnikZajetosciFlaga=0
        buda.czujnikZajetosciRaw=0
    #sprawdzenie stanu baterii
    if(czujnikKwiatek.zasilanie <= 5):
        dodajUsunBlad(7,True)
    else:
        dodajUsunBlad(7,False)
    if(czujnikKwiatek2.zasilanie <= minimalneNapiecieBaterii):
        dodajUsunBlad(8,True)
    else:
        dodajUsunBlad(8,False)
    if(czujnikKwiatek3.zasilanie <= minimalneNapiecieBaterii):
        dodajUsunBlad(9,True)
    else:
        dodajUsunBlad(9,False)
    if(czujnikKwiatek4.zasilanie <= minimalneNapiecieBaterii):
        dodajUsunBlad(10,True)
    else:
        dodajUsunBlad(10,False)
    if(czujnikKwiatek2.wilgotnosc <= minimalnaWilgotnosc and czujnikKwiatek2.slonce < 60):
        dodajUsunBlad(11,True)
    else:
        dodajUsunBlad(11,False)
    if(czujnikKwiatek3.wilgotnosc <= minimalnaWilgotnosc and czujnikKwiatek3.slonce < 60):
        dodajUsunBlad(12,True)
    else:
        dodajUsunBlad(12,False)
    if(czujnikKwiatek4.wilgotnosc <= minimalnaWilgotnosc and czujnikKwiatek4.slonce < 60):
        dodajUsunBlad(13,True)
    else:
        dodajUsunBlad(13,False)
    if(czujnikKwiatek5.zasilanie <= minimalneNapiecieBaterii):
        dodajUsunBlad(14,True)
    else:
        dodajUsunBlad(14,False)
    if(czujnikKwiatek5.wilgotnosc <= minimalnaWilgotnosc and czujnikKwiatek5.slonce < 60):
        dodajUsunBlad(15,True)
    else:
        dodajUsunBlad(15,False)
    if(czujnikKwiatek6.zasilanie <= minimalneNapiecieBaterii):
        dodajUsunBlad(17,True)
    else:
        dodajUsunBlad(17,False)
    if(czujnikKwiatek6.wilgotnosc <= minimalnaWilgotnosc and czujnikKwiatek6.slonce < 60):
        dodajUsunBlad(18,True)
    else:
        dodajUsunBlad(18,False)




def sprawdzTimer():  #SPRAWDZENIE CO WYKONAC O DANEJ PORZE
    #----------------------SPRAWDZENIE BAZY DANYCH SQL-----------------------kasowanie starych rekordow------------
    if (str(time.strftime("%d"))=="01") and (str(time.strftime("%H:%M"))=="01:00") and kasowanieSQL_flaga==False:
        sql_baza.kasujstaredane() #kasowanie starych rekordow z bazy danych
        kasowanieSQL_flaga=True
        dziennik.zapis_dziennika_zdarzen("Skasowano stare dane z SQL")
    if (str(time.strftime("%d"))=="01") and (str(time.strftime("%H:%M"))=="01:01") and kasowanieSQL_flaga==True:
        kasowanieSQL_flaga=False
    #------------------------------------------------------------------------------------------
    autoCzas(lampaTV)
    autoCzas(dekoPok1)
    autoCzas(deko2Pok1)
    #autoCzas(dekoFlaming)
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
        dziennik.zapis_dziennika_zdarzen("AUTO {} -> ON".format(klasa.Opis))
        sterowanieOswietleniem(klasa.Adres,klasa.AutoJasnosc)
        time.sleep(20)
    if(klasa.Flaga==1 and (int(zmiennaOFF.total_seconds())>0) and (int(zmiennaOFF.total_seconds())<60) and klasa.FlagaSterowanieManualne==False and klasa.blad<20):
        dziennik.zapis_dziennika_zdarzen("AUTO {} -> OFF".format(klasa.Opis))
        sterowanieOswietleniem(klasa.Adres,0)
        time.sleep(20)


class pasekInfoCl:
    aktualnaInformacja=""
    wyswietlanaInformacja=""
    informacje=["","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","",""]
    bledy=[[False,"blad czujnika zewnetrznego"],
    [False,"blad czujnika salonu"],
    [False,"blad czujnika sypialni"],
    [False,"blad czujnika kwiatka (Konewka)"],
    [False,"blad czujnika kwiatka 12 (" + czujnikKwiatek2.nazwa + ")"],
    [False,"blad czujnika kwiatka 13 (Pachira)"],
    [False,"blad czujnika kwiatka 14 (Pokrzywa)"],
    [False,"minimalny poziom baterii kwiatka (konewka)"],
    [False,"minimalny poziom baterii kwiatka 12 (Palma)"],
    [False,"minimalny poziom baterii kwiatka 13 (Pachira)"],
    [False,"minimalny poziom baterii kwiatka 14 (Pokrzywa)"],
    [False,"wilgotnosc kwiatka 12 (Palma) ponizej 5%"],
    [False,"wilgotnosc kwiatka 13 (Pachira) ponizej 5%"],
    [False,"wilgotnosc kwiatka 14 (Pokrzywa) ponizej 5%"],
    [False,"minimalny poziom baterii kwiatka 16 (Benjamin)"],
    [False,"wilgotnosc kwiatka 16 (Benjamin) ponizej 5%"],
    [False,"blad czujnika kwiatka 16 (Benjamin)"],
    [False,"minimalny poziom baterii kwiatka 17 (Szeflera)"],
    [False,"wilgotnosc kwiatka 17 ponizej 5% (Szeflera)"],
    [False,"blad czujnika kwiatka 17 (Szeflera)"],
    [False,"mała ilosc wody dla kwiatka - konewka"]]
    pozycjaOdczytuBledu=0
    czas=0
    pozycja=0
pasekInfo=pasekInfoCl()

def dodajUsunBlad(numerBledu,aktywny):
    pasekInfo.bledy[numerBledu][0]=aktywny

def odczytajBlad():
    blad=""
    for x in range(len(pasekInfo.bledy)):
        pasekInfo.pozycjaOdczytuBledu+=1
        if pasekInfo.pozycjaOdczytuBledu > len(pasekInfo.bledy)-1:
            pasekInfo.pozycjaOdczytuBledu=0
        if(pasekInfo.bledy[pasekInfo.pozycjaOdczytuBledu][0] == True):
            blad=pasekInfo.bledy[pasekInfo.pozycjaOdczytuBledu][1]
            break
    return blad

def dodajInfo(informacja):
    for i in range(len(pasekInfo.informacje)):
        if pasekInfo.informacje[i]=="":
            pasekInfo.informacje[i]=informacja
            break

def odczytajInfo():
    informacja=""
    informacja=pasekInfo.informacje[0]
    for i in range(len(pasekInfo.informacje)-1):
        pasekInfo.informacje[i]=pasekInfo.informacje[i+1]
    return informacja
#-------------------NRF24L01------------------------------------------------------------
NRFtx_tablicaAdresow=[0,0,0,0,0,0,0,0,0,0]
NRFtx_tablicaDanych=["","","","","","","","","",""]

class NRFwyslij(threading.Thread): #------WATEK NADAWANIA NRF
    def __init__(self, adres, dane):
        threading.Thread.__init__(self)
        self.adres = adres
        self.dane = dane
    def run(self):
        w=0
        pipesTXflag[self.adres]=True
        while(w<2):
            NRFwyslij2(self.adres,self.dane)
            sleep(2)
            w=w+1
            if(pipesTXflag[self.adres]==False):
                break
        pipesTXflag[self.adres]=False

def NRFwyslij2(adres,wartosc):
    for q in range(10):
        if NRFtx_tablicaAdresow[q]==0:
            NRFtx_tablicaAdresow[q]=adres
            NRFtx_tablicaDanych[q]=wartosc
            break

def NRFsend():
    if NRFtx_tablicaAdresow[0]!=0:
        if(NRFtx_tablicaAdresow[0]==2 or NRFtx_tablicaAdresow[0]==4):
            radio.setPALevel(NRF24.PA_MAX)
        else:
            radio.setPALevel(NRF24.PA_MIN)
        radio.openWritingPipe(pipes[NRFtx_tablicaAdresow[0]])
        time.sleep(.1)
        NRFtransmit(NRFtx_tablicaDanych[0])
        for q in range(9):
            NRFtx_tablicaAdresow[q]=NRFtx_tablicaAdresow[q+1]
            NRFtx_tablicaDanych[q]=NRFtx_tablicaDanych[q+1]
        NRFtx_tablicaAdresow[9]=0
        NRFtx_tablicaDanych[9]=""

def NRFtransmit(dane):
    radio.stopListening()
    message = list(dane)
    radio.write(message)
    radio.startListening()
    while len(message) < 32:
        message.append(0)

def NRFGet():
    receivedMessage = ['','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','']
    stringNRF = ""
    radio.read(receivedMessage, radio.getDynamicPayloadSize())
    for n in receivedMessage:
        if(n>=16 and n <=126):
            stringNRF +=chr(n)
    dziennik.zapis_dziennika_zdarzen(("-----> ODEBRANO: {}".format(stringNRF)))
    return stringNRF

def NRFread( stringNRF ):
    if len(stringNRF)!=0:
        if stringNRF[0]== "#": # '#' - poczatek transmisji
            flaga_NRFOdebral=0
            #------------------------------------------------------------------------------------------------------------
            if stringNRF[1:3]=="01":  #kwiatek
                  if stringNRF[3]== "k":
                      string2=(stringNRF[4:7])
                      czujnikKwiatek.slonce=str(string2)
                      string3=(stringNRF[7:10])
                      czujnikKwiatek.wilgotnosc=str(string3)
                      string4=(stringNRF[10:13])
                      czujnikKwiatek.woda=str(string4)
                      string5=(stringNRF[13:16])
                      czujnikKwiatek.zasilanie=str(string5)
                      sql_baza.dodajRekordKwiatek(czujnikKwiatek.wilgotnosc,czujnikKwiatek.slonce,czujnikKwiatek.woda,czujnikKwiatek.zasilanie)
                      czujnikKwiatek.czas=datetime.datetime.now() #zapisanie czasu ostatniego odbioru
                      dodajUsunBlad(3,False)
                      if(czujnikKwiatek.woda < 10):
                        dodajUsunBlad(20,False)
                      dziennik.zapis_dziennika_zdarzen(("   Kwiatek Slonce: {}%".format(string2)) +("   Wilg: {}%".format(string3)) +("   Woda: {}x10ml".format(string4)) +("   Zas: {}%".format(string5)))
                  if stringNRF[3]== "P":
                      sql_baza.dodajRekordKwiatekPodlanie()
                      dziennik.zapis_dziennika_zdarzen("   Podlanie")
            #------------------------------------------------------------------------------------------------------------
            if stringNRF[1:3]=="02":  #czujnik temperatury 3 - sypialni
                   if stringNRF[3]== "y":
                      string2=(stringNRF[4:6]+"."+stringNRF[6])
                      if(len(stringNRF)>9):
                          string3=(stringNRF[7:10])
                      else:
                          string3=(stringNRF[7:9]+'.0')
                      czujnikPok2.temp=float(string2)
                      czujnikPok2.humi=float(string3)
                      sql_baza.dodajRekordTempSyp(czujnikPok2.temp,czujnikPok2.humi)
                      czujnikPok2.czas=datetime.datetime.now() #zapisanie czasu ostatniego odbioru
                      czujnikPok2.blad=False #kasowanie bledu
                      dodajUsunBlad(2,False)
                      dziennik.zapis_dziennika_zdarzen(("   Sensor3 czujnikPok2.temp: {}*C".format(string2)) + ("   Wilg3: {}%".format(string3)))
                   if stringNRF[3]== "?":
                      string2=(stringNRF[4:7])
                      lampaPok2.Jasnosc=int(string2)
                      if(lampaPok2.Jasnosc==0):
                          lampaPok2.Flaga=0
                      else:
                          lampaPok2.Flaga=1
                      lampaPok2.FlagaSterowanieManualne=True
                      pipesTXflag[2]=False
                      lampaPok2.blad=0
                      dziennik.zapis_dziennika_zdarzen(("   Led Sypialni ON/OFF:{}".format(lampaPok2.Flaga)) + ("   PWM:{}".format(lampaPok2.Jasnosc)))
            #------------------------------------------------------------------------------------------------------------
            if stringNRF[1:3]=="03":  #czujnik  zewnetrzny
                  if stringNRF[3]== "s":
                      string1=(stringNRF[4:9])
                      czujnikZew.lux=int(string1)
                      string2=(stringNRF[9:14])
                      czujnikZew.ir=int(string2)
                      string3=(stringNRF[14:18])
                      czujnikZew.batt=int(string3)
                      sql_baza.dodajRekordSwiatlo(czujnikZew.lux,czujnikZew.ir)
                      oblicz_swiatlo()
                      dziennik.zapis_dziennika_zdarzen("Obliczylem, ze swiatlo wynosci: {}".format(automatykaOswietlenia.swiatloObliczone))
                      dziennik.zapis_dziennika_zdarzen("   Sensor1 zewnetrzny ->   Lux: {}    LuxIR: {}    Bateria: {}".format(czujnikZew.lux,czujnikZew.ir,czujnikZew.batt))
                  if stringNRF[3]== "t":
                      if(stringNRF[4]=="1"):
                          string2=('-'+stringNRF[5:7]+"."+stringNRF[7])
                      else:
                          string2=(stringNRF[5:7]+"."+stringNRF[7])
                      czujnikZew.temp=float(string2)
                      string3=(stringNRF[8:10]+"."+stringNRF[10])
                      czujnikZew.humi=float(string3)
                      sql_baza.dodajRekordTempZew(czujnikZew.temp,czujnikZew.humi,czujnikZew.predkoscWiatru,czujnikZew.kierunekWiatru)
                      string4=stringNRF[11:13]+'.'+stringNRF[13]
                      czujnikZew.predkoscWiatru=float(string4)
                      string5=stringNRF[14:17]
                      czujnikZew.kierunekWiatru=int(string5)
                      czujnikZew.czas=datetime.datetime.now() #zapisanie czasu ostatniego odbioru
                      czujnikZew.blad=False #kasowanie bledu
                      dodajUsunBlad(0,False)
                      dziennik.zapis_dziennika_zdarzen("   Sensor1 zewnetrzny Temp: {}*C   Wilg: {}%   Wiatr: {}m/s   Kier:{}".format(czujnikZew.temp, czujnikZew.humi, czujnikZew.predkoscWiatru, czujnikZew.kierunekWiatru))
            #------------------------------------------------------------------------------------------------------------
            if stringNRF[1:3]=="04":  #czujnik temperatury 2 - pokoju
                  if stringNRF[3]== "t":
                      if(stringNRF[4]=="1"):
                          string2=('-'+stringNRF[5:7]+'.'+stringNRF[7])
                      else:
                          string2=(stringNRF[5:7]+'.'+stringNRF[7])
                      czujnikPok1.temp=float(string2)
                      string3=(stringNRF[8:10]+'.'+stringNRF[10])
                      czujnikPok1.humi=float(string3)
                      sql_baza.dodajRekordTempPok(czujnikPok1.temp,czujnikPok1.humi)
                      string4=(stringNRF[11:14])
                      czujnikPok1.batt=int(string4)
                      czujnikPok1.czas=datetime.datetime.now() #zapisanie czasu ostatniego odbioru
                      czujnikPok1.blad=False #kasowanie bledu
                      dodajUsunBlad(1,False)
                      dziennik.zapis_dziennika_zdarzen(("   Sensor2 czujnikPok1.temp: {}*C".format(string2)) +("   Wilg2: {}%".format(string3)) +("   Batt: {}".format(string4)))
             #------------------------------------------------------------------------------------------------------------
            if stringNRF[1:3]== "05":  #LED - tv
                  if stringNRF[3]== "?":
                      string2=(stringNRF[13:16])
                      if(int(string2)==0):
                          lampaTV.Flaga=0
                      else:
                          lampaTV.Flaga=1
                      if int(string2)>0:
                          lampaTV.Jasnosc=int(string2)
                      pipesTXflag[1]=False
                      lampaTV.blad=0
                      dziennik.zapis_dziennika_zdarzen(("   Led TV ON/OFF:{}".format(lampaTV.Flaga)) + ("   Jasnosc:{}".format(lampaTV.Jasnosc)))
   #------------------------------------------------------------------------------------------------------------
            if stringNRF[1:3]== "06":  #LED LAMPA
                  if stringNRF[3]== "?":
                      string2=(stringNRF[13:16])
                      if(int(string2)==0):
                          lampa1Pok1.Flaga=0
                      else:
                          lampa1Pok1.Flaga=1
                      #lampa1Pok1.Jasnosc=int(string2)
                      pipesTXflag[3]=False
                      lampa1Pok1.blad=0
                      dziennik.zapis_dziennika_zdarzen(("   Led lampa ON/OFF:{}".format(lampa1Pok1.Flaga)) + ("   Jasnosc:{}".format(lampa1Pok1.Jasnosc)))
    #------------------------------------------------------------------------------------------------------------
            if stringNRF[1:3]== "07":  #LED KUCHNIA
                  if stringNRF[3]== "?":
                      if (int(stringNRF[4]) == 1 or int(stringNRF[4]) == 2):
                        lampaKuch.Flaga=1
                      else:
                        lampaKuch.Flaga=0
                      pipesTXflag[4]=False
                      lampaKuch.blad=0
                      dziennik.zapis_dziennika_zdarzen(("   Led kuchnia TRYB:{}".format(lampaKuch.Flaga)))
            #------------------------------------------------------------------------------------------------------------
            if stringNRF[1:3]== "08":  #DEKORACJE POK 1
                  if stringNRF[3]== "?":
                      dekoPok1.Flaga=int(stringNRF[4])
                      pipesTXflag[AdresLampa2]=False
                      dekoPok1.blad=0
                      dziennik.zapis_dziennika_zdarzen(("   Dekoracje Pok 1 ON/OFF:{}".format(dekoPok1.Flaga)))
            #------------------------------------------------------------------------------------------------------------
            if stringNRF[1:3]== "09":  #DEKORACJE 2 POK 1
                  if stringNRF[3]== "?":
                      deko2Pok1.Flaga=int(stringNRF[4])
                      pipesTXflag[AdresLampa3]=False
                      deko2Pok1.blad=0
                      dziennik.zapis_dziennika_zdarzen(("   Dekoracje 2 Pok 1 ON/OFF:{}".format(dekoPok1.Flaga)))
    #------------------------------------------------------------------------------------------------------------
            if stringNRF[1:3]== "10":  #FLAMING
                  if stringNRF[3]== "?":
                      dekoFlaming.Flaga=int(stringNRF[4])
                      pipesTXflag[AdresFlaming]=False
                      dekoFlaming.blad=0
                      dziennik.zapis_dziennika_zdarzen(("   Flaming ON/OFF:{}".format(dekoFlaming.Flaga)))
    #------------------------------------------------------------------------------------------------------------
            if stringNRF[1:3]== "11":  #Uniwersalny modul USB
                  if stringNRF[3]== "?":
                      dekoUsb.Flaga=int(stringNRF[4])
                      pipesTXflag[AdresUsb]=False
                      dekoUsb.blad=0
                      dziennik.zapis_dziennika_zdarzen(("   Uniwersalny USB ON/OFF:{}".format(dekoUsb.Flaga)))
            zapis_danych_xml()
    #------------------------------------------------------------------------------------------------------------
            if stringNRF[1:3]== "18":  #Hydroponika
                  if stringNRF[3]== "?":
                      hydroponika.Flaga=int(stringNRF[4])
                      pipesTXflag[hydroponika.Adres]=False
                      hydroponika.blad=0
                      dziennik.zapis_dziennika_zdarzen(("   Hydroponika ON/OFF:{}".format(hydroponika.Flaga)))
            zapis_danych_xml()
#------------------------------------------------------------------------------------------------------------
            if stringNRF[1:3]== "12":  #kwiatek 2  addres 12
                  if stringNRF[3]== "k":
                      string2=(stringNRF[4:7])
                      czujnikKwiatek2.slonce=int(string2)
                      #string3=(stringNRF[7:10])
                      string5=(stringNRF[14:17])
                      czujnikKwiatek2.wilgotnosc_raw=string5
                      string3 = obliczFunkcje(czujnikKwiatek2.wartoscMin, czujnikKwiatek2.wartoscMax, int((stringNRF[14:17])))
                      czujnikKwiatek2.wilgotnosc=int(string3)
                      string4=(stringNRF[10]+"."+stringNRF[11:13])
                      czujnikKwiatek2.zasilanie=str(string4)
                      sql_baza.dodajRekordKwiatek2(czujnikKwiatek2.wilgotnosc,czujnikKwiatek2.slonce,czujnikKwiatek2.zasilanie,czujnikKwiatek2.wilgotnosc_raw)
                      czujnikKwiatek2.czas=datetime.datetime.now() #zapisanie czasu ostatniego odbioru
                      dodajUsunBlad(4,False)
                      dziennik.zapis_dziennika_zdarzen(("   Kwiatek 12 Slonce: {}%   Wilg: {}%   Zas: {}V".format(string2,string3,string4)))
#------------------------------------------------------------------------------------------------------------
            if stringNRF[1:3]== "13":  #kwiatek 3 adres 13
                  if stringNRF[3]== "k":
                      string2=(stringNRF[4:7])
                      czujnikKwiatek3.slonce=int(string2)
                      #string3=(stringNRF[7:10])
                      string5=(stringNRF[14:17])
                      czujnikKwiatek3.wilgotnosc_raw=string5
                      string3 = obliczFunkcje(czujnikKwiatek3.wartoscMin, czujnikKwiatek3.wartoscMax, int((stringNRF[14:17])))
                      czujnikKwiatek3.wilgotnosc=int(string3)
                      string4=(stringNRF[10]+"."+stringNRF[11:13])
                      czujnikKwiatek3.zasilanie=str(string4)
                      sql_baza.dodajRekordKwiatek3(czujnikKwiatek3.wilgotnosc,czujnikKwiatek3.slonce,czujnikKwiatek3.zasilanie, czujnikKwiatek3.wilgotnosc_raw)
                      czujnikKwiatek3.czas=datetime.datetime.now() #zapisanie czasu ostatniego odbioru
                      dodajUsunBlad(5,False)
                      dziennik.zapis_dziennika_zdarzen(("   Kwiatek 13 Slonce: {}%   Wilg: {}%   Zas: {}V".format(string2,string3,string4)))
#------------------------------------------------------------------------------------------------------------
            if stringNRF[1:3]== "14":  #kwiatek 4 adres 14
                  if stringNRF[3]== "k":
                      string2=(stringNRF[4:7])
                      czujnikKwiatek4.slonce=int(string2)
                      #string3=(stringNRF[7:10])
                      string5=(stringNRF[14:17])
                      czujnikKwiatek4.wilgotnosc_raw=int(string5)
                      string3 = obliczFunkcje(czujnikKwiatek4.wartoscMin, czujnikKwiatek4.wartoscMax, czujnikKwiatek4.wilgotnosc_raw)
                      czujnikKwiatek4.wilgotnosc=int(string3)
                      string4=(stringNRF[10]+"."+stringNRF[11:13])
                      czujnikKwiatek4.zasilanie=str(string4)
                      sql_baza.dodajRekordKwiatek4(czujnikKwiatek4.wilgotnosc,czujnikKwiatek4.slonce,czujnikKwiatek4.zasilanie, czujnikKwiatek4.wilgotnosc_raw)
                      czujnikKwiatek4.czas=datetime.datetime.now() #zapisanie czasu ostatniego odbioru
                      dodajUsunBlad(6,False)
                      dziennik.zapis_dziennika_zdarzen(("   Kwiatek 14 Slonce: {}%   Wilg: {}%   Zas: {}V".format(string2,string3,string4)))
#------------------------------------------------------------------------------------------------------------
            if stringNRF[1:3]== "15":  #BUDA 15
                  if stringNRF[3]== "s":
                      string2=(stringNRF[4:7])
                      buda.temp1=float(string2)/10
                      string5=(stringNRF[7:10])
                      buda.temp2=float(string5)/10
                      string6=(stringNRF[10:13])
                      buda.temp3=float(string6)/10
                      string7=(stringNRF[13])
                      buda.czujnikZajetosciFlaga=int(string7)
                      string8=(stringNRF[14:16])
                      buda.czujnikZajetosciRaw=int(string8)
                      buda.czas=datetime.datetime.now() #zapisanie czasu ostatniego odbioru
                      dziennik.zapis_dziennika_zdarzen(("   Buda t.wew: {}   t.ciepla: {}  t.zimna: {}   f:{}   cz:{}".format(buda.temp1,buda.temp2,buda.temp3,buda.czujnikZajetosciFlaga, buda.czujnikZajetosciRaw)))
 #------------------------------------------------------------------------------------------------------------
            if stringNRF[1:3]== "16":  #kwiatek 5 adres 16
                  if stringNRF[3]== "k":
                      string2=(stringNRF[4:7])
                      czujnikKwiatek5.slonce=int(string2)
                      string5=(stringNRF[14:17])
                      czujnikKwiatek5.wilgotnosc_raw=int(string5)
                      string3 = obliczFunkcje(czujnikKwiatek5.wartoscMin, czujnikKwiatek5.wartoscMax, czujnikKwiatek5.wilgotnosc_raw)
                      czujnikKwiatek5.wilgotnosc=int(string3)
                      string4=(stringNRF[10]+"."+stringNRF[11:13])
                      czujnikKwiatek5.zasilanie=str(string4)
                      sql_baza.dodajRekordKwiatek5(czujnikKwiatek5.wilgotnosc,czujnikKwiatek5.slonce,czujnikKwiatek5.zasilanie, czujnikKwiatek5.wilgotnosc_raw)
                      czujnikKwiatek5.czas=datetime.datetime.now() #zapisanie czasu ostatniego odbioru
                      dodajUsunBlad(16,False)
                      dziennik.zapis_dziennika_zdarzen(("   Kwiatek 16 Slonce: {}%   Wilg: {}%   Zas: {}V".format(string2,string3,string4)))
 #------------------------------------------------------------------------------------------------------------
            if stringNRF[1:3]== "17":  #kwiatek 6 adres 17
                  if stringNRF[3]== "k":
                      string2=(stringNRF[4:7])
                      czujnikKwiatek6.slonce=int(string2)
                      string5=(stringNRF[14:17])
                      czujnikKwiatek6.wilgotnosc_raw=int(string5)
                      string3 = obliczFunkcje(czujnikKwiatek6.wartoscMin, czujnikKwiatek6.wartoscMax, czujnikKwiatek6.wilgotnosc_raw)
                      czujnikKwiatek6.wilgotnosc=int(string3)
                      string4=(stringNRF[10]+"."+stringNRF[11:13])
                      czujnikKwiatek6.zasilanie=str(string4)
                      sql_baza.dodajRekordKwiatek6(czujnikKwiatek6.wilgotnosc,czujnikKwiatek6.slonce,czujnikKwiatek6.zasilanie, czujnikKwiatek6.wilgotnosc_raw)
                      czujnikKwiatek6.czas=datetime.datetime.now() #zapisanie czasu ostatniego odbioru
                      dodajUsunBlad(19,False)
                      dziennik.zapis_dziennika_zdarzen(("   Kwiatek 17 Slonce: {}%   Wilg: {}%   Zas: {}V".format(string2,string3,string4)))
 #------------------------------------------------------------------------------------------------------------
            if stringNRF[1:3]== "99":  #moduł testowy
                  if stringNRF[3]== ".":
                        int1 = ''.join(str(chr(e)) for e in stringNRF[4:8])
                        int2 = ''.join(str(chr(e)) for e in stringNRF[9:])
                        fl1=(float(int1)/1000)
                        dziennik.zapis_stuff('zasilanie: {:.3f}V  -> wilgotnosc: {}'.format(fl1,int2))
            zapis_danych_xml()

def obliczFunkcje(wartoscMin, wartoscMax, pomiar):
    obliczenia=0.0
    #print("dane: {}/{}  -> {}".format(wartoscMin, wartoscMax, float(pomiar)))
    if(float(pomiar) < wartoscMin):
        obliczenia=0
    elif(float(pomiar) > wartoscMax):
        obliczenia=100
    else:
        zmien=wartoscMax-wartoscMin
        obliczenia2=(100.0/zmien)*float(pomiar)
        obliczenia3=(-wartoscMin)*(100.0/zmien)
        obliczenia=obliczenia2+obliczenia3
        #print("obliczenia: {} -> o1:{}, o2:{} / {}".format(zmien,obliczenia2,obliczenia3,obliczenia))
    return int(round(obliczenia))

def zamienLiczbe(liczba):
    if liczba<10:
        return "00"+str(liczba)
    elif liczba>=10 and liczba<100:
        return "0"+str(liczba)
    else: return str(liczba)
#------------------UDP-----------------------------------
def server():
    try:
        message, address = s.recvfrom(1024)
        dziennik.zapis_dziennika_zdarzen(dziennik.data() +" " + "Polaczenie %s: %s" % (address, message))
        transmisja(message, address)
        return message
    except (KeyboardInterrupt, SystemExit):
        raise
    except:
        traceback.print_exc()


class ustawSwiatloZeZwloka(threading.Thread): #------WATEK NADAWANIA NRF
    def __init__(self, adres, jasnosc, czas):
        threading.Thread.__init__(self)
        self.adres = adres
        self.jasnosc = jasnosc
        self.czas = czas
    def run(self):
        time.sleep(self.czas)
        if self.jasnosc==0:
            sterowanieOswietleniem(self.adres,100)
        sterowanieOswietleniem(self.adres,self.jasnosc)
        dziennik.zapis_dziennika_zdarzen("Funkacja spij wlaczona")

def sterowanieOswietleniem(adres, ustawienie):
    if adres==lampaTV.Adres:   #TV
        wiad="#05K{}{:03d}".format(lampaTV.Ustawienie,int(ustawienie))
        if len(wiad)>=15:
            dziennik.zapis_dziennika_zdarzen("Ustawiono Led TV: {}".format(wiad))
            dodajInfo("światło TV: {}".format(ustawienie))
            NRFwyslij(AdresLedTV,wiad).start()
            lampaTV.blad+=1
        else:
            dziennik.zapis_dziennika_zdarzen("BLAD SKLADNI!: {}".format(wiad))
    if adres==lampaPok2.Adres:  #SYPIALNIA
        wiad="#S{:03d}".format(int(ustawienie))
        if len(wiad)>=5:
            dziennik.zapis_dziennika_zdarzen("Ustawiono Led Sypialni: {}".format(wiad))
            dodajInfo("światło w sypialni: {}".format(ustawienie))
            NRFwyslij(AdresSypialnia,wiad).start()
            lampaPok2.blad+=1
        else:
            dziennik.zapis_dziennika_zdarzen("BLAD SKLADNI!: {}".format(wiad))
    if adres==lampaKuch.Adres:  #KUCHNIA
        wiad="#07T{:01d}".format(int(ustawienie))
        if len(wiad)>=5:
            dziennik.zapis_dziennika_zdarzen("Ustawiono Led Kuchni: {}".format(wiad))
            dodajInfo("światło w kuchni: {}".format(ustawienie))
            NRFwyslij(AdresKuchnia,wiad).start()
            lampaKuch.blad+=1
        else:
            dziennik.zapis_dziennika_zdarzen("BLAD SKLADNI!: {}".format(wiad))
    if adres==lampa1Pok1.Adres:  # LAMPA 1 w salonie
        wiad="#05K{}{:03d}".format(lampa1Pok1.Ustawienie, int(ustawienie))
        if len(wiad)>=5:
            lampa1Pok1.Jasnosc=int(ustawienie)
            dziennik.zapis_dziennika_zdarzen("Ustawiono Reflektor 1: {}".format(wiad))
            dodajInfo("reflektor 1 w salonie: {}/{}".format(lampa1Pok1.Ustawienie,int(ustawienie)))
            NRFwyslij(AdresLampa1,wiad).start()
            lampa1Pok1.blad+=1
            if(int(ustawienie) == 0):
                lampa1Pok1.Flaga = 0
            else:
                lampa1Pok1.Flaga = 1
        else:
            dziennik.zapis_dziennika_zdarzen("BLAD SKLADNI!: {}".format(wiad))
    if adres==dekoPok1.Adres:  # dekoracje pok 1 / Reka
        wiad="#08T{:1d}".format(int(ustawienie))
        if len(wiad)>=5:
            dziennik.zapis_dziennika_zdarzen("Ustawiono Lampa 1: {}".format(wiad))
            dodajInfo("dekoracje 1 w salonie: {}".format(ustawienie))
            NRFwyslij(dekoPok1.Adres,wiad).start()
            lampa1Pok1.blad+=1
        else:
            dziennik.zapis_dziennika_zdarzen("BLAD SKLADNI!: {}".format(wiad))
    if adres==deko2Pok1.Adres:  # dekoracje pok 1 / Eifla i inne
        wiad="#09T{:1d}".format(int(ustawienie))
        if len(wiad)>=5:
            dziennik.zapis_dziennika_zdarzen("Ustawiono Lampa 2: {}".format(wiad))
            dodajInfo("dekoracje 2 w salonie: {}".format(ustawienie))
            NRFwyslij(deko2Pok1.Adres,wiad).start()
            dekoPok1.blad+=1
        else:
            dziennik.zapis_dziennika_zdarzen("BLAD SKLADNI!: {}".format(wiad))
    if adres==dekoFlaming.Adres:  # FLAMING
        wiad="#10T{:1d}".format(int(ustawienie))
        if len(wiad)>=5:
            dziennik.zapis_dziennika_zdarzen("Ustawiono Lampa Flaming: {}".format(wiad))
            dodajInfo("flaming: {}".format(ustawienie))
            NRFwyslij(AdresFlaming,wiad).start()
            dekoFlaming.blad+=1
        else:
            dziennik.zapis_dziennika_zdarzen("BLAD SKLADNI!: {}".format(wiad))
    if adres==dekoUsb.Adres:  # Dekoracje - uniwersalny modul USB
        wiad="#11T{:1d}".format(int(ustawienie))
        if len(wiad)>=5:
            dziennik.zapis_dziennika_zdarzen("Ustawiono Uniwersalny USB: {}".format(wiad))
            dodajInfo("uniwersalny USB: {}".format(ustawienie))
            NRFwyslij(AdresUsb,wiad).start()
            dekoUsb.blad+=1
        else:
            dziennik.zapis_dziennika_zdarzen("BLAD SKLADNI!: {}".format(wiad))
    if adres==lampaPok1Tradfri.Adres:  # Tradfri Salon
        if ustawienie==0 or ustawienie==1:
            ikea.ikea_power_group(hubip, user_id, securityid, security_user, adres, ustawienie)
        elif ustawienie>1:
            ikea.ikea_dim_group(hubip, user_id, securityid, security_user, adres, ustawienie)
        dziennik.zapis_dziennika_zdarzen("Tradfri Salon ->: {}".format(ustawienie))
        dodajInfo("oświetlenie w salonie: {}".format(ustawienie))
    if adres==lampaPok1Tradfri.Zarowka:  # Tradfri Salon Zarowka
        if ustawienie==0 or ustawienie==1:
            ikea.ikea_power_light(hubip, user_id, securityid, security_user, adres, ustawienie)
        elif ustawienie>1:
            ikea.ikea_dim_light(hubip, user_id, securityid, security_user, adres, ustawienie)
        dziennik.zapis_dziennika_zdarzen("Tradfri Salon-Zarowka ->: {}".format(ustawienie))
    if adres==lampaJadalniaTradfri.Adres:  # Tradfri Jadalnia
        if ustawienie==0 or ustawienie==1:
            ikea.ikea_power_group(hubip, user_id, securityid, security_user, adres, ustawienie)
        elif ustawienie>1:
            ikea.ikea_dim_group(hubip, user_id, securityid, security_user, adres, ustawienie)
        dziennik.zapis_dziennika_zdarzen("Tradfri Jadalnia ->: {}".format(ustawienie))
        dodajInfo("oświetlenie w jadalni: {}".format(ustawienie))
    if adres==lampaPrzedpokojTradfri.Adres:  # Tradfri przedpokoj
        if ustawienie==0 or ustawienie==1:
            ikea.ikea_power_group(hubip, user_id, securityid, security_user, adres, ustawienie)
        elif ustawienie>1:
            ikea.ikea_dim_group(hubip, user_id, securityid, security_user, adres, ustawienie)
        if(ustawienie>0):
            lampaPrzedpokojTradfri.Status=1
        else:
            lampaPrzedpokojTradfri.Status=0
        dziennik.zapis_dziennika_zdarzen("Tradfri Przedpokoj ->: {}".format(ustawienie))
        dodajInfo("oświetlenie w przedpokoju: {}".format(ustawienie))
    if adres==lampaDuzaTradfri.Adres:  # Tradfri Lampa Duza
        if len(str(ustawienie))==1:
            if int(ustawienie)==0 or int(ustawienie)==1:
                ikea.ikea_power_light(hubip, user_id, securityid, security_user, adres, int(ustawienie))
                dziennik.zapis_dziennika_zdarzen("Tradfri Lampa ON/OFF ->: {}".format(ustawienie))
        elif len(str(ustawienie))==9:
            chKolor1=int(ustawienie[0:3])
            chKolor2=int(ustawienie[3:6])
            chKolor3=int(ustawienie[6:9])
            ikea.ikea_RGB_lamp(hubip, user_id, securityid, security_user, lampaDuzaTradfri.Adres, chKolor1, chKolor2, chKolor3)
            dziennik.zapis_dziennika_zdarzen("Tradfri Lampa kolor ->: {}".format(ustawienie))
            dodajInfo("lampa w salonie -> kolor: {}".format(ustawienie))
        elif len(str(ustawienie))==2 or len(str(ustawienie))==3:
            if int(ustawienie)>1 and int(ustawienie)<=100:
                ikea.ikea_dim_light(hubip, user_id, securityid, security_user, adres, int(ustawienie))
                dziennik.zapis_dziennika_zdarzen("Tradfri Lampa Jasnosc ->: {}".format(ustawienie))
                dodajInfo("lampa w salonie: {}".format(ustawienie))
        else:
            dziennik.zapis_dziennika_zdarzen("Tradfri blad skladni")
    if adres==lampaPok2Tradfri.Adres:  # Tradfri Sypialnia
        if ustawienie==0 or ustawienie==1:
            ikea.ikea_power_group(hubip, user_id, securityid, security_user, lampaPok2Tradfri.Adres, ustawienie)
            lampaPok2Tradfri.Flaga = False
        elif ustawienie>1:
            ikea.ikea_dim_group(hubip, user_id, securityid, security_user, lampaPok2Tradfri.Adres, ustawienie)
            ikea.ikea_power_group(hubip, user_id, securityid, security_user, lampaPok2Tradfri.Adres, 1)
            lampaPok2Tradfri.Flaga = True
        dziennik.zapis_dziennika_zdarzen("Tradfri Sypialnia ->: {}".format(ustawienie))
        dodajInfo("oświetlenie w sypialni: {}".format(ustawienie))
    if adres==hydroponika.Adres:   #Hydroponika
        if int(ustawienie) > 1:
            wiad="#17P1" #wlacz pompe
        else:
            wiad="#17A{:01d}".format(int(ustawienie))
        if len(wiad)>=5:
            dziennik.zapis_dziennika_zdarzen("Ustawiono Hydroponike: {}".format(wiad))
            dodajInfo("Hydroponika: {}".format(ustawienie))
            NRFwyslij(hydroponika.Adres,wiad).start()
        else:
            dziennik.zapis_dziennika_zdarzen("BLAD SKLADNI!: {}".format(wiad))



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
    #dziennik.zapis_dziennika_zdarzen("Zapisano dane")

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
    dziennik.zapis_dziennika_zdarzen("Zapisano ustawienia")

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

def oblicz_swiatlo():
        k=3 #wzmocnienie
        for i in range(4):
            automatykaOswietlenia.wartosciLux[i]=automatykaOswietlenia.wartosciLux[i+1]
        automatykaOswietlenia.wartosciLux[4]=czujnikZew.lux
        automatykaOswietlenia.swiatloObliczone=automatykaOswietlenia.wartosciLux[0]
        for i in range(4):
            automatykaOswietlenia.swiatloObliczone=automatykaOswietlenia.swiatloObliczone+automatykaOswietlenia.wartosciLux[i+1]
        automatykaOswietlenia.swiatloObliczone=(automatykaOswietlenia.swiatloObliczone+((automatykaOswietlenia.wartosciLux[4]*k)))/(5+k)
        if automatykaOswietlenia.swiatloObliczone<czujnikZew.noc_ustawienie:
            czujnikZew.noc_flaga=True
        else:
            czujnikZew.noc_flaga=False
        dziennik.zapis_dziennika_zdarzen("Swiatlo obliczone=  {}".format(automatykaOswietlenia.swiatloObliczone) + " / {}".format(automatykaOswietlenia.wartosciLux))

def jasnosc_wyswietlacza(): #----STEROWANIE WYSWIETLACZEM - WATEK!!!!!!!!!! ----------------------------------------------------
    global swiatlo
    swiatlo_old=0
    while(1):
        swiatlo=czujnik_swiatla()
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
            #dziennik.zapis_dziennika_zdarzen("Jasnosc wyswietlacza:{}   / old:{}, new:{}".format(jasnoscwysw,swiatlo_old,swiatlo))
            swiatlo_old=swiatlo
        time.sleep(5)

#++++++++++++++++++++++++++++++ WYSWIETLANIE ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
bgcolor=(255,255,255,255)
tfps=0.2

def wysw_init():
    global screen, obrazek, czaspogody

    pygame.init()
    resolution = 800, 480
    screen = pygame.display.set_mode(resolution,FULLSCREEN)
    #screen = pygame.display.set_mode(resolution,1)
    pygame.display.set_caption('MojDom')
    screen.fill(bgcolor)
    pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))
    czaspogody=datetime.datetime.utcnow()

pozycja_animacji = [[0,0],[60,-42],[120,-135],[160,-225],[180,-275],[190,-367],[230,-13],[350,-89],[390,-247],[430,-198],[500,-400],[560,-163],[620,-200],[650,-50],[700,-31],[750,-7],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]]
kolorPaskaInfo=(50,100,10,255)

def obraz_glowny():
    global screen, licznik, pozycja_animacji
    global czasodswpogody,ledtvjasnosc, czaspogody, kolorPaskaInfo
    tfps=0
    pozX=0

    kolor=(0,0,0,250)
    kolorczcionki1=(255,255,255,255)
    kolorczcionki2=(255,200,100,255)
    kolorczcionki3=(0,0,0,255)
    kolorczcionki4=(60,60,60,200)
    kolorczcionki5=(255,255,255,255)

    #---ANIMACJA TAPETY -----
    #pogoda.Pogoda.IkonaDzis="02"
    #czujnikZew.noc_flaga=False
    '''
    01d - clear sky
    02d - few clouds
    03d - scattered clouds
    04d - broken clouds
    09d - shower rain
    10d - rain
    11d - thunderstorm
    13d - snow
    50d - mist - fog
    '''
    tapeta=pogoda.Pogoda.IkonaDzis
    tapeta=tapeta.lower()

    if(tapeta.find('02') != -1 or tapeta.find('03') != -1 or tapeta.find('04') != -1): #CLOUDS
        if pozycja_animacji[16][1]==0: #dla zmiany kierunku
            if pozycja_animacji[16][0]>300:
                pozycja_animacji[16][1]=1
            else:
                pozycja_animacji[16][0]=pozycja_animacji[16][0]+1
        else: #dla zmiany kierunku
            if pozycja_animacji[16][0]<0:
                pozycja_animacji[16][1]=0
            else:
                pozycja_animacji[16][0]=pozycja_animacji[16][0]-1
        pozX=(-600)+pozycja_animacji[16][0]
        if(tapeta.find('02') != -1 and czujnikZew.noc_flaga==False):
            kolorczcionki3=(185,242,107,255)
            kolorczcionki4=(235,255,187,255)
        if czujnikZew.noc_flaga==True:
            kolorczcionki3=(190,190,190,255)
            kolorczcionki4=(250,250,250,200)
    pogoda.ikonka(pozX,0,255,True,czujnikZew.noc_flaga,pogoda.Pogoda.IkonaDzis)
    if(tapeta.find('01') != -1):  #CLEAR SKY
        if czujnikZew.noc_flaga==True:
            kolorczcionki2=(180,180,180,255)
        else:
            kolorczcionki2=(100,40,20,255)
        kolorczcionki3=(255,255,155,255)
        kolorczcionki4=(255,215,0,255)
        kolorczcionki5=(255,82,0,255)
    elif(tapeta.find('50') != -1):
        kolorczcionki1=(0,105,56,255)
        kolorczcionki2=(100,40,20,255)
        kolorczcionki3=(95,103,56,255)
        kolorczcionki4=(255,215,0,255)
        kolorczcionki5=(255,82,0,255)
    elif(tapeta.find('09') != -1 or tapeta.find('10') != -1):  #RAIN
        kolorczcionki3=(255,255,155,255)
        kolorczcionki4=(255,255,200,255)
        pogoda.icons(randint(30, 750),randint(70, 300),255,"anim")
        pogoda.icons(randint(30, 750),randint(70, 300),255,"anim")
        pogoda.icons(randint(30, 750),randint(70, 300),255,"anim")
        pogoda.icons(randint(30, 750),randint(30, 300),255,"anim")
        pogoda.icons(randint(30, 750),randint(30, 300),255,"anim")
        pogoda.icons(randint(30, 750),randint(30, 300),255,"anim")
    if(tapeta.find('11') != -1): #THUNDERSTORM
        kolorczcionki3=(255,255,155,255)
        kolorczcionki4=(255,215,0,255)
        kolorczcionki5=(255,82,0,255)
        if pozycja_animacji[17][0]<0:
            pogoda.icons(0,0,255,"DTStorm2")
            pozycja_animacji[17][0]=randint(7, 70)
        else:
            pozycja_animacji[17][0]=pozycja_animacji[17][0]-1
    elif(tapeta.find('13') != -1): #SNOW
        tfps=0.0
        pogoda.icons(pozycja_animacji[0][0],pozycja_animacji[0][1],255,"snowflake1")
        pozycja_animacji[0][1]=pozycja_animacji[0][1]+1
        pogoda.icons(pozycja_animacji[1][0],pozycja_animacji[1][1],255,"snowflake2")
        pozycja_animacji[1][1]=pozycja_animacji[1][1]+2
        pogoda.icons(pozycja_animacji[2][0],pozycja_animacji[2][1],255,"snowflake3")
        pozycja_animacji[2][1]=pozycja_animacji[2][1]+4
        pogoda.icons(pozycja_animacji[3][0],pozycja_animacji[3][1],255,"snowflake3")
        pozycja_animacji[3][1]=pozycja_animacji[3][1]+4
        pogoda.icons(pozycja_animacji[4][0],pozycja_animacji[4][1],255,"snowflake3")
        pozycja_animacji[4][1]=pozycja_animacji[4][1]+4
        pogoda.icons(pozycja_animacji[5][0],pozycja_animacji[5][1],255,"snowflake3")
        pozycja_animacji[5][1]=pozycja_animacji[5][1]+4
        pogoda.icons(pozycja_animacji[6][0],pozycja_animacji[6][1],255,"snowflake3")
        pozycja_animacji[6][1]=pozycja_animacji[6][1]+4
        pogoda.icons(pozycja_animacji[7][0],pozycja_animacji[7][1],255,"snowflake4")
        pozycja_animacji[7][1]=pozycja_animacji[7][1]+1
        pogoda.icons(pozycja_animacji[8][0],pozycja_animacji[8][1],255,"snowflake5")
        pozycja_animacji[8][1]=pozycja_animacji[8][1]+3
        pogoda.icons(pozycja_animacji[9][0],pozycja_animacji[9][1],255,"snowflake5")
        pozycja_animacji[9][1]=pozycja_animacji[9][1]+3
        pogoda.icons(pozycja_animacji[10][0],pozycja_animacji[10][1],255,"snowflake5")
        pozycja_animacji[10][1]=pozycja_animacji[10][1]+3
        pogoda.icons(pozycja_animacji[11][0],pozycja_animacji[11][1],255,"snowflake6")
        pozycja_animacji[11][1]=pozycja_animacji[11][1]+4
        pogoda.icons(pozycja_animacji[12][0],pozycja_animacji[12][1],255,"snowflake6")
        pozycja_animacji[12][1]=pozycja_animacji[12][1]+4
        pogoda.icons(pozycja_animacji[13][0],pozycja_animacji[13][1],255,"snowflake3")
        pozycja_animacji[13][1]=pozycja_animacji[13][1]+5
        pogoda.icons(pozycja_animacji[14][0],pozycja_animacji[14][1],255,"snowflake6")
        pozycja_animacji[14][1]=pozycja_animacji[14][1]+4
        pogoda.icons(pozycja_animacji[15][0],pozycja_animacji[15][1],255,"snowflake6")
        pozycja_animacji[15][1]=pozycja_animacji[15][1]+4
        for px in range(16):
            if pozycja_animacji[px][1]>randint(480, 500):
                pozycja_animacji[px][0]=randint(10, 780)
                pozycja_animacji[px][1]=0
        kolorczcionki4=(160,180,160,255)
        kolorczcionki3=(220,220,250,255)
    #------------------------
    d = datetime.datetime.today()
    dzienTygodnia=wysw.dzien(d.weekday())

    wysw.napis_centralny(screen, str(time.strftime("%H:%M")),"Nimbus Sans L",190,295,90,kolorczcionki1,255) #czas
    wysw.napis_centralny(screen, dzienTygodnia,"Nimbus Sans L",56,620,80,kolorczcionki2,255)  #dzien tygodnia
    wysw.napis_centralny(screen, str(int(time.strftime("%d")))+" "+wysw.miesiac(str(time.strftime("%B"))),"Nimbus Sans L",56,620,120,kolorczcionki2,255)  #dzien tygodnia

    wysw.napis2(screen, "dziś","Nimbus Sans L",56,50,170,kolorczcionki3,255)
    pogoda.ikonka(30,210,255,False,czujnikZew.noc_flaga,pogoda.Pogoda.IkonaDzis)
    pogoda.icons(20,330,255,"arrow_down")
    wysw.napis2(screen, "{:.0f}°C".format(pogoda.Pogoda.TempMinDzis),"Nimbus Sans L",54,70,330,kolorczcionki3,255)
    pogoda.icons(20,380,255,"arrow_up")
    wysw.napis2(screen, "{:.0f}°C".format(pogoda.Pogoda.TempMaxDzis),"Nimbus Sans L",54,70,380,kolorczcionki4,255)
    wysw.napis2(screen, "jutro","Nimbus Sans L",56,230,170,kolorczcionki3,255)
    pogoda.ikonka(220,210,255,False,False,pogoda.Pogoda.IkonaJutro)
    pogoda.icons(205,330,255,"arrow_down")
    wysw.napis2(screen, "{:.0f}°C".format(pogoda.Pogoda.TempMinJutro),"Nimbus Sans L",54,245,330,kolorczcionki3,255)
    pogoda.icons(205,380,255,"arrow_up")
    wysw.napis2(screen, "{:.0f}°C".format(pogoda.Pogoda.TempMaxJutro),"Nimbus Sans L",54,245,380,kolorczcionki4,255)

    wysw.obraz(screen, 390,170,255,"temp_out")
    dlugosc=wysw.napis2(screen, "{:.1f}°C".format(czujnikZew.temp),"Nimbus Sans L",68,485,190,kolorczcionki5,255)
    wysw.napis2(screen, "{:.0f}%".format(czujnikZew.humi),"Nimbus Sans L",48,505+dlugosc,200,kolorczcionki4,255)
    wysw.obraz(screen, 390,258,255,"temp_in")
    dlugosc=wysw.napis2(screen, "{:.1f}°C".format(czujnikPok1.temp),"Nimbus Sans L",68,485,280,kolorczcionki4,255)
    wysw.napis2(screen, "{:.0f}%".format(czujnikPok1.humi),"Nimbus Sans L",48,505+dlugosc,290,kolorczcionki4,255)

    wysw.obraz(screen, 390,350,255,"wind")
    dlugosc=wysw.napis2(screen, "{:.1f}m/s".format(czujnikZew.predkoscWiatru),"Nimbus Sans L",50,485,370,kolorczcionki3,255)

    # PASEK INFORMACYJNY
    pasekInfo.aktualnaInformacja=odczytajInfo()
    if (pasekInfo.aktualnaInformacja != ""):
        pasekInfo.wyswietlanaInformacja=pasekInfo.aktualnaInformacja
        kolorPaskaInfo=(190,255,190,255)
        pasekInfo.czas=60
        pasekInfo.pozycja=3
    else:
        if(pasekInfo.czas==0):
            pasekInfo.wyswietlanaInformacja=odczytajBlad()
            if (pasekInfo.wyswietlanaInformacja != ""):
                 pasekInfo.czas=120
                 pasekInfo.pozycja=3
                 kolorPaskaInfo=(255,100,100,255)

    if(pasekInfo.czas>0):
        pasekInfo.czas-=1
    if(pasekInfo.czas>=0 and pasekInfo.czas<=3):
        pasekInfo.pozycja=pasekInfo.czas

    if(pasekInfo.wyswietlanaInformacja != ""):
        wysw.napis2(screen, pasekInfo.wyswietlanaInformacja,"Nimbus Sans L",46,70,480-(pasekInfo.pozycja*13),kolorPaskaInfo,255)


def obraz_nocny():
    global screen, licznik
    global czasodswpogody,ledtvjasnosc, czaspogody
    kolor=(0,0,0,250)
    kolorczcionki3=(180,180,180,255)

    wysw.napis_centralny_tlo(screen, str(time.strftime("%H:%M")),"Nimbus Sans L",360,400,210,kolorczcionki3,255,(0,0,0,255)) #czas
    wysw.napis_tlo(screen, "Temperatura {:.1f}°C".format(czujnikPok1.temp),"Nimbus Sans L",70,20,410,kolorczcionki3,255,(0,0,0,255))

def LCD():  #----WYSWIETLANIE - WATEK!!!!!!!!!! ------------------------------------------------------------------------------------------------------
    global obraz, tfps
    tryb_nocny=False

    wysw_init()
    while(1):
        for event in pygame.event.get():
            if event.type==pygame.KEYDOWN and event.key==pygame.K_SPACE:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                px=event.pos[0]
                py=event.pos[1]
                print ("You pressed the left mouse button at ({}, {})".format(px,py))
                if(px>750 and px<800 and py>0 and py<50):
                    pygame.quit()
                    sys.exit()
                if(px>17 and px<284 and py>15 and py<227):
                    screen.fill(bgcolor)
                    obraz=0
        #flaga_odczyt_ustawien=wysw.odswiez(czujnikZew.temp,czujnikPok1.temp,czujnikPok2.temp,czujnikZew.humi,czujnikPok1.humi,czujnikPok2.humi,czujnikKwiatek.wilgotnosc,czujnikKwiatek.slonce,czujnikKwiatek.woda,czujnikKwiatek.zasilanie, swiatlo, int(lampa1Pok1.Flaga), int(lampa1Pok1.Jasnosc), int(lampa1Pok1.Ustawienie), int(lampaTV.Flaga), int(lampaTV.Jasnosc), int(lampaPok2.Flaga), int(lampaPok2.Jasnosc), int(lampaKuch.Flaga),czujnikZew.czas,czujnikZew.blad,czujnikPok1.blad,czujnikPok2.blad)
        if(obraz==0):
            if tryb_nocny==False:
                obraz_glowny()
            else:
                obraz_nocny()

        if tryb_nocny==False and swiatlo<2:
            tryb_nocny=True
            screen.fill((0,0,0,255))
        elif tryb_nocny==True and swiatlo>5:
            tryb_nocny=False
            screen.fill(bgcolor)
        pygame.display.update()
        time.sleep(tfps)

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def NRF_SERWER():  #---- SERWER NRF - WATEK!!!!!!!!!! ------------------------------------------------------------------------------------------------------
    flaga_NRFodczytal=0
    tekst=""

    #czasAkcji=datetime.datetime.now()
    while(1):
        #--------NRF-----------------------
        radio.startListening()
        if(len(tekst)>3):
            NRFread(tekst)
        #print(datetime.datetime.now() - czasAkcji)
        while not radio.available(0):
            #time.sleep(.1)
            NRFsend()
        #czasAkcji=datetime.datetime.now()
        tekst=NRFGet()
        radio.stopListening()
        time.sleep(.001)

def ODCZYT_USTAWIEN_WATEK():  #------WATEK ODCZYTUJACY USTAWIENIA Z XML
    q=0
    while(1):
        if q>5:
            q=0
        if q==0:
            pogoda.PrognozaPogody("Rodgau") #pobranie prognozy pogody
        odczyt_ustawien_xml()
        watchdog_reset()
        time.sleep(60)
        q=q+1

def SPRAWDZENIE_TIMERA_WATEK():  #------WATEK SPRAWDZAJACY TIMER
    while(1):
        sprawdzTimer()
        sprawdzCzujniki()
        time.sleep(10)
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#-----START-------------------------------------------------------------------------------------------------------------------------------------------
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(22,GPIO.OUT)
#-------------NRF24L01-------------------------
pipesTXflag=[False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False] #Falga ustawiana gdy nadano i czeka na potwierdzenie
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

pipes = [[0x11, 0x11, 0x11, 0x11, 0x11],[0x33, 0x33, 0x33, 0x33, 0x33],[0x33, 0x33, 0x33, 0x33, 0x44],[0x33, 0x33, 0x33, 0x00, 0x55],[0x33, 0x33, 0x33, 0x00, 0x66],[0x33, 0x33, 0x33, 0x33, 0x77],[0x33, 0x33, 0x33, 0x33, 0x09],[0x33, 0x33, 0x33, 0x33, 0x10],[0x33, 0x33, 0x33, 0x33, 0x11],[0x33, 0x33, 0x33, 0x11, 0x22],[0x33, 0x33, 0x33, 0x11, 0x33],[0x33, 0x33, 0x33, 0x11, 0x44],[0x33, 0x33, 0x33, 0x11, 0x55],[0x33, 0x33, 0x33, 0x11, 0x66],[0x33, 0x33, 0x33, 0x11, 0x77],[0x33, 0x33, 0x33, 0x11, 0x88]]
radio = NRF24(GPIO, spidev.SpiDev())
radio.begin(1,25)
radio.setPayloadSize(24)
radio.setChannel(0x64)
radio.setDataRate(NRF24.BR_250KBPS)
radio.setPALevel(NRF24.PA_MIN)
radio.setAutoAck(True)
radio.openReadingPipe(1, pipes[0])
radio.openWritingPipe(1)
radio.printDetails()
radio.startListening()
#--------------UDP--------------------------
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s.bind(('', AddrOut))
s.setblocking(0)
ready=select.select([s],[],[],1)
#-------------LOGOWANIE DO TRADFRI ----------------
MACaddress='44:91:60:2c:b3:6f'          # ADRES MAC BRAMY
hubip='192.168.0.100' #podstawowy adres ip (gdy nie można odczytac)
securityid = "B5dyJuhKqdgfDdkA"   # HASLO BRAMY
user_id=""
security_user=""
#pobranie adresu IP z serwera
#hubip = ikea.ikea_get_ip(MACaddress)
dziennik.zapis_dziennika_zdarzen("START")
try:
    security_user, user_id =(ikea.tradfri_login(hubip, securityid))
    dziennik.zapis_dziennika_zdarzen("Ikea Tradfri -> id: {}    pass: {}".format(user_id, security_user))
except:
    dziennik.zapis_dziennika_zdarzen("Ikea Tradfri -> nie dziala")
#--------------INNE--------------------------
sql_baza.kasujstaredane()
#-------------WATKI--------------------------
t=threading.Thread(target=LCD)
t.start()
l=threading.Thread(target=jasnosc_wyswietlacza)
l.start()
n=threading.Thread(target=NRF_SERWER)
n.start()
o=threading.Thread(target=ODCZYT_USTAWIEN_WATEK)
o.start()
ti=threading.Thread(target=SPRAWDZENIE_TIMERA_WATEK)
ti.start()
dziennik.kasowanie_dziennika_zdarzen()
#--------------------------------------------
while(1):
    if ready[0]:
        server()
    ready=select.select([s],[],[],0.5)
    time.sleep(.01)
