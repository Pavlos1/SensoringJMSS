#!/bin/sh
modprobe cdc-acm
cd /home/root/arduino_flasher
./flash_arduino current.hex /dev/`ls /dev | grep -i acm | head -n 1` 115200
#sleep 30
cd /home/root/GalileoWebServer
/home/root/GalileoWebServer/read_arduino_data.py
