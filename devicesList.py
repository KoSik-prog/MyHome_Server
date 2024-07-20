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
    from lib.nrfConnect import *
except ImportError:
    print("Import error - devices list")


class Server():
    serverActiveFlag = True

    def read_server_active_flag(self):
        return self.serverActiveFlag

    def set_server_active_flag(self, flag):
        self.serverActiveFlag = flag

server = Server()

sensorOutside = SensorOutside()

sensorRoom1Temperature = SensorRoom('Salon', 'pok1Temp')
sensorRoom2Temperature = SensorRoom('Sypialnia', 'pok2Temp')

#  SENSORS
sensorFlower1 = SensorFlower(1, [0x22, 0x22, 0x22, 0x22, 0x22], "Bonsai", 200.0, 1000.0) #fake address
sensorFlower2 = SensorFlower(2, [0x22, 0x22, 0x22, 0x22, 0x22], "Strelicja", 200.0, 1000.0)
sensorFlower3 = SensorFlower(3, [0x22, 0x22, 0x22, 0x22, 0x22], "Szeflera", 200.0, 1000.0)


class Terrarium:  # TERRARIUM
    tempUP = 0.0
    humiUP = 0.0
    tempDN = 0.0
    humiDN = 0.0
    uvi = 0.0
    spraysToday = 0


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
    label = "Lampa-reka"
    flag = 0
    autoOn = '15:50:00.0000'
    autoOff = '23:05:00.0000'
    autoLuxMin = 50 
    autoBrightness = 1
    flagManualControl = False
    error = 0
    address = [0x33, 0x33, 0x33, 0x33, 0x77]
    nrfPower = NRF24.PA_LOW

    def get_json_data(self):
            retData = {
                "name": self.label,
                "flag": self.flag,
                "autoOn": self.autoOn,
                "autoOff": self.autoOff,
                "autoLuxMin": self.autoLuxMin,
                "autoBrightness": self.autoBrightness,
                "flagManualControl": self.flagManualControl,
                "error": self.error,
                "address": self.address,
                } 
            return retData

    def to_dict(self):
        return self.__dict__

    def from_dict(self, data):
        self.__dict__.update(data)

    def set_param(self, param, setting):
        setattr(self, param, setting)

    def get_param(self, param):
        return getattr(self, param, None)
decorationRoom1 = DecorationRoom1()


class Decoration2Room1:  # Dekoracje 2 w salonie  Eifla i inne
    label = "Dekoracje szafka"
    flag = 0
    autoOn = '15:50:00.0000'
    autoOff = '23:04:00.0000'
    autoLuxMin = 30
    autoBrightness = 1
    flagManualControl = False
    error = 0
    address = [0x33, 0x33, 0x33, 0x33, 0x09]
    nrfPower = NRF24.PA_LOW
    
    def get_json_data(self):
        retData = {
            "name": self.label,
            "flag": self.flag,
            "autoOn": self.autoOn,
            "autoOff": self.autoOff,
            "autoLuxMin": self.autoLuxMin,
            "autoBrightness": self.autoBrightness,
            "flagManualControl": self.flagManualControl,
            "error": self.error,
            "address": self.address,
            } 
        return retData

    def to_dict(self):
        return self.__dict__

    def from_dict(self, data):
        self.__dict__.update(data)

    def set_param(self, param, setting):
        setattr(self, param, setting)

    def get_param(self, param):
        return getattr(self, param, None)
decoration2Room1 = Decoration2Room1()


class DecorationFlamingo:  # Dekoracje w sypialni
    def __init__(self) -> None:
        self.name = "decorationFlamingo"
        self.label = 'Flaming'
        self.flag = 0
        self.autoOn = '21:30:00.0000'
        self.autoOff = '23:59:00.0000'
        self.autoLuxMin = 100 
        self.autoBrightness = 1
        self.flagManualControl = False
        self.error = 0
        self.address = [0x33, 0x33, 0x33, 0x33, 0x10]
        self.nrfPower = NRF24.PA_LOW
    
    def get_json_data(self):
        retData = {
            "name": self.label,
            "flag": self.flag,
            "autoOn": self.autoOn,
            "autoOff": self.autoOff,
            "autoLuxMin": self.autoLuxMin,
            "autoBrightness": self.autoBrightness,
            "flagManualControl": self.flagManualControl,
            "error": self.error,
            "address": self.address,
            } 
        return retData

    def to_dict(self):
        return self.__dict__

    def from_dict(self, data):
        self.__dict__.update(data)

    def set_param(self, param, setting):
        setattr(self, param, setting)

    def get_param(self, param):
        return getattr(self, param, None)
