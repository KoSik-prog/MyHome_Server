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
try:
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
    import asyncio
    import subprocess
    from lib.firebase import *
    from lib.alarm import *
except ImportError:
    print("Import error - socket services")


class Socket:
    usersList = {"kosik" : "Majeczka11", "jusi" : "jw270307"}

    def __init__(self, host='192.168.0.99', port=2223):
        self.host = host
        self.port = port
        self.backlog = 5
        self.size = 1024
        self.server = None
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            self.s.bind((self.host, self.port))
            self.s.listen(self.backlog)
            log.add_log(f"Server successfully started on {self.host}:{self.port}")
        except OSError as e:
            log.add_log(f"Port {self.port} is already in use. Attempting to free it...")
            self.unlock_port(self.port)
            time.sleep(1)
            self.s.bind((self.host, self.port))
            self.s.listen(self.backlog)
            log.add_log(f"Server successfully restarted on {self.host}:{self.port}")

        self.loop = None
        self.stop_event = threading.Event()


    def server_thread(self):
        while server.read_server_active_flag() == True:
            try:
                client, address = self.s.accept() 
                receivedData = client.recv(self.size).decode('utf-8')
                if receivedData:
                    if(receivedData[0] == "!"):
                        self.returnSocketData(client, receivedData) 
                    if(receivedData[0] == "#"):
                        log.add_log("Socket transmit: {} / address:{}".format(receivedData, client))
                        self.transmit(client, receivedData)
                client.close()
            except (KeyboardInterrupt, SystemExit):
                log.add_log('server UDP error')
    
    def unlock_port(self, port):
        try:
            subprocess.run(['sudo', 'fuser', '-k', f'{port}/tcp'], check=True)
            log.add_log(f"Port {port} has been freed.")
        except subprocess.CalledProcessError as e:
            log.add_log(f"Failed to free port {port}: {e}")

    def stop_server(self):
        if self.s:
            self.s.close()
            print("Server socket closed.")

    def sendSocketMsg(self, client, msg):
        encoded_msg = msg.encode('utf-8')
        client.send(encoded_msg)

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
            self.sendSocketMsg(client, toSend)
            
        if(message.find("getDevicesData") != -1):
            jsonData = []
            jsonData.append(decorationRoom1.get_json_data())
            jsonData.append(decoration2Room1.get_json_data())
            jsonData.append(decorationFlamingo.to_dict())
            jsonData.append(hydroponics.to_dict())
            jsonData.append(ledStripRoom1.get_json_data())
            jsonData.append(kitchenLight.to_dict())
            jsonData.append(ledDeskRoom3.get_json_data())
            jsonData.append(ledLego.get_json_data())
            jsonData.append(ledPhotosHeart.get_json_data())
            jsonData.append(ledTerrace.get_json_data())
            jsonData.append(usbPlug.get_json_data())
            toSend = json.dumps(jsonData)
            self.sendSocketMsg(client, toSend)

        if(message.find("setDeviceData") != -1):
            strt = message.find(".")+1
            objectData = message[strt:]
            try:
                data_dict = json.loads(objectData)
                device_name = data_dict.get("name", "")
                if device_name:
                    device_obj = globals().get(device_name)()
                    device_obj.from_dict(data_dict)
                    print(device_obj.to_dict())
                    self.sendSocketMsg(client, '{"status": "ok"}')
                else:
                    log.add_log("Device name not provided in data")
                    self.sendSocketMsg(client, '{"status": "ok"}')
            except json.JSONDecodeError:
               log.add_log("Invalid JSON data")
               self.sendSocketMsg(client, '{"status": "ok"}')
            
        if(message.find("getTasmotaData") != -1):
            toSend = json.dumps(tasmota.get_json_data())
            self.sendSocketMsg(client, toSend)
            
        if(message.find("getErrorsData") != -1):
            toSend = json.dumps(infoStrip.get_errors_array())
            self.sendSocketMsg(client, toSend)
            
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

        if(message.find('alarm.') != -1):
            alarmMsg = message[message.find(".")+1:]
            alarm.alarm("Alarm!", alarmMsg)
            phoneNotification.send_notification("Alarm!", alarmMsg)
            log.add_log("ALARM! -> {}".format(alarmMsg))

        if(message.find('notify.') != -1):
            alarmMsg = message[message.find(".")+1:]
            alarm.alarm("Powiadomienie", alarmMsg)
            # phoneNotification.send_notification("Alarm!", alarmMsg)
            # log.add_log("ALARM! -> {}".format(alarmMsg))

        if(message.find('alarmDeactivate.') != -1):
            try:
                dTime = message[message.find(".")+1:]
                deactiveTime = int(dTime)
                if deactiveTime == 0:
                    alarm.activate_alarm()
                else:
                    alarm.deactivate_alarm(int(deactiveTime))
            except:
                log.add_log("Can't deactivate alarm!")

            
        if(message.find('set^') != -1):
            for device in deviceArray:
                res = device.handle_socketService(message)
                if res[0] == True:
                    self.sendSocketMsg(client, res[1])
                    return True


            # if(message.find('hydroponics.') != -1):  # hydroponics
            #     strt = message.find(".")+1
            #     hydroponics.set_param('flagManualControl', True)
            #     light.set_light(hydroponics.get_param('address'), message[strt])
            #     self.sendSocketMsg(client, "ok")
            # elif(message.find('usbPlug.') != -1):  # uniwersalny modul USB
            #     strt = message.find(".")+1
            #     usbPlug.set_param('flagManualControl', True)
            #     light.set_light(usbPlug.get_param('address'), message[strt])
            # elif(message.find('kitchenlight.') != -1):  # KUCHNIA
            #     strt = message.find(".")+1
            #     kitchenLight.set_param('flagManualControl', True)
            #     light.set_light(kitchenLight.get_param('address'), message[strt])
            #     self.sendSocketMsg(client, "ok")
            # elif(message.find('ledstripecolor.') != -1):
            #     strt = message.find(".")+1
            #     setting = message[strt:]
            #     if len(setting) > 9:
            #         ledStripRoom1.set_param('setting', setting[:9])
            #         ledStripRoom1.brightness = int(setting[9:])
            #     else:
            #         ledStripRoom1.setting = setting
            #     light.set_light(ledStripRoom1.get_param('address'), ledStripRoom1.brightness)
            #     ledStripRoom1.set_param('flagManualControl', True)
            #     self.sendSocketMsg(client, "ok")
            # res = ledStripRoom1.handle_socketService(message)
            # if res[0] == True:
            #     self.sendSocketMsg(client, res[1])
            #     return True
            # elif(message.find('ledstripebrightness.') != -1):
            #     strt = message.find(".")+1
            #     setting = int(message[strt:])
            #     ledStripRoom1.set_param('brightness', int(setting))
            #     light.set_light(ledStripRoom1.get_param('address'), setting)
            #     ledStripRoom1.set_param('flagManualControl', True)
            #     self.sendSocketMsg(client, "ok")

            # res = decorationRoom1.handle_socketService(message)
            # res = decoration2Room1.handle_socketService(message)
            # if res[0] == True:
            #     self.sendSocketMsg(client, res[1])
            #     return True
            # elif(message.find('room1Decorations.') != -1):
            #     strt = message.find(".")+1
            #     light.set_light(decorationRoom1.get_param('address'), message[strt])
            #     decorationRoom1.set_param('flagManualControl', True)
            #     light.set_light(decoration2Room1.get_param('address'), message[strt])
            #     self.sendSocketMsg(client, "ok")

            # res = decorationFlamingo.handle_socketService(message)
            # if res[0] == True:
            #     self.sendSocketMsg(client, res[1])
            #     return True
            # elif(message.find('room2Decorations.') != -1): 
            #     strt = message.find(".")+1
            #     decorationFlamingo.set_param('flagManualControl', True)
            #     light.set_light(decorationFlamingo.get_param('address'), message[strt])
            #     self.sendSocketMsg(client, "ok")
            # elif(message.find('ledDesk.') != -1):
            # res = ledDeskRoom3.handle_socketService(message)
            # if res[0] == True:
            #     self.sendSocketMsg(client, res[1])
            #     return True
                # strt = message.find(".")+1
                # settingBuffer = message[strt:]
                # if(settingBuffer.isdigit()):
                #     if int(settingBuffer) > 100:
                #         settingBuffer = 100
                #     setting = int(settingBuffer)
                #     self.sendSocketMsg(client, "ok")
                # else:
                #     setting = 0
                #     self.sendSocketMsg(client, "setting error")  
                # # ledDeskRoom3.set_param('brightness', setting)
                # light.set_light(ledDeskRoom3.get_param('address'), str(setting))
                # ledDeskRoom3.set_param('flagManualControl', True)
            # res = ledLego.handle_socketService(message)
            # if res[0] == True:
            #     self.sendSocketMsg(client, res[1])
            #     return True
            # elif(message.find('ledLego.') != -1):
            #     strt = message.find(".")+1
            #     settingBuffer = message[strt:]
            #     if(settingBuffer.isdigit()):
            #         if int(settingBuffer) > 100:
            #             settingBuffer = 100
            #         setting = int(settingBuffer)
            #         self.sendSocketMsg(client, "ok")
            #     else:
            #         setting = 0
            #         self.sendSocketMsg(client, "setting error")  
            #     # ledDeskRoom3.set_param('brightness', setting)
            #     light.set_light(ledLego.get_param('address'), str(setting))
            #     ledLego.set_param('flagManualControl', True)
            # res = ledTerrace.handle_socketService(message)
            # if res[0] == True:
            #     self.sendSocketMsg(client, res[1])
            #     return True
            # elif(message.find('ledTerrace.') != -1):
            #     strt = message.find(".")+1
            #     settingBuffer = message[strt:]
            #     if(settingBuffer.isdigit()):
            #         if int(settingBuffer) > 100:
            #             settingBuffer = 100
            #         setting = int(settingBuffer)
            #         self.sendSocketMsg(client, "ok")
            #     else:
            #         setting = 0
            #         self.sendSocketMsg(client, "setting error")  
            #     # ledTerrace.set_param('brightness', setting)
            #     light.set_light(ledTerrace.get_param('address'), str(setting))
            #     ledTerrace.set_param('flagManualControl', True)
            if(message.find('ledHeart.') != -1):
                strt = message.find(".")+1
                settingBuffer = message[strt:]
                if(settingBuffer.isdigit()):
                    if int(settingBuffer) > 100:
                        settingBuffer = 100
                    setting = int(settingBuffer)
                    self.sendSocketMsg(client, "ok")
                else:
                    setting = 0
                    self.sendSocketMsg(client, "setting error")  
                ledPhotosHeart.set_param('brightness', setting)
                light.set_light(ledPhotosHeart.get_param('address'), str(setting))
                ledPhotosHeart.set_param('flagManualControl', True)
            elif(message.find('room1TradfriLampBrightness.') != -1):   # TRADFRI
                strt = message.find(".")+1
                brightness = int(message[strt:])
                if(brightness >= 0 and brightness <= 100):
                    light.set_light(floorLampRoom1Tradfri.get_param('address'), str(brightness))
                else:
                    log.add_log("Tradfri brightness error! -> {}".format(brightness))
                self.sendSocketMsg(client, "ok")
            elif(message.find('room1TradfriLampColor.') != -1):
                strt = message.find(".")+1
                color = message[strt:]
                if len(color) == 9:
                    light.set_light(floorLampRoom1Tradfri.get_param('address'), color)
                else:
                    log.add_log("Tradfri color error! -> {}".format(color))
                self.sendSocketMsg(client, "ok")
            elif(message.find('themeSleep') != -1):   # THEMES
                ledStripRoom1.set_param('flagManualControl', True)
                light.set_light(ledStripRoom1.get_param('address'), "000")
                light.set_light(mainLightRoom1Tradfri.get_param('address'), 0)
                light.set_light(mainLightRoom1Tradfri.bulb, 15)
                light.set_light(floorLampRoom1Tradfri.get_param('address'), 0)
                decorationRoom1.set_param('flagManualControl', True)
                light.set_light(decorationRoom1.get_param('address'), 0)
                decoration2Room1.set_param('flagManualControl', True)
                light.set_light(decoration2Room1.get_param('address'), 0)
                usbPlug.set_param('flagManualControl', True)
                light.set_light(usbPlug.get_param('address'), 0)
                light.set_light(ledLego.get_param('address'), 0)
                light.set_light(ledDeskRoom3.get_param('address'), 0)
                decorationFlamingo.set_param('flagManualControl', True)
                Set_light_with_delay(decorationFlamingo.get_param('address'), 0, 5*60).start()
                kitchenLight.set_param('flagManualControl', True)
                Set_light_with_delay(kitchenLight.get_param('address'), 0, 5*60).start()
                Set_light_with_delay(ledPhotosHeart.get_param('address'), 0, 2*60).start()
                Set_light_with_delay(mainLightRoom1Tradfri.get_param('address'), 0, 30).start()
                log.add_log("Theme: sleep")
            elif(message.find('themeRomantic') != -1):
                if(random.randint(0, 1) == 1):
                    ledStripRoom1.set_param('setting', "255000{:03d}".format(random.randint(20, 120)))
                else:
                    ledStripRoom1.set_param('setting', "255{:03d}000".format(random.randint(20, 120)))
                ledStripRoom1.set_param('flagManualControl', True)
                light.set_light(ledStripRoom1.get_param('address'), ledStripRoom1.get_param('setting'))
                if(random.randint(0, 1) == 1):
                    color = "255000{:03d}".format(random.randint(20, 150))
                else:
                    color = "255{:03d}000".format(random.randint(20, 150))
                light.set_light(floorLampRoom1Tradfri.get_param('address'), color)
                light.set_light(floorLampRoom1Tradfri.get_param('address'), 100)
                if(random.randint(0, 1) == 1):
                    spootLightRoom1.setting = "255000{:03d}000".format(random.randint(20, 120))
                else:
                    spootLightRoom1.setting = "255{:03d}000000".format(random.randint(20, 120))
                light.set_light(spootLightRoom1.get_param('address'), 255)
                light.set_light(mainLightRoom1Tradfri.get_param('address'), 0)
                decorationRoom1.set_param('flagManualControl', True)
                light.set_light(decorationRoom1.get_param('address'), 0)
                decoration2Room1.set_param('flagManualControl', True)
                light.set_light(decoration2Room1.get_param('address'), 1)
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
            self.sendSocketMsg(client, toSend)
        if(message.find('refreshFirebaseToken^') != -1):
            strt = message.find("^") + 1
            login = message[strt:]
            dataArray = login.split(".")
            logUser = dataArray[0]
            logPassword = dataArray[1]
            if len(dataArray) > 2:
                logToken = dataArray[2]
                phoneNotification.update_token(logUser, logToken)
            log.add_log(f"LOG -> {logUser}:{logPassword} - {logToken}")
            try:
                passwordToCheck = self.usersList[logUser.lower()]
            except:
                passwordToCheck = ""
                log.add_log("user not found")
                
            if(logPassword == passwordToCheck):
                log.add_log(f"user {logUser} has logged in")
                toSend = "OK"
            else:
                log.add_log("access denied")
                toSend = "denied"
            self.sendSocketMsg(client, toSend)

    async def transmit(self, client, messag):
        if(messag.find('set^') != -1):
            if(messag.find('hydroponics.') != -1):  # hydroponics
                strt = messag.find(".")+1
                hydroponics.set_param('flagManualControl', True)
                light.set_light(hydroponics.get_param('address'), messag[strt])
            elif(messag.find('kitchenlight.') != -1):  # KUCHNIA
                strt = messag.find(".")+1
                kitchenLight.set_param('flagManualControl', True)
                light.set_light(kitchenLight.get_param('address'), messag[strt])
                self.sendSocketMsg(client, "ok")
            elif(messag.find('ledstripecolor.') != -1):
                strt = messag.find(".")+1
                if int(messag[(strt+9):(strt+12)]) >= 0:
                    ledStripRoom1.setting = messag[(strt):(strt+9)]
                    ledStripRoom1.brightness = int(messag[(strt+9):(strt+12)])
                light.set_light(ledStripRoom1.get_param('address'), ledStripRoom1.brightness)
                ledStripRoom1.set_param('flagManualControl', True)
            elif(messag.find('ledstripebrightness.') != -1):
                zmien = messag[14:17]
                if int(zmien) > 0:
                    ledStripRoom1.brightness = int(zmien)
                light.set_light(ledStripRoom1.get_param('address'), zmien)
                ledStripRoom1.set_param('flagManualControl', True)
        #---------------------------------------------------------------------------------
        if(messag.find('salonOswietlenie.') != -1):   # SALON
            strt = messag.find(".")+1
            chJasnosc = int(messag[strt:strt+3])
            if(chJasnosc >= 0 and chJasnosc <= 100):
                light.set_light(mainLightRoom1Tradfri.get_param('address'), str(chJasnosc))
            else:
                log.add_log("Blad danych! -> {}".format(chJasnosc))
        if(messag.find('tradfriLampaJasn.') != -1):   # LAMPA W SALONIE
            strt = messag.find(".")+1
            chJasnosc = int(messag[strt:strt+3])
            if(chJasnosc >= 0 and chJasnosc <= 100):
                light.set_light(floorLampRoom1Tradfri.get_param('address'), str(chJasnosc))
            else:
                log.add_log("Blad danych! -> {}".format(chJasnosc))
        if(messag.find('tradfriLampaKol.') != -1):   # LAMPA W SALONIE
            strt = messag.find(".")+1
            light.set_light(floorLampRoom1Tradfri.get_param('address'), messag[strt:strt+9])
        if(messag.find('swiatloSypialni.') != -1):   # SYPIALNIA
            strt = messag.find(".")+1
            chJasnosc = int(messag[strt:strt+3])
            ledPhotosHeart.brightness = chJasnosc
            light.set_light(ledLightRoom2Tradfri.get_param('address'), ledPhotosHeart.brightness)
            light.set_light(ledPhotosHeart.get_param('address'), ledPhotosHeart.brightness)
            ledPhotosHeart.set_param('flagManualControl', True)
            decorationFlamingo.set_param('flagManualControl', True)
            light.set_light(decorationFlamingo.get_param('address'), messag[strt])
        if(messag.find('swiatloSypialniTradfri.') != -1):   # SYPIALNIA TRADFRI
            strt = messag.find(".")+1
            chJasnosc = int(messag[strt])
            light.set_light(ledLightRoom2Tradfri.get_param('address'), chJasnosc)
        if(messag.find('swiatloJadalniTradfri.') != -1):   # Jadalnia TRADFRI
            strt = messag.find(".")+1
            chJasnosc = int(messag[strt])
            light.set_light(diningRoomTradfri.get_param('address'), chJasnosc)
        if(messag.find('swiatlokuchni.') != -1):  # KUCHNIA
            strt = messag.find(".")+1
            light.set_light(kitchenLight.get_param('address'), messag[strt])
            kitchenLight.set_param('flagManualControl', True)
        if(messag.find('swiatloPrzedpokoj.') != -1):  # PRZEDPOKOJ
            strt = messag.find(".")+1
            chJasnosc = int(messag[strt:len(messag)])
            light.set_light(hallTradfri.get_param('address'), chJasnosc)
        if(messag.find('reflektor1.') != -1):  # REFLEKTOR LED COLOR
            spootLightRoom1.setting = messag[11:23]
            spootLightRoom1.brightness = messag[23:26]
            light.set_light(spootLightRoom1.get_param('address'), spootLightRoom1.get_param('brightness'))
        if(messag.find('reflektor1kolor.') != -1):  # REFLEKTOR LED COLOR
            spootLightRoom1.setting = messag[16:28]
            light.set_light(spootLightRoom1.get_param('address'), spootLightRoom1.get_param('brightness'))
        if(messag.find('reflektor1jasn.') != -1):  # REFLEKTOR LED COLOR JASNOSC
            spootLightRoom1.brightness = messag[15:18]
            light.set_light(spootLightRoom1.get_param('address'), spootLightRoom1.get_param('brightness'))
        if(messag.find('dekoracjePok1.') != -1):  # DEKORACJE POKOJ 1
            strt = messag.find(".")+1
            light.set_light(decorationRoom1.get_param('address'), messag[strt])
            decorationRoom1.set_param('flagManualControl', True)
            light.set_light(decoration2Room1.get_param('address'), messag[strt])
        if(messag.find('dekoracjePok2.') != -1):  # DEKORACJE POKOJ 2
            strt = messag.find(".")+1
            decorationFlamingo.set_param('flagManualControl', True)
            light.set_light(decorationFlamingo.get_param('address'), messag[strt])
        if(messag.find('hydroponics.') != -1):  # hydroponics
            strt = messag.find(".")+1
            hydroponics.set_param('flagManualControl', True)
            light.set_light(hydroponics.get_param('address'), messag[strt])
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
                ledStripRoom1.set_param('setting', messag[(strt):(strt+9)])
                ledStripRoom1.set_param('brightness', int(messag[(strt+9):(strt+12)]))
            light.set_light(ledStripRoom1.get_param('address'), ledStripRoom1.get_param('brightness'))
            ledStripRoom1.set_param('flagManualControl', True)
        if(messag.find('sterTVjasnosc.') != -1):
            zmien = messag[14:17]
            if int(zmien) > 0:
                ledStripRoom1.set_param('brightness', int(zmien))
            light.set_light(ledStripRoom1.get_param('address'), zmien)
            ledStripRoom1.set_param('flagManualControl', True)
        # if(messag.find('terrarium.') != -1):
        #     strt = messag.find(".T:")+1
        #     terrarium.tempUP = float(messag[(strt+2):(strt+6)])
        #     strt = messag.find("/W:")+1
        #     terrarium.humiUP = float(messag[(strt+2):(strt+5)])
        #     strt = messag.find(",t:")+1
        #     terrarium.tempDN = float(messag[(strt+2):(strt+6)])
        #     strt = messag.find("/w:")+1
        #     terrarium.humiDN = float(messag[(strt+2):(strt+5)])
        #     strt = messag.find("/I:")+1
        #     terrarium.uvi = float(messag[(strt+2):(strt+11)])
        #     log.add_log("   Terrarium TempUP: {}*C, humiUP: {}%  /  TempDN: {}*C, humiDN: {}*C  /  uvi: {}".format(
        #         terrarium.tempUP, terrarium.humiUP, terrarium.tempDN, terrarium.humiDN, terrarium.uvi))
        #     sql.add_record_terrarium(terrarium.tempUP, terrarium.humiUP,
        #                              terrarium.tempDN, terrarium.humiDN, terrarium.uvi)
        if(messag.find('ko2') != -1):
            packet = "#05L" + messag[3:15]
            log.add_log(packet)
            nrf.to_send(ledStripRoom1.get_param('address'), packet, ledStripRoom1.get_param('nrfPower'))
            ledStripRoom1.set_param('flagManualControl', True)
        if(messag.find('gra') != -1):
            packet = "#05G" + messag[3:6]
            log.add_log(packet)
            nrf.to_send(ledStripRoom1.get_param('address'), packet, ledStripRoom1.get_param('nrfPower'))
            ledStripRoom1.set_param('flagManualControl', True)
        if(messag.find('lelw')):  # LAMPA LED white
            packet = "#06W" + messag[4:7]
            #nrf.to_send(ledStripRoom1.get_param('address'), packet, ledStripRoom1.get_param('nrfPower'))
        if(messag.find('pok1max') != -1):
            packet = "#05K255255255255"
            ledStripRoom1.set_param('setting', "255255255")
            ledStripRoom1.set_param('brightness', 255)
            log.add_log(packet)
            log.add_log(packet)
            nrf.to_send(ledStripRoom1.get_param('address'), packet, ledStripRoom1.get_param('nrfPower'))
            # ikea.ikea_dim_group(ikea.ipAddress, ikea.user_id, ikea.securityid,
            #                     ikea.security_user, tradfriDev.salon, 100)
            ledStripRoom1.set_param('flagManualControl', True)
            log.add_log("Tryb swiatel: Pokoj 1 max")
        if(messag.find('spij') != -1):
            light.set_light(ledStripRoom1.get_param('address'), "000")
            ledStripRoom1.set_param('flagManualControl', True)
            light.set_light(decorationRoom1.get_param('address'), 0)
            light.set_light(decoration2Room1.get_param('address'), 0)
            light.set_light(mainLightRoom1Tradfri.get_param('address'), 0)
            light.set_light(mainLightRoom1Tradfri.get_param('bulb'), 15)
            light.set_light(floorLampRoom1Tradfri.get_param('address'), 0)
            decorationRoom1.set_param('flagManualControl', True)
            decoration2Room1.set_param('flagManualControl', True)
            decoration2Room1.set_param('flagManualControl', True)
            Set_light_with_delay(mainLightRoom1Tradfri.get_param('address'), 0, 30).start()
            Set_light_with_delay(decorationFlamingo.get_param('address'), 0, 5*60).start()
            decorationFlamingo.set_param('flagManualControl', True)
            Set_light_with_delay(kitchenLight.get_param('address'), 0, 5*60).start()
            kitchenLight.set_param('flagManualControl', True)
            log.add_log("Tryb swiatel: spij")
        if(messag.find('romantyczny') != -1):
            if(random.randint(0, 1) == 1):
                ledStripRoom1.set_param('setting', "255000{:03d}".format(random.randint(20, 120)))
            else:
                ledStripRoom1.set_param('setting', "255{:03d}000".format(random.randint(20, 120)))
            light.set_light(ledStripRoom1.get_param('address'), ledStripRoom1.get_param('setting'))
            if(random.randint(0, 1) == 1):
                kolor = "255000{:03d}".format(random.randint(20, 150))
            else:
                kolor = "255{:03d}000".format(random.randint(20, 150))
            light.set_light(floorLampRoom1Tradfri.get_param('address'), kolor)
            light.set_light(floorLampRoom1Tradfri.get_param('address'), 100)
            if(random.randint(0, 1) == 1):
                spootLightRoom1.set_param('setting', "255000{:03d}000".format(random.randint(20, 120)))
            else:
                spootLightRoom1.set_param('setting', "255{:03d}000000".format(random.randint(20, 120)))
            light.set_light(spootLightRoom1.get_param('address'), 255)
            light.set_light(mainLightRoom1Tradfri.get_param('address'), 0)
            ledStripRoom1.set_param('flagManualControl', True)
            light.set_light(decorationRoom1.get_param('address'), 0)
            decorationRoom1.set_param('flagManualControl', True)
            light.set_light(decoration2Room1.get_param('address'), 1)
            decoration2Room1.set_param('flagManualControl', True)
            log.add_log("Tryb swiatel: romantyczny  --> "+packet)

socket_server = Socket()