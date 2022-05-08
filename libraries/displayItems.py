# -*- coding: utf-8 -*-
try:
    import select, time, datetime
except ImportError:
    print "Blad importu"

import sys ,os
import pygame, pygame.mixer, pygame.gfxdraw, glob
from pygame.locals import *
from pygame.compat import unichr_, unicode_
from pygame.locals import *
from pygame.compat import geterror
from time import sleep

from libraries.log import *


class PICTURES_CL():
    def __init__(self):
        self.arrow_down = self.load_image('ikony', "arrow_down.gif")
        self.arrow_up = self.load_image('ikony', "arrow_up.gif")
        self.snowflake1 = self.load_image('pic', "snowflake1.gif")
        self.snowflake2 = self.load_image('pic', "snowflake2.gif")
        self.snowflake3 = self.load_image('pic', "snowflake3.gif")
        self.snowflake4 = self.load_image('pic', "snowflake4.gif")
        self.snowflake5 = self.load_image('pic', "snowflake5.gif")
        self.snowflake6 = self.load_image('pic', "snowflake6.gif")
        self.RainAnim1 = self.load_image('pic', "rain_anim1.gif")
        self.DTStorm2 = self.load_image('pic', "T-Storm2.jpg")
    
    def get_icon(self, iconName):
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
        elif(iconName.find("DTStorm2")):
            foto=self.DTStorm2.convert()
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
            print ('Cannot load image:', fullname)
            raise SystemExit(str(geterror()))
        image = image.convert()
        return image
pictures = PICTURES_CL()