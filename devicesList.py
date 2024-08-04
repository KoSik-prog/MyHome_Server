#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:        devices list
# Author:      KoSik
#
# Created:     29.07.2022
# Copyright:   (c) kosik 2022
# -------------------------------------------------------------------------------
# try:
import datetime
import threading
import json
from lib.lib_nrf24 import NRF24
from sensorFlower import *
from lib.sensorOutside import *
from lib.sensorRoom import *
from lib.nrfConnect import *
# except ImportError:
#     print("Import error - devices list")


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


class DecorationRoom1:  # Dekoracje w salonie Reka
    def __init__(self):
        self.label = "Lampa-reka"
        self.flag = False
        self.autoOn = '15:50:00.0000'
        self.autoOff = '23:05:00.0000'
        self.autoLuxMin = 50 
        self.autoBrightness = 1
        self.flagManualControl = False
        self.error = 0
        self.address = [0x33, 0x33, 0x33, 0x33, 0x77]
        self.nrfPower = NRF24.PA_LOW
        self.lock = threading.Lock()

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

    def set_light(self, setting):
        if not isinstance(setting, int):
            setting = int(setting)
        if setting <= 1 and setting >= 0:
            packet = f"#08T{setting:01d}"
            nrf.to_send(self.address, packet, self.nrfPower)
            decoration2Room1.set_light(setting)  # set second decoration module
            log.add_log(f"Ustawiono {self.label}: {setting}")
            infoStrip.add_info(f"{self.label}: {setting}")
            self.set_param("flag", int(setting))
            return True
        return False

    def handle_nrf(self, data):
        if data[1:3] == "08":
            if data[3] == "?":
                if int(data[4]) != 0:
                    self.set_param("flag", True)
                else:
                    self.set_param("flag", False)
                log.add_log(f"   {self.label} TRYB:{self.get_param('flag')}")
                return True
        return False

    def handle_socketService(self, message):
        if(message.find('room1Decorations.') != -1):
            strt = message.find(".")+1
            settingBuffer = message[strt:]
            if(settingBuffer.isdigit()):
                if int(settingBuffer) > 1:
                    settingBuffer = 1
                setting = int(settingBuffer)
                result = "ok"
            else:
                setting = 0
                result = "error" 
            self.set_light(setting)
            self.set_param("flagManualControl", True)
            return True, result
        return False, 0

    def auto_timer(self):
        now = datetime.datetime.now().time()
        autoOnTime = datetime.datetime.strptime(self.autoOn, '%H:%M:%S.%f').time()
        autoOffTime = datetime.datetime.strptime(self.autoOff, '%H:%M:%S.%f').time()

        if self.get_param("flagManualControl") and autoOnTime <= now < (datetime.datetime.combine(datetime.date.today(), autoOnTime) + datetime.timedelta(seconds=15)).time():
            self.set_param("flagManualControl", False)
        elif self.get_param("flagManualControl") and autoOffTime <= now < (datetime.datetime.combine(datetime.date.today(), autoOffTime) + datetime.timedelta(seconds=15)).time():
            self.set_param("flagManualControl", False)

        if (not self.get_param("flag") and sensorOutside.get_calulated_brightness() < self.autoLuxMin and
            autoOnTime <= now <= (datetime.datetime.combine(datetime.date.today(), autoOffTime) - datetime.timedelta(seconds=60)).time() and
            not self.get_param('flagManualControl') and self.get_param('error') < 20):
            log.add_log(f"!!! flag: {self.get_param('flag')} //  flagManualControl: {self.get_param('flagManualControl')}")
            log.add_log(f"AUTO {self.label} -> ON / brightnessCalc: {sensorOutside.get_calulated_brightness()} / setting: {self.autoLuxMin}")
            self.set_light(self.autoBrightness)
            time.sleep(20)

        if (self.get_param("flag") and autoOffTime <= now <= (datetime.datetime.combine(datetime.date.today(), autoOffTime) + datetime.timedelta(seconds=60)).time() and
            not self.get_param("flagManualControl") and self.error < 20):
            log.add_log(f"AUTO {self.label} -> OFF")
            self.set_light(0)
            time.sleep(20)
        time.sleep(1)

    def set_param(self, paramName, value):
        try:
            with self.lock:
                setattr(self, paramName, value)
        except:
            print("Parameter error")
        
    def get_param(self, paramName):
        try:
            with self.lock:
                return getattr(self, paramName)
        except:
            print("Parameter error")

    def to_dict(self):
        def is_serializable(value):
            try:
                json.dumps(value)
                return True
            except (TypeError, OverflowError):
                return False
        return {key: value for key, value in self.__dict__.items() if is_serializable(value) and key != 'lock'}

    def from_dict(self, data):
        for key, value in data.items():
            if key in self.__dict__ and key != 'lock':
                setattr(self, key, value)

    def get_address_value(self):
        addrStr = f"{self.address[-2]:02x}{self.address[-1]:02x}"
        return addrStr[1:3]
decorationRoom1 = DecorationRoom1()


