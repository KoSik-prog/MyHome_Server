#!/usr/bin/env python

# file        : tradfri/tradfriActions.py
#
# author      : KoSik
# date        : 2019/03/10
# version     : v1.0.0
#

import sys
import os
import json
import subprocess

global coap
coap = '/usr/local/bin/coap-client'

def tradfri_power_light(hubip, user_id, securityid, lightbulbid, value):
    tradfriHub = 'coaps://{}:5684/15001/{}' .format(hubip, lightbulbid)

    if value == 1:
        payload = '{ "3311": [{ "5850": 1 }] }'
    else:
        payload = '{ "3311": [{ "5850": 0 }] }'

    api = '{} -m put -u "IDENT{}" -k "{}" -e \'{}\' "{}"' .format(coap, user_id, securityid,
                                                                          payload, tradfriHub)

    if os.path.exists(coap):
        process = subprocess.Popen(api, stdout=subprocess.PIPE, shell=True)
        (output, error) = process.communicate()
    else:
        sys.stderr.write('[-] libcoap: could not find libcoap\n')
        sys.exit(1)
    return output


def tradfri_dim_light(hubip, user_id, securityid, lightbulbid, value):
    """ function for dimming tradfri lightbulb """
    dim = float(value) * 2.55
    tradfriHub = 'coaps://{}:5684/15001/{}'.format(hubip, lightbulbid)
    payload = '{ "3311" : [{ "5851" : %s }] }' % int(dim)

    api = '{} -m put -u "IDENT{}" -k "{}" -e \'{}\' "{}"'.format(coap, user_id, securityid,payload, tradfriHub)

    if os.path.exists(coap):
        process = subprocess.Popen(api, stdout=subprocess.PIPE, shell=True)
        (output, error) = process.communicate()
    else:
        sys.stderr.write('[-] libcoap: could not find libcoap\n')
        sys.exit(1)
    return output

def tradfri_color_light(hubip, user_id, securityid, lightbulbid, value):
    """ function for color temperature tradfri lightbulb """
    tradfriHub = 'coaps://{}:5684/15001/{}'.format(hubip, lightbulbid)

    if value == 'warm':
        payload = '{ "3311" : [{ "5709" : %s, "5710": %s }] }' % ("33135", "27211")
    elif value == 'normal':
        payload = '{ "3311" : [{ "5709" : %s, "5710": %s }] }' % ("30140", "26909")
    elif value == 'cold':
        payload = '{ "3311" : [{ "5709" : %s, "5710": %s }] }' % ("24930", "24684")

    api = '{} -m put -u "IDENT{}" -k "{}" -e \'{}\' "{}"'.format(coap, user_id, securityid, payload, tradfriHub)

    if os.path.exists(coap):
        process = subprocess.Popen(api, stdout=subprocess.PIPE, shell=True)
        (output, error) = process.communicate()
    else:
        sys.stderr.write('[-] libcoap: could not find libcoap\n')
        sys.exit(1)
    return output

def tradfri_color_lamp(hubip, user_id, securityid, lightbulbid, value1, value2):
    """ function for color temperature tradfri lightbulb """
    tradfriHub = 'coaps://{}:5684/15001/{}'.format(hubip, lightbulbid)

    payload = '{ "3311" : [{ "5709" : %s, "5710": %s }] }' % (value1, value2)

    api = '{} -m put -u "IDENT{}" -k "{}" -e \'{}\' "{}"'.format(coap, user_id, securityid, payload, tradfriHub)

    if os.path.exists(coap):
        process = subprocess.Popen(api, stdout=subprocess.PIPE, shell=True)
        (output, error) = process.communicate()
    else:
        sys.stderr.write('[-] libcoap: could not find libcoap\n')
        sys.exit(1)
    return output

