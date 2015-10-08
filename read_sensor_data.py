#!/usr/local/bin/python
# Written by Pavel
# License: CC BY-SA 4.0

import sqlite3
import time
import mraa

light = mraa.Aio(0)
sound = mraa.Aio(1)
temp = mraa.I2c(0)
temp.address(...)

while True:
    light_t = 0
    sound_t = 0
    temp_t = 0
    for i in range(0, 50):
        light_t += light.read()
        sound_t += sound.read()
        temp_t = ...
    con = ...
    with con:
        cur = ...
        cur.exec...
