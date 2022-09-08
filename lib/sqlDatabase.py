#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    import traceback, sqlite3, datetime, sys ,os, time
except ImportError:
    print "Import error"

from lib.log import *

class SQL_CL:
    databaseLoc = '/var/www/html/home_database.db'
    flagBusy = False
    kasowanieSQL_flaga=False

    def add_record(self, databaseName, record):
        for i in range(100):
            if self.flagBusy == False:
                break
            time.sleep(.001)
        self.flagBusy = True
        conn = sqlite3.connect(self.databaseLoc)
        curs = conn.cursor()
        try:
            curs.execute("INSERT INTO zewTemp values(datetime('now','localtime'),?,?,?,?)",[temp, humi, wiatr, kierunek])
            conn.commit()
        except sqlite3.IntegrityError:
            log.add_log("SQL record exist")    
        conn.close()
        self.flagBusy = False

    def add_record_sensor_outdoor_temp (self, temp, humi, wiatr, kierunek):
        for i in range(100):
            if self.flagBusy == False:
                break
            time.sleep(.001)
        self.flagBusy = True
        conn=sqlite3.connect(self.databaseLoc)
        curs=conn.cursor()
        try:
            curs.execute("INSERT INTO zewTemp values(datetime('now','localtime'),?,?,?,?)",[temp, humi, wiatr, kierunek])
            conn.commit()
        except sqlite3.IntegrityError:
            log.add_log("SQL record exist")    
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
            curs.execute("INSERT INTO zewSwiatlo values(datetime('now','localtime'),?,?)",[lux1, ir1])
            conn.commit()
        except sqlite3.IntegrityError:
            log.add_log("SQL record exist")
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
            query = "INSERT INTO {} values(datetime('now','localtime'), {}, {}, {})".format(room, temp, humi, 0)
            curs.execute(query)
            conn.commit()
        except sqlite3.IntegrityError:
            log.add_log("SQL record exist")
        conn.close()
        self.flagBusy = False

    def addRecordWateringCan(self, humidity, sun, water,  power, humidity_raw, watering):
        for i in range(100):
            if self.flagBusy == False:
                break
            time.sleep(.001)
        self.flagBusy = True
        conn=sqlite3.connect(self.databaseLoc)
        curs=conn.cursor()
        try:
            curs.execute("INSERT INTO kwiatek1 values(datetime('now','localtime'), ?, ?, ?, ?, ?, ?)",[humidity, sun, water, power, humidity_raw, watering])
            conn.commit()
        except sqlite3.IntegrityError:
            log.add_log("SQL record exist")
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
            query = "INSERT INTO kwiatek{} values(datetime('now','localtime'), {}, {}, {}, {})".format(flowerNumber, humidity, sun, power, humidity_raw)
            curs.execute(query)
            conn.commit()
        except sqlite3.IntegrityError:
            log.add_log("SQL record exist")
        conn.close()
        self.flagBusy = False

    def addRecordTerrarium(self, tempUP, humiUP, tempDN, humiDN, uvi):
        for i in range(100):
            if self.flagBusy == False:
                break
            time.sleep(.001)
        self.flagBusy = True
        conn=sqlite3.connect(self.databaseLoc)
        curs=conn.cursor()
        try:
            curs.execute("INSERT INTO terrarium values(datetime('now','localtime'),?,?,?,?,?)",[tempUP, humiUP, tempDN, humiDN, uvi])
            conn.commit()
        except sqlite3.IntegrityError:
            log.add_log("SQL record exist")
        conn.close()
        self.flagBusy = False

    def delete_records(self, days):
        for i in range(100):
            if self.flagBusy == False:
                break
            time.sleep(.001)
        self.flagBusy = True
        conn=sqlite3.connect(self.databaseLoc)
        curs=conn.cursor()
        try:
            databases = ["pok1Temp", "Pok2Temp", "zewSwiatlo", "zewTemp", "terrarium", "kwiatek1", "kwiatek2", "kwiatek3", "kwiatek4", "kwiatek5", "kwiatek6"]
            for i in range(len(databases)):
                request = "DELETE FROM {} WHERE timestamp < datetime('now', '-{} days')".format(databases[i], days)
                curs.execute(request)
            curs.execute("VACUUM;")
            conn.commit()
            log.add_log("SQL {} days old records are deleted".format(days))
        except sqlite3.IntegrityError:
            log.add_log("SQL error")
        conn.close()

    def addTable():
        conn=sqlite3.connect('/var/www/html/home_database.db')
        curs=conn.cursor()
        curs.execute("DROP TABLE IF EXISTS kwiatek1;")
        curs.execute("CREATE TABLE IF NOT EXISTS kwiatek1 (timestamp DATETIME PRIMARY KEY, wilgotnosc INTEGER, slonce INTEGER, power INTEGER, wilgotnosc_raw INTEGER, podlanie INTEGER);")
        conn.commit()
        conn.close()


sql = SQL_CL()