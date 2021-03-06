#!/usr/local/bin/python
# Written by Pavel
# License: BSD

#import mraa
import serial
import sqlite3
import time
import os
import re

import sys
import traceback

error_count = 0
#uart = mraa.Uart(0)
#os.system("/sbin/modprobe cdc-acm")
devices = [f for f in os.listdir("/dev") if re.match(r"^ttyUSB[0-9]$", f)] + [f for f in os.listdir("/dev") if re.match(r"^ttyACM[0-9]$", f)]
print "USB TTYs found:", devices
selected_device = "/dev/"+sorted(devices)[0]
ser = serial.Serial(selected_device, 9600)

while True:
    try:
        raw_data = str(ser.readline()).rstrip("\n").rstrip("\r").split("|")
	print raw_data
	if len(raw_data) != 4:
		print "wrong length"
		continue
        # SQL data format is (time, light, colume, temperature, humidity)
        con = sqlite3.connect("sensor_data.db")
        with con:
            cur = con.cursor()
            cur.execute("insert into data values (%d,%d,%d,%f,%f)" %(int(time.time()), int(raw_data[0]), int(raw_data[1]), float(raw_data[2]), float(raw_data[3])))
        con.close()
    except:
        error_count += 1
        print "Something went wrong. Probably race condition. Continuing... %d" %error_count
        if error_count >= 50:
            print "Bailing..."
            os.system("/sbin/reboot")
