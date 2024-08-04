#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:        lights
# Purpose:
#
# Author:      KoSik
#
# Created:     18.05.2022
# Copyright:   (c) kosik 2022
# -------------------------------------------------------------------------------
# try:
import threading
from lib.log import *
from devicesList import *
from lib.infoStrip import *
from lib.nrfConnect import *
from lib.ikea import *
# except ImportError:
#     print("Modul Import Error")

class Set_light_with_delay(threading.Thread):
    def __init__(self, address, brightness, time):
        threading.Thread.__init__(self)
        self.address = address
        self.brightness = brightness
        self.time = time

    def run(self):
        time.sleep(self.time)
        if self.brightness == 0:
            light.set_light(address, 100)
        light.set_light(address, self.brightness)
        log.add_log(f"Funkacja spij dla adresu: {address} wlaczona")


class LIGHTS_CL:
    def set_light(self, address, setting):
        if address == ledStripRoom1.get_param('address'):  # TV
            packet = "#05K{}{:03d}".format(ledStripRoom1.get_param('setting'), int(setting))
            if len(packet) >= 15:
                log.add_log("Ustawiono Led TV: {}".format(packet))
                infoStrip.add_info("światło TV: {}".format(setting))
                nrf.to_send(ledStripRoom1.get_param('address'), packet, ledStripRoom1.get_param('nrfPower'))
                ledStripRoom1.set_param('error', ledStripRoom1.get_param('error')+1)
            else:
                log.add_log("BLAD SKLADNI!: {}".format(packet))
        if address == ledDeskRoom3.get_param('address'):  # LED biurka
            packet = "#19P{:03d}".format(int(setting))
            if len(packet) >= 5:
                log.add_log("Ustawiono Led Biurka: {}".format(packet))
                infoStrip.add_info("światło biurka: {}".format(setting))
                nrf.to_send(ledDeskRoom3.get_param('address'), packet, ledDeskRoom3.get_param('nrfPower'))
                if int(setting) == 0:
                    ledDeskRoom3.set_param('flag', False)
                else:
                    ledDeskRoom3.set_param('flag', True)
                ledDeskRoom3.set_param('error', ledDeskRoom3.get_param('error')+1)
            else:
                log.add_log("BLAD SKLADNI!: {}".format(packet))
        if address == ledLego.get_param('address'):  # LED lego
            packet = "#20P{:03d}".format(int(setting))
            if len(packet) >= 5:
                log.add_log("Ustawiono Led LEGO: {}".format(packet))
                infoStrip.add_info("światło LEGO: {}".format(setting))
                nrf.to_send(ledLego.get_param('address'), packet, ledLego.get_param('nrfPower'))
                # if int(setting) == 0:
                #     ledLego.set_param('flag', 0)
                # else:
                #     ledLego.set_param('flag', 1)
                ledLego.set_param('error', ledLego.get_param('error')+1)
            else:
                log.add_log("BLAD SKLADNI!: {}".format(packet))
        if address == ledTerrace.get_param('address'):  # LED balkon
            packet = "#20P{:03d}".format(int(setting))
            if len(packet) >= 5:
                log.add_log("Ustawiono Led Balkonu: {}".format(packet))
                infoStrip.add_info("światło balkon: {}".format(setting))
                nrf.to_send(ledTerrace.get_param('address'), packet, ledTerrace.get_param('nrfPower'))
                if int(setting) == 0:
                    ledTerrace.set_param('flag', 0)
                else:
                    ledTerrace.set_param('flag', 1)
                ledTerrace.set_param('error', ledTerrace.get_param('error')+1)
            else:
                log.add_log("BLAD SKLADNI!: {}".format(packet))
        if address == ledPhotosHeart.get_param('address'):  # LED serce w sypialni
            packet = "#02P{:03d}".format(int(setting))
            if len(packet) >= 5:
                log.add_log("Ustawiono Led Serce: {}".format(packet))
                infoStrip.add_info("światło serce: {}".format(setting))
                nrf.to_send(ledPhotosHeart.get_param('address'), packet, ledPhotosHeart.get_param('nrfPower'))
                if int(setting) == 0:
                    ledPhotosHeart.set_param('flag', 0)
                else:
                    ledPhotosHeart.set_param('flag', 1)
                ledPhotosHeart.set_param('error', ledPhotosHeart.get_param('error')+1)
            else:
                log.add_log("BLAD SKLADNI!: {}".format(packet))
        if address == kitchenLight.get_param('address'):  # KUCHNIA
            packet = "#06T{:01d}".format(int(setting))
            if len(packet) >= 5:
                log.add_log("Ustawiono Led Kuchni: {}".format(packet))
                infoStrip.add_info("światło w kuchni: {}".format(setting))
                nrf.to_send(kitchenLight.get_param('address'), packet, kitchenLight.get_param('nrfPower'))
                kitchenLight.set_param('flag', int(setting))
                kitchenLight.set_param('error', kitchenLight.get_param('error')+1)
            else:
                log.add_log("BLAD SKLADNI!: {}".format(packet))
        if address == decorationRoom1.get_param('address'):  # dekoracje pok 1 / Reka
            packet = "#08T{:1d}".format(int(setting))
            if len(packet) >= 5:
                log.add_log("Ustawiono Lampa 1: {}".format(packet))
                infoStrip.add_info("dekoracje 1 w salonie: {}".format(setting))
                nrf.to_send(decorationRoom1.get_param('address'), packet, decorationRoom1.get_param('nrfPower'))
                decorationRoom1.set_param('error', decorationRoom1.get_param('error')+1)
                decorationRoom1.set_param('flag', int(setting))
            else:
                log.add_log("BLAD SKLADNI!: {}".format(packet))
        if address == decoration2Room1.get_param('address'):  # dekoracje pok 1 / Eifla i inne
            packet = "#09T{:1d}".format(int(setting))
            if len(packet) >= 5:
                log.add_log("Ustawiono Lampa 2: {}".format(packet))
                infoStrip.add_info("dekoracje 2 w salonie: {}".format(setting))
                nrf.to_send(decoration2Room1.get_param('address'), packet, decoration2Room1.get_param('nrfPower'))
                decoration2Room1.set_param('error', decoration2Room1.get_param('error')+1)
                decoration2Room1.set_param('flag', int(setting))
            else:
                log.add_log("BLAD SKLADNI!: {}".format(packet))
        if address == decorationFlamingo.get_param('address'):  # FLAMING
            packet = "#10T{:1d}".format(int(setting))
            if len(packet) >= 5:
                log.add_log("Ustawiono Lampa Flaming: {}".format(packet))
                infoStrip.add_info("flaming: {}".format(setting))
                nrf.to_send(decorationFlamingo.get_param('address'), packet, decorationFlamingo.get_param('nrfPower'))
                decorationFlamingo.set_param('error', decorationFlamingo.get_param('error')+1)
            else:
                log.add_log("BLAD SKLADNI!: {}".format(packet))
        if address == usbPlug.get_param('address'):  # Uniwersalny modul USB
            packet = "#11T{:1d}".format(int(setting))
            if len(packet) >= 5:
                log.add_log("Ustawiono Uniwersalny USB: {}".format(packet))
                infoStrip.add_info("uniwersalny USB: {}".format(setting))
                nrf.to_send(usbPlug.get_param('address'), packet, usbPlug.get_param('nrfPower'))
                usbPlug.set_param('error', usbPlug.get_param('error')+1)
                usbPlug.set_param('flag', int(setting))
            else:
                log.add_log("BLAD SKLADNI!: {}".format(packet))
        if address == mainLightRoom1Tradfri.get_param('address'):  # Tradfri Salon
            if setting == 0 or setting == 1:
                ikea.ikea_power_group(ikea.ipAddress, ikea.user_id, ikea.securityid,
                                      ikea.security_user, address, setting)
            elif setting > 1:
                ikea.ikea_dim_group(ikea.ipAddress, ikea.user_id, ikea.securityid, ikea.security_user, address, setting)
            log.add_log("Tradfri Salon ->: {}".format(setting))
            infoStrip.add_info("oświetlenie w salonie: {}".format(setting))
        if address == mainLightRoom1Tradfri.bulb:  # Tradfri Salon bulb
            if setting == 0 or setting == 1:
                ikea.ikea_power_light(ikea.ipAddress, ikea.user_id, ikea.securityid,
                                      ikea.security_user, address, setting)
            elif setting > 1:
                ikea.ikea_dim_light(ikea.ipAddress, ikea.user_id, ikea.securityid, ikea.security_user, address, setting)
            log.add_log("Tradfri Salon-bulb ->: {}".format(setting))
        if address == diningRoomTradfri.get_param('address'):  # Tradfri Jadalnia
            if setting == 0 or setting == 1:
                ikea.ikea_power_group(ikea.ipAddress, ikea.user_id, ikea.securityid,
                                      ikea.security_user, address, setting)
            elif setting > 1:
                ikea.ikea_dim_group(ikea.ipAddress, ikea.user_id, ikea.securityid, ikea.security_user, address, setting)
            log.add_log("Tradfri Jadalnia ->: {}".format(setting))
            infoStrip.add_info("oświetlenie w jadalni: {}".format(setting))
        if address == hallTradfri.get_param('address'):  # Tradfri przedpokoj
            if setting == 0 or setting == 1:
                ikea.ikea_power_group(ikea.ipAddress, ikea.user_id, ikea.securityid,
                                      ikea.security_user, address, setting)
            elif setting > 1:
                ikea.ikea_dim_group(ikea.ipAddress, ikea.user_id, ikea.securityid, ikea.security_user, address, setting)
            if(setting > 0):
                hallTradfri.status = 1
            else:
                hallTradfri.status = 0
            log.add_log("Tradfri Przedpokoj ->: {}".format(setting))
            infoStrip.add_info("oświetlenie w przedpokoju: {}".format(setting))
        if address == floorLampRoom1Tradfri.get_param('address'):  # Tradfri Lampa Duza
            if len(str(setting)) == 1:
                if int(setting) == 0 or int(setting) == 1:
                    ikea.ikea_power_light(ikea.ipAddress, ikea.user_id, ikea.securityid,
                                          ikea.security_user, address, int(setting))
                    log.add_log("Tradfri Lampa ON/OFF ->: {}".format(setting))
            elif len(str(setting)) == 9:
                chKolor1 = int(setting[0:3])
                chKolor2 = int(setting[3:6])
                chKolor3 = int(setting[6:9])
                ikea.ikea_RGB_lamp(ikea.ipAddress, ikea.user_id, ikea.securityid, ikea.security_user,
                                   floorLampRoom1Tradfri.get_param('address'), chKolor1, chKolor2, chKolor3)
                log.add_log("Tradfri Lampa kolor ->: {}".format(setting))
                infoStrip.add_info("lampa w salonie -> kolor: {}".format(setting))
            elif len(str(setting)) == 2 or len(str(setting)) == 3:
                if int(setting) > 1 and int(setting) <= 100:
                    ikea.ikea_dim_light(ikea.ipAddress, ikea.user_id, ikea.securityid,
                                        ikea.security_user, address, int(setting))
                    log.add_log("Tradfri Lampa Jasnosc ->: {}".format(setting))
                    infoStrip.add_info("lampa w salonie: {}".format(setting))
            else:
                log.add_log("Tradfri error skladni")
        if address == ledLightRoom2Tradfri.get_param('address'):  # Tradfri Sypialnia
            if setting == 0 or setting == 1:
                ikea.ikea_power_group(ikea.ipAddress, ikea.user_id, ikea.securityid,
                                      ikea.security_user, ledLightRoom2Tradfri.get_param('address'), setting)
                ledLightRoom2Tradfri.flag = False
            elif setting > 1:
                ikea.ikea_dim_group(ikea.ipAddress, ikea.user_id, ikea.securityid,
                                    ikea.security_user, ledLightRoom2Tradfri.get_param('address'), setting)
                ikea.ikea_power_group(ikea.ipAddress, ikea.user_id, ikea.securityid,
                                      ikea.security_user, ledLightRoom2Tradfri.get_param('address'), 1)
                ledLightRoom2Tradfri.flag = True
            log.add_log("Tradfri Sypialnia ->: {}".format(setting))
            infoStrip.add_info("oświetlenie w sypialni: {}".format(setting))
        if address == hydroponics.get_param('address'):  # hydroponics
            if int(setting) > 1:
                packet = "#17P1"  # wlacz pompe
            else:
                packet = "#17A{:01d}".format(int(setting))
            if len(packet) >= 5:
                log.add_log("Ustawiono Hydroponike: {}".format(packet))
                infoStrip.add_info("hydroponics: {}".format(setting))
                nrf.to_send(hydroponics.get_param('address'), packet, hydroponics.get_param('nrfPower'))
            else:
                log.add_log("BLAD SKLADNI!: {}".format(packet))


light = LIGHTS_CL()
