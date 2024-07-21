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


class DecorationRoom1:  # Dekoracje w salonie Reka
    def __init__(self):
        self.label = "Lampa-reka"
        self.flag = 0
        self.autoOn = '15:50:00.0000'
        self.autoOff = '23:05:00.0000'
        self.autoLuxMin = 50 
        self.autoBrightness = 1
        self.flagManualControl = False
        self.error = 0
        self.address = [0x33, 0x33, 0x33, 0x33, 0x77]
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

    def set_light(self, setting):
        if not isinstance(setting, int):
            setting = int(setting)
        if setting <= 1 and setting >= 0:
            packet = f"#08T{setting:01d}"
            nrf.to_send(self.address, packet, self.nrfPower)
            decoration2Room1.set_light(setting) # set second decoration module
            log.add_log(f"Ustawiono dekoracje 1 w salonie: {setting}")
            infoStrip.add_info(f"Dekoracje 1 w salonie: {setting}")
            self.flag = int(setting)
            return True
        return False

    def handle_nrf(self, data):
        if data[1:3] == "08":
            if data[3] == "?":
                if (int(data[4]) != 0):
                    self.flag = 1
                else:
                    self.flag = 0
                log.add_log(f"   Dekoracje 1 w salonie TRYB:{self.flag}")
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
            self.flagManualControl = True
            return True, result
        return False, 0

    def auto_timer(self):
        now = datetime.datetime.now().time()
        autoOnTime = datetime.datetime.strptime(self.autoOn, '%H:%M:%S.%f').time()
        autoOffTime = datetime.datetime.strptime(self.autoOff, '%H:%M:%S.%f').time()

        if self.flagManualControl and autoOnTime <= now < (datetime.datetime.combine(datetime.date.today(), autoOnTime) + datetime.timedelta(seconds=15)).time():
            self.flagManualControl = False

        if self.flagManualControl and autoOffTime <= now < (datetime.datetime.combine(datetime.date.today(), autoOffTime) + datetime.timedelta(seconds=15)).time():
            self.flagManualControl = False

        if (self.flag == 0 and sensorOutside.get_calulated_brightness() < self.autoLuxMin and
            autoOnTime <= now <= (datetime.datetime.combine(datetime.date.today(), autoOffTime) - datetime.timedelta(seconds=60)).time() and
            not self.flagManualControl and self.error < 20):
            log.add_log(f"AUTO {self.label} -> ON / brightnessCalc: {sensorOutside.get_calulated_brightness()} / setting: {self.autoLuxMin}")
            self.setLight(self.autoBrightness)
            time.sleep(20)

        if (self.flag == 1 and autoOffTime <= now <= (datetime.datetime.combine(datetime.date.today(), autoOffTime) + datetime.timedelta(seconds=60)).time() and
            not self.flagManualControl and self.error < 20):
            log.add_log(f"AUTO {self.label} -> OFF")
            self.setLight(0)
            time.sleep(20)
    
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
            log.add_log(f"Ustawiono dekoracje 2 w salonie: {setting}")
            infoStrip.add_info(f"Dekoracje 2 w salonie: {setting}")
            self.flag = int(setting)
            return True
        return False

    def handle_nrf(self, data):
        if data[1:3] == self.get_address_value():
            if data[3] == ".":
                if (int(data[4]) == 1 or int(data[4]) == 2):
                    self.flag = 1
                else:
                    self.flag = 0
                log.add_log(f"   Dekoracje 2 w salonie TRYB:{self.flag}")
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
            self.flagManualControl = True
            return True, result
        return False, 0

    def auto_timer(self):
        now = datetime.datetime.now().time()
        autoOnTime = datetime.datetime.strptime(self.autoOn, '%H:%M:%S.%f').time()
        autoOffTime = datetime.datetime.strptime(self.autoOff, '%H:%M:%S.%f').time()

        if self.flagManualControl and autoOnTime <= now < (datetime.datetime.combine(datetime.date.today(), autoOnTime) + datetime.timedelta(seconds=15)).time():
            self.flagManualControl = False

        if self.flagManualControl and autoOffTime <= now < (datetime.datetime.combine(datetime.date.today(), autoOffTime) + datetime.timedelta(seconds=15)).time():
            self.flagManualControl = False

        if (self.flag == 0 and sensorOutside.get_calulated_brightness() < self.autoLuxMin and
            autoOnTime <= now <= (datetime.datetime.combine(datetime.date.today(), autoOffTime) - datetime.timedelta(seconds=60)).time() and
            not self.flagManualControl and self.error < 20):
            log.add_log(f"AUTO {self.label} -> ON / brightnessCalc: {sensorOutside.get_calulated_brightness()} / setting: {self.autoLuxMin}")
            self.setLight(self.autoBrightness)
            time.sleep(20)

        if (self.flag == 1 and autoOffTime <= now <= (datetime.datetime.combine(datetime.date.today(), autoOffTime) + datetime.timedelta(seconds=60)).time() and
            not self.flagManualControl and self.error < 20):
            log.add_log(f"AUTO {self.label} -> OFF")
            self.setLight(0)
            time.sleep(20)
    
    def to_dict(self):
        return self.__dict__

    def from_dict(self, data):
        self.__dict__.update(data)

    def set_param(self, param, setting):
        setattr(self, param, setting)

    def get_param(self, param):
        return getattr(self, param, None)

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
            log.add_log(f"Ustawiono Lampa Flaming: {setting}")
            infoStrip.add_info(f"Flaming: {setting}")
            self.flag = int(setting)
            return True
        return False

    def handle_nrf(self, data):
        if data[1:3] == "10":
            if data[3] == "?":
                if (int(data[4]) == 1 or int(data[4]) == 2):
                    self.flag = 1
                else:
                    self.flag = 0
                log.add_log(f"   Flaming ON/OFF:{self.flag}")
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
            self.flagManualControl = True
            return True, result
        return False, 0

    def auto_timer(self):
        now = datetime.datetime.now().time()
        autoOnTime = datetime.datetime.strptime(self.autoOn, '%H:%M:%S.%f').time()
        autoOffTime = datetime.datetime.strptime(self.autoOff, '%H:%M:%S.%f').time()

        if self.flagManualControl and autoOnTime <= now < (datetime.datetime.combine(datetime.date.today(), autoOnTime) + datetime.timedelta(seconds=15)).time():
            self.flagManualControl = False

        if self.flagManualControl and autoOffTime <= now < (datetime.datetime.combine(datetime.date.today(), autoOffTime) + datetime.timedelta(seconds=15)).time():
            self.flagManualControl = False

        if (self.flag == 0 and sensorOutside.get_calulated_brightness() < self.autoLuxMin and
            autoOnTime <= now <= (datetime.datetime.combine(datetime.date.today(), autoOffTime) - datetime.timedelta(seconds=60)).time() and
            not self.flagManualControl and self.error < 20):
            log.add_log(f"AUTO {self.label} -> ON / brightnessCalc: {sensorOutside.get_calulated_brightness()} / setting: {self.autoLuxMin}")
            self.setLight(self.autoBrightness)
            time.sleep(20)

        if (self.flag == 1 and autoOffTime <= now <= (datetime.datetime.combine(datetime.date.today(), autoOffTime) + datetime.timedelta(seconds=60)).time() and
            not self.flagManualControl and self.error < 20):
            log.add_log(f"AUTO {self.label} -> OFF")
            self.setLight(0)
            time.sleep(20)
    
    def to_dict(self):
        return self.__dict__

    def from_dict(self, data):
        self.__dict__.update(data)

    def set_param(self, param, setting):
        setattr(self, param, setting)

    def get_param(self, param):
        return getattr(self, param, None)

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

    def set_light(self):
        if self.brightness <= 256 and self.brightness >= 0:
            packet = f"#05K{self.setting}{self.brightness:03d}"
            nrf.to_send(self.address, packet, self.nrfPower)
            log.add_log(f"Ustawiono Led TV: {setting}")
            infoStrip.add_info(f"Led TV: {setting}")
            self.flag = int(setting)
            return True
        return False

    def handle_nrf(self, data):
        if data[1:3] == "05":
            if data[3] == "?":
                self.setting = data[4:13]
                self.brightness = data[13:]
                if (int(self.brightness) > 0):
                    self.flag = 1
                else:
                    self.flag = 0
                # self.flag = True if self.brightness else False # TODO - flag or brightness check
                log.add_log(f"   Led TV ON/OFF:{self.flag}   Jasnosc:{self.brightness}")
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
                self.brightness = setting
                result = "ok"
            else:
                setting = 0
                result = "error" 
            self.set_light()
            self.flagManualControl = True
            return True, result
        elif(message.find('ledstripecolor.') != -1):
            strt = message.find(".")+1
            setting = message[strt:]
            if len(setting) > 9:
                self.setting = setting[:9]
                self.brightness = int(setting[9:])
            else:
                self.setting = setting
            self.set_light()
            self.flagManualControl = True
            return True, result
        return False, 0

    def auto_timer(self):
        now = datetime.datetime.now().time()
        autoOnTime = datetime.datetime.strptime(self.autoOn, '%H:%M:%S.%f').time()
        autoOffTime = datetime.datetime.strptime(self.autoOff, '%H:%M:%S.%f').time()

        if self.flagManualControl and autoOnTime <= now < (datetime.datetime.combine(datetime.date.today(), autoOnTime) + datetime.timedelta(seconds=15)).time():
            self.flagManualControl = False

        if self.flagManualControl and autoOffTime <= now < (datetime.datetime.combine(datetime.date.today(), autoOffTime) + datetime.timedelta(seconds=15)).time():
            self.flagManualControl = False

        if (self.flag == 0 and sensorOutside.get_calulated_brightness() < self.autoLuxMin and
            autoOnTime <= now <= (datetime.datetime.combine(datetime.date.today(), autoOffTime) - datetime.timedelta(seconds=60)).time() and
            not self.flagManualControl and self.error < 20):
            log.add_log(f"AUTO {self.label} -> ON / brightnessCalc: {sensorOutside.get_calulated_brightness()} / setting: {self.autoLuxMin}")
            self.setLight(self.autoBrightness)
            time.sleep(20)

        if (self.flag == 1 and autoOffTime <= now <= (datetime.datetime.combine(datetime.date.today(), autoOffTime) + datetime.timedelta(seconds=60)).time() and
            not self.flagManualControl and self.error < 20):
            log.add_log(f"AUTO {self.label} -> OFF")
            self.setLight(0)
            time.sleep(20)
    
    def to_dict(self):
        return self.__dict__

    def from_dict(self, data):
        self.__dict__.update(data)

    def set_param(self, param, setting):
        setattr(self, param, setting)

    def get_param(self, param):
        return getattr(self, param, None)

    def get_address_value(self):
        addrStr = f"{self.address[-1]:02x}"
        return addrStr
