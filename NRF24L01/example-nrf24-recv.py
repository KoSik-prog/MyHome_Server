#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Example program to receive packets from the radio link
#

import RPi.GPIO as GPIO
from lib_nrf24 import NRF24
import time
import spidev

GPIO.setmode(GPIO.BCM)

pipes = [[0xEE, 0xFD, 0xFD, 0xFD, 0xFF], [0xEE, 0xFD, 0xFD, 0xF0, 0xDF]]

radio = NRF24(GPIO, spidev.SpiDev())
radio.begin(0,17)

radio.setRetries(15,15)

radio.setPayloadSize(16)
radio.setChannel(0x64)
radio.setDataRate(NRF24.BR_250KBPS)
radio.setPALevel(NRF24.PA_MAX)

radio.setAutoAck(True)
radio.enableDynamicPayloads()
radio.enableAckPayload()

radio.openWritingPipe(pipes[0])
radio.openReadingPipe(1, pipes[1])

radio.startListening()
radio.stopListening()

radio.printDetails()

radio.startListening()

c=1
while True:
    print("start:")
    akpl_buf = [c,1, 2, 3,4,5,6,7,8,9,0,1, 2, 3,4,5,6,7,8]
    pipe = [0]
    while not radio.available(pipe):
        time.sleep(10000/1000000.0)

    recv_buffer = []
    radio.read(recv_buffer, radio.getDynamicPayloadSize())
    print ("Received:") ,
    print (recv_buffer)
    c = c + 1
    if (c&1) == 0:
        radio.writeAckPayload(1, akpl_buf, len(akpl_buf))
        print ("Loaded payload reply:"),
        print (akpl_buf)
    else:
        print ("(No return payload)")
