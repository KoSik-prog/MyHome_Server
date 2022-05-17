#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        ikea
# Purpose:
#
# Author:      KoSik
#
# Created:     13.05.2022
# Copyright:   (c) kosik 2022
#-------------------------------------------------------------------------------
import sys, re, os, ConfigParser

from tradfri import tradfriStatus
from tradfri import tradfriActions
from libraries.log import *

import subprocess as sp

class IKEA_CL:
    #-------------LOGOWANIE DO TRADFRI ----------------
    MACaddress='44:91:60:2c:b3:6f'          # ADRES MAC BRAMY
    ipAddress='192.168.0.100' #podstawowy adres ip (gdy nie można odczytac)
    securityid = "B5dyJuhKqdgfDdkA"   # HASLO BRAMY
    user_id=""
    security_user=""
    
    def __init__(self):
        try:   
            ipAdd = self.ikea_get_ip(self.MACaddress)
            if(ipAdd != -1):
                self.ipAddress
                log.add_log("Ikea Tradfri -> Pobrane IP: {}".format(self.MACaddress))
            else:
                log.add_log("Ikea Tradfri -> Stałe IP: {}".format(self.MACaddress))
        except:
            log.add_log("Ikea Tradfri -> nie mozna pobrac adresu IP")
        self.connect()

    def ikea_get_ip(self, MACaddress):
        pipe = sp.Popen( 'arp -a', shell=True, stdout=sp.PIPE, stderr=sp.PIPE )
        res = pipe.communicate()

        ipRetData = res[0]
        for i in range(ipRetData.count('\n')):
            pos = ipRetData.find('\n')
            ipData, ipRetData = ipRetData[:pos], ipRetData[pos+1:]
            if ipData.find(MACaddress) != -1:
                ipAddress = ipData[ipData.find('(')+1 : ipData.find(')')]
                return ipAddress
            else: 
                return -1
        

    def connect(self):
        try:
            self.security_user, self.user_id =(self.tradfri_login(self.ipAddress, self.securityid))
            log.add_log("Ikea Tradfri -> polaczono id: {}    pass: {}".format(self.user_id, self.security_user))
        except:
            log.add_log("Ikea Tradfri -> nie mozna polaczyc z bramka")

    def tradfri_login(self, ipAddress, securityid):
        security=" "
        for x in range(100):
            try:
                security = tradfriStatus.tradfri_get_security(ipAddress, securityid, x)
                user_id=x
                break
            except:
                pkt_pocz=0
        tekst=str(security)
        pkt_s=tekst.find("9091")
        pkt_pocz=tekst.find("u'", pkt_s)
        pkt_konc=tekst.find("'", pkt_pocz+2)
        return (tekst[pkt_pocz+2:pkt_konc],user_id)
        
    def ikea_check(self, ipAddress, securityid, result):
        if result.find("v:") != -1:
            return "0", "0"
        else:
            list=(tradfri_login(ipAddress, securityid))   #logowanie do bramy
            user_id=list[1]
            security_user=list[0]
            log.add_log("Ikea Tradfri -> haslo wygaslo - nowe id: {}".format(user_id))
            return security_user, user_id       

    def ikea_power_light(self, ipAddress, user_id, securityid, security_user, lightid, value):
        result = tradfriActions.tradfri_power_light(ipAddress, user_id, security_user, lightid, value)
        new_pass, new_id = self.ikea_check(ipAddress, securityid, result)
        if(new_id != "0"):
            security_user=new_pass
            user_id = new_id
            result = tradfriActions.tradfri_power_light(ipAddress, user_id, security_user, lightid, value)
            return security_user, user_id
        else:
            return "0", "0"

    def ikea_dim_light(self, ipAddress, user_id, securityid, security_user, lightid,value):
        result = tradfriActions.tradfri_dim_light(ipAddress, user_id, security_user, lightid, value)
        new_pass, new_id = self.ikea_check(ipAddress, securityid, result)
        if(new_id != "0"):
            security_user=new_pass
            user_id = new_id
            result = tradfriActions.tradfri_dim_light(ipAddress, user_id, security_user, lightid, value)
            return security_user, user_id
        else:
            return "0", "0"

    def ikea_color_light(self, ipAddress, user_id, securityid, security_user, lightid,value):    # VALUE COLD/WARM/NORMAL
        result = tradfriActions.tradfri_color_light(ipAddress, user_id, security_user, lightid, value)
        new_pass, new_id = self.ikea_check(ipAddress, securityid, result)
        if(new_id != "0"):
            security_user=new_pass
            user_id = new_id
            result = tradfriActions.tradfri_color_light(ipAddress, user_id, security_user, lightid, value)
            return security_user, user_id
        else:
            return "0", "0"

    def ikea_light_brightness(self, ipAddress, user_id, securityid, security_user, lightid, value):
        result = tradfriActions.tradfri_dim_light(ipAddress, user_id, security_user, lightid, value)
        new_pass, new_id = self.ikea_check(ipAddress, securityid, result)
        if(new_id != "0"):
            security_user=new_pass
            user_id = new_id
            result = tradfriActions.tradfri_dim_light(ipAddress, user_id, security_user, lightid, value)
            return security_user, user_id
        else:
            return "0", "0"

    def ikea_light_color(self, ipAddress, user_id, securityid, lightbulbid, value):  # raczej nie dziala - do poprawy security_user
        result = tradfriActions.tradfri_light_color(ipAddress, user_id, securityid, lightbulbid, value)
        new_pass, new_id = self.ikea_check(ipAddress, securityid, result)
        if(new_id != "0"):
            security_user=new_pass
            user_id = new_id
            result = tradfriActions.tradfri_light_color(ipAddress, user_id, securityid, lightbulbid, value)
            return security_user, user_id
        else:
            return "0", "0"

    def ikea_color_lamp(self, ipAddress, user_id, securityid, security_user, lightid,value1, value2):    # VALUE COLD/WARM/NORMAL
        result = tradfriActions.tradfri_color_lamp(ipAddress, user_id, security_user, lightid, value1, value2)
        new_pass, new_id = self.ikea_check(ipAddress, securityid, result)
        if(new_id != "0"):
            security_user=new_pass
            user_id = new_id
            result = tradfriActions.tradfri_color_lamp(ipAddress, user_id, security_user, lightid, value1, value2)
            return security_user, user_id
        else:
            return "0", "0"

    def ikea_RGB_lamp(self, ipAddress, user_id, securityid, security_user, lightid, red, green, blue):    # VALUE COLD/WARM/NORMAL
        result = tradfriActions.tradfri_RGB_lamp(ipAddress, user_id, security_user, lightid, red, green, blue)
        new_pass, new_id = self.ikea_check(ipAddress, securityid, result)
        if(new_id != "0"):
            security_user=new_pass
            user_id = new_id
            result = tradfriActions.tradfri_RGB_lamp(ipAddress, user_id, security_user, lightid, red, green, blue)
            return security_user, user_id
        else:
            return "0", "0"

    def ikea_power_group(self, ipAddress, user_id, securityid, security_user, groupid, value):
        result = tradfriActions.tradfri_power_group(ipAddress, user_id, security_user, groupid, value)
        log.add_log("rezultat power:  " + result)
        new_pass, new_id = self.ikea_check(ipAddress, securityid, result)
        if(new_id != "0"):
            security_user=new_pass
            user_id = new_id
            result = tradfriActions.tradfri_power_group(ipAddress, user_id, security_user, groupid, value)
            return security_user, user_id
        else:
            return "0", "0"

    def ikea_dim_group(self, ipAddress, user_id, securityid, security_user, groupid,value):
        result = tradfriActions.tradfri_dim_group(ipAddress, user_id, security_user, groupid, value)
        log.add_log("rezultat dim:  " + result)
        new_pass, new_id = self.ikea_check(ipAddress, securityid, result)
        if(new_id != "0"):
            security_user=new_pass
            user_id = new_id
            result = tradfriActions.tradfri_dim_group(ipAddress, user_id, security_user, groupid, value)
            return security_user, user_id
        else:
            return "0", "0"

ikea = IKEA_CL()