class Decoration2Room1:  # Dekoracje 2 w salonie  Eifla i inne
    def __init__(self):
        self.label = "Dekoracje szafka"
        self.flag = 0
        self.autoOn = '15:50:00.0000'
        self.autoOff = '23:04:00.0000'
        self.autoLuxMin = 30
        self.autoBrightness = 1
        self.flagManualControl = False
        self.error = 0
        self.address = [0x33, 0x33, 0x33, 0x33, 0x09]
        self.nrfPower = NRF24.PA_LOW
        self.lock = threading.Lock()
    
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

    def set_light(self, setting):
        if not isinstance(setting, int):
            setting = int(setting)
        if setting <= 1 and setting >= 0:
            packet = f"#{self.get_address_value()}T{setting:01d}"
            nrf.to_send(self.address, packet, self.nrfPower)
            log.add_log(f"Ustawiono {self.label}: {setting}")
            infoStrip.add_info(f"{self.label}: {setting}")
            self.set_param("flag", int(setting))
            return True
        return False

    def handle_nrf(self, data):
        if data[1:3] == self.get_address_value():
            if data[3] == ".":
                if (int(data[4]) == 1 or int(data[4]) == 2):
                    self.set_param("flag", 1)
                else:
                    self.set_param("flag", 0)
                log.add_log(f"   {self.label} TRYB:{self.get_param('flag')}")
                return True
        return False

    def handle_socketService(self, message):
        if(message.find('room1Decorations.') != -1):
            strt = message.find(".")+1
            settingBuffer = message[strt:]
            if(settingBuffer.isdigit()):
                if int(settingBuffer) > 1:
                    settingBuffer = 1
                setting = int(settingBuffer)
                self.set_param("setting", int(settingBuffer))
                result = "ok"
            else:
                self.set_param("setting", 0)
                result = "error" 
            self.set_light(setting)
            self.set_param("flagManualControl", True)
            return True, result
        return False, 0

    def auto_timer(self):
        now = datetime.datetime.now().time()
        autoOnTime = datetime.datetime.strptime(self.autoOn, '%H:%M:%S.%f').time()
        autoOffTime = datetime.datetime.strptime(self.autoOff, '%H:%M:%S.%f').time()

        if self.get_param("flagManualControl") and autoOnTime <= now < (datetime.datetime.combine(datetime.date.today(), autoOnTime) + datetime.timedelta(seconds=15)).time():
            self.set_param("flagManualControl", False)
        elif self.get_param("flagManualControl") and autoOffTime <= now < (datetime.datetime.combine(datetime.date.today(), autoOffTime) + datetime.timedelta(seconds=15)).time():
            self.set_param("flagManualControl", False)

        if (not self.get_param("flag") and sensorOutside.get_calulated_brightness() < self.autoLuxMin and
            autoOnTime <= now <= (datetime.datetime.combine(datetime.date.today(), autoOffTime) - datetime.timedelta(seconds=60)).time() and
            not self.get_param('flagManualControl') and self.get_param('error') < 20):
            log.add_log(f"!!! flag: {self.get_param('flag')} //  flagManualControl: {self.get_param('flagManualControl')}")
            log.add_log(f"AUTO {self.label} -> ON / brightnessCalc: {sensorOutside.get_calulated_brightness()} / setting: {self.autoLuxMin}")
            self.set_light(self.autoBrightness)
            time.sleep(20)

        if (self.get_param("flag") and autoOffTime <= now <= (datetime.datetime.combine(datetime.date.today(), autoOffTime) + datetime.timedelta(seconds=60)).time() and
            not self.get_param("flagManualControl") and self.error < 20):
            log.add_log(f"AUTO {self.label} -> OFF")
            self.set_light(0)
            time.sleep(20)
        time.sleep(1)

    def set_param(self, paramName, value):
        try:
            with self.lock:
                setattr(self, paramName, value)
        except:
            print("Parameter error")
        
    def get_param(self, paramName):
        try:
            with self.lock:
                return getattr(self, paramName)
        except:
            print("Parameter error")
    
    def to_dict(self):
        def is_serializable(value):
            try:
                json.dumps(value)
                return True
            except (TypeError, OverflowError):
                return False
        return {key: value for key, value in self.__dict__.items() if is_serializable(value) and key != 'lock'}

    def from_dict(self, data):
        for key, value in data.items():
            if key in self.__dict__ and key != 'lock':
                setattr(self, key, value)

    def get_address_value(self):
        addrStr = f"{self.address[-1]:02x}"
        return addrStr
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
        self.lock = threading.Lock()
    
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

    def set_light(self, setting):
        if not isinstance(setting, int):
            setting = int(setting)
        if setting <= 1 and setting >= 0:
            packet = f"#{self.get_address_value()}T{setting:01d}"
            nrf.to_send(self.address, packet, self.nrfPower)
            log.add_log(f"Ustawiono {self.label}: {setting}")
            infoStrip.add_info(f"{self.label}: {setting}")
            self.set_param("flag", int(setting))
            return True
        return False

    def handle_nrf(self, data):
        if data[1:3] == "10":
            if data[3] == "?":
                if (int(data[4]) == 1 or int(data[4]) == 2):
                    self.set_param("flag", 1)
                else:
                    self.set_param("flag", 0)
                log.add_log(f"   {self.label} ON/OFF:{self.get_param('flag')}")
                return True
        return False

    def handle_socketService(self, message):
        if(message.find('room2Decorations.') != -1):
            strt = message.find(".")+1
            settingBuffer = message[strt:]
            if(settingBuffer.isdigit()):
                if int(settingBuffer) > 1:
                    settingBuffer = 1
                setting = int(settingBuffer)
                result = "ok"
            else:
                setting = 0
                result = "error" 
            self.set_light(setting)
            self.set_param("flagManualControl", True)
            return True, result
        return False, 0

    def auto_timer(self):
        now = datetime.datetime.now().time()
        autoOnTime = datetime.datetime.strptime(self.autoOn, '%H:%M:%S.%f').time()
        autoOffTime = datetime.datetime.strptime(self.autoOff, '%H:%M:%S.%f').time()

        if self.get_param("flagManualControl") and autoOnTime <= now < (datetime.datetime.combine(datetime.date.today(), autoOnTime) + datetime.timedelta(seconds=15)).time():
            self.set_param("flagManualControl", False)
        elif self.get_param("flagManualControl") and autoOffTime <= now < (datetime.datetime.combine(datetime.date.today(), autoOffTime) + datetime.timedelta(seconds=15)).time():
            self.set_param("flagManualControl", False)

        if (not self.get_param("flag") and sensorOutside.get_calulated_brightness() < self.autoLuxMin and
            autoOnTime <= now <= (datetime.datetime.combine(datetime.date.today(), autoOffTime) - datetime.timedelta(seconds=60)).time() and
            not self.get_param('flagManualControl') and self.error < 20):
            log.add_log(f"AUTO {self.label} -> ON / brightnessCalc: {sensorOutside.get_calulated_brightness()} / setting: {self.autoLuxMin}")
            self.set_light(self.autoBrightness)
            time.sleep(20)

        if (self.get_param("flag") and autoOffTime <= now <= (datetime.datetime.combine(datetime.date.today(), autoOffTime) + datetime.timedelta(seconds=60)).time() and
            not self.get_param("flagManualControl") and self.error < 20):
            log.add_log(f"AUTO {self.label} -> OFF")
            self.set_light(0)
            time.sleep(20)
        time.sleep(1)

    def set_param(self, paramName, value):
        try:
            with self.lock:
                setattr(self, paramName, value)
        except:
            print("Parameter error")
        
    def get_param(self, paramName):
        try:
            with self.lock:
                return getattr(self, paramName)
        except:
            print("Parameter error")
    
    def to_dict(self):
        def is_serializable(value):
            try:
                json.dumps(value)
                return True
            except (TypeError, OverflowError):
                return False
        return {key: value for key, value in self.__dict__.items() if is_serializable(value) and key != 'lock'}

    def from_dict(self, data):
        for key, value in data.items():
            if key in self.__dict__ and key != 'lock':
                setattr(self, key, value)

    def get_address_value(self):
        addrStr = f"{self.address[-1]:02x}"
        return addrStr
