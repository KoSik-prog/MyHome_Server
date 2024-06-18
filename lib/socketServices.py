#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:        socket services
# Purpose:
#
# Author:      KoSik
#
# Created:     07.11.2022
# Copyright:   (c) kosik 2022
# -------------------------------------------------------------------------------
# try:
import socket
import select
import json
import random
import os
from lib.log import *
from lights import *
from .sensorOutside import *
from devicesList import *
from lib.tasmota import *
from lib.nrfConnect import *
from lib.infoStrip import *
from devicesList import *
# from lib.firebase import *
# except ImportError:
#     print("Import error - socket services")


class Socket:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    usersList = {"kosik" : "Majeczka11", "jusi" : "jw270307"}

    def __init__(self, host, port):
        self.host = '192.168.0.99'
        self.port = 2223
        self.backlog = 5 
        self.size = 1024
        
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((self.host, self.port)) 
        self.s.listen(self.backlog)
        # self.s.settimeout(1)

    def server_thread(self):
        while server.read_server_active_flag() == True:
            try:
                client, address = self.s.accept() 
                receivedData = client.recv(self.size)
                if receivedData:
                    if(receivedData[0] == "!"):
                        #log.add_log("Socket return: {}".format(receivedData))
                        self.returnSocketData(client, receivedData) 
                    if(receivedData[0] == "#"):
                        log.add_log("Socket transmit: {} / address:{}".format(receivedData, client))
                        self.transmit(client, receivedData)
                client.close()
            except (KeyboardInterrupt, SystemExit):
                log.add_log('server UDP error')
    
    def __del__(self):
        if hasattr(self, 's'):
            self.s.close()

    def stop_server(self):
        if self.s:
            self.s.close()
            print("Server socket closed.")

    def sendSocketMsg(client, msg):
        log.add_log("Socket tx: {}".format(msg))
        client.send(msg) 
        
    def readStatus(self):
        ready = select.select([self.s], [], [], 0.5)
        return ready
    
    def returnSocketData(self, client, message):
        if(message.find("getMyHomeData") != -1):
            jsonData = []
            jsonData.append(sensorRoom1Temperature.get_json_data())
            jsonData.append(sensorRoom2Temperature.get_json_data())
            jsonData.append(sensorOutside.get_json_data())
            toSend = json.dumps(jsonData)
            client.send(toSend)
            
        if(message.find("getDevicesData") != -1):
            jsonData = []
            jsonData.append(decorationRoom1.get_json_data())
            jsonData.append(decoration2Room1.get_json_data())
            jsonData.append(decorationFlamingo.get_json_data())
            jsonData.append(hydroponics.get_json_data())
            jsonData.append(ledStripRoom1.get_json_data())
            jsonData.append(kitchenLight.get_json_data())
            jsonData.append(ledDeskRoom3.get_json_data())
            jsonData.append(ledLego.get_json_data())
            jsonData.append(ledPhotosHeart.get_json_data())
            jsonData.append(ledTerrace.get_json_data())
            jsonData.append(usbPlug.get_json_data())
            toSend = json.dumps(jsonData)
            client.send(toSend)
            
        if(message.find("getTasmotaData") != -1):
            toSend = json.dumps(tasmota.get_json_data())
            client.send(toSend)
            
        if(message.find("getErrorsData") != -1):
            toSend = json.dumps(infoStrip.get_errors_array())
            client.send(toSend)
            
        if(message.find('setTerrariumData.') != -1):
            receivedMessage = message[message.find(".")+1:]
            dataList = json.loads(receivedMessage)
            terrarium.tempUP = float(dataList["tempTop"])
            terrarium.humiUP = float(dataList["humiTop"])
            terrarium.tempDN = float(dataList["tempBottom"])
            terrarium.humiDN = float(dataList["humiBottom"])
            terrarium.uvi = int(dataList["uvi"])
            terrarium.spraysToday = int(dataList["spraysToday"])
            log.add_log("Terrarium tempUP: {}°C, humiUP: {}%  /  tempDN: {}°C, humiDN: {}%  /  uvi: {} / spr: {}".format(
                terrarium.tempUP, terrarium.humiUP, terrarium.tempDN, terrarium.humiDN, terrarium.uvi, terrarium.spraysToday))
            sql.add_record_terrarium(terrarium.tempUP, terrarium.humiUP,
                                     terrarium.tempDN, terrarium.humiDN, terrarium.uvi)
            
        if(message.find('systemReset.') != -1):
            time.sleep(10)
            sys.stdout.flush()
            log.add_watchdog_log('RESET!')
            os.system('sudo shutdown -r now')
            
        if(message.find('sendToNrf.') != -1):
            strt = message.find(".")+1
            rxData = json.loads(message[strt:])
            mydata = rxData["address"]
            mymessage = rxData["message"]
            log.add_log("TEST!!! {}/{}/{}".format(mydata, rxData["message"], rxData["power"]))
            nrf.to_send(mydata, str(mymessage), int(rxData["power"]))
            
        if(message.find('set^') != -1):
            if(message.find('hydroponics.') != -1):  # hydroponics
                strt = message.find(".")+1
                hydroponics.flagManualControl = True
                light.set_light(hydroponics.address, message[strt])
                client.send("ok")
            elif(message.find('usbPlug.') != -1):  # uniwersalny modul USB
                strt = message.find(".")+1
                usbPlug.flagManualControl = True
                light.set_light(usbPlug.address, message[strt])
            elif(message.find('kitchenlight.') != -1):  # KUCHNIA
                strt = message.find(".")+1
                kitchenLight.flagManualControl = True
                light.set_light(kitchenLight.address, message[strt])
                client.send("ok")
            elif(message.find('ledstripecolor.') != -1):
                strt = message.find(".")+1
                setting = message[strt:]
                if len(setting) > 9:
                    ledStripRoom1.setting = setting[:9]
                    ledStripRoom1.brightness = int(setting[9:])
                else:
                    ledStripRoom1.setting = setting
                light.set_light(ledStripRoom1.address, ledStripRoom1.brightness)
                ledStripRoom1.flagManualControl = True
                client.send("ok")
            elif(message.find('ledstripebrightness.') != -1):
                strt = message.find(".")+1
                setting = int(message[strt:])
                ledStripRoom1.brightness = int(setting)
                light.set_light(ledStripRoom1.address, setting)
                ledStripRoom1.flagManualControl = True
                client.send("ok")
            elif(message.find('room1Decorations.') != -1):
                strt = message.find(".")+1
                light.set_light(decorationRoom1.address, message[strt])
                decorationRoom1.flagManualControl = True
                light.set_light(decoration2Room1.address, message[strt])
                client.send("ok")
            elif(message.find('room2Decorations.') != -1): 
                strt = message.find(".")+1
                decorationFlamingo.flagManualControl = True
                light.set_light(decorationFlamingo.address, message[strt])
                client.send("ok")
            elif(message.find('ledDesk.') != -1):
                strt = message.find(".")+1
                settingBuffer = message[strt:]
                if(settingBuffer.isdigit()):
                    if int(settingBuffer) > 100:
                        settingBuffer = 100
                    setting = int(settingBuffer)
                    client.send("ok")
                else:
                    setting = 0
                    client.send("setting error")  
                # ledDeskRoom3.brightness = setting
                light.set_light(ledDeskRoom3.address, str(setting))
                ledDeskRoom3.flagManualControl = True
            elif(message.find('ledLego.') != -1):
                strt = message.find(".")+1
                settingBuffer = message[strt:]
                if(settingBuffer.isdigit()):
                    if int(settingBuffer) > 100:
                        settingBuffer = 100
                    setting = int(settingBuffer)
                    client.send("ok")
                else:
                    setting = 0
                    client.send("setting error")  
                # ledDeskRoom3.brightness = setting
                light.set_light(ledLego.address, str(setting))
                ledLego.flagManualControl = True
            elif(message.find('ledTerrace.') != -1):
                strt = message.find(".")+1
                settingBuffer = message[strt:]
                if(settingBuffer.isdigit()):
                    if int(settingBuffer) > 100:
                        settingBuffer = 100
                    setting = int(settingBuffer)
                    client.send("ok")
                else:
                    setting = 0
                    client.send("setting error")  
                # ledTerrace.brightness = setting
                light.set_light(ledTerrace.address, str(setting))
                ledTerrace.flagManualControl = True
            elif(message.find('ledHeart.') != -1):
                strt = message.find(".")+1
                settingBuffer = message[strt:]
                if(settingBuffer.isdigit()):
                    if int(settingBuffer) > 100:
                        settingBuffer = 100
                    setting = int(settingBuffer)
                    client.send("ok")
                else:
                    setting = 0
                    client.send("setting error")  
                ledPhotosHeart.brightness = setting
                light.set_light(ledPhotosHeart.address, str(setting))
                ledPhotosHeart.flagManualControl = True
            elif(message.find('room1TradfriLampBrightness.') != -1):   # TRADFRI
                strt = message.find(".")+1
                brightness = int(message[strt:])
                if(brightness >= 0 and brightness <= 100):
                    light.set_light(floorLampRoom1Tradfri.address, str(brightness))
                else:
                    log.add_log("Tradfri brightness error! -> {}".format(brightness))
                client.send("ok")
            elif(message.find('room1TradfriLampColor.') != -1):
                strt = message.find(".")+1
                color = message[strt:]
                if len(color) == 9:
                    light.set_light(floorLampRoom1Tradfri.address, color)
                else:
                    log.add_log("Tradfri color error! -> {}".format(color))
                client.send("ok")
            elif(message.find('themeSleep') != -1):   # THEMES
                ledStripRoom1.flagManualControl = True
                light.set_light(ledStripRoom1.address, "000")
                light.set_light(mainLightRoom1Tradfri.address, 0)
                light.set_light(mainLightRoom1Tradfri.bulb, 15)
                light.set_light(floorLampRoom1Tradfri.address, 0)
                decorationRoom1.flagManualControl = True
                light.set_light(decorationRoom1.address, 0)
                decoration2Room1.flagManualControl = True
                light.set_light(decoration2Room1.address, 0)
                usbPlug.flagManualControl = True
                light.set_light(usbPlug.address, 0)
                light.set_light(ledLego.address, 0)
                light.set_light(ledDeskRoom3.address, 0)
                decorationFlamingo.flagManualControl = True
                Set_light_with_delay(decorationFlamingo.address, 0, 5*60).start()
                kitchenLight.flagManualControl = True
                Set_light_with_delay(kitchenLight.address, 0, 5*60).start()
                Set_light_with_delay(ledPhotosHeart.address, 0, 2*60).start()
                Set_light_with_delay(mainLightRoom1Tradfri.address, 0, 30).start()
                log.add_log("Theme: sleep")
            elif(message.find('themeRomantic') != -1):
                if(random.randint(0, 1) == 1):
                    ledStripRoom1.setting = "255000{:03d}".format(random.randint(20, 120))
                else:
                    ledStripRoom1.setting = "255{:03d}000".format(random.randint(20, 120))
                ledStripRoom1.flagManualControl = True
                light.set_light(ledStripRoom1.address, ledStripRoom1.setting)
                if(random.randint(0, 1) == 1):
                    kolor = "255000{:03d}".format(random.randint(20, 150))
                else:
                    kolor = "255{:03d}000".format(random.randint(20, 150))
                light.set_light(floorLampRoom1Tradfri.address, kolor)
                light.set_light(floorLampRoom1Tradfri.address, 100)
                if(random.randint(0, 1) == 1):
                    spootLightRoom1.setting = "255000{:03d}000".format(random.randint(20, 120))
                else:
                    spootLightRoom1.setting = "255{:03d}000000".format(random.randint(20, 120))
                light.set_light(spootLightRoom1.address, 255)
                light.set_light(mainLightRoom1Tradfri.address, 0)
                decorationRoom1.flagManualControl = True
                light.set_light(decorationRoom1.address, 0)
                decoration2Room1.flagManualControl = True
                light.set_light(decoration2Room1.address, 1)
                log.add_log("Theme: romantic")
        if(message.find('login^') != -1):
            strt = message.find("^") + 1
            login = message[strt:]
            logUser = login[:login.find(".")]
            logPassword = login[login.find(".") + 1:]
            try:
                passwordToCheck = self.usersList[logUser.lower()]
            except:
                passwordToCheck = ""
                log.add_log("user not found")
                
            if(logPassword == passwordToCheck):
                log.add_log("user {} has logged in".format(logUser))
                toSend = "OK"
            else:
                log.add_log("access denied")
                toSend = "denied"
            client.send(toSend)
        if(message.find('refreshFirebaseToken^') != -1):
            strt = message.find("^") + 1
            login = message[strt:]
            dataArray = login.split(".")
            logUser = dataArray[0]
            logPassword = dataArray[1]
            if len(dataArray) > 2:
                logToken = dataArray[2]
                phoneNotification.update_token(logUser, logToken)
            log.add_log("LOG -> {}:{} - {}".format(logUser, logPassword, logToken))
            try:
                passwordToCheck = self.usersList[logUser.lower()]
            except:
                passwordToCheck = ""
                log.add_log("user not found")
                
            if(logPassword == passwordToCheck):
                log.add_log("user {} has logged in".format(logUser))
                toSend = "OK"
            else:
                log.add_log("access denied")
                toSend = "denied"
            client.send(toSend)

    def transmit(self, client, messag):
        if(messag.find('set^') != -1):
            if(messag.find('hydroponics.') != -1):  # hydroponics
                strt = messag.find(".")+1
                hydroponics.flagManualControl = True
                light.set_light(hydroponics.address, messag[strt])
            elif(messag.find('kitchenlight.') != -1):  # KUCHNIA
                strt = messag.find(".")+1
                kitchenLight.flagManualControl = True
                light.set_light
                (kitchenLight.address, messag[strt])
                client.send("ok")
            elif(messag.find('ledstripecolor.') != -1):
                strt = messag.find(".")+1
                if int(messag[(strt+9):(strt+12)]) >= 0:
                    ledStripRoom1.setting = messag[(strt):(strt+9)]
                    ledStripRoom1.brightness = int(messag[(strt+9):(strt+12)])
                light.set_light(ledStripRoom1.address, ledStripRoom1.brightness)
                ledStripRoom1.flagManualControl = True
            elif(messag.find('ledstripebrightness.') != -1):
                zmien = messag[14:17]
                if int(zmien) > 0:
                    ledStripRoom1.brightness = int(zmien)
                light.set_light(ledStripRoom1.address, zmien)
                ledStripRoom1.flagManualControl = True
        #---------------------------------------------------------------------------------
        if(messag.find('salonOswietlenie.') != -1):   # SALON
            strt = messag.find(".")+1
            chJasnosc = int(messag[strt:strt+3])
            if(chJasnosc >= 0 and chJasnosc <= 100):
                light.set_light(mainLightRoom1Tradfri.address, str(chJasnosc))
            else:
                log.add_log("Blad danych! -> {}".format(chJasnosc))
        if(messag.find('tradfriLampaJasn.') != -1):   # LAMPA W SALONIE
            strt = messag.find(".")+1
            chJasnosc = int(messag[strt:strt+3])
            if(chJasnosc >= 0 and chJasnosc <= 100):
                light.set_light(floorLampRoom1Tradfri.address, str(chJasnosc))
            else:
                log.add_log("Blad danych! -> {}".format(chJasnosc))
        if(messag.find('tradfriLampaKol.') != -1):   # LAMPA W SALONIE
            strt = messag.find(".")+1
            light.set_light(floorLampRoom1Tradfri.address, messag[strt:strt+9])
        if(messag.find('swiatloSypialni.') != -1):   # SYPIALNIA
            strt = messag.find(".")+1
            chJasnosc = int(messag[strt:strt+3])
            ledPhotosHeart.brightness = chJasnosc
            light.set_light(ledLightRoom2Tradfri.address, ledPhotosHeart.brightness)
            light.set_light(ledPhotosHeart.address, ledPhotosHeart.brightness)
            ledPhotosHeart.flagManualControl = True
            decorationFlamingo.flagManualControl = True
            light.set_light(decorationFlamingo.address, messag[strt])
        if(messag.find('swiatloSypialniTradfri.') != -1):   # SYPIALNIA TRADFRI
            strt = messag.find(".")+1
            chJasnosc = int(messag[strt])
            light.set_light(ledLightRoom2Tradfri.address, chJasnosc)
        if(messag.find('swiatloJadalniTradfri.') != -1):   # Jadalnia TRADFRI
            strt = messag.find(".")+1
            chJasnosc = int(messag[strt])
            light.set_light(diningRoomTradfri.address, chJasnosc)
        if(messag.find('swiatlokuchni.') != -1):  # KUCHNIA
            strt = messag.find(".")+1
            light.set_light(kitchenLight.address, messag[strt])
            kitchenLight.flagManualControl = True
        if(messag.find('swiatloPrzedpokoj.') != -1):  # PRZEDPOKOJ
            strt = messag.find(".")+1
            chJasnosc = int(messag[strt:len(messag)])
            light.set_light(hallTradfri.address, chJasnosc)
        if(messag.find('reflektor1.') != -1):  # REFLEKTOR LED COLOR
            spootLightRoom1.setting = messag[11:23]
            spootLightRoom1.brightness = messag[23:26]
            light.set_light(spootLightRoom1.address, spootLightRoom1.brightness)
        if(messag.find('reflektor1kolor.') != -1):  # REFLEKTOR LED COLOR
            spootLightRoom1.setting = messag[16:28]
            light.set_light(spootLightRoom1.address, spootLightRoom1.brightness)
        if(messag.find('reflektor1jasn.') != -1):  # REFLEKTOR LED COLOR JASNOSC
            spootLightRoom1.brightness = messag[15:18]
            light.set_light(spootLightRoom1.address, spootLightRoom1.brightness)
        if(messag.find('dekoracjePok1.') != -1):  # DEKORACJE POKOJ 1
            strt = messag.find(".")+1
            light.set_light(decorationRoom1.address, messag[strt])
            decorationRoom1.flagManualControl = True
            light.set_light(decoration2Room1.address, messag[strt])
        if(messag.find('dekoracjePok2.') != -1):  # DEKORACJE POKOJ 2
            strt = messag.find(".")+1
            decorationFlamingo.flagManualControl = True
            light.set_light(decorationFlamingo.address, messag[strt])
        if(messag.find('hydroponics.') != -1):  # hydroponics
            strt = messag.find(".")+1
            hydroponics.flagManualControl = True
            light.set_light(hydroponics.address, messag[strt])
        #if(messag == '?m'):
        #    try:
        #        self.s.sendto('temz{:04.1f}wilz{:04.1f}tem1{:04.1f}wil1{:04.1f}tem2{:04.1f}wil2{:04.1f}'.format(sensorOutside.temperature, sensorOutside.humidity, sensorRoom1Temperature.temp, sensorRoom1Temperature.humi, sensorRoom2Temperature.temp, sensorRoom2Temperature.humi)+'wilk{:03d}slok{:03d}wodk{:03d}zask{:03d}'.format(int(czujnikKwiatek.wilgotnosc), int(
        #            czujnikKwiatek.slonce), int(czujnikKwiatek.woda), int(czujnikKwiatek.power))+'letv{}{}{}'.format(int(ledStripRoom1.flag), ledStripRoom1.setting, ledStripRoom1.brightness)+'lesy{}{:03d}'.format(int(ledLightRoom2.flag), ledLightRoom2.brightness)+'lela{}{:03d}'.format(int(spootLightRoom1.flag), spootLightRoom1.brightness), client)
        #        log.add_log("Wyslano dane UDP")
        #    except:
        #        log.add_log("Blad danych dla UDP")
        if(messag.find('sterTV.') != -1):
            strt = messag.find(".")+1
            if int(messag[(strt+9):(strt+12)]) >= 0:
                ledStripRoom1.setting = messag[(strt):(strt+9)]
                ledStripRoom1.brightness = int(messag[(strt+9):(strt+12)])
            light.set_light(ledStripRoom1.address, ledStripRoom1.brightness)
            ledStripRoom1.flagManualControl = True
        if(messag.find('sterTVjasnosc.') != -1):
            zmien = messag[14:17]
            if int(zmien) > 0:
                ledStripRoom1.brightness = int(zmien)
            light.set_light(ledStripRoom1.address, zmien)
            ledStripRoom1.flagManualControl = True
        if(messag.find('terrarium.') != -1):
            strt = messag.find(".T:")+1
            terrarium.tempUP = float(messag[(strt+2):(strt+6)])
            strt = messag.find("/W:")+1
            terrarium.humiUP = float(messag[(strt+2):(strt+5)])
            strt = messag.find(",t:")+1
            terrarium.tempDN = float(messag[(strt+2):(strt+6)])
            strt = messag.find("/w:")+1
            terrarium.humiDN = float(messag[(strt+2):(strt+5)])
            strt = messag.find("/I:")+1
            terrarium.uvi = float(messag[(strt+2):(strt+11)])
            log.add_log("   Terrarium TempUP: {}*C, humiUP: {}%  /  TempDN: {}*C, humiDN: {}*C  /  uvi: {}".format(
                terrarium.tempUP, terrarium.humiUP, terrarium.tempDN, terrarium.humiDN, terrarium.uvi))
            sql.add_record_terrarium(terrarium.tempUP, terrarium.humiUP,
                                     terrarium.tempDN, terrarium.humiDN, terrarium.uvi)
        if(messag.find('ko2') != -1):
            packet = "#05L" + messag[3:15]
            log.add_log(packet)
            nrf.to_send(ledStripRoom1.addresss, packet, ledStripRoom1.nrfPower)
            ledStripRoom1.flagManualControl = True
        if(messag.find('gra') != -1):
            packet = "#05G" + messag[3:6]
            log.add_log(packet)
            nrf.to_send(ledStripRoom1.addresss, packet, ledStripRoom1.nrfPower)
            ledStripRoom1.flagManualControl = True
        if(messag.find('lelw')):  # LAMPA LED white
            packet = "#06W" + messag[4:7]
            #nrf.to_send(ledStripRoom1.address, packet, ledStripRoom1.nrfPower)
        if(messag.find('pok1max') != -1):
            packet = "#05K255255255255"
            ledStripRoom1.setting = "255255255"
            ledStripRoom1.brightness = 255
            log.add_log(packet)
            log.add_log(packet)
            nrf.to_send(ledStripRoom1.address, packet, ledStripRoom1.nrfPower)
            # ikea.ikea_dim_group(ikea.ipAddress, ikea.user_id, ikea.securityid,
            #                     ikea.security_user, tradfriDev.salon, 100)
            ledStripRoom1.flagManualControl = True
            log.add_log("Tryb swiatel: Pokoj 1 max")
        if(messag.find('dogHouseTryb.') != -1):
            strt = messag.find(".")+1
            packet = "#15T" + messag[strt]
            nrf.to_send(dogHouse.address, packet, dogHouse.nrfPower)
            # light.set_light(ledStripRoom1.address,ledStripRoom1.brightness)
            # ledStripRoom1.flagManualControl=True
        if(messag.find('spij') != -1):
            light.set_light(ledStripRoom1.address, "000")
            ledStripRoom1.flagManualControl = True
            light.set_light(decorationRoom1.address, 0)
            light.set_light(decoration2Room1.address, 0)
            light.set_light(mainLightRoom1Tradfri.address, 0)
            light.set_light(mainLightRoom1Tradfri.bulb, 15)
            light.set_light(floorLampRoom1Tradfri.address, 0)
            decorationRoom1.flagManualControl = True
            decoration2Room1.flagManualControl = True
            decoration2Room1.flagManualControl = True
            Set_light_with_delay(mainLightRoom1Tradfri.address, 0, 30).start()
            Set_light_with_delay(decorationFlamingo.address, 0, 5*60).start()
            decorationFlamingo.flagManualControl = True
            Set_light_with_delay(kitchenLight.address, 0, 5*60).start()
            kitchenLight.flagManualControl = True
            log.add_log("Tryb swiatel: spij")
        if(messag.find('romantyczny') != -1):
            if(random.randint(0, 1) == 1):
                ledStripRoom1.setting = "255000{:03d}".format(random.randint(20, 120))
            else:
                ledStripRoom1.setting = "255{:03d}000".format(random.randint(20, 120))
            light.set_light(ledStripRoom1.address, ledStripRoom1.setting)
            if(random.randint(0, 1) == 1):
                kolor = "255000{:03d}".format(random.randint(20, 150))
            else:
                kolor = "255{:03d}000".format(random.randint(20, 150))
            light.set_light(floorLampRoom1Tradfri.address, kolor)
            light.set_light(floorLampRoom1Tradfri.address, 100)
            if(random.randint(0, 1) == 1):
                spootLightRoom1.setting = "255000{:03d}000".format(random.randint(20, 120))
            else:
                spootLightRoom1.setting = "255{:03d}000000".format(random.randint(20, 120))
            light.set_light(spootLightRoom1.address, 255)
            light.set_light(mainLightRoom1Tradfri.address, 0)
            ledStripRoom1.flagManualControl = True
            light.set_light(decorationRoom1.address, 0)
            decorationRoom1.flagManualControl = True
            light.set_light(decoration2Room1.address, 1)
            decoration2Room1.flagManualControl = True
            log.add_log("Tryb swiatel: romantyczny  --> "+packet)


socket = Socket("192.168.0.99", 2225)