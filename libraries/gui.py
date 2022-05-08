#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    import select, time, datetime, pogoda
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
from libraries.weatherForecast import *
from devicesList import *
from libraries.infoStrip import *

import wysw #tymczasowe

class GUI_CL:
    bgcolor=(255,255,255,255)
    resolution = 800, 480
    #screen = pygame.display.set_mode(resolution, pygame.FULLSCREEN)
    screen = pygame.display.set_mode(resolution,1)
    pozycja_animacji = [[0,0],[60,-42],[120,-135],[160,-225],[180,-275],[190,-367],[230,-13],[350,-89],[390,-247],[430,-198],[500,-400],[560,-163],[620,-200],[650,-50],[700,-31],[750,-7],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]]
    kolorPaskaInfo=(50,100,10,255)

    kolor=(0,0,0,250)
    kolorczcionki1=(255,255,255,255)
    kolorczcionki2=(255,200,100,255)
    kolorczcionki3=(0,0,0,255)
    kolorczcionki4=(60,60,60,200)
    kolorczcionki5=(255,255,255,255)

    swiatlo = 0

    tfps=0
    posX=0
    tryb_nocny=False

    def __init__(self):
        pygame.init()
        pygame.display.set_caption('MojDom')
        self.screen.fill(self.bgcolor)
        pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))

    def lcd(self):  #----WYSWIETLANIE - WATEK!!!!!!!!!! ------------------------------------------------------------------------------------------------------
        obraz=0
        self.tfps=0.2

        while(1):
            for event in pygame.event.get():
                if event.type==pygame.KEYDOWN and event.key==pygame.K_SPACE:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    px=event.pos[0]
                    py=event.pos[1]
                    print ("You pressed the left mouse button at ({}, {})".format(px,py))
                    if(px>750 and px<800 and py>0 and py<50):
                        pygame.quit()
                        sys.exit()
                    if(px>17 and px<284 and py>15 and py<227):
                        screen.fill(self.bgcolor)
                        obraz=0
            #flaga_odczyt_ustawien=wysw.odswiez(czujnikZew.temp,czujnikPok1.temp,czujnikPok2.temp,czujnikZew.humi,czujnikPok1.humi,czujnikPok2.humi,czujnikKwiatek.wilgotnosc,czujnikKwiatek.slonce,czujnikKwiatek.woda,czujnikKwiatek.zasilanie, self.swiatlo, int(lampa1Pok1.Flaga), int(lampa1Pok1.Jasnosc), int(lampa1Pok1.Ustawienie), int(lampaTV.Flaga), int(lampaTV.Jasnosc), int(lampaPok2.Flaga), int(lampaPok2.Jasnosc), int(lampaKuch.Flaga),czujnikZew.czas,czujnikZew.blad,czujnikPok1.blad,czujnikPok2.blad)
            if(obraz==0):
                if self.tryb_nocny==False:
                    self.obraz_glowny()
                else:
                    obraz_nocny()

            if self.tryb_nocny==False and self.swiatlo<2:
                self.tryb_nocny=True
                screen.fill((0,0,0,255))
            elif self.tryb_nocny==True and self.swiatlo>5:
                self.tryb_nocny=False
                screen.fill(self.bgcolor)
            pygame.display.update()
            time.sleep(self.tfps)

    def obraz_glowny(self):
        #---ANIMACJA TAPETY -----
        #pogoda.Pogoda.IkonaDzis="02"
        #czujnikZew.noc_flaga=False
        '''
        01d - clear sky
        02d - few clouds
        03d - scattered clouds
        04d - broken clouds
        09d - shower rain
        10d - rain
        11d - thunderstorm
        13d - snow
        50d - mist - fog
        '''
        #tapeta=pogoda.Pogoda.IkonaDzis
        tapeta = weather.iconToday
        tapeta=tapeta.lower()
        if(tapeta.find('02') != -1 or tapeta.find('03') != -1 or tapeta.find('04') != -1): #CLOUDS
            if self.pozycja_animacji[16][1]==0: #dla zmiany kierunku
                if self.pozycja_animacji[16][0]>300:
                    self.pozycja_animacji[16][1]=1
                else:
                    self.pozycja_animacji[16][0]=self.pozycja_animacji[16][0]+1
            else: #dla zmiany kierunku
                if self.pozycja_animacji[16][0]<0:
                    self.pozycja_animacji[16][1]=0
                else:
                    self.pozycja_animacji[16][0]=self.pozycja_animacji[16][0]-1
            self.posX=(-600)+self.pozycja_animacji[16][0]
            if(tapeta.find('02') != -1 and czujnikZew.noc_flaga==False):
                self.kolorczcionki3=(185,242,107,255)
                self.kolorczcionki4=(235,255,187,255)
            if czujnikZew.noc_flaga==True:
                self.kolorczcionki3=(190,190,190,255)
                self.kolorczcionki4=(250,250,250,200)
        wysw.display_picture(self.screen, self.posX , 0, 255, weather.get_icon(True, czujnikZew.noc_flaga, pogoda.Pogoda.IkonaDzis)) 
        if(tapeta.find('01') != -1):  #CLEAR SKY
            if czujnikZew.noc_flaga==True:
                self.kolorczcionki2=(180,180,180,255)
            else:
                self.kolorczcionki2=(100,40,20,255)
            self.kolorczcionki3=(255,255,155,255)
            self.kolorczcionki4=(255,215,0,255)
            self.kolorczcionki5=(255,82,0,255)
        elif(tapeta.find('50') != -1):
            self.kolorczcionki1=(0,105,56,255)
            self.kolorczcionki2=(100,40,20,255)
            self.kolorczcionki3=(95,103,56,255)
            self.kolorczcionki4=(255,215,0,255)
            self.kolorczcionki5=(255,82,0,255)
        elif(tapeta.find('09') != -1 or tapeta.find('10') != -1):  #RAIN
            self.kolorczcionki3=(255,255,155,255)
            self.kolorczcionki4=(255,255,200,255)
            for i in range(6):
                wysw.display_picture(self.screen, randint(30, 750), randint(70, 300), 255, pictures.get_icon("anim")) 
        if(tapeta.find('11') != -1): #THUNDERSTORM
            self.kolorczcionki3=(255,255,155,255)
            self.kolorczcionki4=(255,215,0,255)
            self.kolorczcionki5=(255,82,0,255)
            if self.pozycja_animacji[17][0]<0:
                pogoda.icons(0,0,255,"DTStorm2")
                self.pozycja_animacji[17][0]=randint(7, 70)
            else:
                self.pozycja_animacji[17][0]=self.pozycja_animacji[17][0]-1
        elif(tapeta.find('13') != -1): #SNOW
            self.tfps=0.0
            pogoda.icons(self.pozycja_animacji[0][0],self.pozycja_animacji[0][1],255,"snowflake1")
            self.pozycja_animacji[0][1]=self.pozycja_animacji[0][1]+1
            pogoda.icons(self.pozycja_animacji[1][0],self.pozycja_animacji[1][1],255,"snowflake2")
            self.pozycja_animacji[1][1]=self.pozycja_animacji[1][1]+2
            pogoda.icons(self.pozycja_animacji[2][0],self.pozycja_animacji[2][1],255,"snowflake3")
            self.pozycja_animacji[2][1]=self.pozycja_animacji[2][1]+4
            pogoda.icons(self.pozycja_animacji[3][0],self.pozycja_animacji[3][1],255,"snowflake3")
            self.pozycja_animacji[3][1]=self.pozycja_animacji[3][1]+4
            pogoda.icons(self.pozycja_animacji[4][0],self.pozycja_animacji[4][1],255,"snowflake3")
            self.pozycja_animacji[4][1]=self.pozycja_animacji[4][1]+4
            pogoda.icons(self.pozycja_animacji[5][0],self.pozycja_animacji[5][1],255,"snowflake3")
            self.pozycja_animacji[5][1]=self.pozycja_animacji[5][1]+4
            pogoda.icons(self.pozycja_animacji[6][0],self.pozycja_animacji[6][1],255,"snowflake3")
            self.pozycja_animacji[6][1]=self.pozycja_animacji[6][1]+4
            pogoda.icons(self.pozycja_animacji[7][0],self.pozycja_animacji[7][1],255,"snowflake4")
            self.pozycja_animacji[7][1]=self.pozycja_animacji[7][1]+1
            pogoda.icons(self.pozycja_animacji[8][0],self.pozycja_animacji[8][1],255,"snowflake5")
            self.pozycja_animacji[8][1]=self.pozycja_animacji[8][1]+3
            pogoda.icons(self.pozycja_animacji[9][0],self.pozycja_animacji[9][1],255,"snowflake5")
            self.pozycja_animacji[9][1]=self.pozycja_animacji[9][1]+3
            pogoda.icons(self.pozycja_animacji[10][0],self.pozycja_animacji[10][1],255,"snowflake5")
            self.pozycja_animacji[10][1]=self.pozycja_animacji[10][1]+3
            pogoda.icons(self.pozycja_animacji[11][0],self.pozycja_animacji[11][1],255,"snowflake6")
            self.pozycja_animacji[11][1]=self.pozycja_animacji[11][1]+4
            pogoda.icons(self.pozycja_animacji[12][0],self.pozycja_animacji[12][1],255,"snowflake6")
            self.pozycja_animacji[12][1]=self.pozycja_animacji[12][1]+4
            pogoda.icons(self.pozycja_animacji[13][0],self.pozycja_animacji[13][1],255,"snowflake3")
            self.pozycja_animacji[13][1]=self.pozycja_animacji[13][1]+5
            pogoda.icons(self.pozycja_animacji[14][0],self.pozycja_animacji[14][1],255,"snowflake6")
            self.pozycja_animacji[14][1]=self.pozycja_animacji[14][1]+4
            pogoda.icons(self.pozycja_animacji[15][0],self.pozycja_animacji[15][1],255,"snowflake6")
            self.pozycja_animacji[15][1]=self.pozycja_animacji[15][1]+4
            for px in range(16):
                if self.pozycja_animacji[px][1]>randint(480, 500):
                    self.pozycja_animacji[px][0]=randint(10, 780)
                    self.pozycja_animacji[px][1]=0
            self.kolorczcionki4=(160,180,160,255)
            self.kolorczcionki3=(220,220,250,255)
        #------------------------
        d = datetime.datetime.today()
        dzienTygodnia=wysw.dzien(d.weekday())

        wysw.napis_centralny(self.screen, str(time.strftime("%H:%M")),"Nimbus Sans L",190,295,90,self.kolorczcionki1,255) #czas
        wysw.napis_centralny(self.screen, dzienTygodnia,"Nimbus Sans L",56,620,80,self.kolorczcionki2,255)  #dzien tygodnia
        wysw.napis_centralny(self.screen, str(int(time.strftime("%d")))+" "+wysw.miesiac(str(time.strftime("%B"))),"Nimbus Sans L",56,620,120,self.kolorczcionki2,255)  #dzien tygodnia

        wysw.napis2(self.screen, "dziś","Nimbus Sans L",56,50,170,self.kolorczcionki3,255)
        pogoda.ikonka(30,210,255,False,czujnikZew.noc_flaga,pogoda.Pogoda.IkonaDzis)
        pogoda.icons(20,330,255,"arrow_down")
        wysw.napis2(self.screen, "{:.0f}°C".format(pogoda.Pogoda.TempMinDzis),"Nimbus Sans L",54,70,330,self.kolorczcionki3,255)
        pogoda.icons(20,380,255,"arrow_up")
        wysw.napis2(self.screen, "{:.0f}°C".format(pogoda.Pogoda.TempMaxDzis),"Nimbus Sans L",54,70,380,self.kolorczcionki4,255)
        wysw.napis2(self.screen, "jutro","Nimbus Sans L",56,230,170,self.kolorczcionki3,255)
        pogoda.ikonka(220,210,255,False,False,pogoda.Pogoda.IkonaJutro)
        pogoda.icons(205,330,255,"arrow_down")
        wysw.napis2(self.screen, "{:.0f}°C".format(pogoda.Pogoda.TempMinJutro),"Nimbus Sans L",54,245,330,self.kolorczcionki3,255)
        pogoda.icons(205,380,255,"arrow_up")
        wysw.napis2(self.screen, "{:.0f}°C".format(pogoda.Pogoda.TempMaxJutro),"Nimbus Sans L",54,245,380,self.kolorczcionki4,255)

        wysw.obraz(self.screen, 390,170,255,"temp_out")
        dlugosc=wysw.napis2(self.screen, "{:.1f}°C".format(czujnikZew.temp),"Nimbus Sans L",68,485,190,self.kolorczcionki5,255)
        wysw.napis2(self.screen, "{:.0f}%".format(czujnikZew.humi),"Nimbus Sans L",48,505+dlugosc,200,self.kolorczcionki4,255)
        wysw.obraz(self.screen, 390,258,255,"temp_in")
        dlugosc=wysw.napis2(self.screen, "{:.1f}°C".format(czujnikPok1.temp),"Nimbus Sans L",68,485,280,self.kolorczcionki4,255)
        wysw.napis2(self.screen, "{:.0f}%".format(czujnikPok1.humi),"Nimbus Sans L",48,505+dlugosc,290,self.kolorczcionki4,255)

        wysw.obraz(self.screen, 390,350,255,"wind")
        dlugosc=wysw.napis2(self.screen, "{:.1f}m/s".format(czujnikZew.predkoscWiatru),"Nimbus Sans L",50,485,370,self.kolorczcionki3,255)

        # PASEK INFORMACYJNY
        infoStrip.actualInformation=infoStrip.read_info()
        if (infoStrip.actualInformation != ""):
            infoStrip.displayedInformation=infoStrip.actualInformation
            self.kolorPaskaInfo=(190,255,190,255)
            infoStrip.time=60
            infoStrip.position=3
        else:
            if(infoStrip.time==0):
                infoStrip.displayedInformation=infoStrip.read_error()
                if (infoStrip.displayedInformation != ""):
                    infoStrip.time=120
                    infoStrip.position=3
                    self.kolorPaskaInfo=(255,100,100,255)

        if(infoStrip.time>0):
            infoStrip.time-=1
        if(infoStrip.time>=0 and infoStrip.time<=3):
            infoStrip.position=infoStrip.time

        if(infoStrip.displayedInformation != ""):
            wysw.napis2(self.screen, infoStrip.displayedInformation,"Nimbus Sans L",46,70,480-(infoStrip.position*13),self.kolorPaskaInfo,255)

    def obraz_nocny(self):
        self.kolorczcionki3=(180,180,180,255)

        wysw.napis_centralny_tlo(screen, str(time.strftime("%H:%M")),"Nimbus Sans L",360,400,210,kolorczcionki3,255,(0,0,0,255)) #czas
        wysw.napis_tlo(screen, "Temperatura {:.1f}°C".format(czujnikPok1.temp),"Nimbus Sans L",70,20,410,kolorczcionki3,255,(0,0,0,255))
gui = GUI_CL()