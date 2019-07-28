#!/usr/bin/env python3
#coding: utf8

from time import sleep
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM) # GPIO (BCM) Nummern statt Board Nummern
 
DIR = 13 # direction gpio 
STEP = 0 # step gpio
CW = 1   # clockwise rotation
CCW = 0  # counter clockvise rotation
SPR = 200 # steps per revolution (360 / 1.8)
          # https://www.amazon.de/gp/product/B07GLMGQB3

GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(STEP, GPIO.OUT)
GPIO.output(DIR, CW)

step_count = SPR
delay = .0208

for x in range(step_count):
    GPIO.output(STEP, GPIO.HIGH)
    sleep(delay)
    GPIO.output(STEP, GPIO.LOW)
    sleep(delay)

sleep(.5)
GPIO.output(DIR, CCW)
for x in range(step_count):
    GPIO.output(STEP, GPIO.HIGH)
    sleep(delay)
    GPIO.output(STEP, GPIO.LOW)
    sleep(delay)

GPIO.cleanup()