decorationFlamingo = DecorationFlamingo()


class UsbPlug:  # USB Wtyk
    label = 'USB-Plug'
    flag = 0
    autoOn = '17:00:00.0000'
    autoOff = '23:00:00.0000'
    autoLuxMin = 1100
    autoBrightness = 1
    flagManualControl = False
    error = 0
    address = [0x33, 0x33, 0x33, 0x33, 0x11]
    nrfPower = NRF24.PA_LOW
    
    def get_json_data(self):
        retData = {
            "name": self.label,
            "flag": self.flag,
            "autoOn": self.autoOn,
            "autoOff": self.autoOff,
            "autoLuxMin": self.autoLuxMin,
            "autoBrightness": self.autoBrightness,
            "flagManualControl": self.flagManualControl,
            "error": self.error,
            "address": self.address,
            } 
        return retData

    def to_dict(self):
        return self.__dict__

    def from_dict(self, data):
        self.__dict__.update(data)

    def set_param(self, param, setting):
        setattr(self, param, setting)

    def get_param(self, param):
        return getattr(self, param, None)
usbPlug = UsbPlug()


class Hydroponics:  # hydroponika
    def __init__(self) -> None:
        self.name = "hydroponics"
        self.label = 'Hydroponika'
        self.flag = 0
        self.autoOn = '09:00:00.0000'
        self.autoOff = '17:00:00.0000'
        self.autoLuxMin = 65000
        self.autoBrightness = 1
        self.flagManualControl = False
        self.error = 0
        self.address = [0x33, 0x33, 0x33, 0x11, 0x88]
        self.nrfPower = NRF24.PA_LOW
    
    def get_json_data(self):
        retData = {
            "name": self.label,
            "flag": self.flag,
            "autoOn": self.autoOn,
            "autoOff": self.autoOff,
            "autoLuxMin": self.autoLuxMin,
            "autoBrightness": self.autoBrightness,
            "flagManualControl": self.flagManualControl,
            "error": self.error,
            "address": self.address,
            } 
        return retData

    def to_dict(self):
        return self.__dict__

    def from_dict(self, data):
        self.__dict__.update(data)

    def set_param(self, param, setting):
        setattr(self, param, setting)

    def get_param(self, param):
        return getattr(self, param, None)
hydroponics = Hydroponics()


class LedStripRoom1:  # LED TV
    def __init__(self):
        self.name = "LedStripRoom1"
        self.label = "LED strip"
        self.flag = 0
        self.autoOn = '16:00:00.0000'
        self.autoOff = '23:00:00.0000'
        self.autoLuxMin = 100
        self.autoBrightness = 70
        self.flagManualControl = False
        self.error = 0
        self.address = [0x33, 0x33, 0x33, 0x33, 0x33]
        self.nrfPower = "PA_LOW"  # Assuming NRF24.PA_LOW is a string
        self.white = 0
        self.brightness = 0
        self.setting = "255255255"
    
    def get_json_data(self):
        retData = {
            "name": self.label,
            "flag": self.flag,
            "autoOn": self.autoOn,
            "autoOff": self.autoOff,
            "autoLuxMin": self.autoLuxMin,
            "autoBrightness": self.autoBrightness,
            "flagManualControl": self.flagManualControl,
            "error": self.error,
            "address": self.address,
            "white": self.white,
            "brightness": self.brightness,
            "setting": self.setting,
            } 
        return retData

    def to_dict(self):
        return self.__dict__

    def from_dict(self, data):
        self.__dict__.update(data)

    def set_param(self, param, setting):
        setattr(self, param, setting)

    def get_param(self, param):
        return getattr(self, param, None)
