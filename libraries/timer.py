#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        timer
# Purpose:
#
# Author:      KoSik
#
# Created:     18.05.2022
# Copyright:   (c) kosik 2022
#-------------------------------------------------------------------------------
try:
    import time
except ImportError:
    print "Blad importu"


from libraries.log import *
from libraries.sqlDatabase import *
from lights import *
from devicesList import *

class TIMER_CL:
    def timer_start(self):
        while(1):
            self.check_timer()
            time.sleep(10)


    def check_timer(self):  #SPRAWDZENIE CO WYKONAC O DANEJ PORZE
        #----------------------SPRAWDZENIE BAZY DANYCH SQL-----------------------kasowanie starych rekordow------------
        if (str(time.strftime("%d"))=="01") and (str(time.strftime("%H:%M"))=="01:00") and SQL_CL.kasowanieSQL_flaga==False:
            sql.delete_records(30) #kasowanie starych rekordow z bazy danych
            SQL_CL.kasowanieSQL_flaga=True
            log.add_log("Skasowano stare dane z SQL")
        if (str(time.strftime("%d"))=="01") and (str(time.strftime("%H:%M"))=="01:01") and SQL_CL.kasowanieSQL_flaga==True:
            SQL_CL.kasowanieSQL_flaga=False
        #------------------------------------------------------------------------------------------
        self.auto_timer(lampaTV)
        self.auto_timer(dekoPok1)
        self.auto_timer(deko2Pok1)
        self.auto_timer(dekoFlaming)
        self.auto_timer(lampaPok2Tradfri)
        self.auto_timer(lampaPok2)#---- LED SYPIALNI
        self.auto_timer(hydroponika)#----Hydroponika
        #self.auto_timer(lampaKuch)#-----LED KUCHNI
        #self.auto_timer(dekoUsb)#----USB Stick


    def auto_timer(self, klasa):
        format = '%H:%M:%S.%f'
        aktual=datetime.datetime.now().time()
        try:
            zmiennaON = datetime.datetime.strptime(str(aktual), format) - datetime.datetime.strptime(klasa.AutoON, format) # obliczenie roznicy czasu
        except ValueError as e:
            print('Blad czasu wł:', e)
        try:
            zmiennaOFF = datetime.datetime.strptime(str(aktual), format) - datetime.datetime.strptime(klasa.AutoOFF, format) # obliczenie roznicy czasu
        except ValueError as e:
            print('Blad czasu wył:', e)
        #-----skasowanie flag ----------
        if(int(zmiennaON.total_seconds())>(-15) and int(zmiennaON.total_seconds())<0 and  klasa.FlagaSterowanieManualne==True):
            klasa.FlagaSterowanieManualne=False
        if(int(zmiennaOFF.total_seconds())>(-15) and int(zmiennaOFF.total_seconds())<0 and klasa.FlagaSterowanieManualne==True):
            klasa.FlagaSterowanieManualne=False
        #------SPRAWDZENIE------------------------
        if(klasa.Flaga==0 and automatykaOswietlenia.swiatloObliczone<klasa.AutoLux_min and (int(zmiennaON.total_seconds())>0) and (int(zmiennaOFF.total_seconds())<(-60)) and klasa.FlagaSterowanieManualne==False and klasa.blad<20):
            log.add_log("AUTO {} -> ON".format(klasa.Opis))
            light.set_light(klasa.address, klasa.AutoJasnosc)
            klasa.Flaga=1
            time.sleep(20)
        if(klasa.Flaga==1 and (int(zmiennaOFF.total_seconds())>0) and (int(zmiennaOFF.total_seconds())<60) and klasa.FlagaSterowanieManualne==False and klasa.blad<20):
            log.add_log("AUTO {} -> OFF".format(klasa.Opis))
            light.set_light(klasa.address, 0)
            klasa.Flaga=0
            time.sleep(20)
timer = TIMER_CL()