decorationFlamingo = DecorationFlamingo()


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
        self.lock = threading.Lock()
    
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

    def set_light(self, color = None, brightness = None):
        if color != None:
            self.setting = color
        if brightness != None:
            self.brightness = brightness
        if self.brightness <= 256 and self.brightness >= 0:
            packet = f"#05K{self.setting}{self.brightness:03d}"
            nrf.to_send(self.address, packet, self.nrfPower)
            log.add_log(f"Ustawiono {self.label}: {self.setting} / {self.brightness}")
            infoStrip.add_info(f"{self.label}: {self.setting} / {self.brightness}")
            return True
        return False

    def handle_nrf(self, data):
        if data[1:3] == "05":
            if data[3] == "?":
                self.set_param('setting', data[4:13])
                self.set_param('brightness', data[13:])
                if (int(self.get_param('brightness')) > 0):
                    self.set_param("flag", 1)
                else:
                    self.set_param("flag", 0)
                # self.flag = True if self.brightness else False # TODO - flag or brightness check
                log.add_log(f"   {self.label} ON/OFF:{self.get_param('flag')}   Jasnosc:{self.get_param('brightness')}")
                return True
        return False

    def handle_socketService(self, message):
        if(message.find('ledstripebrightness.') != -1):
            strt = message.find(".")+1
            settingBuffer = message[strt:]
            if(settingBuffer.isdigit()):
                if int(settingBuffer) > 100:
                    settingBuffer = 100
                setting = int(settingBuffer)
                self.set_param('brightness', setting)
                result = "ok"
            else:
                setting = 0
                result = "error" 
            self.set_light(brightness = setting)
            self.set_param("flagManualControl", True)
            return True, result
        elif(message.find('ledstripecolor.') != -1):
            strt = message.find(".")+1
            setting = message[strt:]
            if len(setting) < 12:
                if len(setting) > 9:
                    self.set_param('setting', setting[:9])
                    self.set_param('brightness', int(setting[9:]))
                else:
                    self.set_param('setting', setting)
                result = "ok"
            else:
                setting = 0
                result = "error" 
            self.set_light(color = setting)
            self.set_param("flagManualControl", True)
            return True, result
        return False, 0

    def auto_timer(self):
        now = datetime.datetime.now().time()
        autoOnTime = datetime.datetime.strptime(self.autoOn, '%H:%M:%S.%f').time()
        autoOffTime = datetime.datetime.strptime(self.autoOff, '%H:%M:%S.%f').time()

        with self.lock:
            flag = self.flag
            flagManualControl = self.flagManualControl
            error = self.error

        if flagManualControl and autoOnTime <= now < (datetime.datetime.combine(datetime.date.today(), autoOnTime) + datetime.timedelta(seconds=15)).time():
            self.set_param("flagManualControl", False)
        elif flagManualControl and autoOffTime <= now < (datetime.datetime.combine(datetime.date.today(), autoOffTime) + datetime.timedelta(seconds=15)).time():
            self.set_param("flagManualControl", False)

        with self.lock:
            flag = self.flag
            flagManualControl = self.flagManualControl
            error = self.error

        if (not flag and sensorOutside.get_calulated_brightness() < self.autoLuxMin and
            autoOnTime <= now <= (datetime.datetime.combine(datetime.date.today(), autoOffTime) - datetime.timedelta(seconds=60)).time() and
            not flagManualControl and error < 20):
            log.add_log(f"!!! flag: {flag} // flagManualControl: {flagManualControl}")
            log.add_log(f"AUTO {self.label} -> ON / brightnessCalc: {sensorOutside.get_calulated_brightness()} / setting: {self.autoLuxMin}")
            self.set_light(self.autoBrightness)
            time.sleep(20)

        if (flag and autoOffTime <= now <= (datetime.datetime.combine(datetime.date.today(), autoOffTime) + datetime.timedelta(seconds=60)).time() and
            not flagManualControl and error < 20):
            log.add_log(f"AUTO {self.label} -> OFF")
            self.set_light(0)
            time.sleep(20)
        time.sleep(1)

    def set_param(self, paramName, value):
        try:
            with self.lock:
                setattr(self, paramName, value)
        except:
            print("Parameter error")
        
    def get_param(self, paramName):
        try:
            with self.lock:
                return getattr(self, paramName)
        except:
            print("Parameter error")
    
    def to_dict(self):
        def is_serializable(value):
            try:
                json.dumps(value)
                return True
            except (TypeError, OverflowError):
                return False
        return {key: value for key, value in self.__dict__.items() if is_serializable(value) and key != 'lock'}

    def from_dict(self, data):
        for key, value in data.items():
            if key in self.__dict__ and key != 'lock':
                setattr(self, key, value)

    def get_address_value(self):
        addrStr = f"{self.address[-1]:02x}"
        return addrStr
ledStripRoom1 = LedStripRoom1()


