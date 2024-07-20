#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:        socket services
# Purpose:
#
# Author:      KoSik
#
# Created:     07.11.2022
# Copyright:   (c) kosik 2022
# -------------------------------------------------------------------------------
try:
    import datetime
    from lib.log import *
    from lib.firebase import *
except ImportError:
    print("Import error - alarm")


class Alarm:
    deactiveTime = 3600

    def __init__(self) -> None:
        self.timestamp = datetime.datetime(2024, 6, 30, 12, 0, 0)

    def activate_alarm(self):
        self.timestamp = datetime.datetime(2024, 6, 30, 12, 0, 0)

    def deactivate_alarm(self, time = 1800):
        self.deactiveTime = time
        self.timestamp = datetime.datetime.now()
        log.add_log(f"Alarm deactivated until -> {self.timestamp + datetime.timedelta(seconds=time)}")

    def alarm(self, title, message):
        if self.check_time_passed(self.timestamp, self.deactiveTime):
            phoneNotification.send_notification(title, message)
            log.add_log("ALARM! -> {}".format(message))
        else:
            log.add_log("Alarm inactive -> {}".format(message))

    def check_time_passed(self, timestamp, deactTime):
        current_time = datetime.datetime.now()
        time_difference = current_time - timestamp
        return time_difference >= datetime.timedelta(seconds=deactTime)



alarm = Alarm()