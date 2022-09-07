#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        displayBrightness
# Purpose:
#
# Author:      KoSik
#
# Created:     18.05.2022
# Copyright:   (c) kosik 2022
#-------------------------------------------------------------------------------
try:
    import time, smbus
except ImportError:
    print "Import error - displayBrightness"

from lib.log import *
from lib.gui import *
import rpi_backlight as backlight


class DISPLAY_BRIGHTNESS_CL:
    swiatlo = 0

    def read_brightness(self):
        bus = smbus.SMBus(1)
        bus.write_byte_data(0x39, 0x00 | 0x80, 0x03)
        bus.write_byte_data(0x39, 0x01 | 0x80, 0x02)
        time.sleep(0.5)
        data = bus.read_i2c_block_data(0x39, 0x0C | 0x80, 2)
        ch0 = data[1] * 256 + data[0]
        return int(ch0)

    def set_brightness(self): #----STEROWANIE WYSWIETLACZEM - WATEK
        swiatlo_old=0
        while(1):
            self.swiatlo = self.read_brightness()
            gui.swiatlo = self.swiatlo
            if self.swiatlo > (swiatlo_old+15) or self.swiatlo < (swiatlo_old - 15): 
                if self.swiatlo < 7:
                    jasnoscwysw = 11
                elif self.swiatlo >= 7 and self.swiatlo < 100:
                    jasnoscwysw=int(((0.645 * self.swiatlo) + 5.4838) + 11)
                elif self.swiatlo>=100 and self.swiatlo < 1000:
                    jasnoscwysw=int(((0.193 * self.swiatlo) + 50.67) + 11)
                elif self.swiatlo>=1000:
                    jasnoscwysw=255
                backlight.set_brightness(jasnoscwysw, smooth=True, duration=2)  # ustawienie jasnosci LCD
                #log.add_log("Jasnosc wyswietlacza:{}   / old:{}, new:{}".format(jasnoscwysw, swiatlo_old, self.swiatlo))
                swiatlo_old = self.swiatlo
            time.sleep(5)
displayBrightness = DISPLAY_BRIGHTNESS_CL()