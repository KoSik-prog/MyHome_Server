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
try:
    import threading
    from lib.log import *
    from devicesList import *
    from lib.infoStrip import *
    from lib.nrfConnect import *
    from lib.ikea import *
except ImportError:
    print("Modul Import Error")

class Set_light_with_delay(threading.Thread):
    def __init__(self, address, brightness, time):
        threading.Thread.__init__(self)
        self.address = address
        self.brightness = brightness
        self.time = time

    def run(self):
        time.sleep(self.time)
        if self.brightness == 0:
            light.set_light(self.address, 100)
        light.set_light(self.address, self.brightness)
        log.add_log("Funkacja spij dla adresu: {} wlaczona".format(self.address))


class LIGHTS_CL:
    def set_light(self, address, setting):
        if address == ledStripRoom1.address:  # TV
            packet = "#05K{}{:03d}".format(ledStripRoom1.setting, int(setting))
            if len(packet) >= 15:
                log.add_log("Ustawiono Led TV: {}".format(packet))
                infoStrip.add_info("światło TV: {}".format(setting))
                nrf.to_send(ledStripRoom1.address, packet, ledStripRoom1.nrfPower)
                ledStripRoom1.error += 1
            else:
                log.add_log("BLAD SKLADNI!: {}".format(packet))
        if address == ledLightRoom2.address:  # SYPIALNIA
            packet = "#S{:03d}".format(int(setting))
            if len(packet) >= 5:
                log.add_log("Ustawiono Led Sypialni: {}".format(packet))
                infoStrip.add_info("światło w sypialni: {}".format(setting))
                nrf.to_send(ledLightRoom2.address, packet, ledLightRoom2.nrfPower)
                ledLightRoom2.error += 1
            else:
                log.add_log("BLAD SKLADNI!: {}".format(packet))
        if address == kitchenLight.address:  # KUCHNIA
            packet = "#06T{:01d}".format(int(setting))
            if len(packet) >= 5:
                log.add_log("Ustawiono Led Kuchni: {}".format(packet))
                infoStrip.add_info("światło w kuchni: {}".format(setting))
                nrf.to_send(kitchenLight.address, packet, kitchenLight.nrfPower)
                kitchenLight.error += 1
            else:
                log.add_log("BLAD SKLADNI!: {}".format(packet))
        if address == spootLightRoom1.address:  # LAMPA 1 w salonie
            packet = "#05K{}{:03d}".format(spootLightRoom1.setting, int(setting))
            if len(packet) >= 5:
                spootLightRoom1.brightness = int(setting)
                log.add_log("Ustawiono Reflektor 1: {}".format(packet))
                infoStrip.add_info("reflektor 1 w salonie: {}/{}".format(spootLightRoom1.setting, int(setting)))
                nrf.to_send(spootLightRoom1.address, packet, spootLightRoom1.nrfPower)
                spootLightRoom1.error += 1
                if(int(setting) == 0):
                    spootLightRoom1.flag = 0
                else:
                    spootLightRoom1.flag = 1
            else:
                log.add_log("BLAD SKLADNI!: {}".format(packet))
        if address == decorationRoom1.address:  # dekoracje pok 1 / Reka
            packet = "#08T{:1d}".format(int(setting))
            if len(packet) >= 5:
                log.add_log("Ustawiono Lampa 1: {}".format(packet))
                infoStrip.add_info("dekoracje 1 w salonie: {}".format(setting))
                nrf.to_send(decorationRoom1.address, packet, decorationRoom1.nrfPower)
                spootLightRoom1.error += 1
            else:
                log.add_log("BLAD SKLADNI!: {}".format(packet))
        if address == decoration2Room1.address:  # dekoracje pok 1 / Eifla i inne
            packet = "#09T{:1d}".format(int(setting))
            if len(packet) >= 5:
                log.add_log("Ustawiono Lampa 2: {}".format(packet))
                infoStrip.add_info("dekoracje 2 w salonie: {}".format(setting))
                nrf.to_send(decoration2Room1.address, packet, decoration2Room1.nrfPower)
                decorationRoom1.error += 1
            else:
                log.add_log("BLAD SKLADNI!: {}".format(packet))
        if address == decorationFlamingo.address:  # FLAMING
            packet = "#10T{:1d}".format(int(setting))
            if len(packet) >= 5:
                log.add_log("Ustawiono Lampa Flaming: {}".format(packet))
                infoStrip.add_info("flaming: {}".format(setting))
                nrf.to_send(decorationFlamingo.address, packet, decorationFlamingo.nrfPower)
                decorationFlamingo.error += 1
            else:
                log.add_log("BLAD SKLADNI!: {}".format(packet))
        if address == usbPlug.address:  # Dekoracje - uniwersalny modul USB
            packet = "#11T{:1d}".format(int(setting))
            if len(packet) >= 5:
                log.add_log("Ustawiono Uniwersalny USB: {}".format(packet))
                infoStrip.add_info("uniwersalny USB: {}".format(setting))
                nrf.to_send(usbPlug.address, packet, usbPlug.nrfPower)
                usbPlug.error += 1
            else:
                log.add_log("BLAD SKLADNI!: {}".format(packet))
        if address == mainLightRoom1Tradfri.address:  # Tradfri Salon
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
        if address == diningRoomTradfri.address:  # Tradfri Jadalnia
            if setting == 0 or setting == 1:
                ikea.ikea_power_group(ikea.ipAddress, ikea.user_id, ikea.securityid,
                                      ikea.security_user, address, setting)
            elif setting > 1:
                ikea.ikea_dim_group(ikea.ipAddress, ikea.user_id, ikea.securityid, ikea.security_user, address, setting)
            log.add_log("Tradfri Jadalnia ->: {}".format(setting))
            infoStrip.add_info("oświetlenie w jadalni: {}".format(setting))
        if address == hallTradfri.address:  # Tradfri przedpokoj
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
        if address == floorLampRoom1Tradfri.address:  # Tradfri Lampa Duza
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
                                   floorLampRoom1Tradfri.address, chKolor1, chKolor2, chKolor3)
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
        if address == ledLightRoom2Tradfri.address:  # Tradfri Sypialnia
            if setting == 0 or setting == 1:
                ikea.ikea_power_group(ikea.ipAddress, ikea.user_id, ikea.securityid,
                                      ikea.security_user, ledLightRoom2Tradfri.address, setting)
                ledLightRoom2Tradfri.flag = False
            elif setting > 1:
                ikea.ikea_dim_group(ikea.ipAddress, ikea.user_id, ikea.securityid,
                                    ikea.security_user, ledLightRoom2Tradfri.address, setting)
                ikea.ikea_power_group(ikea.ipAddress, ikea.user_id, ikea.securityid,
                                      ikea.security_user, ledLightRoom2Tradfri.address, 1)
                ledLightRoom2Tradfri.flag = True
            log.add_log("Tradfri Sypialnia ->: {}".format(setting))
            infoStrip.add_info("oświetlenie w sypialni: {}".format(setting))
        if address == hydroponics.address:  # hydroponics
            if int(setting) > 1:
                packet = "#17P1"  # wlacz pompe
            else:
                packet = "#17A{:01d}".format(int(setting))
            if len(packet) >= 5:
                log.add_log("Ustawiono Hydroponike: {}".format(packet))
                infoStrip.add_info("hydroponics: {}".format(setting))
                nrf.to_send(hydroponics.address, packet, hydroponics.nrfPower)
            else:
                log.add_log("BLAD SKLADNI!: {}".format(packet))


light = LIGHTS_CL()
