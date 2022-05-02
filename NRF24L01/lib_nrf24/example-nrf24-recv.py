#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Example program to receive packets from the radio link
#

import RPi.GPIO as GPIO
from lib_nrf24 import NRF24
import time
import spidev



pipes = [[0xEE, 0xFD, 0xFD, 0xFD, 0xFF], [0xEE, 0xFD, 0xFD, 0xF0, 0xDF]]

radio2 = NRF24(GPIO, GPIO.SpiDev())
radio2.begin(0,17)

radio2.setRetries(15,15)

radio2.setPayloadSize(16)
radio2.setChannel(0x64)
radio2.setDataRate(NRF24.BR_250KBPS)
radio2.setPALevel(NRF24.PA_MAX)

radio2.setAutoAck(True)
radio2.enableDynamicPayloads()
radio2.enableAckPayload()

radio2.openWritingPipe(pipes[0])
radio2.openReadingPipe(1, pipes[1])

radio2.startListening()
radio2.stopListening()

radio2.printDetails()

radio2.startListening()

c=1
while True:
    akpl_buf = [c,1, 2, 3,4,5,6,7,8,9,0,1, 2, 3,4,5,6,7,8]
    pipe = [0]
    while not radio2.available(pipe):
        time.sleep(10000/1000000.0)

    recv_buffer = []
    radio2.read(recv_buffer, radio2.getDynamicPayloadSize())
    print ("Received:") ,
    print (recv_buffer)
    c = c + 1
    if (c&1) == 0:
        radio2.writeAckPayload(1, akpl_buf, len(akpl_buf))
        print ("Loaded payload reply:"),
        print (akpl_buf)
    else:
        print ("(No return payload)")
