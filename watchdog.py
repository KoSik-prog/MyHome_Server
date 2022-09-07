#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      kosik
#
# Created:     21.05.2020
# Copyright:   (c) kosik 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from lib.log import *
from lib.watchdog import *


import xml.etree.cElementTree as ET
import time, os

if __name__ == "__main__":
    watchdog.start()