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

try:
    import socket, select
except ImportError:
    print "UDP import error"

from libraries.log import *
from lights import *

class UDP_CL:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def __init__(self, AddrOut):
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.s.bind(('', AddrOut))
        self.s.setblocking(0)
        ready=select.select([self.s],[],[],1)

    def server(self):
        try:
            message, address = self.s.recvfrom(1024)
            log.add_log(log.actualDate() +" " + "Polaczenie %s: %s" % (address, message))
            self.transmisja(message, address)
        except (KeyboardInterrupt, SystemExit):
            log.add_log('server UDP error')

    def readStatus(self):
        ready = select.select([self.s], [], [], 0.5)
        return ready


    def transmisja(self, messag, adres):
        if(messag.find('salonOswietlenie.') != -1):   # SALON
            strt=messag.find(".")+1
            chJasnosc=int(messag[strt:strt+3])
            if(chJasnosc>=0 and chJasnosc<=100):
                light.set_light(mainLightRoom1Tradfri.address, str(chJasnosc))
            else:
                log.add_log("Blad danych! -> {}".format(chJasnosc))
        if(messag.find('tradfriLampaJasn.') != -1):   # LAMPA W SALONIE
            strt=messag.find(".")+1
            chJasnosc=int(messag[strt:strt+3])
            if(chJasnosc>=0 and chJasnosc<=100):
                light.set_light(floorLampRoom1Tradfri.address, str(chJasnosc))
            else:
                log.add_log("Blad danych! -> {}".format(chJasnosc))
        if(messag.find('tradfriLampaKol.') != -1):   # LAMPA W SALONIE
            strt=messag.find(".")+1
            light.set_light(floorLampRoom1Tradfri.address, messag[strt:strt+9])
        if(messag.find('swiatloSypialni.') != -1):   # SYPIALNIA
            strt=messag.find(".")+1
            chJasnosc=int(messag[strt:strt+3])
            ledLightRoom2.Jasnosc=chJasnosc
            light.set_light(ledLightRoom2Tradfri.address,ledLightRoom2.Jasnosc)
            light.set_light(ledLightRoom2.address,ledLightRoom2.Jasnosc)
            ledLightRoom2.flagManualControl=True
            decorationFlamingo.flagManualControl=True
            light.set_light(decorationFlamingo.address,messag[strt])
        if(messag.find('swiatloSypialniTradfri.') != -1):   # SYPIALNIA TRADFRI
            strt=messag.find(".")+1
            chJasnosc=int(messag[strt])
            light.set_light(ledLightRoom2Tradfri.address,chJasnosc)
        if(messag.find('swiatloJadalniTradfri.') != -1):   # Jadalnia TRADFRI
            strt=messag.find(".")+1
            chJasnosc=int(messag[strt])
            light.set_light(diningRoomTradfri.address,chJasnosc)
        if(messag.find('swiatlokuchni.') != -1):  # KUCHNIA
            strt=messag.find(".")+1
            light.set_light(kitchenLight.address, messag[strt])
            kitchenLight.flagManualControl=True
        if(messag.find('swiatloPrzedpokoj.') != -1):  # PRZEDPOKOJ
            strt=messag.find(".")+1
            chJasnosc=int(messag[strt:len(messag)])
            light.set_light(hallTradfri.address,chJasnosc)
        if(messag.find('reflektor1.') != -1): # REFLEKTOR LED COLOR
            spootLightRoom1.setting=messag[11:23]
            spootLightRoom1.Jasnosc=messag[23:26]
            light.set_light(spootLightRoom1.address, spootLightRoom1.Jasnosc)
        if(messag.find('reflektor1kolor.') != -1): # REFLEKTOR LED COLOR KOLOR
            spootLightRoom1.setting=messag[16:28]
            light.set_light(spootLightRoom1.address,spootLightRoom1.Jasnosc)
        if(messag.find('reflektor1jasn.') != -1): # REFLEKTOR LED COLOR JASNOSC
            spootLightRoom1.Jasnosc=messag[15:18]
            light.set_light(spootLightRoom1.address,spootLightRoom1.Jasnosc)
        if(messag.find('dekoracjePok1.') != -1): # DEKORACJE POKOJ 1
            strt=messag.find(".")+1
            light.set_light(decorationRoom1.address, messag[strt])
            decorationRoom1.flagManualControl=True
            light.set_light(decoration2Room1.address, messag[strt])
        if(messag.find('dekoracjePok2.') != -1): # DEKORACJE POKOJ 2
            strt=messag.find(".")+1
            decorationFlamingo.flagManualControl=True
            light.set_light(decorationFlamingo.address, messag[strt])
        if(messag.find('dekoracjeUSB.') != -1): # uniwersalny modul USB
            strt=messag.find(".")+1
            usbPlug.flagManualControl=True
            light.set_light(usbPlug.address,messag[strt])
        if(messag.find('hyroponics.') != -1): # hyroponics
            strt=messag.find(".")+1
            usbPlug.flagManualControl=True
            light.set_light(self.address,messag[strt])
        if(messag=='?m'):
            try:
                self.s.sendto('temz{:04.1f}wilz{:04.1f}tem1{:04.1f}wil1{:04.1f}tem2{:04.1f}wil2{:04.1f}'.format(sensorOutsideTemperature.temp,sensorOutsideTemperature.humi,sensorRoom1Temperature.temp,sensorRoom1Temperature.humi,sensorRoom2Temperature.temp,sensorRoom2Temperature.humi)+'wilk{:03d}slok{:03d}wodk{:03d}zask{:03d}'.format(int(czujnikKwiatek.wilgotnosc),int(czujnikKwiatek.slonce),int(czujnikKwiatek.woda),int(czujnikKwiatek.power))+'letv{}{}{}'.format(int(ledStripRoom1.flag),ledStripRoom1.setting,ledStripRoom1.Jasnosc)+'lesy{}{:03d}'.format(int(ledLightRoom2.flag),ledLightRoom2.Jasnosc)+'lela{}{:03d}'.format(int(spootLightRoom1.flag),spootLightRoom1.Jasnosc), adres)
                log.add_log("Wyslano dane UDP")
            except:
                log.add_log("Blad danych dla UDP")
        if(messag.find('sterTV.') != -1):
            strt=messag.find(".")+1
            if int(messag[(strt+9):(strt+12)])>=0:
                ledStripRoom1.setting=messag[(strt):(strt+9)]
                ledStripRoom1.Jasnosc=int(messag[(strt+9):(strt+12)])
            light.set_light(ledStripRoom1.address, ledStripRoom1.Jasnosc)
            ledStripRoom1.flagManualControl=True
        if(messag.find('sterTVjasnosc.') != -1):
            zmien=messag[14:17]
            if int(zmien)>0:
                ledStripRoom1.Jasnosc=int(zmien)
            light.set_light(ledStripRoom1.address, zmien)
            ledStripRoom1.flagManualControl=True
        if(messag.find('terrarium.') != -1):
            strt=messag.find(".T:")+1
            terrarium.tempUP=float(messag[(strt+2):(strt+6)])
            strt=messag.find("/W:")+1
            terrarium.humiUP=float(messag[(strt+2):(strt+5)])
            strt=messag.find(",t:")+1
            terrarium.tempDN=float(messag[(strt+2):(strt+6)])
            strt=messag.find("/w:")+1
            terrarium.humiDN=float(messag[(strt+2):(strt+5)])
            strt=messag.find("/I:")+1
            terrarium.UVI=float(messag[(strt+2):(strt+11)])
            log.add_log("   Terrarium TempUP: {}*C, humiUP: {}%  /  TempDN: {}*C, humiDN: {}*C  /  UVI: {}".format(terrarium.tempUP,terrarium.humiUP,terrarium.tempDN,terrarium.humiDN,terrarium.UVI))
            sql.addRecordTerrarium(terrarium.tempUP,terrarium.humiUP,terrarium.tempDN,terrarium.humiDN,terrarium.UVI)
        if(messag.find('ko2') != -1):
            packet="#05L" + messag[3:15]
            log.add_log(packet)
            nrf.toSend(ledStripRoom1.adress, packet, ledStripRoom1.nrfPower)
            ledStripRoom1.flagManualControl=True
        if(messag.find('gra') != -1):
            packet="#05G" + messag[3:6]
            log.add_log(packet)
            nrf.toSend(ledStripRoom1.adress, packet, ledStripRoom1.nrfPower)
            ledStripRoom1.flagManualControl=True
        if(messag.find('lelw')): # LAMPA LED BIALY
            packet="#06W" + messag[4:7]
            #nrf.toSend(ledStripRoom1.address, packet, ledStripRoom1.nrfPower)
        if(messag.find('pok1max') != -1):
            packet="#05K255255255255"
            ledStripRoom1.setting="255255255"
            ledStripRoom1.Jasnosc=255
            log.add_log(packet)
            log.add_log(packet)
            nrf.toSend(ledStripRoom1.address, packet, ledStripRoom1.nrfPower)
            ikea.ikea_dim_group(ikea.ipAddress,ikea.user_id,ikea.securityid,ikea.security_user, tradfriDev.salon, 100)
            ledStripRoom1.flagManualControl=True
            log.add_log("Tryb swiatel: Pokoj 1 max")
        if(messag.find('dogHouseTryb.') != -1):
            strt=messag.find(".")+1
            packet="#15T" + messag[strt]
            nrf.toSend(dogHouse.address, packet, dogHouse.nrfPower)
            #light.set_light(ledStripRoom1.address,ledStripRoom1.Jasnosc)
            #ledStripRoom1.flagManualControl=True
        if(messag.find('spij') != -1):
            light.set_light(ledStripRoom1.address, "000")
            ledStripRoom1.flagManualControl=True
            light.set_light(mainLightRoom1Tradfri.address,0)
            light.set_light(mainLightRoom1Tradfri.bulb,15)
            #light.set_light(diningRoomTradfri.address,0)
            #light.set_light(hallTradfri.address,100)
            light.set_light(floorLampRoom1Tradfri.address,0)
            light.set_light(decorationRoom1.address,0)
            light.set_light(decoration2Room1.address,0)
            #light.set_light(spootLightRoom1.address,0)
            decorationRoom1.flagManualControl=True
            decoration2Room1.flagManualControl=True
            decoration2Room1.flagManualControl=True
            set_light_with_delay(mainLightRoom1Tradfri.address, 0, 30).start()
            #set_light_with_delay(hallTradfri.address, 0, 31).start()
            set_light_with_delay(decorationFlamingo.address, 0, 15*60).start()
            decorationFlamingo.flagManualControl=True
            log.add_log("Tryb swiatel: spij")
        if(messag.find('romantyczny') != -1):
            if(random.randint(0, 1)==1):
                ledStripRoom1.setting="255000{:03d}".format(random.randint(20, 120))
            else:
                ledStripRoom1.setting="255{:03d}000".format(random.randint(20, 120))
            light.set_light(ledStripRoom1.address,ledStripRoom1.setting)
            if(random.randint(0, 1)==1):
                kolor="255000{:03d}".format(random.randint(20, 150))
            else:
                kolor="255{:03d}000".format(random.randint(20, 150))
            light.set_light(floorLampRoom1Tradfri.address,kolor)
            light.set_light(floorLampRoom1Tradfri.address, 100)
            if(random.randint(0, 1)==1):
                spootLightRoom1.setting="255000{:03d}000".format(random.randint(20, 120))
            else:
                spootLightRoom1.setting="255{:03d}000000".format(random.randint(20, 120))
            light.set_light(spootLightRoom1.address, 255)
            light.set_light(mainLightRoom1Tradfri.address, 0)
            ledStripRoom1.flagManualControl=True
            light.set_light(decorationRoom1.address,0)
            decorationRoom1.flagManualControl=True
            light.set_light(decoration2Room1.address,1)
            decoration2Room1.flagManualControl=True
            log.add_log("Tryb swiatel: romantyczny  --> "+packet)
udp = UDP_CL(2222)