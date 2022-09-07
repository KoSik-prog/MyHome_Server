#!/usr/bin/env python
# -*- coding: utf-8 -*-

class DATE_DECODE_CL:
    def day(self, dzientyg):
        if(dzientyg==0):
            return "poniedziałek"
        if(dzientyg==1):
            return "wtorek"
        if(dzientyg==2):
            return "środa"
        if(dzientyg==3):
            return "czwartek"
        if(dzientyg==4):
            return "piątek"
        if(dzientyg==5):
            return "sobota"
        if(dzientyg==6):
            return "niedziela"

    def month(self, mies):
        if(mies=="January"):
            return "stycznia"
        elif(mies=="February"):
            return "lutego"
        elif(mies=="March"):
            return "marca"
        elif(mies=="April"):
            return "kwietnia"
        elif(mies=="May"):
            return "maja"
        elif(mies=="June"):
            return "czerwca"
        elif(mies=="July"):
            return "lipca"
        elif(mies=="August"):
            return "sierpnia"
        elif(mies=="September"):
            return "września"
        elif(mies=="October"):
            return "października"
        elif(mies=="November"):
            return "listopada"
        elif(mies=="December"):
            return "grudnia"
        else:
            return "error"
dateDec = DATE_DECODE_CL()