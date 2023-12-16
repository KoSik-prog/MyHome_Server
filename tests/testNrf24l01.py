import sys, os, threading
try:
    from time import sleep
    import RPi.GPIO as GPIO
    import spidev
except ImportError:
    print("Import error - nrf connect")

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from lib.lib_nrf24 import *

class Nrf():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    radio = NRF24(GPIO, spidev.SpiDev())

    '''txBuffer -> transmit buffer [address, tx_power(PA_LEVEL), message]'''
    txBuffer = [[[], 1, ""], [[], 1, ""], [[], 1, ""], [[], 1, ""], [[], 1, ""],
                [[], 1, ""], [[], 1, ""], [[], 1, ""], [[], 1, ""], [[], 1, ""]]

    def __init__(self, rxAddress):
        self.radio.begin(1, 25)
        self.radio.setPayloadSize(24)
        self.radio.setChannel(0x64)
        self.radio.setDataRate(NRF24.BR_250KBPS)
        self.radio.setPALevel(NRF24.PA_LOW)
        self.radio.setAutoAck(True)
        self.radio.openReadingPipe(1, rxAddress)
        self.radio.openWritingPipe(1)
        self.radio.printDetails()
        self.radio.startListening()

    def nrf24l01_thread(self):
        while True:
            ackPL = [1]
            while not self.radio.available(0):
                time.sleep(1/100)

            receivedMessage = []
            self.radio.read(receivedMessage, self.radio.getDynamicPayloadSize())
            print("Received: {}".format(receivedMessage))

            print("Translating the receivedMessage into unicode characters...")
            string = ""
            for n in receivedMessage:
                # Decode into standard unicode set
                if (n >=32 and n <= 126):
                    string += chr(n)
            print(string)

            self.radio.writeAckPayload(1, ackPL, len(ackPL))
            print("Loaded payload reply of {}".format(ackPL)) 
        # rxBuffer = ""
        # while True:
        #     self.radio.startListening()
        #     # if len(rxBuffer) > 3:
        #     #     self.decode_message(rxBuffer)
        #     while not self.radio.available(0):
        #         self.send()
        #     rxBuffer = self.get_message()
        #     self.radio.stopListening()
        #     time.sleep(.001)

    def to_send(self, address, data, txPower):
        for i in range(len(Nrf.txBuffer)):
            if(Nrf.txBuffer[i][2] == ""):
                Nrf.txBuffer[i][0] = address
                Nrf.txBuffer[i][1] = txPower
                Nrf.txBuffer[i][2] = data
                break

    def send(self):
        if Nrf.txBuffer[0][2] != "":
            self.radio.openWritingPipe(Nrf.txBuffer[0][0])
            self.radio.setPALevel(Nrf.txBuffer[0][2])  # zmiana mocy nadawania
            time.sleep(.01)
            self.transmit(Nrf.txBuffer[0][2])
        for i in range(len(Nrf.txBuffer) - 1):
            Nrf.txBuffer[i] = Nrf.txBuffer[i+1]
        Nrf.txBuffer[len(Nrf.txBuffer) - 1] = [[], 1, ""]

    def transmit(self, data):
        self.radio.stopListening()
        message = list(data)
        self.radio.write(message)
        self.radio.startListening()
        while len(message) < 32:
            message.append(0)
            
    def get_message(self):
        receivedMessage = ['', '', '', '', '', '', '', '', '', '', '', '', '', '',
                           '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']
        stringNRF = ""
        self.radio.read(receivedMessage, self.radio.getDynamicPayloadSize())
        for n in receivedMessage:
            if(n >= 16 and n <= 126):
                stringNRF += chr(n)
        if stringNRF != "":
            print(("-----> ODEBRANO: {}".format(stringNRF)))
        return stringNRF
    
    
nrf = Nrf([0x11, 0x11, 0x11, 0x11, 0x11])

# -----START-------------------------------------
if __name__ == "__main__":
    print("test program NRF24L01")
    nrfTh = threading.Thread(target=nrf.nrf24l01_thread)
    nrfTh.start()