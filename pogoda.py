#!/usr/bin/env python
# -*- coding: utf-8 -*-
try:
    import os, sys, locale, datetime, time, configparser, requests
except ImportError:
    print "Blad importu"

import pygame, pygame.mixer, pygame.gfxdraw, glob, linecache
from pygame.locals import *
from pygame.compat import unichr_, unicode_
from pygame.locals import *
from pygame.compat import geterror

import json
from datetime import datetime, timedelta

class Pog:
    Dzis="Mon"
    Jutro="Mon"
    Temp=0.0
    TempMinDzis=0.0
    TempMinJutro=0.0
    TempMaxDzis=0.0
    TempMaxJutro=0.0
    OpadDzis="0"
    OpadJutro="0"
    IkonaDzis="01d"
    IkonaJutro="01d"
    BaroKierunek=""
    Cisnienie=""
    Wiatr=""
    Wilgotnosc=""

Pogoda = Pog()

class Pog2:
    Dzien="Mon"
    Temp=0.0
    Ikona="Sunny"
    IkonaTeraz="Sunny"
    BaroKierunek=""
    Cisnienie=""
    Wiatr=""
    TempMax=""
    TempMin=""
    Opad=""
    Wilgotnosc=""
Pogoda2 = Pog2()

'''def prognozaDzis(prognoza):
    Pogoda.TempMaxDzis=-50
    Pogoda.TempMinDzis=50
    flaga=0
    select_data = prognoza['list']
    #obliczenia daty
    d = datetime.today()
    for box in select_data:
        if 'dt_txt' in box:
            data=datetime.strptime(box['dt_txt'], '%Y-%m-%d %H:%M:%S')
            if data.date()==d.date():
                #print(box['dt_txt'], box['main']['temp_min'], box['main']['temp_max'], box['wind']['speed'], box['weather'][0]['description'])
                if float(box['main']['temp_max'])>Pogoda.TempMaxDzis:
                    Pogoda.TempMaxDzis=float(box['main']['temp_max'])
                if float(box['main']['temp_min'])<Pogoda.TempMinDzis:
                    Pogoda.TempMinDzis=float(box['main']['temp_min'])
                czas=datetime.strptime("2020-01-01 12:00:00", '%Y-%m-%d %H:%M:%S')
                if flaga==0:
                    Pogoda.IkonaDzis=box['weather'][0]['icon']
                    #print Pogoda.IkonaDzis
                    flaga=1
        else:
            print('weather not found') '''

def prognozaDzis(prognoza):
    Pogoda.TempMaxDzis=-50
    Pogoda.TempMinDzis=50
    flaga=0
    select_data = prognoza['list']
    #obliczenia daty
    d = datetime.today()
    for box in select_data:
        if 'dt' in box:
            if float(box['main']['temp_max'])>Pogoda.TempMaxDzis:
                Pogoda.TempMaxDzis=float(box['main']['temp_max'])
                if(Pogoda.TempMaxDzis > -1 and Pogoda.TempMaxDzis <= 0):
                    Pogoda.TempMaxDzis = 0.0
            if float(box['main']['temp_min'])<Pogoda.TempMinDzis:
                Pogoda.TempMinDzis=float(box['main']['temp_min'])
                if(Pogoda.TempMinDzis > -1 and Pogoda.TempMinDzis <= 0):
                    Pogoda.TempMinDzis = 0.0
            czas=datetime.strptime("2020-01-01 12:00:00", '%Y-%m-%d %H:%M:%S')
            if flaga==0:
                Pogoda.IkonaDzis=box['weather'][0]['icon']
                flaga=1
        else:
            print('weather not found')
        break

def prognozaJutro(prognoza):
    Pogoda.TempMaxJutro=-50
    Pogoda.TempMinJutro=50
    select_data = prognoza['list']
    #obliczenia daty
    d = datetime.today() + timedelta(days=1)
    for box in select_data:
        if 'dt_txt' in box:
            data=datetime.strptime(box['dt_txt'], '%Y-%m-%d %H:%M:%S')
            if data.date()==d.date():
                if float(box['main']['temp_max'])>Pogoda.TempMaxJutro:
                    Pogoda.TempMaxJutro=float(box['main']['temp_max'])
                    if(Pogoda.TempMaxJutro > -1 and Pogoda.TempMaxJutro <= 0):
                        Pogoda.TempMaxJutro = 0.0
                if float(box['main']['temp_min'])<Pogoda.TempMinJutro:
                    Pogoda.TempMinJutro=float(box['main']['temp_min'])
                    if(Pogoda.TempMinJutro > -1 and Pogoda.TempMinJutro <= 0):
                        Pogoda.TempMinJutro = 0.0
                czas=datetime.strptime("2020-01-01 12:00:00", '%Y-%m-%d %H:%M:%S')
                if data.time()==czas.time():
                    Pogoda.IkonaJutro=box['weather'][0]['icon']
                    #print (Pogoda.IkonaJutro)
        else:
            print('weather not found')

