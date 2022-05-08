#!/usr/bin/env python
# -*- coding: utf-8 -*-
try:
    import os, sys, locale, datetime, time, configparser, requests, json, pygame
except ImportError:
    log.add_log("Modul Import Error")

from pygame.compat import geterror
from libraries.log import *

#initialize
pygame.init()
resolution = 800, 480
screen = pygame.display.set_mode(resolution,1)

''' ICONS NR
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

class WEATHER_CL:
    tempMinToday=0.0
    tempMinTomorrow=0.0
    tempMaxToday=0.0
    tempMaxTomorrow=0.0
    iconToday="01d"
    iconTomorrow="01d"

    def __init__(self):
        self.BrokenClouds = self.load_image('ikony', "Broken_Clouds.gif")
        self.ClearSky = self.load_image('ikony', "Clear_Sky.gif")
        self.ClearSkyNight = self.load_image('ikony', "Clear_Sky_Night.gif")
        self.FewClouds = self.load_image('ikony', "Few_Clouds.gif")
        self.Fog = self.load_image('ikony', "Mist.gif")
        self.Rain = self.load_image('ikony', "Rain.gif")
        self.ScatteredClouds = self.load_image('ikony', "Scattered_Clouds.gif")
        self.ScatteredCloudsNight = self.load_image('ikony', "Scattered_Clouds_Night.gif")
        self.ShowerRain = self.load_image('ikony', "Shower_Rain.gif")
        self.Snow = self.load_image('ikony', "Snow.gif")
        self.Thunderstorm = self.load_image('ikony', "Thunderstorm.gif")
        #---
        self.DCloudy = self.load_image('pic', "Cloudy.jpg")
        self.DCloudyNight = self.load_image('pic', "Cloudy_Night.jpg")
        self.DFewClouds = self.load_image('pic', "Few_Clouds.jpg")
        self.DFewCloudsNight = self.load_image('pic', "Few_Clouds_Night.jpg")
        self.DFog = self.load_image('pic', "Fog.jpg")
        self.DRain = self.load_image('pic', "Rain.jpg")
        self.DSnow = self.load_image('pic', "Snow.jpg")
        self.DSnowNight = self.load_image('pic', "Snow_Night.jpg")
        self.DTStorm = self.load_image('pic', "T-Storm.jpg")
        self.DTStorm2 = self.load_image('pic', "T-Storm2.jpg")
        self.DClearSky = self.load_image('pic', "Sun.jpg")
        self.DClearSkyNight = self.load_image('pic', "Clear_Night.jpg")
        #---
        self.NA = self.load_image('ikony', "na.gif")
        self.arrow_down = self.load_image('ikony', "arrow_down.gif")
        self.arrow_up = self.load_image('ikony', "arrow_up.gif")
        self.snowflake1 = self.load_image('pic', "snowflake1.gif")
        self.snowflake2 = self.load_image('pic', "snowflake2.gif")
        self.snowflake3 = self.load_image('pic', "snowflake3.gif")
        self.snowflake4 = self.load_image('pic', "snowflake4.gif")
        self.snowflake5 = self.load_image('pic', "snowflake5.gif")
        self.snowflake6 = self.load_image('pic', "snowflake6.gif")
        self.RainAnim1 = self.load_image('pic', "rain_anim1.gif")

    def forecast_today(self, forecastText):
        self.tempMaxToday=-50
        self.tempMinToday=50
        flag=0
        select_data = forecastText['list']

        d = datetime.datetime.today()
        for box in select_data:
            if 'dt' in box:
                if float(box['main']['temp_max'])>self.tempMaxToday:
                    self.tempMaxToday=float(box['main']['temp_max'])
                    if(self.tempMaxToday > -1 and self.tempMaxToday <= 0):
                        self.tempMaxToday = 0.0
                if float(box['main']['temp_min'])<self.tempMinToday:
                    self.tempMinToday=float(box['main']['temp_min'])
                    if(self.tempMinToday > -1 and self.tempMinToday <= 0):
                        self.tempMinToday = 0.0
                czas=datetime.datetime.strptime("2020-01-01 12:00:00", '%Y-%m-%d %H:%M:%S')
                if flag==0:
                    self.iconToday=box['weather'][0]['icon']
                    flag=1
            else:
                log.add_log('nie znaleziono pogody na dzis')
            break

    def forecast_tomorrow(self, forecastText):
        self.tempMaxTomorrow=-50
        self.tempMinTomorrow=50
        select_data = forecastText['list']
        d = datetime.datetime.today() + datetime.timedelta(days=1)
        for box in select_data:
            if 'dt_txt' in box:
                data=datetime.datetime.strptime(box['dt_txt'], '%Y-%m-%d %H:%M:%S')
                if data.date()==d.date():
                    if float(box['main']['temp_max'])>self.tempMaxTomorrow:
                        self.tempMaxTomorrow=float(box['main']['temp_max'])
                        if(self.tempMaxTomorrow > -1 and self.tempMaxTomorrow <= 0):
                            self.tempMaxTomorrow = 0.0
                    if float(box['main']['temp_min'])<self.tempMinTomorrow:
                        self.tempMinTomorrow=float(box['main']['temp_min'])
                        if(self.tempMinTomorrow > -1 and self.tempMinTomorrow <= 0):
                            self.tempMinTomorrow = 0.0
                    czas=datetime.datetime.strptime("2020-01-01 12:00:00", '%Y-%m-%d %H:%M:%S')
                    if data.time()==czas.time():
                        self.iconTomorrow=box['weather'][0]['icon']
            else:
                log.add_log('nie znaleziono pogody na jutro')

    def get_forecast(self, miasto):
        log.add_log("Pobieram progrnoze pogody...")
        url='https://api.openweathermap.org/data/2.5/forecast?q={}&mode=json&APPID=85b527bafdfc28a92672434b32ead750&units=metric'.format(miasto)
        try:
            json_data = requests.get(url).json()
            self.forecast_today(json_data)
            self.forecast_tomorrow(json_data)
            log.add_log(' Pobrano prognoze pogody dla miasta ' + miasto)
        except:
            log.add_log("Blad polaczenia z serwerem pogody")

    def save_error(self, error):
        file = open('blad_pogody.txt', 'w')
        file.write(error + '\n')
        file.close()
    
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
            self.save_error(iconName)
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
            self.save_error(iconName)
            pic=self.NA.convert()
        return pic
        
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

weather = WEATHER_CL()