def tradfri_RGB_lamp(hubip, user_id, securityid, lightbulbid, r ,g ,b):
    """ function for color temperature tradfri lightbulb """
    tradfriHub = 'coaps://{}:5684/15001/{}'.format(hubip, lightbulbid)

    red = r/2.55
    green = g / 2.55
    blue = b /2.55

    X = red * 0.664511 + green * 0.154324 + blue * 0.162028
    Y = red * 0.283881 + green * 0.668433 + blue * 0.047685
    Z = red * 0.000088 + green * 0.072310 + blue * 0.986039

    x = (X / (X + Y + Z))
    y = (Y / (X + Y + Z))

    xyX = int(x * 65535 + 0.5)
    xyY = int(y * 65535 + 0.5)

    payload = '{ "3311" : [{ "5709" : %s, "5710": %s }] }' % (xyX, xyY)

    api = '{} -m put -u "IDENT{}" -k "{}" -e \'{}\' "{}"'.format(coap, user_id, securityid, payload, tradfriHub)

    if os.path.exists(coap):
        process = subprocess.Popen(api, stdout=subprocess.PIPE, shell=True)
        (output, error) = process.communicate()
    else:
        sys.stderr.write('[-] libcoap: could not find libcoap\n')
        sys.exit(1)
    return output

def tradfri_light_brightness(hubip, user_id, securityid, lightbulbid, value):
    """ function for power on/off tradfri lightbulb """
    tradfriHub = 'coaps://{}:5684/15001/{}' .format(hubip, lightbulbid)

    payload = '{ "3311": [{ "5851" : %s,}] }' % (value)

    api = '{} -m put -u "IDENT{}" -k "{}" -e \'{}\' "{}"' .format(coap, user_id, securityid,
                                                                          payload, tradfriHub)

    if os.path.exists(coap):
        process = subprocess.Popen(api, stdout=subprocess.PIPE, shell=True)
        (output, error) = process.communicate()
    else:
        sys.stderr.write('[-] libcoap: could not find libcoap\n')
        sys.exit(1)
    return output

def tradfri_light_color(hubip, user_id, securityid, lightbulbid, value1):
    """ function for color temperature tradfri lightbulb """
    tradfriHub = 'coaps://{}:5684/15001/{}'.format(hubip, lightbulbid)

    payload = '{ "3311" : [{ "5706" : %s,}] }' % (value1)

    api = '{} -m put -u "IDENT{}" -k "{}" -e \'{}\' "{}"'.format(coap, user_id, securityid, payload, tradfriHub)

    if os.path.exists(coap):
        process = subprocess.Popen(api, stdout=subprocess.PIPE, shell=True)
        (output, error) = process.communicate()
    else:
        sys.stderr.write('[-] libcoap: could not find libcoap\n')
        sys.exit(1)
    return output


def tradfri_power_group(hubip, user_id, securityid, groupid, value):
    """ function for power on/off tradfri lightbulb """
    tradfriHub = 'coaps://{}:5684/15004/{}' .format(hubip, groupid)

    if value == 1:
        payload = '{ "5850" : 1 }'
    else:
        payload = '{ "5850" : 0 }'

    api = '{} -m put -u "IDENT{}" -k "{}" -e \'{}\' "{}"' .format(coap, user_id, securityid, payload, tradfriHub)

    if os.path.exists(coap):
        #result = os.popen(api)
        process = subprocess.Popen(api, stdout=subprocess.PIPE, shell=True)
        (output, error) = process.communicate()
    else:
        sys.stderr.write('[-] libcoap: could not find libcoap\n')
        sys.exit(1)
    return output


def tradfri_dim_group(hubip,user_id, securityid, groupid, value):
    """ function for dimming tradfri lightbulb """
    tradfriHub = 'coaps://{}:5684/15004/{}'.format(hubip, groupid)
    dim = float(value) * 2.55
    payload = '{ "5851" : %s }' % int(dim)

    api = '{} -m put -u "IDENT{}" -k "{}" -e \'{}\' "{}"'.format(coap, user_id, securityid, payload, tradfriHub)

    if os.path.exists(coap):
        process = subprocess.Popen(api, stdout=subprocess.PIPE, shell=True)
        (output, error) = process.communicate()
    else:
        sys.stderr.write('[-] libcoap: could not find libcoap\n')
        sys.exit(1)
    return output