ledStripRoom1 = LedStripRoom1()




class SpootLightRoom1:  # REFLEKTOR W SALONIE
    def __init__(self) -> None:
        self.name = "SpootLightRoom1"
        self.setting = "000000000100"
        self.brightness = 0
        self.flag = 0
        self.error = 0
        self.address = [0x33, 0x33, 0x33, 0x00, 0x55]
        self.nrfPower = NRF24.PA_LOW
        self.label = 'Reflektor 1'


    def to_dict(self):
        return self.__dict__

    def from_dict(self, data):
        self.__dict__.update(data)

    def set_param(self, param, setting):
        setattr(self, param, setting)

    def get_param(self, param):
        return getattr(self, param, None)
spootLightRoom1 = SpootLightRoom1()


class KitchenLight:  # OSWIETLENIE KUCHNI
    def __init__(self) -> None:
        self.name = "kitchenLight"
        self.label = 'Kuchnia'
        self.flag = 0
        self.autoOn = '15:00:00.0000'
        self.autoOff = '23:58:00.0000'
        self.autoLuxMin = 150 
        self.autoBrightness = 1
        self.flagManualControl = False
        self.error = 0
        self.address = [0, 0, 0, 0, 6]
        self.nrfPower = NRF24.PA_LOW
    
    def get_json_data(self):
        retData = {
            "name": self.label,
            "flag": self.flag,
            "autoOn": self.autoOn,
            "autoOff": self.autoOff,
            "autoLuxMin": self.autoLuxMin,
            "autoBrightness": self.autoBrightness,
            "flagManualControl": self.flagManualControl,
            "error": self.error,
            "address": self.address,
            } 
        return retData

    def to_dict(self):
        return self.__dict__

    def from_dict(self, data):
        self.__dict__.update(data)

    def set_param(self, param, setting):
        setattr(self, param, setting)

    def get_param(self, param):
        return getattr(self, param, None)
kitchenLight = KitchenLight()

class LedDeskRoom3:  # LED biurka
    def __init__(self, nrf) -> None:
        self.name = "ledDeskRoom3"
        self.label = "LED Desk"
        self.flag = 0
        self.autoOn = '16:00:00.0000'
        self.autoOff = '23:00:00.0000'
        self.autoLuxMin = 0
        self.autoBrightness = 70
        self.flagManualControl = False
        self.error = 0
        self.address = [0x33, 0x33, 0x33, 0x11, 0x99]
        self.nrfPower = NRF24.PA_LOW
        self.brightness = 0
    
    def get_json_data(self):
        retData = {
            "name": self.label,
            "flag": self.flag,
            "autoOn": self.autoOn,
            "autoOff": self.autoOff,
            "autoLuxMin": self.autoLuxMin,
            "autoBrightness": self.autoBrightness,
            "flagManualControl": self.flagManualControl,
            "error": self.error,
            "address": self.address,
            "brightness": self.brightness
            } 
        return retData

    def to_dict(self):
        return self.__dict__

    def from_dict(self, data):
        self.__dict__.update(data)

    def set_param(self, param, setting):
        setattr(self, param, setting)

    def get_param(self, param):
        return getattr(self, param, None)

    def handle_nrf(self, data):
        if data[1:3] == self.get_address_value():
            if data[3] == "?":
                if data[4:7].isdigit():
                    self.brightness = int(data[4:7])
                else:
                    self.brightness = 0
                self.flag = True if self.brightness else False
                log.add_log(f"   Desk LED ON/OFF:{self.flag} Jasność: {self.brightness}")
                return True
        return False

    def handle_socketService(self, message):
        if(message.find('ledDesk.') != -1):
            strt = message.find(".")+1
            settingBuffer = message[strt:]
            if(settingBuffer.isdigit()):
                if int(settingBuffer) > 100:
                    settingBuffer = 100
                setting = int(settingBuffer)
                result = "ok"
            else:
                setting = 0
                result = "error" 
            packet = f"#{self.get_address_value()}P{int(setting):03d}"
            if len(packet) >= 5:
                log.add_log(f"Ustawiono Led Biurka: {packet}")
                infoStrip.add_info(f"światło biurka: {setting}")
                nrf.to_send(self.address, packet, self.nrfPower)
                if int(setting) == 0:
                    ledDeskRoom3.flag = False
                else:
                    ledDeskRoom3.flag = True
                ledDeskRoom3.error += 1
            else:
                log.add_log(f"BLAD SKLADNI!: {packet}")
            self.flagManualControl = True
            return True, result
        return False, 0

    def get_address_value(self):
        addrStr = f"{self.address[-2]:02x}{self.address[-1]:02x}"
        return addrStr[1:3]
