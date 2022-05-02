#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      kosik
#
# Created:     01.02.2020
# Copyright:   (c) kosik 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------      ,
import requests
import sys
import json
from datetime import datetime, timedelta

class Pog:
    Dzis="Mon"
    Jutro="Mon"
    Temp="0"
    TempMinDzis="0"
    TempMinJutro="0"
    TempMaxDzis="0"
    TempMaxJutro="0"
    OpadDzis="0"
    OpadJutro="0"
    IkonaDzis="Sunny"
    IkonaJutro="Sunny"
    BaroKierunek=""
    Cisnienie=""
    Wiatr=""
    Wilgotnosc=""
Pogoda = Pog()

api_address='http://api.openweathermap.org/data/2.5/weather?APPID=85b527bafdfc28a92672434b32ead750&units=metric&q=Hanau'
api_add='http://api.openweathermap.org/data/2.5/forecast?id=2911007&mode=json&APPID=85b527bafdfc28a92672434b32ead750&units=metric'
url = api_add
json_data = requests.get(url).json()
#print(json_data)

def prognozaDzis(prognoza):
    Pogoda.TempMaxDzis=-50
    Pogoda.TempMinDzis=50
    flaga=0
    select_data = prognoza['list']
    #obliczenia daty
    d = datetime.today()
    for box in select_data:
        if 'dt' in box:
            print (box)
            if float(box['main']['temp_max'])>Pogoda.TempMaxDzis:
                Pogoda.TempMaxDzis=float(box['main']['temp_max'])
            if float(box['main']['temp_min'])<Pogoda.TempMinDzis:
                Pogoda.TempMinDzis=float(box['main']['temp_min'])
            czas=datetime.strptime("2020-01-01 12:00:00", '%Y-%m-%d %H:%M:%S')
            if flaga==0:
                Pogoda.IkonaDzis=box['weather'][0]['description']
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
                if float(box['main']['temp_min'])<Pogoda.TempMinJutro:
                    Pogoda.TempMinJutro=float(box['main']['temp_min'])
                czas=datetime.strptime("2020-01-01 12:00:00", '%Y-%m-%d %H:%M:%S')
                if data.time()==czas.time():
                    Pogoda.IkonaJutro=box['weather'][0]['description']
        else:
            print('weather not found')

prognozaDzis(json_data)
prognozaJutro(json_data)
print('{}/{} -> {}'.format(Pogoda.TempMaxDzis,Pogoda.TempMinDzis, Pogoda.IkonaDzis))
print('{}/{} -> {}'.format(Pogoda.TempMaxJutro,Pogoda.TempMinJutro, Pogoda.IkonaJutro))



