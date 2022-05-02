import RPi.GPIO as GPIO
from lib_nrf24 import NRF24
import time
import spidev

def NRFtransmit(dane):
    radio.stopListening()
    message = list(dane)
    while len(message) < 32:
        message.append(0)
    radio.write(message)
    
GPIO.setmode(GPIO.BCM)

pipes = [[0x33, 0x33, 0x33, 0x33, 0x33],[0x11, 0x11, 0x11, 0x11, 0x55]]

radio = NRF24(GPIO, spidev.SpiDev())
radio.begin(1, 22)

radio.setPayloadSize(16)
radio.setChannel(0x64)
radio.setDataRate(NRF24.BR_250KBPS)
radio.setPALevel(NRF24.PA_MAX)

radio.setAutoAck(True)
#radio.enableDynamicPayloads()
radio.enableAckPayload()
#radio.write_register(NRF24.FEATURE,0x00)
#radio.write_register(NRF24.DYNPD,0x03)

radio.openReadingPipe(1, pipes[1])
radio.openWritingPipe(pipes[0])
radio.printDetails()
radio.stopListening()

while(1):
    message = list("#K020000000")
    #while len(message) < 32:
    #    message.append(0)
    radio.write(message)
    print("sended")
    #radio.startListening()
    time.sleep(.5)
    radio.stopListening()
    time.sleep(.5)
