#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Example program to send packets to the radio link
#


import RPi.GPIO as GPIO
from lib_nrf24 import NRF24
import time
import spidev
import sqlite3

GPIO.setmode(GPIO.BCM)
GPIO.setup(22,GPIO.OUT)

pipes = [[0xe7, 0xe7, 0xe7, 0xe7, 0xe7], [0x33, 0x33, 0x33, 0x33, 0x33]]

radio = NRF24(GPIO, spidev.SpiDev())
radio.begin(1,25)

radio.setPayloadSize(16)
radio.setChannel(0x64)
radio.setDataRate(NRF24.BR_250KBPS)
radio.setPALevel(NRF24.PA_MAX)
radio.setAutoAck(True)
radio.openReadingPipe(1, pipes[1])
radio.openWritingPipe(pipes[0])
radio.printDetails()


c=1
while True:
    buf = ['H', 'E', 'L', 'O',c]
    c = (c + 1) & 255
    # send a packet to receiver
    radio.write(buf)
    print ("Sent:"),
    print (buf)
    # did it return with a payload?
    if radio.isAckPayloadAvailable():
        pl_buffer=[]
        radio.read(pl_buffer, radio.getDynamicPayloadSize())
        print ("Received back:"),
        print (pl_buffer)
    else:
        print ("Received: Ack only, no payload")
    time.sleep(10)
