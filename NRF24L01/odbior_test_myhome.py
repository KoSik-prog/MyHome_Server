import RPi.GPIO as GPIO
from lib_nrf24 import NRF24
import time
import spidev
from datetime import datetime

GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

def czas():
    now = datetime.now()
    return str(now.strftime("%H:%M:%S.%f"))

def NRFtransmit(dane):
    radio.stopListening()
    message = list(dane)
    radio.write(message)
    radio.startListening()
    while len(message) < 32:
        message.append(0)

pipes = [[0x11, 0x11, 0x11, 0x11, 0x11],[0x33, 0x33, 0x33, 0x33, 0x77],[0x33, 0x33, 0x33, 0x33, 0x44],[0x33, 0x33, 0x33, 0x33, 0x55],[0x33, 0x33, 0x33, 0x33, 0x66]]
#NRF24L01
radio = NRF24(GPIO, spidev.SpiDev())
radio.begin(0,25)
radio.setPayloadSize(24)
radio.setChannel(0x64)
radio.setDataRate(NRF24.BR_250KBPS)
radio.setPALevel(NRF24.PA_MIN)
radio.setAutoAck(True)
radio.openReadingPipe(1, pipes[0])
#radio.openWritingPipe(pipes[1])
radio.printDetails()
radio.startListening()

i=0
q=0
while(1):
    i=i+1
    wiad="#?"+str(i)+"00000000"
    radio.startListening()
    # ackPL = [1]
    razy=0
    time.sleep(1)
    while not radio.available(0):
        time.sleep(.001)
        #if q > 100:
        #    razy=razy+1
        #    NRFtransmit(wiad)
        #    print("wyslano: "+wiad)
        #    q=0
        #q=q+1
    receivedMessage = []
    radio.read(receivedMessage, radio.getDynamicPayloadSize())
    string = ""
    for n in receivedMessage:
        if(n>=16 and n <=126):
            string +=chr(n)
    print (czas()+" --> {}".format(string)+" -> za razem="+str(razy))
    time.sleep(.001)
