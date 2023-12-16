#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:        date decode
#
# Author:      KoSik
#
# Created:     26.03.2020
# Copyright:   (c) kosik 2020
# -------------------------------------------------------------------------------

class DateDecode:
    def day(self, dayOfWeek):
        if(dayOfWeek == 0):
            return "poniedziałek"
        if(dayOfWeek == 1):
            return "wtorek"
        if(dayOfWeek == 2):
            return "środa"
        if(dayOfWeek == 3):
            return "czwartek"
        if(dayOfWeek == 4):
            return "piątek"
        if(dayOfWeek == 5):
            return "sobota"
        if(dayOfWeek == 6):
            return "niedziela"

    def month(self, month):
        if(month == "January"):
            return "stycznia"
        elif(month == "February"):
            return "lutego"
        elif(month == "March"):
            return "marca"
        elif(month == "April"):
            return "kwietnia"
        elif(month == "May"):
            return "maja"
        elif(month == "June"):
            return "czerwca"
        elif(month == "July"):
            return "lipca"
        elif(month == "August"):
            return "sierpnia"
        elif(month == "September"):
            return "września"
        elif(month == "October"):
            return "października"
        elif(month == "November"):
            return "listopada"
        elif(month == "December"):
            return "grudnia"
        else:
            return "error"

dateDec = DateDecode()
