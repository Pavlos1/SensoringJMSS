#!/bin/sh
/sbin/modprobe cdc-acm
cd /home/root/GalileoWebServer/arduino_flasher
./flash_arduino current.hex /dev/`ls /dev | grep -i acm | head -n 1` 115200
cd /home/root/GalileoWebServer
/home/root/GalileoWebServer/read_arduino_data.py
