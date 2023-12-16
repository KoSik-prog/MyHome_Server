#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:        web services
# Purpose:
#
# Author:      KoSik
#
# Created:     17.05.2022
# Copyright:   (c) kosik 2022
# -------------------------------------------------------------------------------
try:
    import socket
    import select
    from lib.log import *
    from lights import *
    from sensorOutside import *
    from lib.tasmota import *
except ImportError:
    print("Import error - web services")


class Udp:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def __init__(self, AddrOut):
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.s.bind(('', AddrOut))
        self.s.setblocking(0)
        ready = select.select([self.s], [], [], 1)

    def server(self):
        try:
            message, address = self.s.recvfrom(1024)
            log.add_log(log.actualDate() + " " + "Polaczenie %s: %s" % (address, message))
            self.transmit(message, address)
        except (KeyboardInterrupt, SystemExit):
            log.add_log('server UDP error')

    def readStatus(self):
        ready = select.select([self.s], [], [], 0.5)
        return ready

    def transmit(self, messag, adres):
        if(messag.find('set#') != -1):
            if(messag.find('hydroponics.') != -1):  # hydroponics
                strt = messag.find(".")+1
                hydroponics.flagManualControl = True
                light.set_light(hydroponics.address, messag[strt])
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
        if(messag.find('test') != -1):
            print(adres[0])
            self.s.connect((adres[0], adres[1]))
            msg = "działa!"
            MSGLEN = len(msg)
            totalsent = 0
            while totalsent < MSGLEN:
                sent = self.s.send(msg[totalsent:])
                if sent == 0:
                    raise RuntimeError("socket connection broken")
                totalsent = totalsent + sent
            print(tasmota.get_data())
            data = "działa!!!"
            self.s.send(data.encode())
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
        if(messag.find('usbPlug.') != -1):  # uniwersalny modul USB
            strt = messag.find(".")+1
            usbPlug.flagManualControl = True
            light.set_light(usbPlug.address, messag[strt])
        if(messag.find('hydroponics.') != -1):  # hydroponics
            strt = messag.find(".")+1
            usbPlug.flagManualControl = True
            light.set_light(hydroponics.address, messag[strt])
        if(messag == '?m'):
            try:
                self.s.sendto('temz{:04.1f}wilz{:04.1f}tem1{:04.1f}wil1{:04.1f}tem2{:04.1f}wil2{:04.1f}'.format(sensorOutside.temperature, sensorOutside.humidity, sensorRoom1Temperature.temp, sensorRoom1Temperature.humi, sensorRoom2Temperature.temp, sensorRoom2Temperature.humi)+'letv{}{}{}'.format(int(ledStripRoom1.flag), ledStripRoom1.setting, ledStripRoom1.brightness)+'lesy{}{:03d}'.format(int(ledPhotosHeart.flag), ledPhotosHeart.brightness)+'lela{}{:03d}'.format(int(spootLightRoom1.flag), spootLightRoom1.brightness), adres)
                log.add_log("Wyslano dane UDP")
            except:
                log.add_log("Blad danych dla UDP")
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
            nrf.to_send(ledStripRoom1.adress, packet, ledStripRoom1.nrfPower)
            ledStripRoom1.flagManualControl = True
        if(messag.find('gra') != -1):
            packet = "#05G" + messag[3:6]
            log.add_log(packet)
            nrf.to_send(ledStripRoom1.adress, packet, ledStripRoom1.nrfPower)
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
            ikea.ikea_dim_group(ikea.ipAddress, ikea.user_id, ikea.securityid,
                                ikea.security_user, tradfriDev.salon, 100)
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
            light.set_light(mainLightRoom1Tradfri.address, 0)
            light.set_light(mainLightRoom1Tradfri.bulb, 15)
            light.set_light(floorLampRoom1Tradfri.address, 0)
            light.set_light(decorationRoom1.address, 0)
            light.set_light(decoration2Room1.address, 0)
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


udp = Udp(2222)