def PrognozaPogody(miasto):
    try:
        prognoza(miasto)
    except:
        print "Blad polaczenia z serwerem pogody"

def prognoza(miasto):
    print("Pobieram progrnoze pogody...")
    api_address='http://api.openweathermap.org/data/2.5/weather?APPID=85b527bafdfc28a92672434b32ead750&units=metric&q={}'.format(miasto)
    api_add='https://api.openweathermap.org/data/2.5/forecast?q={}&mode=json&APPID=85b527bafdfc28a92672434b32ead750&units=metric'.format(miasto)
    url = api_add
    json_data = requests.get(url).json()
    #print(api_add)
    #print(json_data)
    prognozaDzis(json_data)
    prognozaJutro(json_data)
    print time.strftime("%H:%M")+' Pobrano prognoze pogody'
    #print tekst

#initialize
pygame.init()
resolution = 800, 620
screen = pygame.display.set_mode(resolution,1)
fg = 230, 230, 230
bg = 0,0,0
wincolor = 0, 0, 0

class Ikony(object):
    def __init__(self):
        self.BrokenClouds = load_image("Broken_Clouds.gif")
        self.ClearSky = load_image("Clear_Sky.gif")
        self.ClearSkyNight = load_image("Clear_Sky_Night.gif")
        self.FewClouds = load_image("Few_Clouds.gif")
        self.Mist = load_image("Mist.gif")
        self.Rain = load_image("Rain.gif")
        self.ScatteredClouds = load_image("Scattered_Clouds.gif")
        self.ScatteredCloudsNight = load_image("Scattered_Clouds_Night.gif")
        self.ShowerRain = load_image("Shower_Rain.gif")
        self.Snow = load_image("Snow.gif")
        self.Thunderstorm = load_image("Thunderstorm.gif")
        #---
        self.DCloudy = load_image2("Cloudy.jpg")
        self.DCloudyNight = load_image2("Cloudy_Night.jpg")
        self.DFewClouds = load_image2("Few_Clouds.jpg")
        self.DFewCloudsNight = load_image2("Few_Clouds_Night.jpg")
        self.DFog = load_image2("Fog.jpg")
        self.DRain = load_image2("Rain.jpg")
        self.DSnow = load_image2("Snow.jpg")
        self.DSnowNight = load_image2("Snow_Night.jpg")
        self.DTStorm = load_image2("T-Storm.jpg")
        self.DTStorm2 = load_image2("T-Storm2.jpg")
        self.DClearSky = load_image2("Sun.jpg")
        self.DClearSkyNight = load_image2("Clear_Night.jpg")
        #---
        self.NA = load_image("na.gif")
        self.arrow_down = load_image("arrow_down.gif")
        self.arrow_up = load_image("arrow_up.gif")
        self.snowflake1 = load_image2("snowflake1.gif")
        self.snowflake2 = load_image2("snowflake2.gif")
        self.snowflake3 = load_image2("snowflake3.gif")
        self.snowflake4 = load_image2("snowflake4.gif")
        self.snowflake5 = load_image2("snowflake5.gif")
        self.snowflake6 = load_image2("snowflake6.gif")
        self.RainAnim1 = load_image2("rain_anim1.gif")


