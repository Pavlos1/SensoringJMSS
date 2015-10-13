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
temp.address(0x49)
temp.writeWordReg(1, 0b1011000001100000)
error_count = 0

while True:
    try:
        light_t = 0
        sound_t = 0
        temp_t = 0
        for i in range(0, 50):
            light_t += light.read()
            sound_t += sound.read()
            raw_read = temp.readWordReg(0)
            msb = raw_read & 0b11111111
            lsb = (raw_read >> 8)
            if (lsb & 1) == 1:
                lsb >>= 3
                msb <<= 5
            else:
                lsb >>= 4
                msb <<= 4
            correct_read = msb | lsb
            temp_t += (correct_read * 0.0625)
            time.sleep(0.1)
        con = sqlite3.connect("sensor_data.db")
        with con:
            cur = con.cursor()
            command = "insert into data values (%d,%d,%d,%f,%f)" %(int(time.time()), int(light_t/50 - 290), int(sound_t/50), temp_t/50, 0)
            print command
            cur.execute(command)
        con.close()
        error_count = 0
    except:
        error_count += 1
        if error_count < 50:
            print "Something went wrong. Continuing... %d" %error_count
        else:
            print "error_count >= 50. Bailing..."
            os.system("/sbin/reboot")
