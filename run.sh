#!/bin/bash

pkill -9 python3
pkill -9 python

python3 -m vision.camera_server &
python3 main.py 
