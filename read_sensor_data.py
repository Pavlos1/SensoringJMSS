#!/usr/local/bin/python
# Written by Pavel
# License: CC BY-SA 4.0

import sqlite3
import time
import os
import mraa

light = mraa.Aio(0)
sound = mraa.Aio(1)
temp = mraa.I2c(0)
temp.address(...)
error_count = 0

while True:
    try:
        light_t = 0
        sound_t = 0
        temp_t = 0
        for i in range(0, 50):
            light_t += light.read()
            sound_t += sound.read()
            temp_t += ...
        con = sqlite3.connect("sensor_data.db")
        with con:
            cur = con.cursor()
            cur.exec("insert into data (%d,%d,%d,%f,%f)" %(int(time.time()), int(light_t/50), int(sound_t/50), 
temp_t/50, 0))
        con.close()
        error_count = 0
        time.sleep(0.1)
    except:
        if error_count < 20:
            print "Something went wrong. Continuing... %d" %error_count
        else:
            print "error_count >= 20. Bailing..."
            os.system("/sbin/reboot")
