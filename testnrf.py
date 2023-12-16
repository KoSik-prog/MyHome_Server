from lib.nrfConnect import *
from lib.lib_nrf24 import NRF24

nrf.to_send([0x33, 0x33, 0x33, 0x11, 0x99], "50", NRF24.PA_LOW)

print("sended")