class KitchenLight:  # OSWIETLENIE KUCHNI
    def __init__(self) -> None:
        self.name = "kitchenLight"
        self.label = 'Kuchnia'
        self.flag = False
        self.autoOn = '09:00:00.0000' #'15:00:00.0000'
        self.autoOff = '23:58:00.0000'
        self.autoLuxMin = 65000#150 
        self.autoBrightness = 1
        self.flagManualControl = False
        self.error = 0
        self.address = [0, 0, 0, 0, 6]
        self.nrfPower = NRF24.PA_LOW
        self.lock = threading.Lock()
    
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

    def set_light(self, setting):
        if not isinstance(setting, int):
            setting = int(setting)
        if setting < 10 and setting >= 0:
            packet = f"#{self.get_address_value()}T{setting:01d}"
            nrf.to_send(self.address, packet, self.nrfPower)
            log.add_log(f"Ustawiono {self.label}: {setting}")
            infoStrip.add_info(f"{self.label}: {setting}")
            return True
        return False

    def handle_nrf(self, data):
        if data[1:3] == self.get_address_value():
            if data[3] == ".":
                if (int(data[4]) == 1 or int(data[4]) == 2):
                    self.set_param('flag', True)
                else:
                    self.set_param('flag', False)
                log.add_log(f"   {self.label} TRYB (flaga):{self.get_param('flag')}")
                return True
        return False

    def handle_socketService(self, message):
        if(message.find('kitchenlight.') != -1):
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
            self.set_light(setting)
            self.set_param("flagManualControl", True)
            return True, result
        return False, 0

    def auto_timer(self):
        now = datetime.datetime.now().time()
        autoOnTime = datetime.datetime.strptime(self.autoOn, '%H:%M:%S.%f').time()
        autoOffTime = datetime.datetime.strptime(self.autoOff, '%H:%M:%S.%f').time()

        if self.get_param("flagManualControl") and autoOnTime <= now < (datetime.datetime.combine(datetime.date.today(), autoOnTime) + datetime.timedelta(seconds=15)).time():
            self.set_param("flagManualControl", False)
        elif self.get_param("flagManualControl") and autoOffTime <= now < (datetime.datetime.combine(datetime.date.today(), autoOffTime) + datetime.timedelta(seconds=15)).time():
            self.set_param("flagManualControl", False)

        if (not self.get_param("flag") and sensorOutside.get_calulated_brightness() < self.autoLuxMin and
            autoOnTime <= now <= (datetime.datetime.combine(datetime.date.today(), autoOffTime) - datetime.timedelta(seconds=60)).time() and
            not self.get_param('flagManualControl') and self.get_param('error') < 20):
            log.add_log(f"!!! flag: {self.get_param('flag')} //  flagManualControl: {self.get_param('flagManualControl')}")
            log.add_log(f"AUTO {self.label} -> ON / brightnessCalc: {sensorOutside.get_calulated_brightness()} / setting: {self.autoLuxMin}")
            self.set_light(self.autoBrightness)
            time.sleep(20)

        if (self.get_param("flag") and autoOffTime <= now <= (datetime.datetime.combine(datetime.date.today(), autoOffTime) + datetime.timedelta(seconds=60)).time() and
            not self.get_param("flagManualControl") and self.error < 20):
            log.add_log(f"AUTO {self.label} -> OFF")
            self.set_light(0)
            time.sleep(20)
        time.sleep(1)

    def set_param(self, paramName, value):
        try:
            with self.lock:
                setattr(self, paramName, value)
        except:
            print("Parameter error")
        
    def get_param(self, paramName):
        try:
            with self.lock:
                return getattr(self, paramName)
        except:
            print("Parameter error")
    
    def to_dict(self):
        def is_serializable(value):
            try:
                json.dumps(value)
                return True
            except (TypeError, OverflowError):
                return False
        return {key: value for key, value in self.__dict__.items() if is_serializable(value) and key != 'lock'}

    def from_dict(self, data):
        for key, value in data.items():
            if key in self.__dict__ and key != 'lock':
                setattr(self, key, value)

    def get_address_value(self):
        addrStr = f"{self.address[-1]:02x}"
        return addrStr
kitchenLight = KitchenLight()


class LedDeskRoom3:  # LED biurka
    def __init__(self) -> None:
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
        self.lock = threading.Lock()
    
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

    def set_light(self, setting):
        if not isinstance(setting, int):
            setting = int(setting)
        if setting < 100 and setting >= 0:
            packet = f"#{self.get_address_value()}P{int(setting):03d}"
            nrf.to_send(self.address, packet, self.nrfPower)
            log.add_log(f"Ustawiono {self.label}: {setting}")
            infoStrip.add_info(f"{self.label}: {setting}")
            return True
        return False

    def handle_nrf(self, data):
        if data[1:3] == self.get_address_value():
            if data[3] == "?":
                if data[4:7].isdigit():
                    self.brightness = int(data[4:7])
                else:
                    self.brightness = 0
                if self.get_param('brightness'):
                    self.set_param('flag', True)
                else:
                    self.set_param('flag', False)
                log.add_log(f"   {self.label} ON/OFF:{self.get_param('flag')} Jasność: {self.get_param('brightness')}")
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
            self.set_light(setting)
            # if int(setting) == 0:
            #     ledDeskRoom3.flag = False
            # else:
            #     ledDeskRoom3.flag = True
            self.error += 1
            self.set_param("flagManualControl", True)
            return True, result
        return False, 0

    def auto_timer(self):
        now = datetime.datetime.now().time()
        autoOnTime = datetime.datetime.strptime(self.autoOn, '%H:%M:%S.%f').time()
        autoOffTime = datetime.datetime.strptime(self.autoOff, '%H:%M:%S.%f').time()

        if self.get_param("flagManualControl") and autoOnTime <= now < (datetime.datetime.combine(datetime.date.today(), autoOnTime) + datetime.timedelta(seconds=15)).time():
            self.set_param("flagManualControl", False)
        elif self.get_param("flagManualControl") and autoOffTime <= now < (datetime.datetime.combine(datetime.date.today(), autoOffTime) + datetime.timedelta(seconds=15)).time():
            self.set_param("flagManualControl", False)

        if (not self.get_param("flag") and sensorOutside.get_calulated_brightness() < self.autoLuxMin and
            autoOnTime <= now <= (datetime.datetime.combine(datetime.date.today(), autoOffTime) - datetime.timedelta(seconds=60)).time() and
            not self.get_param('flagManualControl') and self.get_param('error') < 20):
            log.add_log(f"!!! flag: {self.get_param('flag')} //  flagManualControl: {self.get_param('flagManualControl')}")
            log.add_log(f"AUTO {self.label} -> ON / brightnessCalc: {sensorOutside.get_calulated_brightness()} / setting: {self.autoLuxMin}")
            self.set_light(self.autoBrightness)
            time.sleep(20)

        if (self.get_param("flag") and autoOffTime <= now <= (datetime.datetime.combine(datetime.date.today(), autoOffTime) + datetime.timedelta(seconds=60)).time() and
            not self.get_param("flagManualControl") and self.error < 20):
            log.add_log(f"AUTO {self.label} -> OFF")
            self.set_light(0)
            time.sleep(20)
        time.sleep(1)

    def set_param(self, paramName, value):
        try:
            with self.lock:
                setattr(self, paramName, value)
        except:
            print("Parameter error")
        
    def get_param(self, paramName):
        try:
            with self.lock:
                return getattr(self, paramName)
        except:
            print("Parameter error")
    
    def to_dict(self):
        def is_serializable(value):
            try:
                json.dumps(value)
                return True
            except (TypeError, OverflowError):
                return False
        return {key: value for key, value in self.__dict__.items() if is_serializable(value) and key != 'lock'}

    def from_dict(self, data):
        for key, value in data.items():
            if key in self.__dict__ and key != 'lock':
                setattr(self, key, value)

    def get_address_value(self):
        addrStr = f"{self.address[-2]:02x}{self.address[-1]:02x}"
        return addrStr[1:3]
