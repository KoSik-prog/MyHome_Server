#!/usr/bin/env python
# -*- coding: utf-8 -*-
try:
    import os, sys, locale, datetime, time, configparser, requests, json, pygame
except ImportError:
    log.add_log("Modul Import Error")

from pygame.compat import geterror
from libraries.log import *

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

weather = WEATHER_CL()