def load_image(name):   # ZALADOWANIE IKONY
    main_dir = os.path.split(os.path.abspath(__file__))[0]
    data_dir = os.path.join(main_dir, 'ikony')
    fullname = os.path.join(data_dir, name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error:
        print ('Cannot load image:', fullname)
        raise SystemExit(str(geterror()))
    image = image.convert()
    return image

def load_image2(name): #ZALADOWANIE DUZEGO OBRAZU Z KATALOGU PIC
    main_dir = os.path.split(os.path.abspath(__file__))[0]
    data_dir = os.path.join(main_dir, 'pic')
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

def ikonka(osx ,osy, alpha, duzy, noc, naz):
    nazwa=naz.lower()
    '''
    01d - clear sky
    02d - few clouds
    03d - scattered clouds
    04d - broken clouds
    09d - shower rain
    10d - rain
    11d - thunderstorm
    13d - snow
    50d - mist
    '''
    if(nazwa.find('01') != -1):  #CLEAR SKY
        if(duzy==True):
            if(noc==True):
                obrazek=ikona.DClearSkyNight.convert()
            else:
                obrazek=ikona.DClearSky.convert()
        else:
            if(noc==True):
                obrazek=ikona.ClearSkyNight.convert()
            else:
                obrazek=ikona.ClearSky.convert()
    elif(nazwa.find('02') != -1):  # FEW CLOUDS
        if(duzy==True):
            if(noc==True):
                obrazek=ikona.DFewCloudsNight.convert()
            else:
                obrazek=ikona.DFewClouds.convert()
        else:
            obrazek=ikona.FewClouds.convert()
    elif(nazwa.find('03') != -1):  #SCATTERED CLOUDS
        if(duzy==True):
            if(noc==True):
                obrazek=ikona.DCloudyNight.convert()
            else:
                obrazek=ikona.DCloudy.convert()
        else:
            obrazek=ikona.ScatteredClouds.convert()
    elif(nazwa.find('04') != -1):  #BROKEN CLOUDS
        if(duzy==True):
            if(noc==True):
                obrazek=ikona.DCloudyNight.convert()
            else:
                obrazek=ikona.DCloudy.convert()
        else:
            obrazek=ikona.BrokenClouds.convert()
    elif(nazwa.find('09') != -1): #SHOWER RAIN
        if(duzy==True):
            obrazek=ikona.DRain.convert()
        else:
            obrazek=ikona.ShowerRain.convert()
    elif(nazwa.find('10') != -1): #RAIN
        if(duzy==True):
            obrazek=ikona.DRain.convert()
        else:
            obrazek=ikona.Rain.convert()
    elif(nazwa.find('11') != -1):  #THUNDERSTORM
        if(duzy==True):
            obrazek=ikona.DTStorm.convert()
        else:
            obrazek=ikona.Thunderstorm.convert()
    elif(nazwa.find('13') != -1):  #SNOW
        if(duzy==True):
            if(noc==True):
                obrazek=ikona.DSnowNight.convert()
            else:
                obrazek=ikona.DSnow.convert()
        else:
            obrazek=ikona.Snow.convert()
    elif(nazwa.find('50') != -1):  #mist - fog
        if(duzy==True):
            obrazek=ikona.DFog.convert()
        else:
            obrazek=ikona.Fog.convert()
    #---------------------------
    else:
        zapis_bledu(nazwa)
        obrazek=ikona.NA.convert()
    obrazek = obrazek.convert_alpha()
    obrazek.set_alpha(alpha)
    screen.blit(obrazek, (osx, osy))

def icons(osx ,osy, alpha, nazwa):
    if(nazwa == "DTStorm2"):
        foto=ikona.DTStorm2.convert()
    elif(nazwa == "arrow_down"):
        foto=ikona.arrow_down.convert()
    elif(nazwa == "arrow_up"):
        foto=ikona.arrow_up.convert()
    elif(nazwa == "steady"):
        foto=ikona.baro_steady.convert()
    elif(nazwa == "rising"):
        foto=ikona.baro_up.convert()
    elif(nazwa == "rising rapidly"):
        foto=ikona.baro_up.convert()
    elif(nazwa == "falling"):
        foto=ikona.baro_down.convert()
    elif(nazwa == "falling rapidly"):
        foto=ikona.baro_down.convert()
    elif(nazwa.find('anim') != -1):
        foto=ikona.RainAnim1.convert()
    elif(nazwa.find('snowflake1') != -1):
        foto=ikona.snowflake1.convert()
    elif(nazwa.find('snowflake2') != -1):
        foto=ikona.snowflake2.convert()
    elif(nazwa.find('snowflake3') != -1):
        foto=ikona.snowflake3.convert()
    elif(nazwa.find('snowflake4') != -1):
        foto=ikona.snowflake4.convert()
    elif(nazwa.find('snowflake5') != -1):
        foto=ikona.snowflake5.convert()
    elif(nazwa.find('snowflake6') != -1):
        foto=ikona.snowflake6.convert()
    else:
        zapis_bledu(nazwa)
        foto=ikona.NA.convert()
    foto.set_alpha(alpha)
    screen.blit(foto, (osx, osy))

def zapis_bledu(blad):
    plik = open('blad_pogody.txt', 'w')
    plik.write(blad+'\n')
    plik.close()