ledDeskRoom3 = LedDeskRoom3()


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
        self.address = [0x33, 0x33, 0x33, 0x22, 0x22]
        self.nrfPower = NRF24.PA_LOW
        self.brightness = 0
        self.lock = threading.Lock()
    
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

    def set_light(self, setting):
        if not isinstance(setting, int):
            setting = int(setting)
        if setting < 100 and setting >= 0:
            packet = f"#{self.get_address_value()}P{setting:03d}"
            nrf.to_send(self.address, packet, self.nrfPower)
            log.add_log(f"Ustawiono {self.label}: {setting}")
            infoStrip.add_info(f"{self.label}: {setting}")
            return True
        return False

    def handle_nrf(self, data):
        if data[1:3] == self.get_address_value():
            if data[3] == "?":
                if data[4:7].isdigit():
                    self.set_param('brightness', int(data[4:7]))
                else:
                    self.set_param('brightness', 0)
                if self.get_param('brightness'):
                    self.set_param('flag', True)
                else:
                    self.set_param('flag', False)
                log.add_log(f"   LEGO LED ON/OFF:{self.get_param('flag')} Jasność: {self.get_param('brightness')}")
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
            self.set_light(setting)
            self.set_param("flagManualControl", True)
            return True, result
        return False, 0

    def auto_timer(self):
        now = datetime.datetime.now().time()
        autoOnTime = datetime.datetime.strptime(self.autoOn, '%H:%M:%S.%f').time()
        autoOffTime = datetime.datetime.strptime(self.autoOff, '%H:%M:%S.%f').time()

        if self.get_param("flagManualControl") and autoOnTime <= now < (datetime.datetime.combine(datetime.date.today(), autoOnTime) + datetime.timedelta(seconds=15)).time():
            self.set_param("flagManualControl", False)
        elif self.get_param("flagManualControl") and autoOffTime <= now < (datetime.datetime.combine(datetime.date.today(), autoOffTime) + datetime.timedelta(seconds=15)).time():
            self.set_param("flagManualControl", False)

        if (not self.get_param("flag") and sensorOutside.get_calulated_brightness() < self.autoLuxMin and
            autoOnTime <= now <= (datetime.datetime.combine(datetime.date.today(), autoOffTime) - datetime.timedelta(seconds=60)).time() and
            not self.get_param('flagManualControl') and self.get_param('error') < 20):
            log.add_log(f"!!! flag: {self.get_param('flag')} //  flagManualControl: {self.get_param('flagManualControl')}")
            log.add_log(f"AUTO {self.label} -> ON / brightnessCalc: {sensorOutside.get_calulated_brightness()} / setting: {self.autoLuxMin}")
            self.set_light(self.autoBrightness)
            time.sleep(20)

        if (self.get_param("flag") and autoOffTime <= now <= (datetime.datetime.combine(datetime.date.today(), autoOffTime) + datetime.timedelta(seconds=60)).time() and
            not self.get_param("flagManualControl") and self.error < 20):
            log.add_log(f"AUTO {self.label} -> OFF")
            self.set_light(0)
            time.sleep(20)
        time.sleep(1)

    def set_param(self, paramName, value):
        try:
            with self.lock:
                setattr(self, paramName, value)
        except:
            print("Parameter error")
        
    def get_param(self, paramName):
        try:
            with self.lock:
                return getattr(self, paramName)
        except:
            print("Parameter error")
    
    def to_dict(self):
        def is_serializable(value):
            try:
                json.dumps(value)
                return True
            except (TypeError, OverflowError):
                return False
        return {key: value for key, value in self.__dict__.items() if is_serializable(value) and key != 'lock'}

    def from_dict(self, data):
        for key, value in data.items():
            if key in self.__dict__ and key != 'lock':
                setattr(self, key, value)

    def get_address_value(self):
        addrStr = f"{self.address[-2]:02x}{self.address[-1]:02x}"
        return addrStr[1:3]
ledLego = LedLego()


