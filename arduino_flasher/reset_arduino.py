#!/usr/local/bin/python

import mraa
import time

resetPin = mraa.Gpio(8)
resetPin.dir(mraa.DIR_OUT)

resetPin.write(0)
time.sleep(0.2)
resetPin.write(1)
