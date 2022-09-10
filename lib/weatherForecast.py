#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:        weather forecast
# Purpose:
#
# Author:      KoSik
#
# Created:     18.09.2021
# Copyright:   (c) kosik 2021
# -------------------------------------------------------------------------------

try:
    import os
    import sys
    import locale
    import datetime
    import time
    import configparser
    import requests
    import json
    import pygame
except ImportError:
    log.add_log("Modul Import Error")

from pygame.compat import geterror
from lib.log import *
from devicesList import *

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

class Weather:
    tempMinToday = 0.0
    tempMinTomorrow = 0.0
    tempMaxToday = 0.0
    tempMaxTomorrow = 0.0
    iconToday = "01d"
    iconTomorrow = "01d"

    def __init__(self, city, path):
        self.city = city
        self.id = self.read_auth_key(path)

    def weather_thread(self):
        while server.read_server_active_flag() == True:
            weather.get_forecast(self.city, self.id)
            time.sleep(300)

    def forecast_today(self, forecastText):
        self.tempMaxToday = -50
        self.tempMinToday = 50
        flag = 0
        select_data = forecastText['list']

        d = datetime.datetime.today()
        for box in select_data:
            if 'dt' in box:
                if float(box['main']['temp_max']) > self.tempMaxToday:
                    self.tempMaxToday = float(box['main']['temp_max'])
                    if(self.tempMaxToday > -1 and self.tempMaxToday <= 0):
                        self.tempMaxToday = 0.0
                if float(box['main']['temp_min']) < self.tempMinToday:
                    self.tempMinToday = float(box['main']['temp_min'])
                    if(self.tempMinToday > -1 and self.tempMinToday <= 0):
                        self.tempMinToday = 0.0
                czas = datetime.datetime.strptime("2020-01-01 12:00:00", '%Y-%m-%d %H:%M:%S')
                if flag == 0:
                    self.iconToday = box['weather'][0]['icon']
                    flag = 1
            else:
                log.add_log('nie znaleziono pogody na dzis')
            break

    def forecast_tomorrow(self, forecastText):
        self.tempMaxTomorrow = -50
        self.tempMinTomorrow = 50
        select_data = forecastText['list']
        d = datetime.datetime.today() + datetime.timedelta(days=1)
        for box in select_data:
            if 'dt_txt' in box:
                data = datetime.datetime.strptime(box['dt_txt'], '%Y-%m-%d %H:%M:%S')
                if data.date() == d.date():
                    if float(box['main']['temp_max']) > self.tempMaxTomorrow:
                        self.tempMaxTomorrow = float(box['main']['temp_max'])
                        if(self.tempMaxTomorrow > -1 and self.tempMaxTomorrow <= 0):
                            self.tempMaxTomorrow = 0.0
                    if float(box['main']['temp_min']) < self.tempMinTomorrow:
                        self.tempMinTomorrow = float(box['main']['temp_min'])
                        if(self.tempMinTomorrow > -1 and self.tempMinTomorrow <= 0):
                            self.tempMinTomorrow = 0.0
                    czas = datetime.datetime.strptime("2020-01-01 12:00:00", '%Y-%m-%d %H:%M:%S')
                    if data.time() == czas.time():
                        self.iconTomorrow = box['weather'][0]['icon']
            else:
                log.add_log('nie znaleziono pogody na jutro')

    def get_forecast(self, city, id):
        url = 'https://api.openweathermap.org/data/2.5/forecast?q={}&mode=json&APPID={}&units=metric'.format(city, id)
        try:
            json_data = requests.get(url).json()
            self.forecast_today(json_data)
            self.forecast_tomorrow(json_data)
            log.add_log('Pobrano prognoze pogody dla miasta ' + city)
        except:
            log.add_log("Blad polaczenia z serwerem pogody")

    def get_icon_today(self):
        return self.iconToday

    def get_icon_tomorrow(self):
        return self.iconTomorrow
    
    def read_auth_key(self, path):
        f = open(path + "/forecastAuth.key", "r")
        return f.read()


weather = Weather("Rodgau", 'Desktop/Home')