class LedTerrace:  # LED balkon
    def __init__(self):
        self.label = "LED Terrace"
        self.flag = 0
        self.autoOn = '20:00:00.0000'
        self.autoOff = '23:00:00.0000'
        self.autoLuxMin = 100  # brightness setting for auto light
        self.autoBrightness = 100
        self.flagManualControl = False
        self.error = 0
        self.address = [0x00, 0x00, 0x00, 0x20, 0x20]
        self.nrfPower = NRF24.PA_LOW
        self.brightness = 0
        self.lock = threading.Lock()
    
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

    def set_light(self, setting):
        if not isinstance(setting, int):
            setting = int(setting)
        if setting < 100 and setting >= 0:
            packet = f"#{self.get_address_value()}P{setting:03d}"
            nrf.to_send(self.address, packet, self.nrfPower)
            log.add_log(f"Ustawiono {self.label}: {setting}")
            infoStrip.add_info(f"{self.label}: {setting}")
            return True
        return False

    def handle_nrf(self, data):
        if data[1:3] == self.get_address_value():
            if data[3] == "?":
                if data[4] == "P":
                    if data[5:9].isdigit():
                        self.brightness = int(data[5:9])
                    else:
                        self.brightness = 0
                    if self.get_param('brightness'):
                        self.set_param('flag', True)
                    else:
                        self.set_param('flag', False)
                    log.add_log(f"   {self.label} ON/OFF:{self.get_param('flag')} Jasność: {self.get_param('brightness')}")
                    return True
        return False

    def handle_socketService(self, message):
        if(message.find('ledTerrace.') != -1):
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
            self.set_light(setting)
            self.set_param("flagManualControl", True)
            return True, result
        return False, 0

    def auto_timer(self):
        now = datetime.datetime.now().time()
        autoOnTime = datetime.datetime.strptime(self.autoOn, '%H:%M:%S.%f').time()
        autoOffTime = datetime.datetime.strptime(self.autoOff, '%H:%M:%S.%f').time()

        if self.get_param("flagManualControl") and autoOnTime <= now < (datetime.datetime.combine(datetime.date.today(), autoOnTime) + datetime.timedelta(seconds=15)).time():
            self.set_param("flagManualControl", False)
        elif self.get_param("flagManualControl") and autoOffTime <= now < (datetime.datetime.combine(datetime.date.today(), autoOffTime) + datetime.timedelta(seconds=15)).time():
            self.set_param("flagManualControl", False)

        if (not self.get_param("flag") and sensorOutside.get_calulated_brightness() < self.autoLuxMin and
            autoOnTime <= now <= (datetime.datetime.combine(datetime.date.today(), autoOffTime) - datetime.timedelta(seconds=60)).time() and
            not self.get_param('flagManualControl') and self.get_param('error') < 20):
            log.add_log(f"!!! flag: {self.get_param('flag')} //  flagManualControl: {self.get_param('flagManualControl')}")
            log.add_log(f"AUTO {self.label} -> ON / brightnessCalc: {sensorOutside.get_calulated_brightness()} / setting: {self.autoLuxMin}")
            self.set_light(self.autoBrightness)
            time.sleep(20)

        if (self.get_param("flag") and autoOffTime <= now <= (datetime.datetime.combine(datetime.date.today(), autoOffTime) + datetime.timedelta(seconds=60)).time() and
            not self.get_param("flagManualControl") and self.error < 20):
            log.add_log(f"AUTO {self.label} -> OFF")
            self.set_light(0)
            time.sleep(20)
        time.sleep(1)

    def set_param(self, paramName, value):
        try:
            with self.lock:
                setattr(self, paramName, value)
        except:
            print("Parameter error")
        
    def get_param(self, paramName):
        try:
            with self.lock:
                return getattr(self, paramName)
        except:
            print("Parameter error")
    
    def to_dict(self):
        def is_serializable(value):
            try:
                json.dumps(value)
                return True
            except (TypeError, OverflowError):
                return False
        return {key: value for key, value in self.__dict__.items() if is_serializable(value) and key != 'lock'}

    def from_dict(self, data):
        for key, value in data.items():
            if key in self.__dict__ and key != 'lock':
                setattr(self, key, value)

    def get_address_value(self):
        addrStr = f"{self.address[-1]:02x}"
        return addrStr
ledTerrace = LedTerrace()


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
        self.lock = threading.Lock()
    
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

    def set_light(self, setting):
        if not isinstance(setting, int):
            setting = int(setting)
        if int(setting) > 1:
            packet = "#17P1"
        else:
            packet = f"#17A{setting}"
        nrf.to_send(self.address, packet, self.nrfPower)
        log.add_log(f"Ustawiono {self.label}: {setting}")
        infoStrip.add_info(f"{self.name}: {setting}")
        return True

    def handle_nrf(self, data):
        if data[1:3] == self.get_address_value():
            if data[3] == "?":
                if data[4].isdigit():
                    self.set_param('flag', int(data[4]))
                else:
                    self.set_param('flag', 0)
                log.add_log(f"   {self.label} ON/OFF:{self.get_param('flag')}")
                return True
        return False

    def handle_socketService(self, message):
        if(message.find('hydroponics.') != -1):
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
            self.set_light(setting)
            self.set_param("flagManualControl", True)
            return True, result
        return False, 0

    def auto_timer(self):
        now = datetime.datetime.now().time()
        autoOnTime = datetime.datetime.strptime(self.autoOn, '%H:%M:%S.%f').time()
        autoOffTime = datetime.datetime.strptime(self.autoOff, '%H:%M:%S.%f').time()

        if self.get_param("flagManualControl") and autoOnTime <= now < (datetime.datetime.combine(datetime.date.today(), autoOnTime) + datetime.timedelta(seconds=15)).time():
            self.set_param("flagManualControl", False)
        elif self.get_param("flagManualControl") and autoOffTime <= now < (datetime.datetime.combine(datetime.date.today(), autoOffTime) + datetime.timedelta(seconds=15)).time():
            self.set_param("flagManualControl", False)

        if (not self.get_param("flag") and sensorOutside.get_calulated_brightness() < self.autoLuxMin and
            autoOnTime <= now <= (datetime.datetime.combine(datetime.date.today(), autoOffTime) - datetime.timedelta(seconds=60)).time() and
            not self.get_param('flagManualControl') and self.get_param('error') < 20):
            log.add_log(f"!!! flag: {self.get_param('flag')} //  flagManualControl: {self.get_param('flagManualControl')}")
            log.add_log(f"AUTO {self.label} -> ON / brightnessCalc: {sensorOutside.get_calulated_brightness()} / setting: {self.autoLuxMin}")
            self.set_light(self.autoBrightness)
            time.sleep(20)

        if (self.get_param("flag") and autoOffTime <= now <= (datetime.datetime.combine(datetime.date.today(), autoOffTime) + datetime.timedelta(seconds=60)).time() and
            not self.get_param("flagManualControl") and self.error < 20):
            log.add_log(f"AUTO {self.label} -> OFF")
            self.set_light(0)
            time.sleep(20)
        time.sleep(1)

    def set_param(self, paramName, value):
        try:
            with self.lock:
                setattr(self, paramName, value)
        except:
            print("Parameter error")
        
    def get_param(self, paramName):
        try:
            with self.lock:
                return getattr(self, paramName)
        except:
            print("Parameter error")
    
    def to_dict(self):
        def is_serializable(value):
            try:
                json.dumps(value)
                return True
            except (TypeError, OverflowError):
                return False
        return {key: value for key, value in self.__dict__.items() if is_serializable(value) and key != 'lock'}

    def from_dict(self, data):
        for key, value in data.items():
            if key in self.__dict__ and key != 'lock':
                setattr(self, key, value)

    def get_address_value(self):
        addrStr = f"{self.address[-2]:02x}{self.address[-1]:02x}"
        return addrStr[1:3]
