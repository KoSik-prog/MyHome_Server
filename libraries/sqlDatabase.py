#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    import traceback, sqlite3, datetime, sys ,os, time
except ImportError:
    print "Import error"

from libraries.log import *

class SQL_CL:
    databaseLoc = '/var/www/html/home_database.db'
    flagBusy = False

    def addRecordSensorOutdoorTemp (self, temp, humi, wiatr, kierunek):
        for i in range(100):
            if self.flagBusy == False:
                break
            time.sleep(.001)
        self.flagBusy = True
        conn=sqlite3.connect(self.databaseLoc)
        curs=conn.cursor()
        try:
            curs.execute("INSERT INTO tempzewnetrzna values(datetime('now','localtime'),?,?,?,?)",[temp,humi,wiatr,kierunek])
            conn.commit()
        except sqlite3.IntegrityError:
            print("SQL record exist")    
        conn.close()
        self.flagBusy = False

    def addRecordSensorOutdoorLight (self, lux1, ir1):
        for i in range(100):
            if self.flagBusy == False:
                break
            time.sleep(.001)
        self.flagBusy = True
        conn=sqlite3.connect(self.databaseLoc)
        curs=conn.cursor()
        try:
            curs.execute("INSERT INTO swiatlo values(datetime('now','localtime'),?,?)",[lux1,ir1])
            conn.commit()
        except sqlite3.IntegrityError:
            print("SQL record exist")
        conn.close()
        self.flagBusy = False

    def addRecordSensorTemp(self, room, temp, humi):
        for i in range(100):
            if self.flagBusy == False:
                break
            time.sleep(.001)
        self.flagBusy = True
        conn=sqlite3.connect(self.databaseLoc)
        curs=conn.cursor()
        try:
            curs.execute("INSERT INTO ? values(datetime('now','localtime'),?,?)",[room, temp,humi])
            conn.commit()
        except sqlite3.IntegrityError:
            print("SQL record exist")
        conn.close()
        self.flagBusy = False

    def addRecordFlower(self, flowerNumber, humidity, sun, power, humidity_raw):
        for i in range(100):
            if self.flagBusy == False:
                break
            time.sleep(.001)
        self.flagBusy = True
        conn=sqlite3.connect(self.databaseLoc)
        curs=conn.cursor()
        try:
            if(flowerNumber == 1):
                curs.execute("INSERT INTO kwiatek values(datetime('now','localtime'),?,?,?,?)",[humidity, sun, power, humidity_raw])
            else:
                curs.execute("INSERT INTO kwiatek? values(datetime('now','localtime'),?,?,?,?)",[flowerNumber, humidity, sun, power, humidity_raw])
            conn.commit()
        except sqlite3.IntegrityError:
            print("SQL record exist")
        conn.close()
        self.flagBusy = False

    def delete_records(self, days):
        #daysVar = "timestamp<datetime('now', '{} days')".format(days)
        for i in range(100):
            if self.flagBusy == False:
                break
            time.sleep(.001)
        self.flagBusy = True
        conn=sqlite3.connect(self.databaseLoc)
        curs=conn.cursor()
        try:
            curs.execute("DELETE FROM temppokoju WHERE timestamp < datetime('now', '{day} days')".format(day = days))
            curs.execute("DELETE FROM tempsypialni WHERE timestamp < datetime('now', '{day} days')".format(day = days))
            curs.execute("DELETE FROM tempzewnetrzna WHERE timestamp < datetime('now', '{day} days')".format(day = days))
            curs.execute("DELETE FROM swiatlo WHERE timestamp < datetime('now', '{day} days')".format(day = days))
            curs.execute("DELETE FROM kwiatek WHERE timestamp < datetime('now', '{day} days')".format(day = days))
            curs.execute("DELETE FROM kwiatek2 WHERE timestamp < datetime('now', '{day} days')".format(day = days))
            curs.execute("DELETE FROM kwiatek3 WHERE timestamp < datetime('now', '{day} days')".format(day = days))
            curs.execute("DELETE FROM kwiatek4 WHERE timestamp < datetime('now', '{day} days')".format(day = days))
            curs.execute("DELETE FROM kwiatek5 WHERE timestamp < datetime('now', '{day} days')".format(day = days))
            curs.execute("DELETE FROM kwiatek6 WHERE timestamp < datetime('now', '{day} days')".format(day = days))
            conn.commit()
        except sqlite3.IntegrityError:
            print("SQL error")
        conn.close()


sql = SQL_CL()