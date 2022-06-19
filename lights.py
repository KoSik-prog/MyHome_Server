#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        lights
# Purpose:
#
# Author:      KoSik
#
# Created:     18.05.2022
# Copyright:   (c) kosik 2022
#-------------------------------------------------------------------------------
try:
    import threading
except ImportError:
    print "Blad importu"

from libraries.log import *
from devicesList import *
from libraries.infoStrip import *
from libraries.nrfConnect import *
from libraries.ikea import *

#addressy  ==>>
addressLedTV = 1
addressSypialnia = 2
addressLampa1 = 3
addressKuchnia = 4
addressLampa2 = 5 #Dekoracje 1 REKA
addressLampa3 = 6 #Dekoracje 2 Eifla
addressFlaming = 7 #Dekoracje Flaming
addressUsb = 8 #Modul uniwersalny USB
addressCzujnikKwiatka1 = 9
addressCzujnikKwiatka2 = 10
addressCzujnikKwiatka3 = 11
addressBuda = 12
addressCzujnikKwiatka4 = 13
addressHydroponika = 15

class set_light_with_delay(threading.Thread): #------WATEK NADAWANIA NRF
    def __init__(self, address, jasnosc, czas):
        threading.Thread.__init__(self)
        self.address = address
        self.jasnosc = jasnosc
        self.czas = czas
    def run(self):
        time.sleep(self.czas)
        if self.jasnosc == 0:
            light.set_light(self.address, 100)
        light.set_light(self.address, self.jasnosc)
        log.add_log("Funkacja spij wlaczona")

