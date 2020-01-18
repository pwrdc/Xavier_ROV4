#!/bin/bash

sudo pip3 install Jetson.GPIO

sudo groupadd -f -r gpio
sudo usermod -a -G gpio dlinano

sudo cp /usr/local/lib/python3.6/dist-packages/Jetson/GPIO/99-gpio.rules /etc/udev/rules.d/

sudo udevadm control --reload-rules && sudo udevadm trigger