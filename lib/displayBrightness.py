#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:        displayBrightness
# Purpose:
#
# Author:      KoSik
#
# Created:     18.05.2022
# Copyright:   (c) kosik 2022
# -------------------------------------------------------------------------------
try:
    import time
    import smbus
    from lib.log import *
    import rpi_backlight as backlight
except ImportError:
    print("Import error - displayBrightness")

class DisplayBrightness:
    light = 0

    def read_brightness(self):
        bus = smbus.SMBus(1)
        bus.write_byte_data(0x39, 0x00 | 0x80, 0x03)
        bus.write_byte_data(0x39, 0x01 | 0x80, 0x02)
        time.sleep(0.5)
        data = bus.read_i2c_block_data(0x39, 0x0C | 0x80, 2)
        ch0 = data[1] * 256 + data[0]
        return int(ch0)

    def set_brightness_thread(self):
        lightOld = 0
        margin = 15

        while(1):
            self.light = self.read_brightness()
            if self.light > (lightOld+margin) or self.light < (lightOld-margin):
                if self.light < 7:
                    displayBrightness = 11
                elif self.light >= 7 and self.light < 100:
                    displayBrightness = int(((0.645 * self.light) + 5.4838) + 11)
                elif self.light >= 100 and self.light < 1000:
                    displayBrightness = int(((0.193 * self.light) + 50.67) + 11)
                elif self.light >= 1000:
                    displayBrightness = 255
                backlight.set_brightness(displayBrightness, smooth=True, duration=2)
                lightOld = self.light
            time.sleep(5)

    def get_light(self):
        return self.light

displayBrightness = DisplayBrightness()
