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
    print "Blad importu UDP"

from libraries.log import *
from lights import *

class UDP_CL:
    #Adresy  ==>>
    AdresLedTV = 1
    AdresSypialnia = 2
    AdresLampa1 = 3
    AdresKuchnia = 4
    AdresLampa2 = 5 #Dekoracje 1 REKA
    AdresLampa3 = 6 #Dekoracje 2 Eifla
    AdresFlaming = 7 #Dekoracje Flaming
    AdresUsb = 8 #Modul uniwersalny USB
    AdresCzujnikKwiatka1 = 9
    AdresCzujnikKwiatka2 = 10
    AdresCzujnikKwiatka3 = 11
    AdresBuda = 12
    AdresCzujnikKwiatka4 = 13
    AdresHydroponika = 15

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
            pocz=messag.find(".")+1
            chJasnosc=int(messag[pocz:pocz+3])
            if(chJasnosc>=0 and chJasnosc<=100):
                light.set_light(lampaPok1Tradfri.Adres, str(chJasnosc))
            else:
                log.add_log("Blad danych! -> {}".format(chJasnosc))
        if(messag.find('tradfriLampaJasn.') != -1):   # LAMPA W SALONIE
            pocz=messag.find(".")+1
            chJasnosc=int(messag[pocz:pocz+3])
            if(chJasnosc>=0 and chJasnosc<=100):
                light.set_light(lampaDuzaTradfri.Adres, str(chJasnosc))
            else:
                log.add_log("Blad danych! -> {}".format(chJasnosc))
        if(messag.find('tradfriLampaKol.') != -1):   # LAMPA W SALONIE
            pocz=messag.find(".")+1
            light.set_light(lampaDuzaTradfri.Adres, messag[pocz:pocz+9])
        if(messag.find('swiatloSypialni.') != -1):   # SYPIALNIA
            pocz=messag.find(".")+1
            chJasnosc=int(messag[pocz:pocz+3])
            lampaPok2.Jasnosc=chJasnosc
            light.set_light(lampaPok2Tradfri.Adres,lampaPok2.Jasnosc)
            light.set_light(lampaPok2.Adres,lampaPok2.Jasnosc)
            lampaPok2.FlagaSterowanieManualne=True
            dekoFlaming.FlagaSterowanieManualne=True
            light.set_light(dekoFlaming.Adres,messag[pocz])
        if(messag.find('swiatloSypialniTradfri.') != -1):   # SYPIALNIA TRADFRI
            pocz=messag.find(".")+1
            chJasnosc=int(messag[pocz])
            light.set_light(lampaPok2Tradfri.Adres,chJasnosc)
        if(messag.find('swiatloJadalniTradfri.') != -1):   # Jadalnia TRADFRI
            pocz=messag.find(".")+1
            chJasnosc=int(messag[pocz])
            light.set_light(lampaJadalniaTradfri.Adres,chJasnosc)
        if(messag.find('swiatlokuchni.') != -1):  # KUCHNIA
            pocz=messag.find(".")+1
            light.set_light(self.AdresKuchnia,messag[pocz])
            lampaKuch.FlagaSterowanieManualne=True
        if(messag.find('swiatloPrzedpokoj.') != -1):  # PRZEDPOKOJ
            pocz=messag.find(".")+1
            chJasnosc=int(messag[pocz:len(messag)])
            light.set_light(lampaPrzedpokojTradfri.Adres,chJasnosc)
        if(messag.find('reflektor1.') != -1): # REFLEKTOR LED COLOR
            lampa1Pok1.Ustawienie=messag[11:23]
            lampa1Pok1.Jasnosc=messag[23:26]
            light.set_light(self.AdresLampa1,lampa1Pok1.Jasnosc)
        if(messag.find('reflektor1kolor.') != -1): # REFLEKTOR LED COLOR KOLOR
            lampa1Pok1.Ustawienie=messag[16:28]
            light.set_light(lampa1Pok1.Adres,lampa1Pok1.Jasnosc)
        if(messag.find('reflektor1jasn.') != -1): # REFLEKTOR LED COLOR JASNOSC
            lampa1Pok1.Jasnosc=messag[15:18]
            light.set_light(lampa1Pok1.Adres,lampa1Pok1.Jasnosc)
        if(messag.find('dekoracjePok1.') != -1): # DEKORACJE POKOJ 1
            pocz=messag.find(".")+1
            light.set_light(dekoPok1.Adres, messag[pocz])
            dekoPok1.FlagaSterowanieManualne=True
            light.set_light(deko2Pok1.Adres, messag[pocz])
        if(messag.find('dekoracjePok2.') != -1): # DEKORACJE POKOJ 2
            pocz=messag.find(".")+1
            dekoFlaming.FlagaSterowanieManualne=True
            light.set_light(dekoFlaming.Adres, messag[pocz])
        if(messag.find('dekoracjeUSB.') != -1): # uniwersalny modul USB
            pocz=messag.find(".")+1
            dekoUsb.FlagaSterowanieManualne=True
            light.set_light(dekoUsb.Adres,messag[pocz])
        if(messag.find('hydroponika.') != -1): # Hydroponika
            pocz=messag.find(".")+1
            dekoUsb.FlagaSterowanieManualne=True
            light.set_light(self.AdresHydroponika,messag[pocz])
        if(messag=='?m'):
            try:
                self.s.sendto('temz{:04.1f}wilz{:04.1f}tem1{:04.1f}wil1{:04.1f}tem2{:04.1f}wil2{:04.1f}'.format(czujnikZew.temp,czujnikZew.humi,czujnikPok1.temp,czujnikPok1.humi,czujnikPok2.temp,czujnikPok2.humi)+'wilk{:03d}slok{:03d}wodk{:03d}zask{:03d}'.format(int(czujnikKwiatek.wilgotnosc),int(czujnikKwiatek.slonce),int(czujnikKwiatek.woda),int(czujnikKwiatek.zasilanie))+'letv{}{}{}'.format(int(lampaTV.Flaga),lampaTV.Ustawienie,lampaTV.Jasnosc)+'lesy{}{:03d}'.format(int(lampaPok2.Flaga),lampaPok2.Jasnosc)+'lela{}{:03d}'.format(int(lampa1Pok1.Flaga),lampa1Pok1.Jasnosc), adres)
                log.add_log("Wyslano dane UDP")
            except:
                log.add_log("Blad danych dla UDP")
        if(messag.find('sterTV.') != -1):
            pocz=messag.find(".")+1
            if int(messag[(pocz+9):(pocz+12)])>=0:
                lampaTV.Ustawienie=messag[(pocz):(pocz+9)]
                lampaTV.Jasnosc=int(messag[(pocz+9):(pocz+12)])
            light.set_light(self.AdresLedTV, lampaTV.Jasnosc)
            lampaTV.FlagaSterowanieManualne=True
        if(messag.find('sterTVjasnosc.') != -1):
            zmien=messag[14:17]
            if int(zmien)>0:
                lampaTV.Jasnosc=int(zmien)
            light.set_light(self.AdresLedTV, zmien)
            lampaTV.FlagaSterowanieManualne=True
        if(messag.find('terrarium.') != -1):
            pocz=messag.find(".T:")+1
            terrarium.tempUP=float(messag[(pocz+2):(pocz+6)])
            pocz=messag.find("/W:")+1
            terrarium.wilgUP=float(messag[(pocz+2):(pocz+5)])
            pocz=messag.find(",t:")+1
            terrarium.tempDN=float(messag[(pocz+2):(pocz+6)])
            pocz=messag.find("/w:")+1
            terrarium.wilgDN=float(messag[(pocz+2):(pocz+5)])
            pocz=messag.find("/I:")+1
            terrarium.UVI=float(messag[(pocz+2):(pocz+11)])
            log.add_log("   Terrarium TempUP: {}*C, WilgUP: {}%  /  TempDN: {}*C, WilgDN: {}*C  /  UVI: {}".format(terrarium.tempUP,terrarium.wilgUP,terrarium.tempDN,terrarium.wilgDN,terrarium.UVI))
            sql.addRecordTerrarium(terrarium.tempUP,terrarium.wilgUP,terrarium.tempDN,terrarium.wilgDN,terrarium.UVI)
        if(messag.find('ko2') != -1):
            wiad="#05L" + messag[3:15]
            log.add_log(wiad)
            nrf.NRFwyslij(lampaTV.adress, wiad)
            lampaTV.FlagaSterowanieManualne=True
        if(messag.find('gra') != -1):
            wiad="#05G" + messag[3:6]
            log.add_log(wiad)
            nrf.NRFwyslij(lampaTV.adress, wiad)
            lampaTV.FlagaSterowanieManualne=True
        if(messag.find('lelw')): # LAMPA LED BIALY
            wiad="#06W" + messag[4:7]
            #nrf.NRFwyslij(lampaTV.address, wiad)
        if(messag.find('pok1max') != -1):
            wiad="#05K255255255255"
            lampaTV.Ustawienie="255255255"
            lampaTV.Jasnosc=255
            log.add_log(wiad)
            log.add_log(wiad)
            nrf.NRFwyslij(lampaTV.address, wiad)
            ikea.ikea_dim_group(ikea.ipAddress,ikea.user_id,ikea.securityid,ikea.security_user, tradfriDev.salon, 100)
            lampaTV.FlagaSterowanieManualne=True
            log.add_log("Tryb swiatel: Pokoj 1 max")
        if(messag.find('budaTryb.') != -1):
            pocz=messag.find(".")+1
            wiad="#15T" + messag[pocz]
            nrf.NRFwyslij(buda.address, wiad)
            #light.set_light(self.AdresLedTV,lampaTV.Jasnosc)
            #lampaTV.FlagaSterowanieManualne=True
        if(messag.find('spij') != -1):
            light.set_light(self.AdresLedTV,"000")
            lampaTV.FlagaSterowanieManualne=True
            light.set_light(lampaPok1Tradfri.Adres,0)
            light.set_light(lampaPok1Tradfri.Zarowka,15)
            #light.set_light(lampaJadalniaTradfri.Adres,0)
            #light.set_light(lampaPrzedpokojTradfri.Adres,100)
            light.set_light(lampaDuzaTradfri.Adres,0)
            light.set_light(dekoPok1.Adres,0)
            light.set_light(deko2Pok1.Adres,0)
            #light.set_light(lampa1Pok1.Adres,0)
            dekoPok1.FlagaSterowanieManualne=True
            deko2Pok1.FlagaSterowanieManualne=True
            deko2Pok1.FlagaSterowanieManualne=True
            set_light_with_delay(lampaPok1Tradfri.Adres, 0, 30)
            #set_light_with_delay(lampaPrzedpokojTradfri.Adres, 0, 31).start()
            #set_light_with_delay(dekoFlaming.Adres, 0, 30*60).start()
            dekoFlaming.FlagaSterowanieManualne=True
            log.add_log("Tryb swiatel: spij")
        if(messag.find('romantyczny') != -1):
            if(random.randint(0, 1)==1):
                lampaTV.Ustawienie="255000{:03d}".format(random.randint(20, 120))
            else:
                lampaTV.Ustawienie="255{:03d}000".format(random.randint(20, 120))
            light.set_light(lampaTV.Adres,lampaTV.Ustawienie)
            if(random.randint(0, 1)==1):
                kolor="255000{:03d}".format(random.randint(20, 150))
            else:
                kolor="255{:03d}000".format(random.randint(20, 150))
            light.set_light(lampaDuzaTradfri.Adres,kolor)
            light.set_light(lampaDuzaTradfri.Adres, 100)
            if(random.randint(0, 1)==1):
                lampa1Pok1.Ustawienie="255000{:03d}000".format(random.randint(20, 120))
            else:
                lampa1Pok1.Ustawienie="255{:03d}000000".format(random.randint(20, 120))
            light.set_light(lampa1Pok1.Adres, 255)
            light.set_light(lampaPok1Tradfri.Adres, 0)
            lampaTV.FlagaSterowanieManualne=True
            light.set_light(dekoPok1.Adres,0)
            dekoPok1.FlagaSterowanieManualne=True
            light.set_light(deko2Pok1.Adres,1)
            deko2Pok1.FlagaSterowanieManualne=True
            log.add_log("Tryb swiatel: romantyczny  --> "+wiad)
udp = UDP_CL(2222)