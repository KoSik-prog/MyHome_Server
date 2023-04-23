#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:        display
# Purpose:
#
# Author:      KoSik
#
# Created:     1.03.2021
# Copyright:   (c) kosik 2021
# -------------------------------------------------------------------------------
try:
    import sys
    import os
    import pygame
    import pygame.mixer
    import pygame.gfxdraw
    import glob
    from pygame.locals import *
    from pygame.compat import unichr_, unicode_
    from pygame.locals import *
    from pygame.compat import geterror
    from lib.log import *
except ImportError:
    print("Import error - display")

pygame.init()

class Display:
    pygame.display.set_caption('MojDom')
    resolution = 800, 480
    #screen = pygame.display.set_mode(resolution, pygame.FULLSCREEN)
    screen = pygame.display.set_mode(resolution, 1)

    def __init__(self, imgFolder):
        self.screen.fill((255, 255, 255))
        pygame.mouse.set_cursor((8, 8), (0, 0), (0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0))
        self.imgFolder = imgFolder

        self.brokenClouds = self.load_image(imgFolder, "Broken_Clouds.gif")
        self.clearSky = self.load_image(imgFolder, "Clear_Sky.gif")
        self.clearSkyNight = self.load_image(imgFolder, "Clear_Sky_Night.gif")
        self.fewClouds = self.load_image(imgFolder, "Few_Clouds.gif")
        self.fog = self.load_image(imgFolder, "Mist.gif")
        self.rain = self.load_image(imgFolder, "Rain.gif")
        self.scatteredClouds = self.load_image(imgFolder, "Scattered_Clouds.gif")
        self.scatteredCloudsNight = self.load_image(imgFolder, "Scattered_Clouds_Night.gif")
        self.showerRain = self.load_image(imgFolder, "Shower_Rain.gif")
        self.snow = self.load_image(imgFolder, "Snow.gif")
        self.thunderstorm = self.load_image(imgFolder, "Thunderstorm.gif")
        # ---
        self.dCloudy = self.load_image(imgFolder, "Cloudy.jpg")
        self.dCloudyNight = self.load_image(imgFolder, "Cloudy_Night.jpg")
        self.dFewClouds = self.load_image(imgFolder, "Few_Clouds.jpg")
        self.dFewCloudsNight = self.load_image(imgFolder, "Few_Clouds_Night.jpg")
        self.dFog = self.load_image(imgFolder, "Fog.jpg")
        self.dRain = self.load_image(imgFolder, "Rain.jpg")
        self.dSnow = self.load_image(imgFolder, "Snow.jpg")
        self.dSnowNight = self.load_image(imgFolder, "Snow_Night.jpg")
        self.dTStorm = self.load_image(imgFolder, "T-Storm.jpg")
        self.dTStorm2 = self.load_image(imgFolder, "T-Storm2.jpg")
        self.dClearSky = self.load_image(imgFolder, "Sun.jpg")
        self.dClearSkyNight = self.load_image(imgFolder, "Clear_Night.jpg")
        # ---
        self.na = self.load_image(imgFolder, "na.gif")
        self.arrow_down = self.load_image(imgFolder, "arrow_down.gif")
        self.arrow_up = self.load_image(imgFolder, "arrow_up.gif")
        self.snowflake1 = self.load_image(imgFolder, "snowflake1.gif")
        self.snowflake2 = self.load_image(imgFolder, "snowflake2.gif")
        self.snowflake3 = self.load_image(imgFolder, "snowflake3.gif")
        self.snowflake4 = self.load_image(imgFolder, "snowflake4.gif")
        self.snowflake5 = self.load_image(imgFolder, "snowflake5.gif")
        self.snowflake6 = self.load_image(imgFolder, "snowflake6.gif")
        self.rainAnim1 = self.load_image(imgFolder, "rain_anim1.gif")
        # ---
        self.tempin = self.load_image(imgFolder, "temp_in.gif")
        self.tempout = self.load_image(imgFolder, "temp_out.gif")
        self.wind = self.load_image(imgFolder, "wind.gif")

    def get_background(self, night, iconName):
        iconName = iconName.lower()
        if(iconName.find('01') != -1):  # CLEAR SKY
            if(night == True):
                pic = self.dClearSkyNight.convert()
            else:
                pic = self.dClearSky.convert()
        elif(iconName.find('02') != -1):  # FEW CLOUDS
            if(night == True):
                pic = self.dFewCloudsNight.convert()
            else:
                pic = self.dFewClouds.convert()
        elif(iconName.find('03') != -1):  # SCATTERED CLOUDS
            if(night == True):
                pic = self.dCloudyNight.convert()
            else:
                pic = self.dCloudy.convert()
        elif(iconName.find('04') != -1):  # BROKEN CLOUDS
            if(night == True):
                pic = self.dCloudyNight.convert()
            else:
                pic = self.dCloudy.convert()
        elif(iconName.find('09') != -1):  # SHOWER RAIN
            pic = self.dRain.convert()
        elif(iconName.find('10') != -1):  # RAIN
            pic = self.dRain.convert()
        elif(iconName.find('11') != -1):  # THUNDERSTORM
            pic = self.dTStorm.convert()
        elif(iconName.find('13') != -1):  # SNOW
            if(night == True):
                pic = self.dSnowNight.convert()
            else:
                pic = self.dSnow.convert()
        elif(iconName.find('50') != -1):  # mist - fog
            pic = self.dFog.convert()
        else:
            log.add_error_log("image not found: {}".format(iconName))
            pic = self.na.convert()
        return pic

    def get_icon(self, night, iconName):
        iconName = iconName.lower()
        if(iconName.find('01') != -1):  # CLEAR SKY
            if(night == True):
                pic = self.clearSkyNight.convert()
            else:
                pic = self.clearSky.convert()
        elif(iconName.find('02') != -1):  # FEW CLOUDS
            pic = self.fewClouds.convert()
        elif(iconName.find('03') != -1):  # SCATTERED CLOUDS
            pic = self.scatteredClouds.convert()
        elif(iconName.find('04') != -1):  # BROKEN CLOUDS
            pic = self.brokenClouds.convert()
        elif(iconName.find('09') != -1):  # SHOWER RAIN
            pic = self.showerRain.convert()
        elif(iconName.find('10') != -1):  # RAIN
            pic = self.rain.convert()
        elif(iconName.find('11') != -1):  # THUNDERSTORM
            pic = self.thunderstorm.convert()
        elif(iconName.find('13') != -1):  # SNOW
            pic = self.snow.convert()
        elif(iconName.find('50') != -1):  # mist - fog
            pic = self.fog.convert()
        else:
            log.add_error_log("image not found: {}".format(iconName))
            pic = self.na.convert()
        return pic

    def get_picture(self, iconName):
        if(iconName == "arrow_down"):
            foto = self.arrow_down.convert()
        elif(iconName == "arrow_up"):
            foto = self.arrow_up.convert()
        elif(iconName.find('anim') != -1):
            foto = self.rainAnim1.convert()
        elif(iconName.find('snowflake1') != -1):
            foto = self.snowflake1.convert()
        elif(iconName.find('snowflake2') != -1):
            foto = self.snowflake2.convert()
        elif(iconName.find('snowflake3') != -1):
            foto = self.snowflake3.convert()
        elif(iconName.find('snowflake4') != -1):
            foto = self.snowflake4.convert()
        elif(iconName.find('snowflake5') != -1):
            foto = self.snowflake5.convert()
        elif(iconName.find('snowflake6') != -1):
            foto = self.snowflake6.convert()
        elif(iconName.find("DTStorm2") != -1):
            foto = self.dTStorm2.convert()
        elif(iconName.find("temp_out") != -1):
            foto = self.tempout.convert()
        elif(iconName.find("temp_in") != -1):
            foto = self.tempin.convert()
        elif(iconName.find("wind") != -1):
            foto = self.wind.convert()
        else:
            foto = self.na.convert()
        return foto

    def load_image(self, folder, name):
        main_dir = os.path.split(os.path.abspath(__file__))[0]
        data_dir = os.path.join(main_dir, '../' + folder)
        fullname = os.path.join(data_dir, name)
        try:
            image = pygame.image.load(fullname)
        except pygame.error:
            log.add_log('Cannot load image:', fullname)
            raise SystemExit(str(geterror()))
        image = image.convert()
        return image

    def display_picture(self, screen, osx, osy, alpha, picture):
        picture = picture.convert_alpha()
        picture.set_alpha(alpha)
        screen.blit(picture, (osx, osy))

    def box(self, screen, x, y, w, h, color):
        pygame.gfxdraw.box(screen, Rect((x, y), (w, h)), color)

    def text_center(self, screen, text, font, size, x, y, color, alpha):
        a_sys_font = pygame.font.SysFont(font, size)
        ren = a_sys_font.render(unicode(text, 'utf-8'), True, color)
        ren.set_alpha(alpha)
        screen.blit(ren, (x - ren.get_width() // 2, y - ren.get_height() // 2))

    def text_center_background(self, screen, text, font, size, x, y, color, alpha, bgcolor):
        a_sys_font = pygame.font.SysFont(font, size)
        ren = a_sys_font.render(unicode(text, 'utf-8'), True, color)
        ren.set_alpha(alpha)
        self.box(screen, x - ren.get_width() // 2, y - ren.get_height() //
                 2, ren.get_width()+30, ren.get_height(), bgcolor)
        screen.blit(ren, (x - ren.get_width() // 2, y - ren.get_height() // 2))

    def text_background(self, screen, text, font, size, x, y, color, alpha, bgcolor):
        a_sys_font = pygame.font.SysFont(font, size)
        text = a_sys_font.render(unicode(text, 'utf-8'), True, color)
        text.set_alpha(alpha)
        self.box(screen, x, y, text.get_width()+30, text.get_height(), bgcolor)
        screen.blit(text, (x, y))

    def text2(self, screen, text, font, size, x, y, color, alpha):
        a_sys_font = pygame.font.SysFont(font, size)
        text = a_sys_font.render(unicode(text, 'utf-8'), True, color)
        text.set_alpha(alpha)
        screen.blit(text, (x, y))
        return text.get_width()

    def set_background_colour(self, colour):
        self.screen.fill(colour)

    def update(self):
        pygame.display.update()


display = Display('assets/img')
