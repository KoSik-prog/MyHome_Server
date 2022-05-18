#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        nrf_connect
# Purpose:
#
# Author:      KoSik
#
# Created:     17.05.2022
# Copyright:   (c) kosik 2022
#-------------------------------------------------------------------------------
from time import sleep
import RPi.GPIO as GPIO
import spidev

from libraries.log import *
from devicesList import *
from lib_nrf24 import NRF24
from libraries.sqlDatabase import *
from libraries.infoStrip import *

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

class NRF_CL():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    NRFtx_tablicaAdresow=[0,0,0,0,0,0,0,0,0,0]
    NRFtx_tablicaDanych=["","","","","","","","","",""]
    pipesTXflag=[False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False] #Falga ustawiana gdy nadano i czeka na potwierdzenie
    radio = NRF24(GPIO, spidev.SpiDev())
    pipes = [[0x11, 0x11, 0x11, 0x11, 0x11],[0x33, 0x33, 0x33, 0x33, 0x33],[0x33, 0x33, 0x33, 0x33, 0x44],[0x33, 0x33, 0x33, 0x00, 0x55],[0x33, 0x33, 0x33, 0x00, 0x66],[0x33, 0x33, 0x33, 0x33, 0x77],[0x33, 0x33, 0x33, 0x33, 0x09],[0x33, 0x33, 0x33, 0x33, 0x10],[0x33, 0x33, 0x33, 0x33, 0x11],[0x33, 0x33, 0x33, 0x11, 0x22],[0x33, 0x33, 0x33, 0x11, 0x33],[0x33, 0x33, 0x33, 0x11, 0x44],[0x33, 0x33, 0x33, 0x11, 0x55],[0x33, 0x33, 0x33, 0x11, 0x66],[0x33, 0x33, 0x33, 0x11, 0x77],[0x33, 0x33, 0x33, 0x11, 0x88]]

    def __init__(self):
        self.radio.begin(1,25)
        self.radio.setPayloadSize(24)
        self.radio.setChannel(0x64)
        self.radio.setDataRate(NRF24.BR_250KBPS)
        self.radio.setPALevel(NRF24.PA_MIN)
        self.radio.setAutoAck(True)
        self.radio.openReadingPipe(1, self.pipes[0])
        self.radio.openWritingPipe(1)
        self.radio.printDetails()
        self.radio.startListening()

    def server(self):  #---- SERWER NRF - WATEK!!!!!!!!!! ------------------------------------------------------------------------------------------------------
        flaga_NRFodczytal=0
        tekst=""

        #czasAkcji=datetime.datetime.now()
        while(1):
            #--------NRF-----------------------
            self.radio.startListening()
            if(len(tekst)>3):
                self.NRFread(tekst)
            #print(datetime.datetime.now() - czasAkcji)
            while not self.radio.available(0):
                #time.sleep(.1)
                self.NRFsend()
            #czasAkcji=datetime.datetime.now()
            tekst= self.NRFGet()
            self.radio.stopListening()
            time.sleep(.001)

    def NRFwyslij(self, adres, dane):
        w=0
        self.pipesTXflag[adres]=True
        while(w<2):
            self.NRFwyslij2(adres, dane)
            sleep(2)
            w=w+1
            if(self.pipesTXflag[adres]==False):
                break
        self.pipesTXflag[adres]=False

    def NRFwyslij2(self, adres, wartosc):
        for q in range(10):
            if self.NRFtx_tablicaAdresow[q]==0:
                self.NRFtx_tablicaAdresow[q]=adres
                self.NRFtx_tablicaDanych[q]=wartosc
                break

    def NRFsend(self):
        if self.NRFtx_tablicaAdresow[0]!=0:
            if(self.NRFtx_tablicaAdresow[0]==2 or self.NRFtx_tablicaAdresow[0]==4):
                self.radio.setPALevel(NRF24.PA_MAX)
            else:
                self.radio.setPALevel(NRF24.PA_MIN)
            self.radio.openWritingPipe(self.pipes[self.NRFtx_tablicaAdresow[0]])
            time.sleep(.1)
            self.NRFtransmit(self.NRFtx_tablicaDanych[0])
            for q in range(9):
                self.NRFtx_tablicaAdresow[q]=self.NRFtx_tablicaAdresow[q+1]
                self.NRFtx_tablicaDanych[q]=self.NRFtx_tablicaDanych[q+1]
            self.NRFtx_tablicaAdresow[9]=0
            self.NRFtx_tablicaDanych[9]=""

    def NRFtransmit(self, dane):
        self.radio.stopListening()
        message = list(dane)
        self.radio.write(message)
        self.radio.startListening()
        while len(message) < 32:
            message.append(0)

    def NRFGet(self):
        receivedMessage = ['','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','']
        stringNRF = ""
        self.radio.read(receivedMessage, self.radio.getDynamicPayloadSize())
        for n in receivedMessage:
            if(n>=16 and n <=126):
                stringNRF +=chr(n)
        log.add_log(("-----> ODEBRANO: {}".format(stringNRF)))
        return stringNRF

    def NRFread(self, stringNRF):
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
                        sql.addRecordWateringCan(czujnikKwiatek.wilgotnosc, czujnikKwiatek.slonce, czujnikKwiatek.woda, czujnikKwiatek.zasilanie, 0, 0) #ostatni parametr to podlanie poprawic!!!
                        czujnikKwiatek.czas=datetime.datetime.now() #zapisanie czasu ostatniego odbioru
                        infoStrip.set_error(3,False)
                        if(czujnikKwiatek.woda < 10):
                            infoStrip.set_error(20,False)
                        log.add_log(("   Kwiatek Slonce: {}%".format(string2)) +("   Wilg: {}%".format(string3)) +("   Woda: {}x10ml".format(string4)) +("   Zas: {}%".format(string5)))
                    if stringNRF[3]== "P":
                        sql.addRecordFlowerPodlanie()
                        log.add_log("   Podlanie")
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
                        sql.addRecordSensorTemp(czujnikPok2.sqlRoom, czujnikPok2.temp,czujnikPok2.humi)
                        czujnikPok2.czas=datetime.datetime.now() #zapisanie czasu ostatniego odbioru
                        czujnikPok2.blad=False #kasowanie bledu
                        infoStrip.set_error(2,False)
                        log.add_log(("   Sensor3 czujnikPok2.temp: {}*C".format(string2)) + ("   Wilg3: {}%".format(string3)))
                    if stringNRF[3]== "?":
                        string2=(stringNRF[4:7])
                        lampaPok2.Jasnosc=int(string2)
                        if(lampaPok2.Jasnosc==0):
                            lampaPok2.Flaga=0
                        else:
                            lampaPok2.Flaga=1
                        lampaPok2.FlagaSterowanieManualne=True
                        self.pipesTXflag[2]=False
                        lampaPok2.blad=0
                        log.add_log(("   Led Sypialni ON/OFF:{}".format(lampaPok2.Flaga)) + ("   PWM:{}".format(lampaPok2.Jasnosc)))
                #------------------------------------------------------------------------------------------------------------
                if stringNRF[1:3]=="03":  #czujnik  zewnetrzny
                    if stringNRF[3]== "s":
                        string1=(stringNRF[4:9])
                        czujnikZew.lux=int(string1)
                        string2=(stringNRF[9:14])
                        czujnikZew.ir=int(string2)
                        string3=(stringNRF[14:18])
                        czujnikZew.batt=int(string3)
                        sql.addRecordSensorOutdoorLight(czujnikZew.lux,czujnikZew.ir)
                        self.oblicz_swiatlo()
                        log.add_log("Obliczylem, ze swiatlo wynosci: {}".format(automatykaOswietlenia.swiatloObliczone))
                        log.add_log("   Sensor1 zewnetrzny ->   Lux: {}    LuxIR: {}    Bateria: {}".format(czujnikZew.lux,czujnikZew.ir,czujnikZew.batt))
                    if stringNRF[3]== "t":
                        if(stringNRF[4]=="1"):
                            string2=('-'+stringNRF[5:7]+"."+stringNRF[7])
                        else:
                            string2=(stringNRF[5:7]+"."+stringNRF[7])
                        czujnikZew.temp=float(string2)
                        string3=(stringNRF[8:10]+"."+stringNRF[10])
                        czujnikZew.humi=float(string3)
                        sql.add_record_sensor_outdoor_temp(czujnikZew.temp,czujnikZew.humi,czujnikZew.predkoscWiatru,czujnikZew.kierunekWiatru)
                        string4=stringNRF[11:13]+'.'+stringNRF[13]
                        czujnikZew.predkoscWiatru=float(string4)
                        string5=stringNRF[14:17]
                        czujnikZew.kierunekWiatru=int(string5)
                        czujnikZew.czas=datetime.datetime.now() #zapisanie czasu ostatniego odbioru
                        czujnikZew.blad=False #kasowanie bledu
                        infoStrip.set_error(0,False)
                        log.add_log("   Sensor1 zewnetrzny Temp: {}*C   Wilg: {}%   Wiatr: {}m/s   Kier:{}".format(czujnikZew.temp, czujnikZew.humi, czujnikZew.predkoscWiatru, czujnikZew.kierunekWiatru))
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
                        sql.addRecordSensorTemp(czujnikPok1.sqlRoom, czujnikPok1.temp,czujnikPok1.humi)
                        string4=(stringNRF[11:14])
                        czujnikPok1.batt=int(string4)
                        czujnikPok1.czas=datetime.datetime.now() #zapisanie czasu ostatniego odbioru
                        czujnikPok1.blad=False #kasowanie bledu
                        infoStrip.set_error(1,False)
                        log.add_log(("   Sensor2 czujnikPok1.temp: {}*C".format(string2)) +("   Wilg2: {}%".format(string3)) +("   Batt: {}".format(string4)))
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
                        self.pipesTXflag[1]=False
                        lampaTV.blad=0
                        log.add_log(("   Led TV ON/OFF:{}".format(lampaTV.Flaga)) + ("   Jasnosc:{}".format(lampaTV.Jasnosc)))
    #------------------------------------------------------------------------------------------------------------
                if stringNRF[1:3]== "06":  #LED LAMPA
                    if stringNRF[3]== "?":
                        string2=(stringNRF[13:16])
                        if(int(string2)==0):
                            lampa1Pok1.Flaga=0
                        else:
                            lampa1Pok1.Flaga=1
                        #lampa1Pok1.Jasnosc=int(string2)
                        self.pipesTXflag[3]=False
                        lampa1Pok1.blad=0
                        log.add_log(("   Led lampa ON/OFF:{}".format(lampa1Pok1.Flaga)) + ("   Jasnosc:{}".format(lampa1Pok1.Jasnosc)))
        #------------------------------------------------------------------------------------------------------------
                if stringNRF[1:3]== "07":  #LED KUCHNIA
                    if stringNRF[3]== "?":
                        if (int(stringNRF[4]) == 1 or int(stringNRF[4]) == 2):
                            lampaKuch.Flaga=1
                        else:
                            lampaKuch.Flaga=0
                        self.pipesTXflag[4]=False
                        lampaKuch.blad=0
                        log.add_log(("   Led kuchnia TRYB:{}".format(lampaKuch.Flaga)))
                #------------------------------------------------------------------------------------------------------------
                if stringNRF[1:3]== "08":  #DEKORACJE POK 1
                    if stringNRF[3]== "?":
                        dekoPok1.Flaga=int(stringNRF[4])
                        self.pipesTXflag[AdresLampa2]=False
                        dekoPok1.blad=0
                        log.add_log(("   Dekoracje Pok 1 ON/OFF:{}".format(dekoPok1.Flaga)))
                #------------------------------------------------------------------------------------------------------------
                if stringNRF[1:3]== "09":  #DEKORACJE 2 POK 1
                    if stringNRF[3]== "?":
                        deko2Pok1.Flaga=int(stringNRF[4])
                        self.pipesTXflag[AdresLampa3]=False
                        deko2Pok1.blad=0
                        log.add_log(("   Dekoracje 2 Pok 1 ON/OFF:{}".format(dekoPok1.Flaga)))
        #------------------------------------------------------------------------------------------------------------
                if stringNRF[1:3]== "10":  #FLAMING
                    if stringNRF[3]== "?":
                        dekoFlaming.Flaga=int(stringNRF[4])
                        self.pipesTXflag[AdresFlaming]=False
                        dekoFlaming.blad=0
                        log.add_log(("   Flaming ON/OFF:{}".format(dekoFlaming.Flaga)))
        #------------------------------------------------------------------------------------------------------------
                if stringNRF[1:3]== "11":  #Uniwersalny modul USB
                    if stringNRF[3]== "?":
                        dekoUsb.Flaga=int(stringNRF[4])
                        self.pipesTXflag[AdresUsb]=False
                        dekoUsb.blad=0
                        log.add_log(("   Uniwersalny USB ON/OFF:{}".format(dekoUsb.Flaga)))
        #------------------------------------------------------------------------------------------------------------
                if stringNRF[1:3]== "18":  #Hydroponika
                    if stringNRF[3]== "?":
                        hydroponika.Flaga=int(stringNRF[4])
                        self.pipesTXflag[hydroponika.Adres]=False
                        hydroponika.blad=0
                        log.add_log(("   Hydroponika ON/OFF:{}".format(hydroponika.Flaga)))
    #------------------------------------------------------------------------------------------------------------
                if stringNRF[1:3]== "12":  #kwiatek 2  addres 12
                    if stringNRF[3]== "k":
                        string2=(stringNRF[4:7])
                        czujnikKwiatek2.slonce=int(string2)
                        #string3=(stringNRF[7:10])
                        string5=(stringNRF[14:17])
                        czujnikKwiatek2.wilgotnosc_raw=string5
                        string3 = self.obliczFunkcje(czujnikKwiatek2.wartoscMin, czujnikKwiatek2.wartoscMax, int((stringNRF[14:17])))
                        czujnikKwiatek2.wilgotnosc=int(string3)
                        string4=(stringNRF[10]+"."+stringNRF[11:13])
                        czujnikKwiatek2.zasilanie=str(string4)
                        sql.addRecordFlower(2, czujnikKwiatek2.wilgotnosc,czujnikKwiatek2.slonce,czujnikKwiatek2.zasilanie,czujnikKwiatek2.wilgotnosc_raw)
                        czujnikKwiatek2.czas=datetime.datetime.now() #zapisanie czasu ostatniego odbioru
                        infoStrip.set_error(4,False)
                        log.add_log(("   Kwiatek 12 Slonce: {}%   Wilg: {}%   Zas: {}V".format(string2,string3,string4)))
    #------------------------------------------------------------------------------------------------------------
                if stringNRF[1:3]== "13":  #kwiatek 3 adres 13
                    if stringNRF[3]== "k":
                        string2=(stringNRF[4:7])
                        czujnikKwiatek3.slonce=int(string2)
                        #string3=(stringNRF[7:10])
                        string5=(stringNRF[14:17])
                        czujnikKwiatek3.wilgotnosc_raw=string5
                        string3 = self.obliczFunkcje(czujnikKwiatek3.wartoscMin, czujnikKwiatek3.wartoscMax, int((stringNRF[14:17])))
                        czujnikKwiatek3.wilgotnosc=int(string3)
                        string4=(stringNRF[10]+"."+stringNRF[11:13])
                        czujnikKwiatek3.zasilanie=str(string4)
                        sql.addRecordFlower(3, czujnikKwiatek3.wilgotnosc,czujnikKwiatek3.slonce,czujnikKwiatek3.zasilanie, czujnikKwiatek3.wilgotnosc_raw)
                        czujnikKwiatek3.czas=datetime.datetime.now() #zapisanie czasu ostatniego odbioru
                        infoStrip.set_error(5,False)
                        log.add_log(("   Kwiatek 13 Slonce: {}%   Wilg: {}%   Zas: {}V".format(string2,string3,string4)))
    #------------------------------------------------------------------------------------------------------------
                if stringNRF[1:3]== "14":  #kwiatek 4 adres 14
                    if stringNRF[3]== "k":
                        string2=(stringNRF[4:7])
                        czujnikKwiatek4.slonce=int(string2)
                        #string3=(stringNRF[7:10])
                        string5=(stringNRF[14:17])
                        czujnikKwiatek4.wilgotnosc_raw=int(string5)
                        string3 = self.obliczFunkcje(czujnikKwiatek4.wartoscMin, czujnikKwiatek4.wartoscMax, czujnikKwiatek4.wilgotnosc_raw)
                        czujnikKwiatek4.wilgotnosc=int(string3)
                        string4=(stringNRF[10]+"."+stringNRF[11:13])
                        czujnikKwiatek4.zasilanie=str(string4)
                        sql.addRecordFlower(4, czujnikKwiatek4.wilgotnosc,czujnikKwiatek4.slonce,czujnikKwiatek4.zasilanie, czujnikKwiatek4.wilgotnosc_raw)
                        czujnikKwiatek4.czas=datetime.datetime.now() #zapisanie czasu ostatniego odbioru
                        infoStrip.set_error(6,False)
                        log.add_log(("   Kwiatek 14 Slonce: {}%   Wilg: {}%   Zas: {}V".format(string2,string3,string4)))
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
                        log.add_log(("   Buda t.wew: {}   t.ciepla: {}  t.zimna: {}   f:{}   cz:{}".format(buda.temp1,buda.temp2,buda.temp3,buda.czujnikZajetosciFlaga, buda.czujnikZajetosciRaw)))
    #------------------------------------------------------------------------------------------------------------
                if stringNRF[1:3]== "16":  #kwiatek 5 adres 16
                    if stringNRF[3]== "k":
                        string2=(stringNRF[4:7])
                        czujnikKwiatek5.slonce=int(string2)
                        string5=(stringNRF[14:17])
                        czujnikKwiatek5.wilgotnosc_raw=int(string5)
                        string3 = self.obliczFunkcje(czujnikKwiatek5.wartoscMin, czujnikKwiatek5.wartoscMax, czujnikKwiatek5.wilgotnosc_raw)
                        czujnikKwiatek5.wilgotnosc=int(string3)
                        string4=(stringNRF[10]+"."+stringNRF[11:13])
                        czujnikKwiatek5.zasilanie=str(string4)
                        sql.addRecordFlower(5, czujnikKwiatek5.wilgotnosc,czujnikKwiatek5.slonce,czujnikKwiatek5.zasilanie, czujnikKwiatek5.wilgotnosc_raw)
                        czujnikKwiatek5.czas=datetime.datetime.now() #zapisanie czasu ostatniego odbioru
                        infoStrip.set_error(16,False)
                        log.add_log(("   Kwiatek 16 Slonce: {}%   Wilg: {}%   Zas: {}V".format(string2,string3,string4)))
    #------------------------------------------------------------------------------------------------------------
                if stringNRF[1:3]== "17":  #kwiatek 6 adres 17
                    if stringNRF[3]== "k":
                        string2=(stringNRF[4:7])
                        czujnikKwiatek6.slonce=int(string2)
                        string5=(stringNRF[14:17])
                        czujnikKwiatek6.wilgotnosc_raw=int(string5)
                        string3 = self.obliczFunkcje(czujnikKwiatek6.wartoscMin, czujnikKwiatek6.wartoscMax, czujnikKwiatek6.wilgotnosc_raw)
                        czujnikKwiatek6.wilgotnosc=int(string3)
                        string4=(stringNRF[10]+"."+stringNRF[11:13])
                        czujnikKwiatek6.zasilanie=str(string4)
                        sql.addRecordFlower(6, czujnikKwiatek6.wilgotnosc,czujnikKwiatek6.slonce,czujnikKwiatek6.zasilanie, czujnikKwiatek6.wilgotnosc_raw)
                        czujnikKwiatek6.czas=datetime.datetime.now() #zapisanie czasu ostatniego odbioru
                        infoStrip.set_error(19,False)
                        log.add_log(("   Kwiatek 17 Slonce: {}%   Wilg: {}%   Zas: {}V".format(string2,string3,string4)))
    #------------------------------------------------------------------------------------------------------------
                if stringNRF[1:3]== "99":  #testowy
                    if stringNRF[3]== ".":
                            int1 = ''.join(str(chr(e)) for e in stringNRF[4:8])
                            int2 = ''.join(str(chr(e)) for e in stringNRF[9:])
                            fl1=(float(int1)/1000)
                            log.add_stuff_log('zasilanie: {:.3f}V  -> wilgotnosc: {}'.format(fl1,int2))

    def oblicz_swiatlo(self):
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
        log.add_log("Swiatlo obliczone=  {}".format(automatykaOswietlenia.swiatloObliczone) + " / {}".format(automatykaOswietlenia.wartosciLux))

    def obliczFunkcje(self, wartoscMin, wartoscMax, pomiar):
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
nrf = NRF_CL()