hydroponics = Hydroponics()


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
    lock = threading.Lock()
    
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

    def set_light(self, setting):
        if not isinstance(setting, int):
            setting = int(setting)
        if setting <= 1 and setting >= 0:
            packet = f"#{self.get_address_value()}T{setting:01d}"
            nrf.to_send(self.address, packet, self.nrfPower)
            log.add_log(f"Ustawiono {self.label}: {setting}")
            infoStrip.add_info(f"{self.name}: {setting}")
            return True
        return False

    def handle_nrf(self, data):
        if data[1:3] == self.get_address_value():
            if data[3] == "?":
                if data[4].isdigit():
                    self.set_param("flag", int(data[4]))
                else:
                    self.set_param("flag", 0)
                log.add_log(f"   {self.label} ON/OFF:{self.get_param('flag')}")
                return True
        return False

    def handle_socketService(self, message):
        if(message.find('usbPlug.') != -1):
            strt = message.find(".")+1
            settingBuffer = message[strt:]
            if(settingBuffer.isdigit()):
                if int(settingBuffer) > 1:
                    settingBuffer = 1
                setting = int(settingBuffer)
                result = "ok"
            else:
                setting = 0
                result = "error" 
            self.set_light(setting)
            self.set_param("flagManualControl", True)
            return True, result
        return False, 0

    def auto_timer(self):
        now = datetime.datetime.now().time()
        autoOnTime = datetime.datetime.strptime(self.autoOn, '%H:%M:%S.%f').time()
        autoOffTime = datetime.datetime.strptime(self.autoOff, '%H:%M:%S.%f').time()

        if self.get_param("flagManualControl") and autoOnTime <= now < (datetime.datetime.combine(datetime.date.today(), autoOnTime) + datetime.timedelta(seconds=15)).time():
            self.set_param("flagManualControl", False)
        elif self.get_param("flagManualControl") and autoOffTime <= now < (datetime.datetime.combine(datetime.date.today(), autoOffTime) + datetime.timedelta(seconds=15)).time():
            self.set_param("flagManualControl", False)

        if (not self.get_param("flag") and sensorOutside.get_calulated_brightness() < self.autoLuxMin and
            autoOnTime <= now <= (datetime.datetime.combine(datetime.date.today(), autoOffTime) - datetime.timedelta(seconds=60)).time() and
            not self.get_param('flagManualControl') and self.get_param('error') < 20):
            log.add_log(f"!!! flag: {self.get_param('flag')} //  flagManualControl: {self.get_param('flagManualControl')}")
            log.add_log(f"AUTO {self.label} -> ON / brightnessCalc: {sensorOutside.get_calulated_brightness()} / setting: {self.autoLuxMin}")
            self.set_light(self.autoBrightness)
            time.sleep(20)

        if (self.get_param("flag") and autoOffTime <= now <= (datetime.datetime.combine(datetime.date.today(), autoOffTime) + datetime.timedelta(seconds=60)).time() and
            not self.get_param("flagManualControl") and self.error < 20):
            log.add_log(f"AUTO {self.label} -> OFF")
            self.set_light(0)
            time.sleep(20)
        time.sleep(1)

    def set_param(self, paramName, value):
        try:
            with self.lock:
                setattr(self, paramName, value)
        except:
            print("Parameter error")
        
    def get_param(self, paramName):
        try:
            with self.lock:
                return getattr(self, paramName)
        except:
            print("Parameter error")
    
    def to_dict(self):
        def is_serializable(value):
            try:
                json.dumps(value)
                return True
            except (TypeError, OverflowError):
                return False
        return {key: value for key, value in self.__dict__.items() if is_serializable(value) and key != 'lock'}

    def from_dict(self, data):
        for key, value in data.items():
            if key in self.__dict__ and key != 'lock':
                setattr(self, key, value)

    def get_address_value(self):
        addrStr = f"{self.address[-1]:02x}"
        return addrStr
usbPlug = UsbPlug()




