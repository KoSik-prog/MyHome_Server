#!/usr/bin/env python

# file        : tradfri-lights.py
# purpose     : getting status from the Ikea tradfri smart lights
#
# author      : harald van der laan
# date        : 2017/04/10
# version     : v1.1.0
#
# changelog   :
# - v1.1.0      refactor for cleaner code                               (harald)
# - v1.0.0      initial concept                                         (harald)

"""
    tradfri-lights.py - controlling the Ikea tradfri smart lights

    This module requires libcoap with dTLS compiled, at this moment there is no python coap module
    that supports coap with dTLS. see ../bin/README how to compile libcoap with dTLS support
"""

# pylint convention disablement:
# C0103 -> invalid-name
# C0200 -> consider-using-enumerate
# pylint: disable=C0200, C0103

from __future__ import print_function

import sys, os, re
import ConfigParser
import argparse
import ikea
from tradfri import tradfriStatus
from time import sleep

#-------------LOGOWANIE DO TRADFRI ----------------
print("start...")
MACaddress='44:91:60:2c:b3:6f'          # ADRES MAC BRAMY
hubip='192.168.0.100' #podstawowy adres ip (gdy nie mo?na odczytac)
securityid = "B5dyJuhKqdgfDdkA"   # HASLO BRAMY
user_id=""
security_user=""
#pobranie adresu IP z serwera
hubip = ikea.ikea_get_ip(MACaddress)

#polaczenie
list2=(ikea.tradfri_login(hubip, securityid))   #logowanie do bramy
user_id=list2[1]
security_user=list2[0]

devices = tradfriStatus.tradfri_get_devices(hubip, user_id, security_user)
print("Urzadzenia: {}".format(devices))
groups = tradfriStatus.tradfri_get_groups(hubip, user_id, security_user)
print("Grupy: {}".format(groups))
print(" START...")
#bulbs=tradfriStatus.tradfri_get_lightbulb(hubip, security_user, 65551)
#print("Zarowki: {}".format(bulbs))
#-----
#security_user=""
print("stary sec_user: " + security_user)
new_pass, new_id = ikea.ikea_dim_group(hubip, user_id, securityid, security_user, 131082, 5)
if(new_id != "0"):
    security_user=new_pass
    user_id = new_id
    print("nowy sec_user: " + security_user)

sleep(1)

#new_pass, new_id = ikea.ikea_dim_light(hubip, user_id, securityid, security_user, 65559, 30)

'''print(". ")
ikea.ikea_dim_group(hubip, user_id, securityid, security_user, 131082, 10)
sleep(1)
print(". ")
ikea.ikea_dim_group(hubip, user_id, securityid, security_user, 131082, 30)
sleep(1)
print(". ")
ikea.ikea_dim_group(hubip, user_id, securityid, security_user, 131082, 50)
sleep(1)
print(". ")
ikea.ikea_dim_group(hubip, user_id, securityid, security_user, 131082, 70)
sleep(1)'''
#print(". ")
#print(ikea.ikea_dim_group(hubip, user_id, securityid, security_user, 131082, 50))


#ikea.ikea_dim_light(hubip, user_id, security_user, 65541, 100)
#for x in range(40):
#    ikea.ikea_color_lamp(hubip, user_id, security_user, 65551, 25000, (x*1000))
#    sleep(1)