class LIGHTS_CL:
    def set_light(self, address, setting):
        if address==lampaTV.address:   #TV
            wiad="#05K{}{:03d}".format(lampaTV.Ustawienie, int(setting))
            if len(wiad)>=15:
                log.add_log("Ustawiono Led TV: {}".format(wiad))
                infoStrip.add_info("światło TV: {}".format(setting))
                nrf.toSend(lampaTV.address, wiad, lampaTV.nrfPower)
                lampaTV.blad+=1
            else:
                log.add_log("BLAD SKLADNI!: {}".format(wiad))
        if address == lampaPok2.address:  #SYPIALNIA
            wiad="#S{:03d}".format(int(setting))
            if len(wiad)>=5:
                log.add_log("Ustawiono Led Sypialni: {}".format(wiad))
                infoStrip.add_info("światło w sypialni: {}".format(setting))
                nrf.toSend(lampaPok2.address, wiad, lampaPok2.nrfPower)
                lampaPok2.blad+=1
            else:
                log.add_log("BLAD SKLADNI!: {}".format(wiad))
        if address == lampaKuch.address:  #KUCHNIA
            wiad="#07T{:01d}".format(int(setting))
            if len(wiad)>=5:
                log.add_log("Ustawiono Led Kuchni: {}".format(wiad))
                infoStrip.add_info("światło w kuchni: {}".format(setting))
                nrf.toSend(lampaKuch.address, wiad, lampaKuch.nrfPower)
                lampaKuch.blad+=1
            else:
                log.add_log("BLAD SKLADNI!: {}".format(wiad))
        if address==lampa1Pok1.address:  # LAMPA 1 w salonie
            wiad="#05K{}{:03d}".format(lampa1Pok1.setting, int(setting))
            if len(wiad)>=5:
                lampa1Pok1.Jasnosc=int(setting)
                log.add_log("Ustawiono Reflektor 1: {}".format(wiad))
                infoStrip.add_info("reflektor 1 w salonie: {}/{}".format(lampa1Pok1.setting,int(setting)))
                nrf.toSend(lampa1Pok1.address, wiad, lampa1Pok1.nrfPower)
                lampa1Pok1.blad+=1
                if(int(setting) == 0):
                    lampa1Pok1.Flaga = 0
                else:
                    lampa1Pok1.Flaga = 1
            else:
                log.add_log("BLAD SKLADNI!: {}".format(wiad))
        if address==dekoPok1.address:  # dekoracje pok 1 / Reka
            wiad="#08T{:1d}".format(int(setting))
            if len(wiad)>=5:
                log.add_log("Ustawiono Lampa 1: {}".format(wiad))
                infoStrip.add_info("dekoracje 1 w salonie: {}".format(setting))
                nrf.toSend(dekoPok1.address, wiad, dekoPok1.nrfPower)
                lampa1Pok1.blad+=1
            else:
                log.add_log("BLAD SKLADNI!: {}".format(wiad))
        if address==deko2Pok1.address:  # dekoracje pok 1 / Eifla i inne
            wiad="#09T{:1d}".format(int(setting))
            if len(wiad)>=5:
                log.add_log("Ustawiono Lampa 2: {}".format(wiad))
                infoStrip.add_info("dekoracje 2 w salonie: {}".format(setting))
                nrf.toSend(deko2Pok1.address, wiad, deko2Pok1.nrfPower)
                dekoPok1.blad+=1
            else:
                log.add_log("BLAD SKLADNI!: {}".format(wiad))
        if address==dekoFlaming.address:  # FLAMING
            wiad="#10T{:1d}".format(int(setting))
            if len(wiad)>=5:
                log.add_log("Ustawiono Lampa Flaming: {}".format(wiad))
                infoStrip.add_info("flaming: {}".format(setting))
                nrf.toSend(dekoFlaming.address, wiad, dekoFlaming.nrfPower)
                dekoFlaming.blad+=1
            else:
                log.add_log("BLAD SKLADNI!: {}".format(wiad))
        if address==dekoUsb.address:  # Dekoracje - uniwersalny modul USB
            wiad="#11T{:1d}".format(int(setting))
            if len(wiad)>=5:
                log.add_log("Ustawiono Uniwersalny USB: {}".format(wiad))
                infoStrip.add_info("uniwersalny USB: {}".format(setting))
                nrf.toSend(dekoUsb.address, wiad, dekoUsb.nrfPower)
                dekoUsb.blad+=1
            else:
                log.add_log("BLAD SKLADNI!: {}".format(wiad))
        if address==lampaPok1Tradfri.address:  # Tradfri Salon
            if setting==0 or setting==1:
                ikea.ikea_power_group(ikea.ipAddress, ikea.user_id, ikea.securityid, ikea.security_user, address, setting)
            elif setting>1:
                ikea.ikea_dim_group(ikea.ipAddress, ikea.user_id, ikea.securityid, ikea.security_user, address, setting)
            log.add_log("Tradfri Salon ->: {}".format(setting))
            infoStrip.add_info("oświetlenie w salonie: {}".format(setting))
        if address==lampaPok1Tradfri.Zarowka:  # Tradfri Salon Zarowka
            if setting==0 or setting==1:
                ikea.ikea_power_light(ikea.ipAddress,ikea.user_id,ikea.securityid,ikea.security_user, address, setting)
            elif setting>1:
                ikea.ikea_dim_light(ikea.ipAddress,ikea.user_id,ikea.securityid,ikea.security_user, address, setting)
            log.add_log("Tradfri Salon-Zarowka ->: {}".format(setting))
        if address==lampaJadalniaTradfri.address:  # Tradfri Jadalnia
            if setting==0 or setting==1:
                ikea.ikea_power_group(ikea.ipAddress,ikea.user_id,ikea.securityid,ikea.security_user, address, setting)
            elif setting>1:
                ikea.ikea_dim_group(ikea.ipAddress,ikea.user_id,ikea.securityid,ikea.security_user, address, setting)
            log.add_log("Tradfri Jadalnia ->: {}".format(setting))
            infoStrip.add_info("oświetlenie w jadalni: {}".format(setting))
        if address==lampaPrzedpokojTradfri.address:  # Tradfri przedpokoj
            if setting==0 or setting==1:
                ikea.ikea_power_group(ikea.ipAddress,ikea.user_id,ikea.securityid,ikea.security_user, address, setting)
            elif setting>1:
                ikea.ikea_dim_group(ikea.ipAddress,ikea.user_id,ikea.securityid,ikea.security_user, address, setting)
            if(setting>0):
                lampaPrzedpokojTradfri.Status=1
            else:
                lampaPrzedpokojTradfri.Status=0
            log.add_log("Tradfri Przedpokoj ->: {}".format(setting))
            infoStrip.add_info("oświetlenie w przedpokoju: {}".format(setting))
        if address==lampaDuzaTradfri.address:  # Tradfri Lampa Duza
            if len(str(setting))==1:
                if int(setting)==0 or int(setting)==1:
                    ikea.ikea_power_light(ikea.ipAddress,ikea.user_id,ikea.securityid,ikea.security_user, address, int(setting))
                    log.add_log("Tradfri Lampa ON/OFF ->: {}".format(setting))
            elif len(str(setting))==9:
                chKolor1=int(setting[0:3])
                chKolor2=int(setting[3:6])
                chKolor3=int(setting[6:9])
                ikea.ikea_RGB_lamp(ikea.ipAddress,ikea.user_id,ikea.securityid,ikea.security_user, lampaDuzaTradfri.address, chKolor1, chKolor2, chKolor3)
                log.add_log("Tradfri Lampa kolor ->: {}".format(setting))
                infoStrip.add_info("lampa w salonie -> kolor: {}".format(setting))
            elif len(str(setting))==2 or len(str(setting))==3:
                if int(setting)>1 and int(setting)<=100:
                    ikea.ikea_dim_light(ikea.ipAddress,ikea.user_id,ikea.securityid,ikea.security_user, address, int(setting))
                    log.add_log("Tradfri Lampa Jasnosc ->: {}".format(setting))
                    infoStrip.add_info("lampa w salonie: {}".format(setting))
            else:
                log.add_log("Tradfri blad skladni")
        if address==lampaPok2Tradfri.address:  # Tradfri Sypialnia
            if setting==0 or setting==1:
                ikea.ikea_power_group(ikea.ipAddress,ikea.user_id,ikea.securityid,ikea.security_user, lampaPok2Tradfri.address, setting)
                lampaPok2Tradfri.Flaga = False
            elif setting>1:
                ikea.ikea_dim_group(ikea.ipAddress,ikea.user_id,ikea.securityid,ikea.security_user, lampaPok2Tradfri.address, setting)
                ikea.ikea_power_group(ikea.ipAddress,ikea.user_id,ikea.securityid,ikea.security_user, lampaPok2Tradfri.address, 1)
                lampaPok2Tradfri.Flaga = True
            log.add_log("Tradfri Sypialnia ->: {}".format(setting))
            infoStrip.add_info("oświetlenie w sypialni: {}".format(setting))
        if address==hydroponika.address:   #Hydroponika
            if int(setting) > 1:
                wiad="#17P1" #wlacz pompe
            else:
                wiad="#17A{:01d}".format(int(setting))
            if len(wiad)>=5:
                log.add_log("Ustawiono Hydroponike: {}".format(wiad))
                infoStrip.add_info("Hydroponika: {}".format(setting))
                nrf.toSend(hydroponika.address, wiad, hydroponika.nrfPower)
            else:
                log.add_log("BLAD SKLADNI!: {}".format(wiad))
light = LIGHTS_CL()