ledDeskRoom3 = LedDeskRoom3(nrf)


class LedLego:  # LED LEGO Strelicja
    def __init__(self) -> None:
        self.name = "ledLego"
        self.label = "LED Lego"
        self.flag = 0
        self.autoOn = '16:00:00.0000'
        self.autoOff = '23:00:00.0000'
        self.autoLuxMin = 50  # brightness setting for auto light
        self.autoBrightness = 20
        self.flagManualControl = False
        self.error = 0
        self.address = [0x33, 0x33, 0x33, 0x22, 0x00]
        self.nrfPower = NRF24.PA_LOW
        self.brightness = 0
    
    def get_json_data(self):
        retData = {
            "name": self.label,
            "flag": self.flag,
            "autoOn": self.autoOn,
            "autoOff": self.autoOff,
            "autoLuxMin": self.autoLuxMin,
            "autoBrightness": self.autoBrightness,
            "flagManualControl": self.flagManualControl,
            "error": self.error,
            "address": self.address,
            "brightness": self.brightness
            } 
        return retData

    def handle_nrf(self, data):
        if data[1:3] == self.get_address_value():
            if data[3] == "?":
                if data[4:7].isdigit():
                    self.brightness = int(data[4:7])
                else:
                    self.brightness = 0
                self.flag = True if self.brightness else False
                log.add_log(f"   LEGO LED ON/OFF:{self.flag} Jasność: {self.brightness}")
                return True
        return False

    def handle_socketService(self, message):
        if(message.find('ledLego.') != -1):
            strt = message.find(".")+1
            settingBuffer = message[strt:]
            if(settingBuffer.isdigit()):
                if int(settingBuffer) > 100:
                    settingBuffer = 100
                setting = int(settingBuffer)
                result = "ok"
            else:
                setting = 0
                result = "error" 
                packet = "#20P{:03d}".format(int(setting))
                if len(packet) >= 5:
                    log.add_log("Ustawiono Led LEGO: {}".format(packet))
                    infoStrip.add_info("światło LEGO: {}".format(setting))
                    nrf.to_send(self.address, packet, self.nrfPower)
                    self.flagManualControl = True
            return True, result
        return False, 0
    
    def to_dict(self):
        return self.__dict__

    def from_dict(self, data):
        self.__dict__.update(data)

    def set_param(self, param, setting):
        setattr(self, param, setting)

    def get_param(self, param):
        return getattr(self, param, None)

    def get_address_value(self):
        addrStr = f"{self.address[-2]:02x}{self.address[-1]:02x}"
        return addrStr[1:3]
ledLego = LedLego()


class LedTerrace:  # LED balkon
    label = "LED Terrace"
    flag = 0
    autoOn = '20:00:00.0000'
    autoOff = '23:00:00.0000'
    autoLuxMin = 100  # brightness setting for auto light
    autoBrightness = 100
    flagManualControl = False
    error = 0
    address = [0x00, 0x00, 0x00, 0x20, 0x20]
    nrfPower = NRF24.PA_LOW
    brightness = 0
    
    def get_json_data(self):
        retData = {
            "name": self.label,
            "flag": self.flag,
            "autoOn": self.autoOn,
            "autoOff": self.autoOff,
            "autoLuxMin": self.autoLuxMin,
            "autoBrightness": self.autoBrightness,
            "flagManualControl": self.flagManualControl,
            "error": self.error,
            "address": self.address,
            "brightness": self.brightness
            } 
        return retData

    def to_dict(self):
        return self.__dict__

    def from_dict(self, data):
        self.__dict__.update(data)

    def set_param(self, param, setting):
        setattr(self, param, setting)

    def get_param(self, param):
        return getattr(self, param, None)
