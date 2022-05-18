#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        others
# Purpose:
#
# Author:      KoSik
#
# Created:     17.05.2022
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

class ustawSwiatloZeZwloka(threading.Thread): #------WATEK NADAWANIA NRF
    def __init__(self, adres, jasnosc, czas):
        threading.Thread.__init__(self)
        self.adres = adres
        self.jasnosc = jasnosc
        self.czas = czas
    def run(self):
        time.sleep(self.czas)
        if self.jasnosc==0:
            sterowanieOswietleniem(self.adres,100)
        sterowanieOswietleniem(self.adres,self.jasnosc)
        log.add_log("Funkacja spij wlaczona")

def sterowanieOswietleniem(adres, ustawienie):
    if adres==lampaTV.Adres:   #TV
        wiad="#05K{}{:03d}".format(lampaTV.Ustawienie,int(ustawienie))
        if len(wiad)>=15:
            log.add_log("Ustawiono Led TV: {}".format(wiad))
            infoStrip.add_info("światło TV: {}".format(ustawienie))
            nrf.NRFwyslij(AdresLedTV,wiad)
            lampaTV.blad+=1
        else:
            log.add_log("BLAD SKLADNI!: {}".format(wiad))
    if adres==lampaPok2.Adres:  #SYPIALNIA
        wiad="#S{:03d}".format(int(ustawienie))
        if len(wiad)>=5:
            log.add_log("Ustawiono Led Sypialni: {}".format(wiad))
            infoStrip.add_info("światło w sypialni: {}".format(ustawienie))
            nrf.NRFwyslij(AdresSypialnia,wiad)
            lampaPok2.blad+=1
        else:
            log.add_log("BLAD SKLADNI!: {}".format(wiad))
    if adres==lampaKuch.Adres:  #KUCHNIA
        wiad="#07T{:01d}".format(int(ustawienie))
        if len(wiad)>=5:
            log.add_log("Ustawiono Led Kuchni: {}".format(wiad))
            infoStrip.add_info("światło w kuchni: {}".format(ustawienie))
            nrf.NRFwyslij(AdresKuchnia,wiad)
            lampaKuch.blad+=1
        else:
            log.add_log("BLAD SKLADNI!: {}".format(wiad))
    if adres==lampa1Pok1.Adres:  # LAMPA 1 w salonie
        wiad="#05K{}{:03d}".format(lampa1Pok1.Ustawienie, int(ustawienie))
        if len(wiad)>=5:
            lampa1Pok1.Jasnosc=int(ustawienie)
            log.add_log("Ustawiono Reflektor 1: {}".format(wiad))
            infoStrip.add_info("reflektor 1 w salonie: {}/{}".format(lampa1Pok1.Ustawienie,int(ustawienie)))
            nrf.NRFwyslij(AdresLampa1,wiad)
            lampa1Pok1.blad+=1
            if(int(ustawienie) == 0):
                lampa1Pok1.Flaga = 0
            else:
                lampa1Pok1.Flaga = 1
        else:
            log.add_log("BLAD SKLADNI!: {}".format(wiad))
    if adres==dekoPok1.Adres:  # dekoracje pok 1 / Reka
        wiad="#08T{:1d}".format(int(ustawienie))
        if len(wiad)>=5:
            log.add_log("Ustawiono Lampa 1: {}".format(wiad))
            infoStrip.add_info("dekoracje 1 w salonie: {}".format(ustawienie))
            nrf.NRFwyslij(dekoPok1.Adres,wiad)
            lampa1Pok1.blad+=1
        else:
            log.add_log("BLAD SKLADNI!: {}".format(wiad))
    if adres==deko2Pok1.Adres:  # dekoracje pok 1 / Eifla i inne
        wiad="#09T{:1d}".format(int(ustawienie))
        if len(wiad)>=5:
            log.add_log("Ustawiono Lampa 2: {}".format(wiad))
            infoStrip.add_info("dekoracje 2 w salonie: {}".format(ustawienie))
            nrf.NRFwyslij(deko2Pok1.Adres,wiad)
            dekoPok1.blad+=1
        else:
            log.add_log("BLAD SKLADNI!: {}".format(wiad))
    if adres==dekoFlaming.Adres:  # FLAMING
        wiad="#10T{:1d}".format(int(ustawienie))
        if len(wiad)>=5:
            log.add_log("Ustawiono Lampa Flaming: {}".format(wiad))
            infoStrip.add_info("flaming: {}".format(ustawienie))
            nrf.NRFwyslij(AdresFlaming,wiad)
            dekoFlaming.blad+=1
        else:
            log.add_log("BLAD SKLADNI!: {}".format(wiad))
    if adres==dekoUsb.Adres:  # Dekoracje - uniwersalny modul USB
        wiad="#11T{:1d}".format(int(ustawienie))
        if len(wiad)>=5:
            log.add_log("Ustawiono Uniwersalny USB: {}".format(wiad))
            infoStrip.add_info("uniwersalny USB: {}".format(ustawienie))
            nrf.NRFwyslij(AdresUsb,wiad)
            dekoUsb.blad+=1
        else:
            log.add_log("BLAD SKLADNI!: {}".format(wiad))
    if adres==lampaPok1Tradfri.Adres:  # Tradfri Salon
        if ustawienie==0 or ustawienie==1:
            ikea.ikea_power_group(ikea.ipAddress, ikea.user_id, ikea.securityid, ikea.security_user, adres, ustawienie)
        elif ustawienie>1:
            ikea.ikea_dim_group(ikea.ipAddress, ikea.user_id, ikea.securityid, ikea.security_user, adres, ustawienie)
        log.add_log("Tradfri Salon ->: {}".format(ustawienie))
        infoStrip.add_info("oświetlenie w salonie: {}".format(ustawienie))
    if adres==lampaPok1Tradfri.Zarowka:  # Tradfri Salon Zarowka
        if ustawienie==0 or ustawienie==1:
            ikea.ikea_power_light(ikea.ipAddress,ikea.user_id,ikea.securityid,ikea.security_user, adres, ustawienie)
        elif ustawienie>1:
            ikea.ikea_dim_light(ikea.ipAddress,ikea.user_id,ikea.securityid,ikea.security_user, adres, ustawienie)
        log.add_log("Tradfri Salon-Zarowka ->: {}".format(ustawienie))
    if adres==lampaJadalniaTradfri.Adres:  # Tradfri Jadalnia
        if ustawienie==0 or ustawienie==1:
            ikea.ikea_power_group(ikea.ipAddress,ikea.user_id,ikea.securityid,ikea.security_user, adres, ustawienie)
        elif ustawienie>1:
            ikea.ikea_dim_group(ikea.ipAddress,ikea.user_id,ikea.securityid,ikea.security_user, adres, ustawienie)
        log.add_log("Tradfri Jadalnia ->: {}".format(ustawienie))
        infoStrip.add_info("oświetlenie w jadalni: {}".format(ustawienie))
    if adres==lampaPrzedpokojTradfri.Adres:  # Tradfri przedpokoj
        if ustawienie==0 or ustawienie==1:
            ikea.ikea_power_group(ikea.ipAddress,ikea.user_id,ikea.securityid,ikea.security_user, adres, ustawienie)
        elif ustawienie>1:
            ikea.ikea_dim_group(ikea.ipAddress,ikea.user_id,ikea.securityid,ikea.security_user, adres, ustawienie)
        if(ustawienie>0):
            lampaPrzedpokojTradfri.Status=1
        else:
            lampaPrzedpokojTradfri.Status=0
        log.add_log("Tradfri Przedpokoj ->: {}".format(ustawienie))
        infoStrip.add_info("oświetlenie w przedpokoju: {}".format(ustawienie))
    if adres==lampaDuzaTradfri.Adres:  # Tradfri Lampa Duza
        if len(str(ustawienie))==1:
            if int(ustawienie)==0 or int(ustawienie)==1:
                ikea.ikea_power_light(ikea.ipAddress,ikea.user_id,ikea.securityid,ikea.security_user, adres, int(ustawienie))
                log.add_log("Tradfri Lampa ON/OFF ->: {}".format(ustawienie))
        elif len(str(ustawienie))==9:
            chKolor1=int(ustawienie[0:3])
            chKolor2=int(ustawienie[3:6])
            chKolor3=int(ustawienie[6:9])
            ikea.ikea_RGB_lamp(ikea.ipAddress,ikea.user_id,ikea.securityid,ikea.security_user, lampaDuzaTradfri.Adres, chKolor1, chKolor2, chKolor3)
            log.add_log("Tradfri Lampa kolor ->: {}".format(ustawienie))
            infoStrip.add_info("lampa w salonie -> kolor: {}".format(ustawienie))
        elif len(str(ustawienie))==2 or len(str(ustawienie))==3:
            if int(ustawienie)>1 and int(ustawienie)<=100:
                ikea.ikea_dim_light(ikea.ipAddress,ikea.user_id,ikea.securityid,ikea.security_user, adres, int(ustawienie))
                log.add_log("Tradfri Lampa Jasnosc ->: {}".format(ustawienie))
                infoStrip.add_info("lampa w salonie: {}".format(ustawienie))
        else:
            log.add_log("Tradfri blad skladni")
    if adres==lampaPok2Tradfri.Adres:  # Tradfri Sypialnia
        if ustawienie==0 or ustawienie==1:
            ikea.ikea_power_group(ikea.ipAddress,ikea.user_id,ikea.securityid,ikea.security_user, lampaPok2Tradfri.Adres, ustawienie)
            lampaPok2Tradfri.Flaga = False
        elif ustawienie>1:
            ikea.ikea_dim_group(ikea.ipAddress,ikea.user_id,ikea.securityid,ikea.security_user, lampaPok2Tradfri.Adres, ustawienie)
            ikea.ikea_power_group(ikea.ipAddress,ikea.user_id,ikea.securityid,ikea.security_user, lampaPok2Tradfri.Adres, 1)
            lampaPok2Tradfri.Flaga = True
        log.add_log("Tradfri Sypialnia ->: {}".format(ustawienie))
        infoStrip.add_info("oświetlenie w sypialni: {}".format(ustawienie))
    if adres==hydroponika.Adres:   #Hydroponika
        if int(ustawienie) > 1:
            wiad="#17P1" #wlacz pompe
        else:
            wiad="#17A{:01d}".format(int(ustawienie))
        if len(wiad)>=5:
            log.add_log("Ustawiono Hydroponike: {}".format(wiad))
            infoStrip.add_info("Hydroponika: {}".format(ustawienie))
            nrf.NRFwyslij(hydroponika.Adres,wiad)
        else:
            log.add_log("BLAD SKLADNI!: {}".format(wiad))