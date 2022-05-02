#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame, pygame.mixer, pygame.gfxdraw, glob, linecache
import os
import locale
import sys
import time
from pygame.locals import *
from pygame.compat import unichr_, unicode_
from pygame.locals import *
from pygame.compat import geterror

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, 'ikony')

#initialize
pygame.init()
resolution = 800, 620
screen = pygame.display.set_mode(resolution,1)
fg = 230, 230, 230
bg = 0,0,0
wincolor = 0, 0, 0

class Ikony(object):
    def __init__(self):
        self.Cloudy = load_image("Cloudy.gif")
        self.Fog = load_image("Fog.gif")
        self.Hail = load_image("Hail.gif")
        self.PartlySunny = load_image("Partly Sunny.gif")
        self.Rain = load_image("Rain.gif")
        self.Snow = load_image("Snow.gif")
        self.Sleet = load_image("Sleet.gif")
        self.Storm = load_image("Storm.gif")
        self.Wind = load_image("Wind.gif")
        self.Sun = load_image("Sun.gif")
        self.NA = load_image("na.gif")
        self.baro_steady = load_image("baro_straight.jpg")
        self.baro_up = load_image("baro_up.jpg")
        self.baro_down = load_image("baro_down.jpg")


def load_image(name):
    fullname = os.path.join(data_dir, name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error:
        print ('Cannot load image:', fullname)
        raise SystemExit(str(geterror()))
    image = image.convert()
    return image

global ikona
ikona = Ikony()

def napis(tekst, font, rozmiar, x, y, color, alpha):
    a_sys_font = pygame.font.SysFont(font, rozmiar)
    ren = a_sys_font.render(unicode(tekst,'utf-8'), 1, color,bg)
    ren.set_alpha(alpha)
    pygame.gfxdraw.box(screen, Rect((x,y),(ren.get_width(),ren.get_height())),bg)
    screen.blit(ren, (x, y))
    pygame.display.update()

def ikonka(osx ,osy, alpha, nazwa):
    if(nazwa == "Baro"):
        obrazek=ikona.Baro.convert()
    elif(nazwa == "Clear"):
        obrazek=ikona.Sun.convert()
    elif(nazwa == "Clear Night"):
        obrazek=ikona.Sun.convert()
    elif(nazwa == "Cloudy"):
        obrazek=ikona.Cloudy.convert()
    elif(nazwa == "Cloudy Night"):
        obrazek=ikona.Cloudy.convert()
    elif(nazwa == "Drop"):
        obrazek=ikona.Rain.convert()
    elif(nazwa == "Fair"):
        obrazek=ikona.Sun.convert()
    elif(nazwa == "Hail"):
        obrazek=ikona.Hail.convert()
    elif(nazwa == "Mostly Cloudy"):
        obrazek=ikona.PartlySunny.convert()
    elif(nazwa == "Mostly Sunny"):
        obrazek=ikona.PartlySunny.convert()
    elif(nazwa == "Partly Cloudy"):
        obrazek=ikona.PartlySunny.convert()
    elif(nazwa == "AM Clouds / PM Sun"):
        obrazek=ikona.PartlySunny.convert()
    elif(nazwa == "Partly Sunny"):
        obrazek=ikona.PartlySunny.convert()
    elif(nazwa == "PM T-Storms"):
        obrazek=ikona.Storm.convert()
    elif(nazwa == "Rain / Wind"):
        obrazek=ikona.Rain.convert()
    elif(nazwa == "Rain"):
        obrazek=ikona.Rain.convert()
    elif(nazwa == "AM Rain"):
        obrazek=ikona.Rain.convert()
    elif(nazwa == "PM Rain"):
        obrazek=ikona.Rain.convert()
    elif(nazwa == "Light Rain"):
        obrazek=ikona.Rain.convert()
    elif(nazwa == "AM Light Rain"):
        obrazek=ikona.Rain.convert()
    elif(nazwa == "PM Light Rain"):
        obrazek=ikona.Rain.convert()
    elif(nazwa == "Few Showers"):
        obrazek=ikona.Rain.convert()
    elif(nazwa == "Rain / Snow"):
        obrazek=ikona.Sleet.convert()
    elif(nazwa == "Scattered T-Storms"):
        obrazek=ikona.Storm.convert()
    elif(nazwa == "Snow"):
        obrazek=ikona.Snow.convert()
    elif(nazwa == "Light Snow"):
        obrazek=ikona.Snow.convert()
    elif(nazwa == "PM Snow Showers"):
        obrazek=ikona.Snow.convert()
    elif(nazwa == "AM Snow Showers"):
        obrazek=ikona.Snow.convert()
    elif(nazwa == "Few Snow Showers"):
        obrazek=ikona.Snow.convert()
    elif(nazwa == "Storm"):
        obrazek=ikona.Storm.convert()
    elif(nazwa == "Sunny"):
        obrazek=ikona.Sun.convert()
    elif(nazwa == "T-Storms"):
        obrazek=ikona.Storm.convert()
    elif(nazwa == "Wind"):
        obrazek=ikona.Wind.convert()
    elif(nazwa == "Wind_small"):
        obrazek=ikona.Wind.convert()
    elif(nazwa == "Heavy Rain"):
        obrazek=ikona.Rain.convert()
    elif(nazwa == "Showers" or nazwa=="PM Showers" or nazwa=="AM Showers"):
        obrazek=ikona.Rain.convert()
    elif(nazwa == "Light Rain Shower"):
        obrazek=ikona.Rain.convert()
    elif(nazwa == "AM Rain / Snow Showers"):
        obrazek=ikona.Rain.convert()
    elif(nazwa == "Light Snow Shower"):
        obrazek=ikona.Snow.convert()
    elif(nazwa == "Light Drizzle"):
        obrazek=ikona.Rain.convert()
    elif(nazwa == "Drizzle"):
        obrazek=ikona.Rain.convert()
    elif(nazwa == "Fog"):
        obrazek=ikona.Fog.convert()
    elif(nazwa == "AM Fog / PM Sun"):
        obrazek=ikona.Fog.convert()
    elif(nazwa == "Patches of Fog"):
        obrazek=ikona.Fog.convert()
    elif(nazwa == "Snow Shower"):
        obrazek=ikona.Snow.convert()
    elif(nazwa == "Sleet"):
        obrazek=ikona.Sleet.convert()
    elif(nazwa == "PM Rain / Snow"):
        obrazek=ikona.Sleet.convert()
    else:
        #print nazwa
        zapis_bledu(nazwa)
        obrazek=ikona.NA.convert()
    obrazek = obrazek.convert_alpha()
    obrazek.set_alpha(alpha)
    #pygame.draw.rect(screen, (0,0,0), Rect((osx,osy),(obrazek.get_height(),obrazek.get_width())))
    screen.blit(obrazek, (osx, osy))
    #pygame.display.update()

def ikony(osx ,osy, alpha, nazwa):
    if(nazwa == "baro_steady"):
        foto=ikona.baro_steady.convert()
    if(nazwa == "steady"):
        foto=ikona.baro_steady.convert()
    elif(nazwa == "rising"):
        foto=ikona.baro_up.convert()
    elif(nazwa == "rising rapidly"):
        foto=ikona.baro_up.convert()
    elif(nazwa == "falling"):
        foto=ikona.baro_down.convert()
    elif(nazwa == "falling rapidly"):
        foto=ikona.baro_down.convert()
    else:
        zapis_bledu(nazwa)
        foto=ikona.NA.convert()
    foto.set_alpha(alpha)
    screen.blit(foto, (osx, osy))

def zapis_bledu(blad):
    plik = open('blad_pogody.txt', 'w')
    plik.write(blad+'\n')
    plik.close()

def box(x,y,w,h,color):
    pygame.gfxdraw.box(screen, Rect((x,y),(w,h)), color)
    #pygame.display.update()

def main():
    print "start..."
    initialize_display()
    box(10,35,200,50,(0,255,50,190))
    box(120,55,100,90,(0,255,50,190))
    napis("jakis tekst","Nimbus Sans L",60,50,65,(255,5,155,25),25)

    obrazek = ikona.MostlyCloudy
    obrazek.set_alpha(255)
    pygame.draw.rect(screen, (0,0,0), Rect((30,300),(180,140)))
    screen.blit(obrazek, (30, 300))
    pygame.display.update()

    ikonka(400,300,255,"Baro")



#if __name__ == '__main__': main()


