#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:        timer
# Purpose:
#
# Author:      KoSik
#
# Created:     18.05.2022
# Copyright:   (c) kosik 2022
# -------------------------------------------------------------------------------
try:
    import time
    from lib.log import *
    from lib.sqlDatabase import *
    from lights import *
    from devicesList import *
except ImportError:
    print("Import error - timer")


class Timer:
    def timer_thread(self):
        while server.read_server_active_flag() == True:
            self.check_timer()
            time.sleep(10)

    def check_timer(self):
        # ----------------------SQL records check -------------------------------------------------
        if (str(time.strftime("%d")) == "01") and (str(time.strftime("%H:%M")) == "01:00") and Sql.flagSqlRecordsDelete == False:
            sql.delete_records(30)  # delete old records
            Sql.flagSqlRecordsDelete = True
            log.add_log("Obsolete SQL data deleted")
        if (str(time.strftime("%d")) == "01") and (str(time.strftime("%H:%M")) == "01:01") and Sql.flagSqlRecordsDelete == True:
            Sql.flagSqlRecordsDelete = False
        # ------------------------------------------------------------------------------------------
        for device in deviceArray:
            device.auto_timer()

timer = Timer()
