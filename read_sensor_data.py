#!/usr/local/bin/python
# Written by Pavel
# License: BSD

import sqlite3
import time
import os
import mraa

light = mraa.Aio(0)
sound = mraa.Aio(1)
i2c = mraa.I2c(0)
#pins A0 and A1 tied to ground, so address is 0x40
i2c.address(0x40)
#reset hdc1008
i2c.writeReg(0x02, 144L)
#configuration; see datasheet. sets hdc1008 to measure temperature and humidity simultaneously
i2c.writeReg(0x02, 16L)
error_count = 0

while True:
    try:
        light_t = 0
        sound_t = 0
        temp_t = 0
        humid_t = 0
        for i in range(0, 50):
            light_t += light.read()
            sound_t += sound.read()
            #writing to register 0 and then requesting a read starts measurement; see datasheet
            i2c.writeWordReg(0x00, 0L)
            i2c.writeByte(0x000)
            #allow the sensor time to take measurement. 100ms is overkill, actually.
            time.sleep(0.1)
            #read 4 bytes; 2 for temperature and 2 for humidity
            i2c_read = i2c.read(4)
            # conversions to SI; see data sheet
            temp_t += ((((i2c_read[0] << 8) | i2c_read[1]) * 165.0) / (2**16)) - 40.0
            humid_t += float((i2c_read[2] << 8) | i2c_read[3]) / (2**16)
        con = sqlite3.connect("sensor_data.db")
        with con:
            cur = con.cursor()
            command = "insert into data values (%d,%d,%d,%f,%f)" %(int(time.time()), int(light_t/50 - 288), int(sound_t/50), temp_t/50, humid_t/50)
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
