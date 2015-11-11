#!/bin/sh
/bin/screen -S data_logger -X quit
/bin/screen -dm -S data_logger /home/root/GalileoWebServer/startlogger.sh $1
