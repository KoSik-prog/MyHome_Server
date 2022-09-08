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

from sensorFlower import *
from sensorOutside import *
from deviceWaterCan import *
from lib.log import *
from devicesList import *
from lib.lib_nrf24 import NRF24
from lib.sqlDatabase import *
from lib.infoStrip import *

class Nrf():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    radio = NRF24(GPIO, spidev.SpiDev())

    '''txBuffer -> transmit buffer [address, tx_power(PA_LEVEL), message]'''
    txBuffer = [ [[], 1, ""], [[], 1, ""], [[], 1, ""], [[], 1, ""], [[], 1, ""], [[], 1, ""], [[], 1, ""], [[], 1, ""], [[], 1, ""], [[], 1, ""]]

    def __init__(self, rxAddress):
        self.radio.begin(1,25)
        self.radio.setPayloadSize(24)
        self.radio.setChannel(0x64)
        self.radio.setDataRate(NRF24.BR_250KBPS)
        self.radio.setPALevel(NRF24.PA_LOW)
        self.radio.setAutoAck(True)
        self.radio.openReadingPipe(1, rxAddress)
        self.radio.openWritingPipe(1)
        self.radio.printDetails()
        self.radio.startListening()

    def nrf24l01_thread(self):
        rxBuffer = ""
        while server.read_server_active_flag() == True:
            self.radio.startListening()
            if len(rxBuffer) > 3:
                self.decode_message(rxBuffer)
            while not self.radio.available(0):
                self.send()
            rxBuffer = self.get_message()
            self.radio.stopListening()
            time.sleep(.001)

    def to_send(self, address, data, txPower):
        for i in range(len(Nrf.txBuffer)):
            if(Nrf.txBuffer[i][2] == ""):
                Nrf.txBuffer[i][0] = address
                Nrf.txBuffer[i][1] = txPower
                Nrf.txBuffer[i][2] = data
                break

    def send(self):
        if Nrf.txBuffer[0][2] != "":
            self.radio.openWritingPipe(Nrf.txBuffer[0][0])
            self.radio.setPALevel(Nrf.txBuffer[0][2]) #zmiana mocy nadawania
            time.sleep(.01)
            print("NRF addr: {} / power: {} / send: {}".format(Nrf.txBuffer[0][0], Nrf.txBuffer[0][1], Nrf.txBuffer[0][2]))
            self.transmit(Nrf.txBuffer[0][2])
        for i in range(len(Nrf.txBuffer) - 1):
            Nrf.txBuffer[i] = Nrf.txBuffer[i+1]
        Nrf.txBuffer[len(Nrf.txBuffer) - 1] = [ [], 1, "" ]

    def transmit(self, data):
        self.radio.stopListening()
        message = list(data)
        self.radio.write(message)
        self.radio.startListening()
        while len(message) < 32:
            message.append(0)

    def get_message(self):
        receivedMessage = ['','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','']
        stringNRF = ""
        self.radio.read(receivedMessage, self.radio.getDynamicPayloadSize())
        for n in receivedMessage:
            if(n>=16 and n <=126):
                stringNRF +=chr(n)
        if stringNRF != "":
                log.add_log(("-----> ODEBRANO: {}".format(stringNRF)))
        return stringNRF

    def decode_message(self, stringNRF):
        if len(stringNRF)!=0:
            if stringNRF[0]== "#": # '#' - poczatek transmisji
                flaga_NRFOdebral=0
                #------------------------------------------------------------------------------------------------------------
                if stringNRF[1:3]=="02":  #czujnik temperatury 3 - sypialni
                    if stringNRF[3]== "y":
                        string2=(stringNRF[4:6]+"."+stringNRF[6])
                        if(len(stringNRF)>9):
                            string3=(stringNRF[7:10])
                        else:
                            string3=(stringNRF[7:9]+'.0')
                        sensorRoom2Temperature.temp=float(string2)
                        sensorRoom2Temperature.humi=float(string3)
                        sql.add_record_sensor_temp(sensorRoom2Temperature.sqlRoom, sensorRoom2Temperature.temp,sensorRoom2Temperature.humi)
                        sensorRoom2Temperature.time = datetime.datetime.now() #zapisanie czasu ostatniego odbioru
                        sensorRoom2Temperature.error=False #kasowanie bledu
                        infoStrip.set_error(2,False)
                        log.add_log(("   Sensor3 sensorRoom2Temperature.temp: {}*C".format(string2)) + ("   Wilg3: {}%".format(string3)))
                    if stringNRF[3]== "?":
                        string2=(stringNRF[4:7])
                        ledLightRoom2.brightness=int(string2)
                        if(ledLightRoom2.brightness==0):
                            ledLightRoom2.flag=0
                        else:
                            ledLightRoom2.flag=1
                        ledLightRoom2.flagManualControl=True
                        ledLightRoom2.error=0
                        log.add_log(("   Led Sypialni ON/OFF:{}".format(ledLightRoom2.flag)) + ("   PWM:{}".format(ledLightRoom2.brightness)))
                #------------------------------------------------------------------------------------------------------------
                if stringNRF[1:3]=="03":  #czujnik  zewnetrzny
                    sensorOutside.add_record(stringNRF)
                    """if stringNRF[3]== "s":
                        string1=(stringNRF[4:9])
                        sensorOutside.light=int(string1)
                        string2=(stringNRF[9:14])
                        sensorOutside.ir=int(string2)
                        string3=(stringNRF[14:18])
                        sensorOutside.power=int(string3)
                        sql.add_record_sensor_outdoor_light(sensorOutside.light,sensorOutside.ir)
                        self.calculate_light_value()
                        log.add_log("Obliczylem, ze swiatlo wynosci: {}".format(lightingAutomation.calculatedBrightness))
                        log.add_log("   Sensor1 zewnetrzny ->   Lux: {}    LuxIR: {}    Bateria: {}".format(sensorOutside.light,sensorOutside.ir,sensorOutside.power))
                    if stringNRF[3]== "t":
                        if(stringNRF[4]=="1"):
                            string2=('-'+stringNRF[5:7]+"."+stringNRF[7])
                        else:
                            string2=(stringNRF[5:7]+"."+stringNRF[7])
                        sensorOutside.temperature=float(string2)
                        string3=(stringNRF[8:10]+"."+stringNRF[10])
                        sensorOutside.humidity=float(string3)
                        sql.add_record_sensor_outdoor_temp(sensorOutside.temperature,sensorOutside.humidity,sensorOutside.windSpeed,sensorOutside.windDirection)
                        string4=stringNRF[11:13]+'.'+stringNRF[13]
                        sensorOutside.windSpeed=float(string4)
                        string5=stringNRF[14:17]
                        sensorOutside.windDirection=int(string5)
                        sensorOutside.time=datetime.datetime.now() #zapisanie czasu ostatniego odbioru
                        sensorOutside.errorFlag=False #kasowanie bledu
                        infoStrip.set_error(0,False)
                        log.add_log("   Sensor1 zewnetrzny Temp: {}*C   Wilg: {}%   Wiatr: {}m/s   Kier:{}".format(sensorOutside.temperature, sensorOutside.humidity, sensorOutside.windSpeed, sensorOutside.windDirection))
                    """
                #------------------------------------------------------------------------------------------------------------
                if stringNRF[1:3]=="04":  #czujnik temperatury 2 - pokoju
                    if stringNRF[3]== "t":
                        if(stringNRF[4]=="1"):
                            string2=('-'+stringNRF[5:7]+'.'+stringNRF[7])
                        else:
                            string2=(stringNRF[5:7]+'.'+stringNRF[7])
                        sensorRoom1Temperature.temp=float(string2)
                        string3=(stringNRF[8:10]+'.'+stringNRF[10])
                        sensorRoom1Temperature.humi=float(string3)
                        sql.add_record_sensor_temp(sensorRoom1Temperature.sqlRoom, sensorRoom1Temperature.temp,sensorRoom1Temperature.humi)
                        string4=(stringNRF[11:14])
                        sensorRoom1Temperature.batt=int(string4)
                        sensorRoom1Temperature.time = datetime.datetime.now() #zapisanie czasu ostatniego odbioru
                        sensorRoom1Temperature.error=False #kasowanie bledu
                        infoStrip.set_error(1,False)
                        log.add_log(("   Sensor2 sensorRoom1Temperature.temp: {}*C".format(string2)) +("   Wilg2: {}%".format(string3)) +("   Batt: {}".format(string4)))
                #------------------------------------------------------------------------------------------------------------
                if stringNRF[1:3]== "05":  #LED - tv
                    if stringNRF[3]== "?":
                        string2=(stringNRF[13:16])
                        if(int(string2)==0):
                            ledStripRoom1.flag=0
                        else:
                            ledStripRoom1.flag=1
                        if int(string2)>0:
                            ledStripRoom1.brightness=int(string2)
                        ledStripRoom1.error=0
                        log.add_log(("   Led TV ON/OFF:{}".format(ledStripRoom1.flag)) + ("   Jasnosc:{}".format(ledStripRoom1.brightness)))
    #------------------------------------------------------------------------------------------------------------
                if stringNRF[1:3]== "06":  #LED LAMPA
                    if stringNRF[3]== "?":
                        string2=(stringNRF[13:16])
                        if(int(string2)==0):
                            spootLightRoom1.flag=0
                        else:
                            spootLightRoom1.flag=1
                        #spootLightRoom1.brightness=int(string2)
                        spootLightRoom1.error=0
                        log.add_log(("   Led lampa ON/OFF:{}".format(spootLightRoom1.flag)) + ("   Jasnosc:{}".format(spootLightRoom1.brightness)))
        #------------------------------------------------------------------------------------------------------------
                if stringNRF[1:3]== "07":  #LED KUCHNIA
                    if stringNRF[3]== "?":
                        if (int(stringNRF[4]) == 1 or int(stringNRF[4]) == 2):
                            kitchenLight.flag=1
                        else:
                            kitchenLight.flag=0
                        kitchenLight.error=0
                        log.add_log(("   Led kuchnia TRYB:{}".format(kitchenLight.flag)))
                #------------------------------------------------------------------------------------------------------------
                if stringNRF[1:3]== "08":  #DEKORACJE POK 1
                    if stringNRF[3]== "?":
                        decorationRoom1.flag=int(stringNRF[4])
                        decorationRoom1.error=0
                        log.add_log(("   Dekoracje Pok 1 ON/OFF:{}".format(decorationRoom1.flag)))
                #------------------------------------------------------------------------------------------------------------
                if stringNRF[1:3]== "09":  #DEKORACJE 2 POK 1
                    if stringNRF[3]== "?":
                        decoration2Room1.flag=int(stringNRF[4])
                        decoration2Room1.error=0
                        log.add_log(("   Dekoracje 2 Pok 1 ON/OFF:{}".format(decorationRoom1.flag)))
        #------------------------------------------------------------------------------------------------------------
                if stringNRF[1:3]== "10":  #FLAMING
                    if stringNRF[3]== "?":
                        decorationFlamingo.flag=int(stringNRF[4])
                        decorationFlamingo.error=0
                        log.add_log(("   Flaming ON/OFF:{}".format(decorationFlamingo.flag)))
        #------------------------------------------------------------------------------------------------------------
                if stringNRF[1:3]== "11":  #Uniwersalny modul USB
                    if stringNRF[3]== "?":
                        usbPlug.flag=int(stringNRF[4])
                        usbPlug.error=0
                        log.add_log(("   Uniwersalny USB ON/OFF:{}".format(usbPlug.flag)))
        #------------------------------------------------------------------------------------------------------------
                if stringNRF[1:3]== "18":  #hyroponics
                    if stringNRF[3]== "?":
                        hyroponics.flag=int(stringNRF[4])
                        hyroponics.error=0
                        log.add_log(("   hyroponics ON/OFF:{}".format(hyroponics.flag)))
    #------------------------------------------------------------------------------------------------------------
                if stringNRF[1:3]== "12":  #kwiatek 2  addres 12
                    sensorFlower2.add_record(stringNRF)
                    infoStrip.set_error(4,False)  # poprawic - przeniesc do klasy urzadzenia
    #------------------------------------------------------------------------------------------------------------
                if stringNRF[1:3]== "13":  #kwiatek 3 adres 13
                    sensorFlower3.add_record(stringNRF)
                    infoStrip.set_error(5,False)
    #------------------------------------------------------------------------------------------------------------
                if stringNRF[1:3]== "14":  #kwiatek 4 adres 14
                    sensorFlower4.add_record(stringNRF)
                    infoStrip.set_error(6,False)
    #------------------------------------------------------------------------------------------------------------
                if stringNRF[1:3]== "16":  #kwiatek 5 adres 16
                    sensorFlower5.add_record(stringNRF)
                    infoStrip.set_error(16,False)
    #------------------------------------------------------------------------------------------------------------
                if stringNRF[1:3]== "17":  #kwiatek 6 adres 17
                    sensorFlower6.add_record(stringNRF)
                    infoStrip.set_error(19,False)
    #------------------------------------------------------------------------------------------------------------
                if stringNRF[1:3]== "15":  #dogHouse 15
                    if stringNRF[3]== "s":
                        string2=(stringNRF[4:7])
                        dogHouse.temp1=float(string2)/10
                        string5=(stringNRF[7:10])
                        dogHouse.temp2=float(string5)/10
                        string6=(stringNRF[10:13])
                        dogHouse.temp3=float(string6)/10
                        string7=(stringNRF[13])
                        dogHouse.czujnikZajetosciflaga=int(string7)
                        string8=(stringNRF[14:16])
                        dogHouse.czujnikZajetosciRaw=int(string8)
                        dogHouse.time=datetime.datetime.now() #zapisanie czasu ostatniego odbioru
                        log.add_log(("   dogHouse t.wew: {}   t.ciepla: {}  t.zimna: {}   f:{}   cz:{}".format(dogHouse.temp1,dogHouse.temp2,dogHouse.temp3,dogHouse.czujnikZajetosciflaga, dogHouse.czujnikZajetosciRaw)))
    #------------------------------------------------------------------------------------------------------------
                if stringNRF[1:3]== "99":  #test module
                    if stringNRF[3]== ".":
                            int1 = ''.join(str(chr(e)) for e in stringNRF[4:8])
                            int2 = ''.join(str(chr(e)) for e in stringNRF[9:])
                            fl1=(float(int1)/1000)
                            log.add_log('power: {:.3f}V  -> humidity: {}'.format(fl1,int2))

    """def calculate_light_value(self):
        k=3 #wzmocnienie
        for i in range(4):
            lightingAutomation.LUXvalue[i]=lightingAutomation.LUXvalue[i+1]
        lightingAutomation.LUXvalue[4]=sensorOutside.light
        lightingAutomation.calculatedBrightness=lightingAutomation.LUXvalue[0]
        for i in range(4):
            lightingAutomation.calculatedBrightness=lightingAutomation.calculatedBrightness+lightingAutomation.LUXvalue[i+1]
        lightingAutomation.calculatedBrightness=(lightingAutomation.calculatedBrightness+((lightingAutomation.LUXvalue[4]*k)))/(5+k)
        if lightingAutomation.calculatedBrightness<sensorOutside.nightSetting:
            sensorOutside.nightFlag=True
        else:
            sensorOutside.nightFlag=False
        log.add_log("Swiatlo obliczone=  {}".format(lightingAutomation.calculatedBrightness) + " / {}".format(lightingAutomation.LUXvalue))"""


nrf = Nrf([0x11, 0x11, 0x11, 0x11, 0x11])