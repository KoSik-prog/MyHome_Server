#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    import select, time, datetime
except ImportError:
    print "Blad importu"
    
from time import sleep
from random import randint

from lib.log import *
from lib.weatherForecast import *
from devicesList import *
from lib.infoStrip import *
from lib.dateDecode import *
from lib.display import *
from lib.displayBrightness import *
from sensorOutside import *

class Gui:
    bgcolor=(255,255,255,255)
    pozycja_animacji = [[0,0],[60,-42],[120,-135],[160,-225],[180,-275],[190,-367],[230,-13],[350,-89],[390,-247],[430,-198],[500,-400],[560,-163],[620,-200],[650,-50],[700,-31],[750,-7],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]]
    kolorPaskaInfo=(50,100,10,255)

    kolor=(0,0,0,250)
    kolorczcionki1=(255,255,255,255)
    kolorczcionki2=(255,200,100,255)
    kolorczcionki3=(0,0,0,255)
    kolorczcionki4=(60,60,60,200)
    kolorczcionki5=(255,255,255,255)

    tfps = 0
    posX = 0
    tryb_nocny = False

    def gui_thread(self):
        obraz = 0
        self.tfps = 0.2

        while server.read_server_active_flag() == True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    px=event.pos[0]
                    py=event.pos[1]
                    print ("click ({}, {})".format(px,py))
                    if(px>750 and px<800 and py>0 and py<50):
                        server.set_server_active_flag(False)
                        pygame.quit()
                        sys.exit()
                    if(px>17 and px<284 and py>15 and py<227):
                        display.set_background_colour(self.bgcolor)
                        obraz=0
            #flaga_odczyt_ustawien=wysw.odswiez(sensorOutside.temperature,sensorRoom1Temperature.temp,sensorRoom2Temperature.temp,sensorOutside.humidity,sensorRoom1Temperature.humi,sensorRoom2Temperature.humi,czujnikKwiatek.wilgotnosc,czujnikKwiatek.slonce,czujnikKwiatek.woda,czujnikKwiatek.power, self.light, int(spootLightRoom1.flag), int(spootLightRoom1.brightness), int(spootLightRoom1.setting), int(ledStripRoom1.flag), int(ledStripRoom1.brightness), int(ledLightRoom2.flag), int(ledLightRoom2.brightness), int(kitchenLight.flag),sensorOutside.czas,sensorOutside.errorFlag,sensorRoom1Temperature.error,sensorRoom2Temperature.error)
            if(obraz == 0):
                if self.tryb_nocny == False:
                    self.obraz_glowny()
                else:
                    self.obraz_nocny()

            if self.tryb_nocny == False and displayBrightness.get_light() < 2:
                self.tryb_nocny = True
                display.set_background_colour((0, 0, 0, 255))
            elif self.tryb_nocny == True and displayBrightness.get_light() > 5:
                self.tryb_nocny = False
                display.set_background_colour(self.bgcolor)
            display.update()
            time.sleep(self.tfps)

    def obraz_glowny(self):
        #---ANIMACJA TAPETY -----
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
        tapeta = weather.iconToday
        tapeta = tapeta.lower()
        if(tapeta.find('02') != -1 or tapeta.find('03') != -1 or tapeta.find('04') != -1): #CLOUDS
            self.kolorczcionki1 = (255,255,255,255)
            self.kolorczcionki2 = (255,200,100,255)
            self.kolorczcionki5 = (255,255,255,255)
            if self.pozycja_animacji[16][1] == 0: #dla zmiany kierunku
                if self.pozycja_animacji[16][0] > 300:
                    self.pozycja_animacji[16][1] = 1
                else:
                    self.pozycja_animacji[16][0] = self.pozycja_animacji[16][0]+1
            else: #dla zmiany kierunku
                if self.pozycja_animacji[16][0] < 0:
                    self.pozycja_animacji[16][1] = 0
                else:
                    self.pozycja_animacji[16][0] = self.pozycja_animacji[16][0]-1
            self.posX = (-600) + self.pozycja_animacji[16][0]
            if(tapeta.find('02') != -1 and sensorOutside.nightFlag == False):
                self.kolorczcionki3 = (185,242,107,255)
                self.kolorczcionki4 = (235,255,187,255)
            else:
                self.kolorczcionki3 = (0,0,0,255)
                self.kolorczcionki4 = (60,60,60,200)
            if sensorOutside.nightFlag == True:
                self.kolorczcionki3 = (190,190,190,255)
                self.kolorczcionki4 = (250,250,250,200)
        display.display_picture(display.screen, self.posX , 0, 255, display.get_background(sensorOutside.nightFlag, weather.iconToday)) 
        if(tapeta.find('01') != -1):  #CLEAR SKY
            self.kolorczcionki1=(255,255,255,255)
            self.posX=0
            if sensorOutside.nightFlag==True:
                self.kolorczcionki2=(180,180,180,255)
            else:
                self.kolorczcionki2=(100,40,20,255)
            self.kolorczcionki3=(255,255,155,255)
            self.kolorczcionki4=(255,215,0,255)
            self.kolorczcionki5=(255,82,0,255)
        elif(tapeta.find('50') != -1):
            self.posX=0
            self.kolorczcionki1=(0,105,56,255)
            self.kolorczcionki2=(100,40,20,255)
            self.kolorczcionki3=(95,103,56,255)
            self.kolorczcionki4=(255,215,0,255)
            self.kolorczcionki5=(255,82,0,255)
        elif(tapeta.find('09') != -1 or tapeta.find('10') != -1):  #RAIN
            self.posX=0
            self.kolorczcionki1=(255,255,255,255)
            self.kolorczcionki2=(255,200,100,255)
            self.kolorczcionki5=(255,255,255,255)
            self.kolorczcionki3=(255,255,155,255)
            self.kolorczcionki4=(255,255,200,255)
            for i in range(6):
                display.display_picture(display.screen, randint(30, 750), randint(70, 300), 255, display.get_picture("anim")) 
        elif(tapeta.find('11') != -1): #THUNDERSTORM
            self.posX=0
            self.kolorczcionki1=(255,255,255,255)
            self.kolorczcionki2=(255,200,100,255)
            self.kolorczcionki3=(255,255,155,255)
            self.kolorczcionki4=(255,215,0,255)
            self.kolorczcionki5=(255,82,0,255)
            if self.pozycja_animacji[17][0]<0:
                display.display_picture(display.screen,0, 0, 255, display.get_picture("DTStorm2"))
                self.pozycja_animacji[17][0]=randint(7, 70)
            else:
                self.pozycja_animacji[17][0]=self.pozycja_animacji[17][0]-1
        elif(tapeta.find('13') != -1): #SNOW
            self.posX=0
            self.tfps=0.0
            flakesArray=[["snowflake1", 1], ["snowflake2", 2], ["snowflake3", 4], ["snowflake3", 4], ["snowflake3", 4], ["snowflake3", 4], ["snowflake3", 4], ["snowflake4", 1], ["snowflake5", 3], ["snowflake5", 3], ["snowflake5", 3], ["snowflake6", 4], ["snowflake6", 4], ["snowflake3", 5], ["snowflake6", 4], ["snowflake6", 4]]
            for i in range(15):
                display.display_picture(display.screen, self.pozycja_animacji[i][0], self.pozycja_animacji[i][1], 255, display.get_picture(flakesArray[i][0]))
                self.pozycja_animacji[i][1]=self.pozycja_animacji[i][1]+flakesArray[i][1]
            for px in range(16):
                if self.pozycja_animacji[px][1]>randint(480, 500):
                    self.pozycja_animacji[px][0]=randint(10, 780)
                    self.pozycja_animacji[px][1]=0
            self.kolorczcionki1=(255,255,255,255)
            self.kolorczcionki2=(255,200,100,255)
            self.kolorczcionki5=(255,255,255,255)
            self.kolorczcionki4=(160,180,160,255)
            self.kolorczcionki3=(220,220,250,255)
        #------------------------
        d = datetime.datetime.today()
        dzienTygodnia=dateDec.day(d.weekday())

        display.text_center(display.screen, str(time.strftime("%H:%M")),"Nimbus Sans L",190,295,90,self.kolorczcionki1,255) #czas
        display.text_center(display.screen, dzienTygodnia,"Nimbus Sans L",56,620,80,self.kolorczcionki2,255)  #dzien tygodnia
        display.text_center(display.screen, str(int(time.strftime("%d")))+" "+dateDec.month(str(time.strftime("%B"))),"Nimbus Sans L",56,620,120,self.kolorczcionki2,255)  #dzien tygodnia

        display.text2(display.screen, "dziś","Nimbus Sans L",56,50,170,self.kolorczcionki3,255)
        display.display_picture(display.screen, 30, 210, 255, display.get_icon(sensorOutside.nightFlag, weather.iconToday))
        display.display_picture(display.screen, 20, 330, 255, display.get_picture("arrow_down"))
        display.text2(display.screen, "{:.0f}°C".format(weather.tempMinToday),"Nimbus Sans L",54,70,330,self.kolorczcionki3,255)
        display.display_picture(display.screen, 20, 380, 255, display.get_picture("arrow_up"))
        display.text2(display.screen, "{:.0f}°C".format(weather.tempMaxToday),"Nimbus Sans L",54,70,380,self.kolorczcionki4,255)
        display.text2(display.screen, "jutro","Nimbus Sans L",56,230,170,self.kolorczcionki3,255)
        display.display_picture(display.screen, 220, 210, 255, display.get_icon(sensorOutside.nightFlag, weather.iconTomorrow))
        display.display_picture(display.screen, 205, 330, 255, display.get_picture("arrow_down"))
        display.text2(display.screen, "{:.0f}°C".format(weather.tempMinTomorrow),"Nimbus Sans L",54,245,330,self.kolorczcionki3,255)
        display.display_picture(display.screen, 205, 380, 255, display.get_picture("arrow_up"))
        display.text2(display.screen, "{:.0f}°C".format(weather.tempMaxTomorrow),"Nimbus Sans L",54,245,380,self.kolorczcionki4,255)

        display.display_picture(display.screen, 390, 170, 255, display.get_picture("temp_out"))
        dlugosc=display.text2(display.screen, "{:.1f}°C".format(sensorOutside.temperature),"Nimbus Sans L",68,485,190,self.kolorczcionki5,255)
        display.text2(display.screen, "{:.0f}%".format(sensorOutside.humidity),"Nimbus Sans L",48,505+dlugosc,200,self.kolorczcionki4,255)
        display.display_picture(display.screen, 390, 258, 255, display.get_picture("temp_in"))
        dlugosc=display.text2(display.screen, "{:.1f}°C".format(sensorRoom1Temperature.temp),"Nimbus Sans L",68,485,280,self.kolorczcionki4,255)
        display.text2(display.screen, "{:.0f}%".format(sensorRoom1Temperature.humi),"Nimbus Sans L",48,505+dlugosc,290,self.kolorczcionki4,255)

        display.display_picture(display.screen, 390, 350, 255, display.get_picture("wind"))
        dlugosc=display.text2(display.screen, "{:.1f}m/s".format(sensorOutside.windSpeed),"Nimbus Sans L",50,485,370,self.kolorczcionki3,255)

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
            display.text2(display.screen, infoStrip.displayedInformation,"Nimbus Sans L",46,70,480-(infoStrip.position*13),self.kolorPaskaInfo,255)

    def obraz_nocny(self):
        self.kolorczcionki3=(180,180,180,255)

        display.text_center_background(display.screen, str(time.strftime("%H:%M")),"Nimbus Sans L",360,400,210, self.kolorczcionki3,255,(0,0,0,255)) #czas
        display.text_background(display.screen, "Temperatura {:.1f}°C".format(sensorRoom1Temperature.temp),"Nimbus Sans L",70,20,410, self.kolorczcionki3,255,(0,0,0,255))

gui = Gui()