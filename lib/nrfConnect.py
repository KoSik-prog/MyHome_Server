#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:        nrf_connect
# Purpose:
#
# Author:      KoSik
#
# Created:     17.05.2022
# Copyright:   (c) kosik 2022
# -------------------------------------------------------------------------------
# try:
from time import sleep
import RPi.GPIO as GPIO
import spidev
from sensorFlower import *
from .sensorOutside import *
from deviceWaterCan import *
from lib.log import *
from devicesList import *
from .lib_nrf24 import NRF24
from lib.sqlDatabase import *
from lib.infoStrip import *
# except ImportError:
#     print("Import error - nrf connect")


class Nrf():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    radio = NRF24(GPIO, spidev.SpiDev())

    '''txBuffer -> transmit buffer [address, tx_power(PA_LEVEL), message]'''
    txBuffer = [[[], 1, ""], [[], 1, ""], [[], 1, ""], [[], 1, ""], [[], 1, ""],
                [[], 1, ""], [[], 1, ""], [[], 1, ""], [[], 1, ""], [[], 1, ""]]

    def __init__(self, rxAddress):
        self.radio.begin(1, 25)
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
            self.radio.setPALevel(Nrf.txBuffer[0][2])  # zmiana mocy nadawania
            time.sleep(.01)
            log.add_log("NRF addr: {} / power: {} / send: {}".format(Nrf.txBuffer[0][0], Nrf.txBuffer[0][1], Nrf.txBuffer[0][2]))
            self.transmit(Nrf.txBuffer[0][2])
        for i in range(len(Nrf.txBuffer) - 1):
            Nrf.txBuffer[i] = Nrf.txBuffer[i+1]
        Nrf.txBuffer[len(Nrf.txBuffer) - 1] = [[], 1, ""]

    def transmit(self, data):
        self.radio.stopListening()
        message = list(data)
        self.radio.write(message)
        self.radio.startListening()
        while len(message) < 32:
            message.append(0)

    def get_message(self):
        receivedMessage = ['', '', '', '', '', '', '', '', '', '', '', '', '', '',
                           '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']
        stringNRF = ""
        self.radio.read(receivedMessage, self.radio.getDynamicPayloadSize())
        for n in receivedMessage:
            if(n >= 16 and n <= 126):
                stringNRF += chr(n)
        if stringNRF != "":
            log.add_log(("-----> ODEBRANO: {}".format(stringNRF)))
        return stringNRF

    def decode_message(self, stringNRF):
        if len(stringNRF) != 0:
            if stringNRF[0] == "#":  # '#' - poczatek transmisji
                flaga_NRFOdebral = 0
                # ------------------------------------------------------------------------------------------------------------
                if stringNRF[1:3] == "02":  # czujnik temperatury 3 - sypialni
                    if stringNRF[3] == "t":
                        sensorRoom2Temperature.decode_data(stringNRF)
                    if stringNRF[3] == "s":
                        if stringNRF[4:7].isdigit():
                            ledPhotosHeart.set_param('brightness', int(stringNRF[4:7]))
                        else:
                            ledPhotosHeart.set_param('brightness', 0)
                        if ledPhotosHeart.get_param('brightness'):
                            ledPhotosHeart.set_param('flag', True)
                        else:
                            ledPhotosHeart.set_param('flag', False)
                        log.add_log(("   Led Heart ON/OFF:{} Jasność: {}".format(ledPhotosHeart.get_param('flag'), ledPhotosHeart.get_param('brightness'))))
                # ------------------------------------------------------------------------------------------------------------
                if stringNRF[1:3] == "03":  #outside sensor
                    sensorOutside.add_record(stringNRF)
                # ------------------------------------------------------------------------------------------------------------
                if stringNRF[1:3] == "04":  # czujnik temperatury 2 - pokoju
                    sensorRoom1Temperature.decode_data(stringNRF)
                # ------------------------------------------------------------------------------------------------------------
                if stringNRF[1:3] == "05":  # LED - tv
                    if stringNRF[3] == "?":
                        string2 = (stringNRF[13:16])
                        if(int(string2) == 0):
                            ledStripRoom1.set_param('flag', 0)
                        else:
                            ledStripRoom1.set_param('flag', 1)
                        if int(string2) > 0:
                            ledStripRoom1.set_param('brightness', int(string2))
                        ledStripRoom1.set_param('error', 0)
                        log.add_log(("   Led TV ON/OFF:{}".format(ledStripRoom1.get_param('flag'))) +
                                    ("   Jasnosc:{}".format(ledStripRoom1.get_param('brightness'))))
                # ------------------------------------------------------------------------------------------------------------
                if stringNRF[1:3] == "06":  # LED KUCHNIA
                    if stringNRF[3] == ".":
                        if (int(stringNRF[4]) == 1 or int(stringNRF[4]) == 2):
                            kitchenLight.set_param('flag', 1)
                        else:
                            kitchenLight.set_param('flag', 0)
                        kitchenLight.set_param('error', 0)
                        log.add_log(("   Led kuchnia TRYB:{}".format(kitchenLight.get_param('flag'))))
                # ------------------------------------------------------------------------------------------------------------
                if stringNRF[1:3] == "07":  # LED LAMPA
                    if stringNRF[3] == "?":
                        string2 = (stringNRF[13:16])
                        if(int(string2) == 0):
                            spootLightRoom1.set_param('flag', 0)
                        else:
                            spootLightRoom1.set_param('flag', 1)
                        # spootLightRoom1.brightness=int(string2)
                        spootLightRoom1.set_param('error', 0)
                        log.add_log(("   Led lampa ON/OFF:{}".format(spootLightRoom1.get_param('flag'))) +
                                    ("   Jasnosc:{}".format(spootLightRoom1.get_param('brightness'))))
                # ------------------------------------------------------------------------------------------------------------
                if stringNRF[1:3] == "08":  # DEKORACJE POK 1
                    if stringNRF[3] == "?":
                        decorationRoom1.set_param('flag', int(stringNRF[4]))
                        decorationRoom1.set_param('error', 0)
                        log.add_log(("   Dekoracje Pok 1 ON/OFF:{}".format(decorationRoom1.get_param('flag'))))
                # ------------------------------------------------------------------------------------------------------------
                if stringNRF[1:3] == "09":  # DEKORACJE 2 POK 1
                    if stringNRF[3] == "?":
                        decoration2Room1.set_param('flag', int(stringNRF[4]))
                        decoration2Room1.set_param('error', 0)
                        log.add_log(("   Dekoracje 2 Pok 1 ON/OFF:{}".format(decorationRoom1.get_param('flag'))))
                # ------------------------------------------------------------------------------------------------------------
                if stringNRF[1:3] == "10":  # FLAMING
                    if stringNRF[3] == "?":
                        decorationFlamingo.set_param('flag', int(stringNRF[4]))
                        decorationFlamingo.set_param('error', 0)
                        log.add_log(("   Flaming ON/OFF:{}".format(decorationFlamingo.get_param('flag'))))
                # ------------------------------------------------------------------------------------------------------------
                if stringNRF[1:3] == "11":  # Uniwersalny modul USB
                    if stringNRF[3] == "?":
                        usbPlug.set_param('flag', int(stringNRF[4]))
                        usbPlug.set_param('error', 0)
                        log.add_log(("   USB Wtyk ON/OFF:{}".format(usbPlug.get_param('flag'))))
                # ------------------------------------------------------------------------------------------------------------
                if stringNRF[1:3] == "18":  # hydroponics
                    if stringNRF[3] == "?":
                        hydroponics.set_param('flag', int(stringNRF[4]))
                        hydroponics.set_param('error', 0)
                        log.add_log(("   hydroponics ON/OFF:{}".format(hydroponics.get_param('flag'))))
                # ------------------------------------------------------------------------------------------------------------
                if stringNRF[1:3] == "19":  # desk light
                    if stringNRF[3] == "?":
                        if stringNRF[4:7].isdigit():
                            ledDeskRoom3.set_param('brightness', int(stringNRF[4:7]))
                        else:
                            ledDeskRoom3.set_param('brightness', 0)
                        if ledDeskRoom3.get_param('brightness'):
                            ledDeskRoom3.set_param('flag', True)
                        else:
                            ledDeskRoom3.set_param('flag', False)
                        log.add_log(("   Desk LED ON/OFF:{} Jasność: {}".format(ledDeskRoom3.get_param('flag'), ledDeskRoom3.get_param('brightness'))))
                # ------------------------------------------------------------------------------------------------------------
                if stringNRF[1:3] == "20":  # lego light
                    if stringNRF[3] == "?":
                        if stringNRF[4:7].isdigit():
                            ledLego.set_param('brightness', int(stringNRF[4:7]))
                        else:
                            ledLego.set_param('brightness', 0)
                        if ledLego.get_param('brightness'):
                            ledLego.set_param('flag', True)
                        else:
                            ledLego.set_param('flag', False)
                        log.add_log(("   LEGO LED ON/OFF:{} Jasność: {}".format(ledLego.get_param('flag'), ledLego.get_param('brightness'))))
                # ------------------------------------------------------------------------------------------------------------
                if stringNRF[1:3] == "20":  # terrace light
                    if stringNRF[3] == "?":
                        if stringNRF[4] == "P":
                            if stringNRF[5:9].isdigit():
                                ledTerrace.brightness = int(stringNRF[5:9])
                            else:
                                ledTerrace.set_param('brightness', 0)
                            if ledTerrace.get_param('brightness'):
                                ledTerrace.set_param('flag', True)
                            else:
                                ledTerrace.set_param('flag', False)
                            log.add_log(("   Terrace LED ON/OFF:{} Jasność: {}".format(ledTerrace.get_param('flag'), ledTerrace.get_param('brightness'))))
                # ------------------------------------------------------------------------------------------------------------
                if stringNRF[1:3] == "12":  # kwiatek 2  addres 12
                    sensorFlower1.add_record(stringNRF)
                    infoStrip.set_error(4, False)  # poprawic - przeniesc do klasy urzadzenia
                # ------------------------------------------------------------------------------------------------------------
                if stringNRF[1:3] == "13":  # kwiatek 3 adres 13
                    sensorFlower2.add_record(stringNRF)
                    infoStrip.set_error(5, False)
                # ------------------------------------------------------------------------------------------------------------
                if stringNRF[1:3] == "14":  # kwiatek 5 adres 14
                    sensorFlower3.add_record(stringNRF)
                    infoStrip.set_error(16, False)
                # ------------------------------------------------------------------------------------------------------------
                # if stringNRF[1:3] == "15":  # dogHouse 15
                #     if stringNRF[3] == "s":
                #         string2 = (stringNRF[4:7])
                #         dogHouse.temp1 = float(string2)/10
                #         string5 = (stringNRF[7:10])
                #         dogHouse.temp2 = float(string5)/10
                #         string6 = (stringNRF[10:13])
                #         dogHouse.temp3 = float(string6)/10
                #         string7 = (stringNRF[13])
                #         dogHouse.czujnikZajetosciflaga = int(string7)
                #         string8 = (stringNRF[14:16])
                #         dogHouse.czujnikZajetosciRaw = int(string8)
                #         dogHouse.time = datetime.datetime.now()  # zapisanie czasu ostatniego odbioru
                #         log.add_log(("   dogHouse t.wew: {}   t.ciepla: {}  t.zimna: {}   f:{}   cz:{}".format(
                #             dogHouse.temp1, dogHouse.temp2, dogHouse.temp3, dogHouse.czujnikZajetosciflaga, dogHouse.czujnikZajetosciRaw)))
    # ------------------------------------------------------------------------------------------------------------
                if stringNRF[1:3] == "99":  # test module
                    log.add_log('TEST!: {}'.format(stringNRF))


nrf = Nrf([0x11, 0x11, 0x11, 0x11, 0x11])
