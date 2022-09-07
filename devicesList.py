#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        sensorFlower
# Author:      KoSik
#
# Created:     29.05.2022
# Copyright:   (c) kosik 2022
#-------------------------------------------------------------------------------

import datetime
from sensorFlower import *
from deviceWaterCan import *
from lib.lib_nrf24 import NRF24

class sensorOutsideTemperatureCl:   #CZUJNIK TEMPERATURY ZEWNETRZNEJ
    temp = 1.1
    humi = 1.1
    batt = 1.1
    lux = 0
    ir = 0
    windSpeed = 0
    windDirection = 0
    time = datetime.datetime.now()
    error = False
    flagNight = False
    nightSetting = 60  #ustawienie kiedy noc
sensorOutsideTemperature = sensorOutsideTemperatureCl

class sensorRoom1TemperatureCl:  #SALON
    temp = 2.2
    humi = 2.2
    batt = 2.2
    time = datetime.datetime.now()
    error = False
    sqlRoom = 'pok1Temp'
sensorRoom1Temperature = sensorRoom1TemperatureCl

class sensorRoom2TemperatureCl:   #SYPIALNIA
    temp = 3.3
    humi = 3.3
    batt = 3.3
    time = datetime.datetime.now()
    error = False
    sqlRoom = 'pok2Temp'
sensorRoom2Temperature = sensorRoom2TemperatureCl

'''class czujnikKwiatekCl:   #KWIATEK
    address = [0x33, 0x33, 0x33, 0x11, 0x22]
    woda=0
    light=0
    humidity=100
    power=100
    time=datetime.datetime.now()
    error = "blebleble"
czujnikKwiatek=czujnikKwiatekCl'''

#  DEVICES
#automatycznaKonewka = DEVICE_WATER_CAN_CL([0x33, 0x33, 0x33, 0x11, 0x22], "Konewka - Palma")

#  SENSORS
sensorFlower2 = SENSOR_FLOWER_CL(2, [0x33, 0x33, 0x33, 0x11, 0x33], "Palma", 120.0, 500.0)
sensorFlower3 = SENSOR_FLOWER_CL(3, [0x33, 0x33, 0x33, 0x11, 0x44], "Pachira", 380.0, 500.0)
sensorFlower4 = SENSOR_FLOWER_CL(4, [0x33, 0x33, 0x33, 0x11, 0x66], "Pokrzywa", 280.0, 580.0)
sensorFlower5 = SENSOR_FLOWER_CL(5, [0x33, 0x33, 0x33, 0x11, 0x77], "Benjamin", 400.0, 550.0)
sensorFlower6 = SENSOR_FLOWER_CL(6, [0x33, 0x33, 0x33, 0x11, 0x88], "Szeflera", 260.0, 500.0)

class terrariumCl:   #TERRARIUM
    tempUP = 0.0
    humiUP = 0.0
    tempDN = 0.0
    humiDN = 0.0
    UVI = 0.0
terrarium = terrariumCl

class dogHouseCl:   #dogHouse
    address = [0x33, 0x33, 0x33, 0x11, 0x55]
    nrfPower = NRF24.PA_LOW
    temp1 = 0.0
    temp2 = 0.0
    temp3 = 0.0
    czujnikZajetosciflaga = False
    czujnikZajetosciRaw = 0
    tryb = 0
    time = datetime.datetime.now()
dogHouse = dogHouseCl

class decorationRoom1Cl:     #Dekoracje w salonie Reka
    flag = 0
    autoOn = '15:50:00.0000'
    autoOff = '23:05:00.0000'
    autoLuxMin = 600 #ustawienie minimum oswietlenia przy ktorym zalaczy sie swiatlo
    flagManualControl = False
    autoBrightness = 1
    error = 0
    address = [0x33, 0x33, 0x33, 0x33, 0x77]
    nrfPower = NRF24.PA_LOW
    label = "Lampa-reka"
decorationRoom1 = decorationRoom1Cl

class decoration2Room1Cl:     #Dekoracje 2 w salonie  Eifla i inne
    flag = 0
    autoOn = '15:50:00.0000'
    autoOff = '23:04:00.0000'
    autoLuxMin = 500 #ustawienie minimum oswietlenia przy ktorym zalaczy sie swiatlo
    flagManualControl = False
    autoBrightness = 1
    error = 0
    address = [0x33, 0x33, 0x33, 0x33, 0x09]
    nrfPower = NRF24.PA_LOW
    label = "Dekoracje szafka"
decoration2Room1 = decoration2Room1Cl

