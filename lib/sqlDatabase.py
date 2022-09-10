#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:        sql database
# Purpose:
#
# Author:      KoSik
#
# Created:     19.09.2019
# Copyright:   (c) kosik 2019
# -------------------------------------------------------------------------------
try:
    import traceback
    import sqlite3
    import datetime
    import sys
    import os
    import time
except ImportError:
    print "Import error"
from lib.log import *


class Sql:
    databaseLoc = '/var/www/html/home_database.db'
    flagBusy = False
    flagSqlRecordsDelete = False

    def add_record_sensor_outdoor_temp(self, temp, humi, wiatr, kierunek):
        self.add_record("zewTemp", "{}, {}, {}, {}".format(temp, humi, wiatr, kierunek))

    def add_record_sensor_outdoor_light(self, lux1, ir1):
        self.add_record("zewSwiatlo", "{}, {}".format(lux1, ir1))

    def add_record_sensor_temp(self, room, temp, humi):
        self.add_record(room, "{}, {}, 0".format(temp, humi))

    def add_record_watering_can(self, humidity, sun, water,  power, humidity_raw, watering):
        self.add_record("kwiatek1", "{}, {}, {}, {}, {}, {}".format(
            humidity, sun, water, power, humidity_raw, watering))

    def add_record_flower(self, flowerNumber, humidity, sun, power, humidity_raw):
        self.add_record("kwiatek{}".format(flowerNumber), "{}, {}, {}, {}".format(humidity, sun, power, humidity_raw))

    def add_record_terrarium(self, tempUP, humiUP, tempDN, humiDN, uvi):
        self.add_record("terrarium", "{}, {}, {}, {}, {}".format(tempUP, humiUP, tempDN, humiDN, uvi))

    def add_record(self, databaseName, record):
        for i in range(100):
            if self.flagBusy == False:
                break
            time.sleep(.001)
        self.flagBusy = True
        conn = sqlite3.connect(self.databaseLoc)
        curs = conn.cursor()
        try:
            curs.execute("INSERT INTO {} values(datetime('now','localtime'), {})".format(databaseName, record))
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
        conn = sqlite3.connect(self.databaseLoc)
        curs = conn.cursor()
        try:
            databases = ["pok1Temp", "Pok2Temp", "zewSwiatlo", "zewTemp", "terrarium",
                         "kwiatek1", "kwiatek2", "kwiatek3", "kwiatek4", "kwiatek5", "kwiatek6"]
            for i in range(len(databases)):
                request = "DELETE FROM {} WHERE timestamp < datetime('now', '-{} days')".format(databases[i], days)
                curs.execute(request)
            curs.execute("VACUUM;")
            conn.commit()
            log.add_log("SQL {} days old records are deleted".format(days))
        except sqlite3.IntegrityError:
            log.add_log("SQL error")
        conn.close()

    def add_table(self, name, data):
        """
        example data -> timestamp DATETIME PRIMARY KEY, wilgotnosc INTEGER, slonce INTEGER, power INTEGER, wilgotnosc_raw INTEGER, podlanie INTEGER
        """
        conn = sqlite3.connect('/var/www/html/home_database.db')
        curs = conn.cursor()
        curs.execute("DROP TABLE IF EXISTS {};".format(name))
        curs.execute("CREATE TABLE IF NOT EXISTS {} ({});".format(name, data))
        conn.commit()
        conn.close()


sql = Sql()
