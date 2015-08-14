#!/usr/local/bin/python
# Written by Pavel.
# License: WTFPL; if you change the source, you must also change the name.

#import mraa
import serial
import sqlite3
import time
import os
import re

#uart = mraa.Uart(0)
os.system("/sbin/modprobe cdc-acm")
acm_devices = [f for f in os.listdir("/dev") if re.match(r"^ttyACM[0-9]$", f)]
print "ACM TTYs found:", acm_devices
selected_device = "/dev/"+acm_devices[0]
ser = serial.Serial(selected_device, 9600)

while True:
    try:
        raw_sound = int(str(ser.readline()).rstrip("\n").rstrip("\r"))
        # SQL data format is (time, light, colume, temperature, humidity)
        # But for the test we will only do time+sound
        con = sqlite3.connect("sound_test_data.db")
        with con:
            cur = con.cursor()
            cur.execute("insert into data values (%d,%d)" %(int(time.time()), raw_sound))
        con.close()
        print raw_sound
    except:
        continue