class decorationFlamingoCl:     #Dekoracje w sypialni
    flag = 0
    autoOn = '21:30:00.0000'
    autoOff = '23:59:00.0000'
    flagManualControl = False
    autoBrightness = 1
    autoLuxMin = 300 #ustawienie minimum oswietlenia przy ktrym zalaczy sie swiatlo
    error = 0
    address = [0x33, 0x33, 0x33, 0x33, 0x10]
    nrfPower = NRF24.PA_LOW
    label = 'Flaming'
decorationFlamingo = decorationFlamingoCl

class usbPlugCl:     #USB Stick
    autoOn = '17:00:00.0000'
    autoOff = '23:00:00.0000'
    autoLuxMin = 1100
    autoBrightness = 1
    flag = 0
    error = 0
    flagManualControl = False
    address = [0x33, 0x33, 0x33, 0x33, 0x11]
    nrfPower = NRF24.PA_LOW
    label = 'USB-Stick'
usbPlug = usbPlugCl

class hyroponicsCl:     #hyroponika
    address = [0x33, 0x33, 0x33, 0x11, 0x88]
    nrfPower = NRF24.PA_LOW
    autoOn = '08:00:00.0000'
    autoOff = '19:00:00.0000'
    autoLuxMin = 65000
    flag = 0
    error = 0
    autoBrightness = 1
    flagManualControl = False
    label = 'Hyroponika'
hyroponics = hyroponicsCl

class ledStripRoom1Cl:     #LED TV
    nrfPower = NRF24.PA_LOW
    setting = "255255255"
    Bialy = 000
    brightness = 70
    flag = 0
    autoOn = '16:00:00.0000'
    autoOff = '23:00:00.0000'
    autoLuxMin = 600 #ustawienie minimum oswietlenia przy ktrym zalaczy sie swiatlo
    flagManualControl = False
    autoBrightness = 70
    error = 0
    address = [0x33, 0x33, 0x33, 0x33, 0x33]
    label="LED TV"
ledStripRoom1 = ledStripRoom1Cl

class ledLightRoom2Cl:  # OSWIETLENIE SYPIALNI
    brightness = 0
    flag = 0
    autoOn = '21:00:00.0000'
    autoOff = '23:50:00.0000'
    autoLuxMin = 200 #ustawienie minimum oswietlenia przy ktrym zalaczy sie swiatlo
    flagManualControl = False
    autoBrightness = 5
    error = 0
    address = [0x33, 0x33, 0x33, 0x33, 0x44]
    nrfPower = NRF24.PA_LOW
    label = 'Sypialnia'
ledLightRoom2 = ledLightRoom2Cl

class spootLightRoom1Cl:  # REFLEKTOR W SALONIE
    setting = "000000000100"
    brightness = 0
    flag = 0
    error = 0
    address = [0x33, 0x33, 0x33, 0x00, 0x55]
    nrfPower = NRF24.PA_LOW
    label = 'Reflektor 1'
spootLightRoom1 = spootLightRoom1Cl

class kitchenLightCl:  # OSWIETLENIE KUCHNI
    flag = 0
    autoOn = '15:00:00.0000'
    autoOff = '23:58:00.0000'
    flagManualControl = False
    autoBrightness = 1
    autoLuxMin = 1300 #ustawienie minimum oswietlenia przy ktrym zalaczy sie swiatlo
    error = 0
    address = [0, 0, 0, 0, 6]
    nrfPower = NRF24.PA_LOW
    label = 'Kuchnia'
kitchenLight = kitchenLightCl

class floorLampRoom1TradfriCl:
    address = "65537" #Adres="131079"  -> grupa
    status = False
floorLampRoom1Tradfri = floorLampRoom1TradfriCl

class mainLightRoom1TradfriCl:
    bulb = "65559"
    address = "131074"
    status = False
mainLightRoom1Tradfri = mainLightRoom1TradfriCl

class diningRoomTradfriCl:
    address = "131075"
    status = False
diningRoomTradfri = diningRoomTradfriCl

class ledLightRoom2TradfriCl:  #SYPIALNIA
    address = "131082"
    flag = 0
    autoOn = '21:10:00.0000'
    autoOff = '23:50:00.0000'
    autoLuxMin = 600
    flagManualControl = False
    autoBrightness = 5
    error = 0
    label = "Lampy sypialnia"
ledLightRoom2Tradfri = ledLightRoom2TradfriCl

class hallTradfriCl: #przedpokoj
    address = "131077"
    status = False
    label = "Oswietlenie przedpokoj"
hallTradfri = hallTradfriCl

class lightingAutomationCl:
    LUXvalue = [2000,2000,2000,2000,2000]
    calculatedBrightness = 2000
lightingAutomation = lightingAutomationCl()