# ++++++++++ IKEA TRADFRI ++++++++++
class MainLightRoom1Tradfri:
    def __init__(self) -> None:
        self.name = "TradfriSalon"
        self.label = "Tradfri Salon"
        self.flag = 0
        self.brightness = 0
        self.bulb = "65559"
        self.address = "131074"
        self.status = False
        self.lock = threading.Lock()
    
    def get_json_data(self):
        retData = {
            "name": self.label,
            "flag": self.flag,
            "error": self.error,
            "address": self.address,
            "brightness": self.brightness
            } 
        return retData

    def set_light(self, setting):
        if not isinstance(setting, int):
            setting = int(setting)
        if setting == 0 or setting == 1:
                ikea.ikea_power_group(ikea.ipAddress, ikea.user_id, ikea.securityid, ikea.security_user, address, setting)
        elif setting > 1:
            ikea.ikea_dim_group(ikea.ipAddress, ikea.user_id, ikea.securityid, ikea.security_user, address, setting)
        log.add_log(f"Ustawiono {self.label}: {setting}")
        infoStrip.add_info(f"{self.name}: {setting}")
        return True

    def handle_socketService(self, message):
        if(message.find('usbPlug.') != -1):
            strt = message.find(".")+1
            settingBuffer = message[strt:]
            if(settingBuffer.isdigit()):
                if int(settingBuffer) > 1:
                    settingBuffer = 1
                setting = int(settingBuffer)
                result = "ok"
            else:
                setting = 0
                result = "error" 
            self.set_light(setting)
            self.set_param("flagManualControl", True)
            return True, result
        return False, 0

    def set_param(self, paramName, value):
        try:
            with self.lock:
                setattr(self, paramName, value)
        except:
            print("Parameter error")
        
    def get_param(self, paramName):
        try:
            with self.lock:
                return getattr(self, paramName)
        except:
            print("Parameter error")

    def handle_socketService(self, message):
        return [0]

    def handle_nrf(self, data):
        return False

    def auto_timer(self):
        return

    def to_dict(self):
        def is_serializable(value):
            try:
                json.dumps(value)
                return True
            except (TypeError, OverflowError):
                return False
        return {key: value for key, value in self.__dict__.items() if is_serializable(value) and key != 'lock'}

    def from_dict(self, data):
        for key, value in data.items():
            if key in self.__dict__ and key != 'lock':
                setattr(self, key, value)
mainLightRoom1Tradfri = MainLightRoom1Tradfri()

# !!!!! DEACTIVATED !!!!!
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
        self.lock = threading.Lock()
    
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

    def set_param(self, paramName, value):
        try:
            with self.lock:
                setattr(self, paramName, value)
        except:
            print("Parameter error")
        
    def get_param(self, paramName):
        try:
            with self.lock:
                return getattr(self, paramName)
        except:
            print("Parameter error")

    def to_dict(self):
        def is_serializable(value):
            try:
                json.dumps(value)
                return True
            except (TypeError, OverflowError):
                return False
        return {key: value for key, value in self.__dict__.items() if is_serializable(value) and key != 'lock'}

    def from_dict(self, data):
        for key, value in data.items():
            if key in self.__dict__ and key != 'lock':
                setattr(self, key, value)
ledPhotosHeart = LedPhotosHeart()


class FloorLampRoom1Tradfri:
    def __init__(self) -> None:
        self.address = "65537"  # address="131079"  -> group
        self.status = False
        self.lock = threading.Lock()

    def set_param(self, paramName, value):
        try:
            with self.lock:
                setattr(self, paramName, value)
        except:
            print("Parameter error")
        
    def get_param(self, paramName):
        try:
            with self.lock:
                return getattr(self, paramName)
        except:
            print("Parameter error")

    def to_dict(self):
        def is_serializable(value):
            try:
                json.dumps(value)
                return True
            except (TypeError, OverflowError):
                return False
        return {key: value for key, value in self.__dict__.items() if is_serializable(value) and key != 'lock'}

    def from_dict(self, data):
        for key, value in data.items():
            if key in self.__dict__ and key != 'lock':
                setattr(self, key, value)
floorLampRoom1Tradfri = FloorLampRoom1Tradfri()


class DiningRoomTradfri:
    def __init__(self) -> None:
        self.address = "131075"
        self.status = False
        self.lock = threading.Lock()

    def set_param(self, paramName, value):
        try:
            with self.lock:
                setattr(self, paramName, value)
        except:
            print("Parameter error")
        
    def get_param(self, paramName):
        try:
            with self.lock:
                return getattr(self, paramName)
        except:
            print("Parameter error")

    def to_dict(self):
        def is_serializable(value):
            try:
                json.dumps(value)
                return True
            except (TypeError, OverflowError):
                return False
        return {key: value for key, value in self.__dict__.items() if is_serializable(value) and key != 'lock'}

    def from_dict(self, data):
        for key, value in data.items():
            if key in self.__dict__ and key != 'lock':
                setattr(self, key, value)
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
        self.lock = threading.Lock()

    def set_param(self, paramName, value):
        try:
            with self.lock:
                setattr(self, paramName, value)
        except:
            print("Parameter error")
        
    def get_param(self, paramName):
        try:
            with self.lock:
                return getattr(self, paramName)
        except:
            print("Parameter error")

    def to_dict(self):
        def is_serializable(value):
            try:
                json.dumps(value)
                return True
            except (TypeError, OverflowError):
                return False
        return {key: value for key, value in self.__dict__.items() if is_serializable(value) and key != 'lock'}

    def from_dict(self, data):
        for key, value in data.items():
            if key in self.__dict__ and key != 'lock':
                setattr(self, key, value)
ledLightRoom2Tradfri = LedLightRoom2Tradfri()


class HallTradfri:
    def __init__(self) -> None:
        self.address = "131077"
        self.status = False
        self.label = "Oswietlenie przedpokoj"
        self.lock = threading.Lock()

    def set_param(self, paramName, value):
        try:
            with self.lock:
                setattr(self, paramName, value)
        except:
            print("Parameter error")
        
    def get_param(self, paramName):
        try:
            with self.lock:
                return getattr(self, paramName)
        except:
            print("Parameter error")

    def to_dict(self):
        def is_serializable(value):
            try:
                json.dumps(value)
                return True
            except (TypeError, OverflowError):
                return False
        return {key: value for key, value in self.__dict__.items() if is_serializable(value) and key != 'lock'}

    def from_dict(self, data):
        for key, value in data.items():
            if key in self.__dict__ and key != 'lock':
                setattr(self, key, value)
hallTradfri = HallTradfri()

deviceArray = [decorationRoom1, decoration2Room1, decorationFlamingo, ledDeskRoom3, ledStripRoom1, 
               ledLego, kitchenLight, sensorOutside, sensorRoom1Temperature, sensorFlower1, sensorFlower2, 
               sensorFlower3, ledTerrace, mainLightRoom1Tradfri]
nrf.set_devicesList(deviceArray)

