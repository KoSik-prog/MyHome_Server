#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:        watchdog main program
# Purpose:
#
# Author:      KoSik
#
# Created:     21.05.2020
# Copyright:   (c) kosik 2020
# -------------------------------------------------------------------------------
try:
    from lib.log import *
    from lib.watchdog import *
    import xml.etree.cElementTree as ET
    import time
    import os
except ImportError:
    print("Import error - watchdog main")


if __name__ == "__main__":
    watchdog.start()