ledTerrace = LedTerrace()


class LedPhotosHeart:  # LED serce w sypialni
    def __init__(self) -> None:
        self.name = "LedPhotosHeart"
        self.label = "LED serce"
        self.flag = 0
        self.autoOn = '20:00:00.0000'
        self.autoOff = '23:00:00.0000'
        self.autoLuxMin = 50  # brightness setting for auto light
        self.autoBrightness = 10
        self.flagManualControl = False
        self.error = 0
        self.address = [0x00, 0x00, 0x00, 0x00, 0x22]
        self.nrfPower = NRF24.PA_LOW
        self.brightness = 70
    
    def get_json_data(self):
        retData = {
            "name": self.label,
            "flag": self.flag,
            "autoOn": self.autoOn,
            "autoOff": self.autoOff,
            "autoLuxMin": self.autoLuxMin,
            "autoBrightness": self.autoBrightness,
            "flagManualControl": self.flagManualControl,
            "error": self.error,
            "address": self.address,
            "brightness": self.brightness
            } 
        return retData

    def to_dict(self):
        return self.__dict__

    def from_dict(self, data):
        self.__dict__.update(data)

    def set_param(self, param, setting):
        setattr(self, param, setting)

    def get_param(self, param):
        return getattr(self, param, None)
ledPhotosHeart = LedPhotosHeart()


class FloorLampRoom1Tradfri:
    def __init__(self) -> None:
        self.address = "65537"  # address="131079"  -> group
        self.status = False

    def to_dict(self):
        return self.__dict__

    def from_dict(self, data):
        self.__dict__.update(data)

    def set_param(self, param, setting):
        setattr(self, param, setting)

    def get_param(self, param):
        return getattr(self, param, None)
floorLampRoom1Tradfri = FloorLampRoom1Tradfri()


class MainLightRoom1Tradfri:
    def __init__(self) -> None:
        self.bulb = "65559"
        self.address = "131074"
        self.status = False

    def to_dict(self):
        return self.__dict__

    def from_dict(self, data):
        self.__dict__.update(data)

    def set_param(self, param, setting):
        setattr(self, param, setting)

    def get_param(self, param):
        return getattr(self, param, None)
mainLightRoom1Tradfri = MainLightRoom1Tradfri()


class DiningRoomTradfri:
    def __init__(self) -> None:
        self.address = "131075"
        self.status = False

    def to_dict(self):
        return self.__dict__

    def from_dict(self, data):
        self.__dict__.update(data)

    def set_param(self, param, setting):
        setattr(self, param, setting)

    def get_param(self, param):
        return getattr(self, param, None)
diningRoomTradfri = DiningRoomTradfri()


class LedLightRoom2Tradfri:
    def __init__(self) -> None:
        self.address = "131082"
        self.flag = 0
        self.autoOn = '21:10:00.0000'
        self.autoOff = '23:50:00.0000'
        self.autoLuxMin = 30
        self.flagManualControl = False
        self.autoBrightness = 5
        self.error = 0
        self.label = "Lampy sypialnia"

    def to_dict(self):
        return self.__dict__

    def from_dict(self, data):
        self.__dict__.update(data)

    def set_param(self, param, setting):
        setattr(self, param, setting)

    def get_param(self, param):
        return getattr(self, param, None)
ledLightRoom2Tradfri = LedLightRoom2Tradfri()


class HallTradfri:
    def __init__(self) -> None:
        self.address = "131077"
        self.status = False
        self.label = "Oswietlenie przedpokoj"

    def to_dict(self):
        return self.__dict__

    def from_dict(self, data):
        self.__dict__.update(data)

    def set_param(self, param, setting):
        setattr(self, param, setting)

    def get_param(self, param):
        return getattr(self, param, None)
hallTradfri = HallTradfri()

nrf.set_devicesList([ledDeskRoom3, ledLego])

