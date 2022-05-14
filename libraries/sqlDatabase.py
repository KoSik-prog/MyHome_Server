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
            curs.execute("INSERT INTO zewSwiatlo values(datetime('now','localtime'),?,?)",[lux1, ir1])
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
            query = "INSERT INTO {} values(datetime('now','localtime'), {}, {}, {})".format(room, temp, humi, 0)
            curs.execute(query)
            conn.commit()
        except sqlite3.IntegrityError:
            print("SQL record exist")
        conn.close()
        self.flagBusy = False

    def addRecordWateringCan(self, humidity, sun,water,  power, humidity_raw, watering):
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
            query = "INSERT INTO kwiatek{} values(datetime('now','localtime'), {}, {}, {}, {})".format(flowerNumber, humidity, sun, power, humidity_raw)
            curs.execute(query)
            conn.commit()
        except sqlite3.IntegrityError:
            print("SQL record exist")
        conn.close()
        self.flagBusy = False

    def addRecordTerrarium(self, temp1, humi1, temp2, humi2, uvi):
        for i in range(100):
            if self.flagBusy == False:
                break
            time.sleep(.001)
        self.flagBusy = True
        conn=sqlite3.connect(self.databaseLoc)
        curs=conn.cursor()
        try:
            curs.execute("INSERT INTO terrarium values(datetime('now','localtime'),?,?,?,?,?)",[temp1, humi1, temp2, humi2, uvi])
            conn.commit()
        except sqlite3.IntegrityError:
            print("SQL record exist")
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
            curs.execute("DELETE FROM pok1Temp WHERE timestamp < datetime('now', '30 days')")
            curs.execute("DELETE FROM Pok2Temp WHERE timestamp < datetime('now', '30 days')")
            curs.execute("DELETE FROM zewSwiatlo WHERE timestamp < datetime('now', '30 days')")
            curs.execute("DELETE FROM zewTemp WHERE timestamp < datetime('now', '30 days')")
            curs.execute("DELETE FROM terrarium WHERE timestamp < datetime('now', '30 days')")
            curs.execute("DELETE FROM kwiatek1 WHERE timestamp < datetime('now', '30 days')")
            curs.execute("DELETE FROM kwiatek2 WHERE timestamp < datetime('now', '30 days')")
            curs.execute("DELETE FROM kwiatek3 WHERE timestamp < datetime('now', '30 days')")
            curs.execute("DELETE FROM kwiatek4 WHERE timestamp < datetime('now', '30 days')")
            curs.execute("DELETE FROM kwiatek5 WHERE timestamp < datetime('now', '30 days')")
            curs.execute("DELETE FROM kwiatek6 WHERE timestamp < datetime('now', '30 days')")
            conn.commit()
        except sqlite3.IntegrityError:
            print("SQL error")
        conn.close()

    def addTable():
        conn=sqlite3.connect('/var/www/html/home_database.db')
        curs=conn.cursor()
        curs.execute("DROP TABLE IF EXISTS kwiatek1;")
        curs.execute("CREATE TABLE IF NOT EXISTS kwiatek1 (timestamp DATETIME PRIMARY KEY, wilgotnosc INTEGER, slonce INTEGER, zasilanie INTEGER, wilgotnosc_raw INTEGER, podlanie INTEGER);")
        conn.commit()
        conn.close()


sql = SQL_CL()