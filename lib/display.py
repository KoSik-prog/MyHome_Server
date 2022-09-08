#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys ,os
import pygame, pygame.mixer, pygame.gfxdraw, glob
from pygame.locals import *
from pygame.compat import unichr_, unicode_
from pygame.locals import *
from pygame.compat import geterror

from lib.log import *

pygame.init()

class DISPLAY_CL:
    pygame.display.set_caption('MojDom')
    resolution = 800, 480
    #screen = pygame.display.set_mode(resolution, pygame.FULLSCREEN)
    screen = pygame.display.set_mode(resolution,1)

    def __init__(self):
        self.screen.fill((255,255,255))
        pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))

        self.BrokenClouds = self.load_image('assets/pic', "Broken_Clouds.gif")
        self.ClearSky = self.load_image('assets/pic', "Clear_Sky.gif")
        self.ClearSkyNight = self.load_image('assets/pic', "Clear_Sky_Night.gif")
        self.FewClouds = self.load_image('assets/pic', "Few_Clouds.gif")
        self.Fog = self.load_image('assets/pic', "Mist.gif")
        self.Rain = self.load_image('assets/pic', "Rain.gif")
        self.ScatteredClouds = self.load_image('assets/pic', "Scattered_Clouds.gif")
        self.ScatteredCloudsNight = self.load_image('assets/pic', "Scattered_Clouds_Night.gif")
        self.ShowerRain = self.load_image('assets/pic', "Shower_Rain.gif")
        self.Snow = self.load_image('assets/pic', "Snow.gif")
        self.Thunderstorm = self.load_image('assets/pic', "Thunderstorm.gif")
        #---
        self.DCloudy = self.load_image('assets/img', "Cloudy.jpg")
        self.DCloudyNight = self.load_image('assets/img', "Cloudy_Night.jpg")
        self.DFewClouds = self.load_image('assets/img', "Few_Clouds.jpg")
        self.DFewCloudsNight = self.load_image('assets/img', "Few_Clouds_Night.jpg")
        self.DFog = self.load_image('assets/img', "Fog.jpg")
        self.DRain = self.load_image('assets/img', "Rain.jpg")
        self.DSnow = self.load_image('assets/img', "Snow.jpg")
        self.DSnowNight = self.load_image('assets/img', "Snow_Night.jpg")
        self.DTStorm = self.load_image('assets/img', "T-Storm.jpg")
        self.DTStorm2 = self.load_image('assets/img', "T-Storm2.jpg")
        self.DClearSky = self.load_image('assets/img', "Sun.jpg")
        self.DClearSkyNight = self.load_image('assets/img', "Clear_Night.jpg")
        #---
        self.NA = self.load_image('assets/pic', "na.gif")
        self.arrow_down = self.load_image('assets/pic', "arrow_down.gif")
        self.arrow_up = self.load_image('assets/pic', "arrow_up.gif")
        self.snowflake1 = self.load_image('assets/img', "snowflake1.gif")
        self.snowflake2 = self.load_image('assets/img', "snowflake2.gif")
        self.snowflake3 = self.load_image('assets/img', "snowflake3.gif")
        self.snowflake4 = self.load_image('assets/img', "snowflake4.gif")
        self.snowflake5 = self.load_image('assets/img', "snowflake5.gif")
        self.snowflake6 = self.load_image('assets/img', "snowflake6.gif")
        self.RainAnim1 = self.load_image('assets/img', "rain_anim1.gif")
        #---
        self.tempin = self.load_image('assets/pic', "temp_in.gif")
        self.tempout = self.load_image('assets/pic', "temp_out.gif")
        self.wind = self.load_image('assets/pic', "wind.gif")

    def get_background(self, night, iconName):
        iconName=iconName.lower()
        if(iconName.find('01') != -1):  #CLEAR SKY
            if(night == True):
                pic=self.DClearSkyNight.convert()
            else:
                pic=self.DClearSky.convert()
        elif(iconName.find('02') != -1):  # FEW CLOUDS
            if(night==True):
                pic=self.DFewCloudsNight.convert()
            else:
                pic=self.DFewClouds.convert()
        elif(iconName.find('03') != -1):  #SCATTERED CLOUDS
            if(night==True):
                pic=self.DCloudyNight.convert()
            else:
                pic=self.DCloudy.convert()
        elif(iconName.find('04') != -1):  #BROKEN CLOUDS
            if(night==True):
                pic=self.DCloudyNight.convert()
            else:
                pic=self.DCloudy.convert()
        elif(iconName.find('09') != -1): #SHOWER RAIN
            pic=self.DRain.convert()
        elif(iconName.find('10') != -1): #RAIN
            pic=self.DRain.convert()
        elif(iconName.find('11') != -1):  #THUNDERSTORM
            pic=self.DTStorm.convert()
        elif(iconName.find('13') != -1):  #SNOW
            if(night==True):
                pic=self.DSnowNight.convert()
            else:
                pic=self.DSnow.convert()
        elif(iconName.find('50') != -1):  #mist - fog
            pic=self.DFog.convert()
        else:
            log.add_error_log("icon not found: {}".format(iconName))
            pic=self.NA.convert()
        return pic

    def get_icon(self, night, iconName):
        iconName=iconName.lower()
        if(iconName.find('01') != -1):  #CLEAR SKY
            if(night==True):
                pic=self.ClearSkyNight.convert()
            else:
                pic=self.ClearSky.convert()
        elif(iconName.find('02') != -1):  # FEW CLOUDS
            pic=self.FewClouds.convert()
        elif(iconName.find('03') != -1):  #SCATTERED CLOUDS
            pic=self.ScatteredClouds.convert()
        elif(iconName.find('04') != -1):  #BROKEN CLOUDS
            pic=self.BrokenClouds.convert()
        elif(iconName.find('09') != -1): #SHOWER RAIN
            pic=self.ShowerRain.convert()
        elif(iconName.find('10') != -1): #RAIN
            pic=self.Rain.convert()
        elif(iconName.find('11') != -1):  #THUNDERSTORM
            pic=self.Thunderstorm.convert()
        elif(iconName.find('13') != -1):  #SNOW
            pic=self.Snow.convert()
        elif(iconName.find('50') != -1):  #mist - fog
            pic=self.Fog.convert()
        else:
            log.add_error_log("icon not found: {}".format(iconName))
            pic=self.NA.convert()
        return pic

    def get_picture(self, iconName):
        if(iconName == "arrow_down"):
            foto=self.arrow_down.convert()
        elif(iconName == "arrow_up"):
            foto=self.arrow_up.convert()
        elif(iconName.find('anim') != -1):
            foto=self.RainAnim1.convert()
        elif(iconName.find('snowflake1') != -1):
            foto=self.snowflake1.convert()
        elif(iconName.find('snowflake2') != -1):
            foto=self.snowflake2.convert()
        elif(iconName.find('snowflake3') != -1):
            foto=self.snowflake3.convert()
        elif(iconName.find('snowflake4') != -1):
            foto=self.snowflake4.convert()
        elif(iconName.find('snowflake5') != -1):
            foto=self.snowflake5.convert()
        elif(iconName.find('snowflake6') != -1):
            foto=self.snowflake6.convert()
        elif(iconName.find("DTStorm2") != -1):
            foto=self.DTStorm2.convert()
        elif(iconName.find("temp_out") != -1):
            foto=self.tempout.convert()
        elif(iconName.find("temp_in") != -1):
            foto=self.tempin.convert()
        elif(iconName.find("wind") != -1):
            foto=self.wind.convert()
        else:
            foto=self.NA.convert()
        return foto

    def load_image(self, folder, name):   # ZALADOWANIE IKONY
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
        pygame.gfxdraw.box(screen, Rect((x, y),(w, h)), color)

    def text_center(self, screen, tekst, font, rozmiar, x, y, color, alpha):
        a_sys_font = pygame.font.SysFont(font, rozmiar)
        ren = a_sys_font.render(unicode(tekst,'utf-8'), True, color)
        ren.set_alpha(alpha)
        screen.blit(ren, (x - ren.get_width() // 2, y - ren.get_height() // 2))
    
    def text_center_background(self, screen, tekst, font, rozmiar, x, y, color, alpha, bgcolor):
        a_sys_font = pygame.font.SysFont(font, rozmiar)
        ren = a_sys_font.render(unicode(tekst,'utf-8'), True, color)
        ren.set_alpha(alpha)
        self.box(screen, x - ren.get_width() // 2,y - ren.get_height() // 2,ren.get_width()+30,ren.get_height(),bgcolor)
        screen.blit(ren, (x - ren.get_width() // 2, y - ren.get_height() // 2))

    def text_background(self, screen, tekst, font, rozmiar, x, y, color, alpha,bgcolor):
        a_sys_font = pygame.font.SysFont(font, rozmiar)
        text = a_sys_font.render(unicode(tekst,'utf-8'),True, color)
        text.set_alpha(alpha)
        self.box(screen, x,y,text.get_width()+30,text.get_height(),bgcolor)
        screen.blit(text, (x, y))

    def text2(self, screen, tekst, font, rozmiar, x, y, color, alpha):
        a_sys_font = pygame.font.SysFont(font, rozmiar)
        text = a_sys_font.render(unicode(tekst,'utf-8'),True, color)
        text.set_alpha(alpha)
        screen.blit(text, (x, y))
        return text.get_width()

    def set_background_colour(self, colour):
        self.screen.fill(colour)

    def update(self):
        pygame.display.update()
display = DISPLAY_CL()