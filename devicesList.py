#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:        devices list
# Author:      KoSik
#
# Created:     29.07.2022
# Copyright:   (c) kosik 2022
# -------------------------------------------------------------------------------
try:
    import datetime
    from lib.lib_nrf24 import NRF24
    from sensorFlower import *
    from lib.sensorOutside import *
    from lib.sensorRoom import *
    from deviceWaterCan import *
    from lib.sensorRoom import *
except ImportError:
    print("Import error - devices list")


class Server():
    serverActiveFlag = True

    def read_server_active_flag(self):
        return self.serverActiveFlag

    def set_server_active_flag(self, flag):
        self.serverActiveFlag = flag


server = Server()

"""class SensorOutsideTemperature:   #CZUJNIK TEMPERATURY ZEWNETRZNEJ
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
sensorOutsideTemperature = SensorOutsideTemperature()"""

"""class SensorRoom1Temperature:  # SALON
    temp = 2.2
    humi = 2.2
    batt = 2.2
    time = datetime.datetime.now()
    error = False
    sqlRoom = 'pok1Temp'
sensorRoom1Temperature = SensorRoom1Temperature()"""

"""class SensorRoom2Temperature:  # SYPIALNIA
    temp = 3.3
    humi = 3.3
    batt = 3.3
    time = datetime.datetime.now()
    error = False
    sqlRoom = 'pok2Temp'
sensorRoom2Temperature = SensorRoom2Temperature()"""

sensorOutside = SensorOutside()

sensorRoom1Temperature = SensorRoom('Salon', 'pok1Temp')
sensorRoom2Temperature = SensorRoom('Sypialnia', 'pok2Temp')

#  DEVICES
#automatycznaKonewka = DEVICE_WATER_CAN_CL([0x33, 0x33, 0x33, 0x11, 0x22], "Konewka - Palma")

#  SENSORS
sensorFlower2 = SensorFlower(2, [0x33, 0x33, 0x33, 0x11, 0x33], "Palma", 120.0, 500.0)
sensorFlower3 = SensorFlower(3, [0x33, 0x33, 0x33, 0x11, 0x44], "Pachira", 380.0, 500.0)
sensorFlower4 = SensorFlower(4, [0x33, 0x33, 0x33, 0x11, 0x66], "Pokrzywa", 280.0, 580.0)
sensorFlower5 = SensorFlower(5, [0x33, 0x33, 0x33, 0x11, 0x77], "Benjamin", 400.0, 550.0)
sensorFlower6 = SensorFlower(6, [0x33, 0x33, 0x33, 0x11, 0x88], "Szeflera", 260.0, 500.0)


class Terrarium:  # TERRARIUM
    tempUP = 0.0
    humiUP = 0.0
    tempDN = 0.0
    humiDN = 0.0
    uvi = 0.0


terrarium = Terrarium()


class dogHouse:  # dogHouse
    address = [0x33, 0x33, 0x33, 0x11, 0x55]
    nrfPower = NRF24.PA_LOW
    temp1 = 0.0
    temp2 = 0.0
    temp3 = 0.0
    czujnikZajetosciflaga = False
    czujnikZajetosciRaw = 0
    tryb = 0
    time = datetime.datetime.now()


dogHouse = dogHouse()


class DecorationRoom1:  # Dekoracje w salonie Reka
    flag = 0
    autoOn = '15:50:00.0000'
    autoOff = '23:05:00.0000'
    autoLuxMin = 600 
    flagManualControl = False
    autoBrightness = 1
    error = 0
    address = [0x33, 0x33, 0x33, 0x33, 0x77]
    nrfPower = NRF24.PA_LOW
    label = "Lampa-reka"


decorationRoom1 = DecorationRoom1()


class Decoration2Room1:  # Dekoracje 2 w salonie  Eifla i inne
    flag = 0
    autoOn = '15:50:00.0000'
    autoOff = '23:04:00.0000'
    autoLuxMin = 500
    flagManualControl = False
    autoBrightness = 1
    error = 0
    address = [0x33, 0x33, 0x33, 0x33, 0x09]
    nrfPower = NRF24.PA_LOW
    label = "Dekoracje szafka"


decoration2Room1 = Decoration2Room1()


class DecorationFlamingo:  # Dekoracje w sypialni
    flag = 0
    autoOn = '21:30:00.0000'
    autoOff = '23:59:00.0000'
    flagManualControl = False
    autoBrightness = 1
    autoLuxMin = 300 
    error = 0
    address = [0x33, 0x33, 0x33, 0x33, 0x10]
    nrfPower = NRF24.PA_LOW
    label = 'Flaming'


decorationFlamingo = DecorationFlamingo()


class UsbPlug:  # USB Stick
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


usbPlug = UsbPlug()


class Hyroponics:  # hyroponika
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


hyroponics = Hyroponics()


class LedStripRoom1:  # LED TV
    nrfPower = NRF24.PA_LOW
    setting = "255255255"
    white = 000
    brightness = 70
    flag = 0
    autoOn = '16:00:00.0000'
    autoOff = '23:00:00.0000'
    autoLuxMin = 600  # brightness setting for auto light
    flagManualControl = False
    autoBrightness = 70
    error = 0
    address = [0x33, 0x33, 0x33, 0x33, 0x33]
    label = "LED strip"


ledStripRoom1 = LedStripRoom1()


class LedLightRoom2:  # OSWIETLENIE SYPIALNI
    brightness = 0
    flag = 0
    autoOn = '21:00:00.0000'
    autoOff = '23:50:00.0000'
    autoLuxMin = 200
    flagManualControl = False
    autoBrightness = 5
    error = 0
    address = [0x33, 0x33, 0x33, 0x33, 0x44]
    nrfPower = NRF24.PA_LOW
    label = 'Sypialnia'


ledLightRoom2 = LedLightRoom2()


class SpootLightRoom1:  # REFLEKTOR W SALONIE
    setting = "000000000100"
    brightness = 0
    flag = 0
    error = 0
    address = [0x33, 0x33, 0x33, 0x00, 0x55]
    nrfPower = NRF24.PA_LOW
    label = 'Reflektor 1'


spootLightRoom1 = SpootLightRoom1()


class KitchenLight:  # OSWIETLENIE KUCHNI
    flag = 0
    autoOn = '15:00:00.0000'
    autoOff = '23:58:00.0000'
    flagManualControl = False
    autoBrightness = 1
    autoLuxMin = 1300 
    error = 0
    address = [0, 0, 0, 0, 6]
    nrfPower = NRF24.PA_LOW
    label = 'Kuchnia'


kitchenLight = KitchenLight()


class FloorLampRoom1Tradfri:
    address = "65537"  # address="131079"  -> group
    status = False


floorLampRoom1Tradfri = FloorLampRoom1Tradfri()


class MainLightRoom1Tradfri:
    bulb = "65559"
    address = "131074"
    status = False


mainLightRoom1Tradfri = MainLightRoom1Tradfri()


class DiningRoomTradfri:
    address = "131075"
    status = False


diningRoomTradfri = DiningRoomTradfri()


class LedLightRoom2Tradfri:
    address = "131082"
    flag = 0
    autoOn = '21:10:00.0000'
    autoOff = '23:50:00.0000'
    autoLuxMin = 600
    flagManualControl = False
    autoBrightness = 5
    error = 0
    label = "Lampy sypialnia"


ledLightRoom2Tradfri = LedLightRoom2Tradfri()


class HallTradfri:
    address = "131077"
    status = False
    label = "Oswietlenie przedpokoj"


hallTradfri = HallTradfri()
