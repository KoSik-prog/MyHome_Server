#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      kosik
#
# Created:     25.10.2019
# Copyright:   (c) kosik 2019
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from __future__ import print_function

import sys, re, os, json, time, ConfigParser

from tradfri import tradfriStatus
from tradfri import tradfriActions
from tqdm import tqdm

def tradfri_login(hubip, securityid):
    security=" "
    for x in range(100):
        try:
            security = tradfriStatus.tradfri_get_security(hubip, securityid, x)
            user_id=x
            break
        except:
            pkt_pocz=0
    tekst=str(security)
    pkt_s=tekst.find("9091")
    pkt_pocz=tekst.find("u'", pkt_s)
    pkt_konc=tekst.find("'", pkt_pocz+2)
    return (tekst[pkt_pocz+2:pkt_konc],user_id)
    
def ikea_check(hubip, securityid, result):
    if result.find("v:") != -1:
        return "0", "0"
    else:
        list=(tradfri_login(hubip, securityid))   #logowanie do bramy
        user_id=list[1]
        security_user=list[0]
        print("Ikea Tradfri -> haslo wygaslo - nowe id: {}".format(user_id))
        return security_user, user_id
        
def ikea_get_ip(MACaddress):
    mac_results = [re.findall('^[\w\?\.]+|(?<=\s)\([\d\.]+\)|(?<=at\s)[\w\:]+', i) for i in os.popen('arp -a')]
    hubip = ""
    for i in range(len(mac_results)):
        if mac_results[i][2] == MACaddress:
            IPaddress=mac_results[i][1]
            hubip=IPaddress[1:IPaddress.find(')')]
            print('Ikea Tradfri -> MAC:{}   IP:{}'.format(MACaddress,hubip)) 
    return hubip        

def ikea_power_light(hubip, user_id, securityid, security_user, lightid, value):
    result = tradfriActions.tradfri_power_light(hubip, user_id, security_user, lightid, value)
    new_pass, new_id = ikea_check(hubip, securityid, result)
    if(new_id != "0"):
        security_user=new_pass
        user_id = new_id
        result = tradfriActions.tradfri_power_light(hubip, user_id, security_user, lightid, value)
        return security_user, user_id
    else:
        return "0", "0"

def ikea_dim_light(hubip, user_id, securityid, security_user, lightid,value):
    result = tradfriActions.tradfri_dim_light(hubip, user_id, security_user, lightid, value)
    new_pass, new_id = ikea_check(hubip, securityid, result)
    if(new_id != "0"):
        security_user=new_pass
        user_id = new_id
        result = tradfriActions.tradfri_dim_light(hubip, user_id, security_user, lightid, value)
        return security_user, user_id
    else:
        return "0", "0"

def ikea_color_light(hubip, user_id, securityid, security_user, lightid,value):    # VALUE COLD/WARM/NORMAL
    result = tradfriActions.tradfri_color_light(hubip, user_id, security_user, lightid, value)
    new_pass, new_id = ikea_check(hubip, securityid, result)
    if(new_id != "0"):
        security_user=new_pass
        user_id = new_id
        result = tradfriActions.tradfri_color_light(hubip, user_id, security_user, lightid, value)
        return security_user, user_id
    else:
        return "0", "0"

def ikea_light_brightness(hubip, user_id, securityid, security_user, lightid, value):
    result = tradfriActions.tradfri_dim_light(hubip, user_id, security_user, lightid, value)
    new_pass, new_id = ikea_check(hubip, securityid, result)
    if(new_id != "0"):
        security_user=new_pass
        user_id = new_id
        result = tradfriActions.tradfri_dim_light(hubip, user_id, security_user, lightid, value)
        return security_user, user_id
    else:
        return "0", "0"

def ikea_light_color(hubip, user_id, securityid, lightbulbid, value):  # raczej nie dziala - do poprawy security_user
    result = tradfriActions.tradfri_light_color(hubip, user_id, securityid, lightbulbid, value)
    new_pass, new_id = ikea_check(hubip, securityid, result)
    if(new_id != "0"):
        security_user=new_pass
        user_id = new_id
        result = tradfriActions.tradfri_light_color(hubip, user_id, securityid, lightbulbid, value)
        return security_user, user_id
    else:
        return "0", "0"

def ikea_color_lamp(hubip, user_id, securityid, security_user, lightid,value1, value2):    # VALUE COLD/WARM/NORMAL
    result = tradfriActions.tradfri_color_lamp(hubip, user_id, security_user, lightid, value1, value2)
    new_pass, new_id = ikea_check(hubip, securityid, result)
    if(new_id != "0"):
        security_user=new_pass
        user_id = new_id
        result = tradfriActions.tradfri_color_lamp(hubip, user_id, security_user, lightid, value1, value2)
        return security_user, user_id
    else:
        return "0", "0"

def ikea_RGB_lamp(hubip, user_id, securityid, security_user, lightid, red, green, blue):    # VALUE COLD/WARM/NORMAL
    result = tradfriActions.tradfri_RGB_lamp(hubip, user_id, security_user, lightid, red, green, blue)
    new_pass, new_id = ikea_check(hubip, securityid, result)
    if(new_id != "0"):
        security_user=new_pass
        user_id = new_id
        result = tradfriActions.tradfri_RGB_lamp(hubip, user_id, security_user, lightid, red, green, blue)
        return security_user, user_id
    else:
        return "0", "0"

def ikea_power_group(hubip, user_id, securityid, security_user, groupid, value):
    result = tradfriActions.tradfri_power_group(hubip, user_id, security_user, groupid, value)
    print("rezultat power:  " + result)
    new_pass, new_id = ikea_check(hubip, securityid, result)
    if(new_id != "0"):
        security_user=new_pass
        user_id = new_id
        result = tradfriActions.tradfri_power_group(hubip, user_id, security_user, groupid, value)
        return security_user, user_id
    else:
        return "0", "0"

def ikea_dim_group(hubip, user_id, securityid, security_user, groupid,value):
    result = tradfriActions.tradfri_dim_group(hubip, user_id, security_user, groupid, value)
    print("rezultat dim:  " + result)
    new_pass, new_id = ikea_check(hubip, securityid, result)
    if(new_id != "0"):
        security_user=new_pass
        user_id = new_id
        result = tradfriActions.tradfri_dim_group(hubip, user_id, security_user, groupid, value)
        return security_user, user_id
    else:
        return "0", "0"