ledStripRoom1 = LedStripRoom1()


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

    def set_light(self, setting):
        if not isinstance(setting, int):
            setting = int(setting)
        if setting < 10 and setting >= 0:
            packet = f"#{self.get_address_value()}T{setting:01d}"
            nrf.to_send(self.address, packet, self.nrfPower)
            log.add_log(f"Ustawiono Led Kuchni: {packet}".format(setting))
            infoStrip.add_info(f"światło w kuchni: {setting}".format(setting))
            return True
        return False

    def handle_nrf(self, data):
        if data[1:3] == self.get_address_value():
            if data[3] == ".":
                if (int(data[4]) == 1 or int(data[4]) == 2):
                    self.flag = 1
                else:
                    self.flag = 0
                log.add_log(f"   Led kuchnia TRYB:{self.flag}")
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
            self.flagManualControl = True
            return True, result
        return False, 0

    def auto_timer(self):
        now = datetime.datetime.now().time()
        autoOnTime = datetime.datetime.strptime(self.autoOn, '%H:%M:%S.%f').time()
        autoOffTime = datetime.datetime.strptime(self.autoOff, '%H:%M:%S.%f').time()

        if self.flagManualControl and autoOnTime <= now < (datetime.datetime.combine(datetime.date.today(), autoOnTime) + datetime.timedelta(seconds=15)).time():
            self.flagManualControl = False

        if self.flagManualControl and autoOffTime <= now < (datetime.datetime.combine(datetime.date.today(), autoOffTime) + datetime.timedelta(seconds=15)).time():
            self.flagManualControl = False

        if (self.flag == 0 and sensorOutside.get_calulated_brightness() < self.autoLuxMin and
            autoOnTime <= now <= (datetime.datetime.combine(datetime.date.today(), autoOffTime) - datetime.timedelta(seconds=60)).time() and
            not self.flagManualControl and self.error < 20):
            log.add_log(f"AUTO {self.label} -> ON / brightnessCalc: {sensorOutside.get_calulated_brightness()} / setting: {self.autoLuxMin}")
            self.setLight(self.autoBrightness)
            time.sleep(20)

        if (self.flag == 1 and autoOffTime <= now <= (datetime.datetime.combine(datetime.date.today(), autoOffTime) + datetime.timedelta(seconds=60)).time() and
            not self.flagManualControl and self.error < 20):
            log.add_log(f"AUTO {self.label} -> OFF")
            self.setLight(0)
            time.sleep(20)
    
    def to_dict(self):
        return self.__dict__

    def from_dict(self, data):
        self.__dict__.update(data)

    def set_param(self, param, setting):
        setattr(self, param, setting)

    def get_param(self, param):
        return getattr(self, param, None)

    def get_address_value(self):
        addrStr = f"{self.address[-1]:02x}"
        return addrStr
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

    def set_light(self, setting):
        if not isinstance(setting, int):
            setting = int(setting)
        if setting < 100 and setting >= 0:
            packet = f"#{self.get_address_value()}P{int(setting):03d}"
            nrf.to_send(self.address, packet, self.nrfPower)
            log.add_log(f"Ustawiono Led Biurka: {setting}")
            infoStrip.add_info(f"światło biurka: {setting}")
            return True
        return False

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
            self.set_light(setting)
            # if int(setting) == 0:
            #     ledDeskRoom3.flag = False
            # else:
            #     ledDeskRoom3.flag = True
            self.error += 1
            self.flagManualControl = True
            return True, result
        return False, 0

    def auto_timer(self):
        now = datetime.datetime.now().time()
        autoOnTime = datetime.datetime.strptime(self.autoOn, '%H:%M:%S.%f').time()
        autoOffTime = datetime.datetime.strptime(self.autoOff, '%H:%M:%S.%f').time()

        if self.flagManualControl and autoOnTime <= now < (datetime.datetime.combine(datetime.date.today(), autoOnTime) + datetime.timedelta(seconds=15)).time():
            self.flagManualControl = False

        if self.flagManualControl and autoOffTime <= now < (datetime.datetime.combine(datetime.date.today(), autoOffTime) + datetime.timedelta(seconds=15)).time():
            self.flagManualControl = False

        if (self.flag == 0 and sensorOutside.get_calulated_brightness() < self.autoLuxMin and
            autoOnTime <= now <= (datetime.datetime.combine(datetime.date.today(), autoOffTime) - datetime.timedelta(seconds=60)).time() and
            not self.flagManualControl and self.error < 20):
            log.add_log(f"AUTO {self.label} -> ON / brightnessCalc: {sensorOutside.get_calulated_brightness()} / setting: {self.autoLuxMin}")
            self.setLight(self.autoBrightness)
            time.sleep(20)

        if (self.flag == 1 and autoOffTime <= now <= (datetime.datetime.combine(datetime.date.today(), autoOffTime) + datetime.timedelta(seconds=60)).time() and
            not self.flagManualControl and self.error < 20):
            log.add_log(f"AUTO {self.label} -> OFF")
            self.setLight(0)
            time.sleep(20)
    
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

    def set_light(self, setting):
        if not isinstance(setting, int):
            setting = int(setting)
        if setting < 100 and setting >= 0:
            packet = f"#{self.get_address_value()}P{setting:03d}"
            nrf.to_send(self.address, packet, self.nrfPower)
            log.add_log("Ustawiono Led LEGO: {}".format(setting))
            infoStrip.add_info("światło LEGO: {}".format(setting))
            return True
        return False

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
            self.set_light(setting)
            self.flagManualControl = True
            return True, result
        return False, 0

    def auto_timer(self):
        now = datetime.datetime.now().time()
        autoOnTime = datetime.datetime.strptime(self.autoOn, '%H:%M:%S.%f').time()
        autoOffTime = datetime.datetime.strptime(self.autoOff, '%H:%M:%S.%f').time()

        if self.flagManualControl and autoOnTime <= now < (datetime.datetime.combine(datetime.date.today(), autoOnTime) + datetime.timedelta(seconds=15)).time():
            self.flagManualControl = False

        if self.flagManualControl and autoOffTime <= now < (datetime.datetime.combine(datetime.date.today(), autoOffTime) + datetime.timedelta(seconds=15)).time():
            self.flagManualControl = False

        if (self.flag == 0 and sensorOutside.get_calulated_brightness() < self.autoLuxMin and
            autoOnTime <= now <= (datetime.datetime.combine(datetime.date.today(), autoOffTime) - datetime.timedelta(seconds=60)).time() and
            not self.flagManualControl and self.error < 20):
            log.add_log(f"AUTO {self.label} -> ON / brightnessCalc: {sensorOutside.get_calulated_brightness()} / setting: {self.autoLuxMin}")
            self.setLight(self.autoBrightness)
            time.sleep(20)

        if (self.flag == 1 and autoOffTime <= now <= (datetime.datetime.combine(datetime.date.today(), autoOffTime) + datetime.timedelta(seconds=60)).time() and
            not self.flagManualControl and self.error < 20):
            log.add_log(f"AUTO {self.label} -> OFF")
            self.setLight(0)
            time.sleep(20)
    
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
            log.add_log("Ustawiono Led Balkonu: {}".format(setting))
            infoStrip.add_info("światło balkon: {}".format(setting))
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
                    self.flag = True if self.brightness else False
                    log.add_log(f"   Terrace LED ON/OFF:{self.flag} Jasność: {self.brightness}")
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
            self.flagManualControl = True
            return True, result
        return False, 0

    def auto_timer(self):
        now = datetime.datetime.now().time()
        autoOnTime = datetime.datetime.strptime(self.autoOn, '%H:%M:%S.%f').time()
        autoOffTime = datetime.datetime.strptime(self.autoOff, '%H:%M:%S.%f').time()

        if self.flagManualControl and autoOnTime <= now < (datetime.datetime.combine(datetime.date.today(), autoOnTime) + datetime.timedelta(seconds=15)).time():
            self.flagManualControl = False

        if self.flagManualControl and autoOffTime <= now < (datetime.datetime.combine(datetime.date.today(), autoOffTime) + datetime.timedelta(seconds=15)).time():
            self.flagManualControl = False

        if (self.flag == 0 and sensorOutside.get_calulated_brightness() < self.autoLuxMin and
            autoOnTime <= now <= (datetime.datetime.combine(datetime.date.today(), autoOffTime) - datetime.timedelta(seconds=60)).time() and
            not self.flagManualControl and self.error < 20):
            log.add_log(f"AUTO {self.label} -> ON / brightnessCalc: {sensorOutside.get_calulated_brightness()} / setting: {self.autoLuxMin}")
            self.setLight(self.autoBrightness)
            time.sleep(20)

        if (self.flag == 1 and autoOffTime <= now <= (datetime.datetime.combine(datetime.date.today(), autoOffTime) + datetime.timedelta(seconds=60)).time() and
            not self.flagManualControl and self.error < 20):
            log.add_log(f"AUTO {self.label} -> OFF")
            self.setLight(0)
            time.sleep(20)
    
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
        log.add_log(f"Ustawiono {self.label}: {setting}".format(setting))
        infoStrip.add_info(f"{self.name}: {setting}".format(setting))
        return True

    def handle_nrf(self, data):
        if data[1:3] == self.get_address_value():
            if data[3] == "?":
                if data[4].isdigit():
                    self.flag = int(data[4])
                else:
                    self.flag = 0
                log.add_log(f"   Terrace LED ON/OFF:{self.flag}")
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
            self.flagManualControl = True
            return True, result
        return False, 0

    def auto_timer(self):
        now = datetime.datetime.now().time()
        autoOnTime = datetime.datetime.strptime(self.autoOn, '%H:%M:%S.%f').time()
        autoOffTime = datetime.datetime.strptime(self.autoOff, '%H:%M:%S.%f').time()

        if self.flagManualControl and autoOnTime <= now < (datetime.datetime.combine(datetime.date.today(), autoOnTime) + datetime.timedelta(seconds=15)).time():
            self.flagManualControl = False

        if self.flagManualControl and autoOffTime <= now < (datetime.datetime.combine(datetime.date.today(), autoOffTime) + datetime.timedelta(seconds=15)).time():
            self.flagManualControl = False

        if (self.flag == 0 and sensorOutside.get_calulated_brightness() < self.autoLuxMin and
            autoOnTime <= now <= (datetime.datetime.combine(datetime.date.today(), autoOffTime) - datetime.timedelta(seconds=60)).time() and
            not self.flagManualControl and self.error < 20):
            log.add_log(f"AUTO {self.label} -> ON / brightnessCalc: {sensorOutside.get_calulated_brightness()} / setting: {self.autoLuxMin}")
            self.setLight(self.autoBrightness)
            time.sleep(20)

        if (self.flag == 1 and autoOffTime <= now <= (datetime.datetime.combine(datetime.date.today(), autoOffTime) + datetime.timedelta(seconds=60)).time() and
            not self.flagManualControl and self.error < 20):
            log.add_log(f"AUTO {self.label} -> OFF")
            self.setLight(0)
            time.sleep(20)
    
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
            log.add_log(f"Ustawiono {self.label}: {setting}".format(setting))
            infoStrip.add_info(f"{self.name}: {setting}".format(setting))
            return True
        return False

    def handle_nrf(self, data):
        if data[1:3] == self.get_address_value():
            if data[3] == "?":
                if data[4].isdigit():
                    self.flag = int(data[4])
                else:
                    self.flag = 0
                log.add_log(f"   Terrace LED ON/OFF:{self.flag}")
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
            self.flagManualControl = True
            return True, result
        return False, 0

    def auto_timer(self):
        now = datetime.datetime.now().time()
        autoOnTime = datetime.datetime.strptime(self.autoOn, '%H:%M:%S.%f').time()
        autoOffTime = datetime.datetime.strptime(self.autoOff, '%H:%M:%S.%f').time()

        if self.flagManualControl and autoOnTime <= now < (datetime.datetime.combine(datetime.date.today(), autoOnTime) + datetime.timedelta(seconds=15)).time():
            self.flagManualControl = False

        if self.flagManualControl and autoOffTime <= now < (datetime.datetime.combine(datetime.date.today(), autoOffTime) + datetime.timedelta(seconds=15)).time():
            self.flagManualControl = False

        if (self.flag == 0 and sensorOutside.get_calulated_brightness() < self.autoLuxMin and
            autoOnTime <= now <= (datetime.datetime.combine(datetime.date.today(), autoOffTime) - datetime.timedelta(seconds=60)).time() and
            not self.flagManualControl and self.error < 20):
            log.add_log(f"AUTO {self.label} -> ON / brightnessCalc: {sensorOutside.get_calulated_brightness()} / setting: {self.autoLuxMin}")
            self.setLight(self.autoBrightness)
            time.sleep(20)

        if (self.flag == 1 and autoOffTime <= now <= (datetime.datetime.combine(datetime.date.today(), autoOffTime) + datetime.timedelta(seconds=60)).time() and
            not self.flagManualControl and self.error < 20):
            log.add_log(f"AUTO {self.label} -> OFF")
            self.setLight(0)
            time.sleep(20)
    
    def to_dict(self):
        return self.__dict__

    def from_dict(self, data):
        self.__dict__.update(data)

    def set_param(self, param, setting):
        setattr(self, param, setting)

    def get_param(self, param):
        return getattr(self, param, None)

    def get_address_value(self):
        addrStr = f"{self.address[-1]:02x}"
        return addrStr
usbPlug = UsbPlug()











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

deviceArray = [decorationRoom1, decoration2Room1, decorationFlamingo, ledDeskRoom3, ledStripRoom1, ledLego, kitchenLight, sensorOutside, sensorRoom1Temperature, sensorFlower1, sensorFlower2, sensorFlower3]
nrf.set_devicesList(deviceArray)

