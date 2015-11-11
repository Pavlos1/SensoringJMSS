#!/bin/sh
/usr/local/bin/ntpdate -buv time.nist.gov
/usr/local/bin/ntpd
/sbin/modprobe usbserial # general (serial) driver
/sbin/modprobe i2c-dev # i2c
/sbin/modprobe ftdi_sio # for genuine arduino nanos
/sbin/modprobe cdc-acm # for all other arduinos
# For nano clones using CH34x chips:
cd ~/src/ch34
/usr/bin/make load

case "$1" in
    galileo)
        cd /home/root/GalileoWebServer
        /home/root/GalileoWebServer/read_sensor_data.py
        ;;

    nano)
        cd /home/root/GalileoWebServer/arduino_flasher
        ./flash_arduino current.hex /dev/`ls /dev | grep ttyUSB | head -n 1` 57600
        cd /home/root/GalileoWebServer
        /home/root/GalileoWebServer/read_arduino_data.py
        ;;

    uno)
        cd /home/root/GalileoWebServer/arduino_flasher
        ./flash_arduino current.hex /dev/`ls /dev | grep ttyACM | head -n 1` 115200
        cd /home/root/GalileoWebServer
        /home/root/GalileoWebServer/read_arduino_data.py
        ;;

    *)
        echo "No option selected, defaulting to nano"
        cd /home/root/GalileoWebServer/arduino_flasher
        ./flash_arduino current.hex /dev/`ls /dev | grep ttyUSB | head -n 1` 57600
        cd /home/root/GalileoWebServer
        /home/root/GalileoWebServer/read_arduino_data.py
        ;;
esac

/bin/bash
