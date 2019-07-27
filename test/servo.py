#!/usr/bin/env python3
#coding: utf8

import time
from adafruit_servokit import ServoKit

kit = ServoKit(channels=16) # Type des Boards, hier 16 Kanäle

kit.servo[0].angle = 0
time.sleep(5)
kit.servo[0].angle = 90
kit.servo[4].angle = 0
kit.servo[4].angle = 120

 


