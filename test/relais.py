#!/usr/bin/env python3
#coding: utf8

import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM) # GPIO Nummern statt Board Nummern
 
RELAIS_1_GPIO = 24
GPIO.setup(RELAIS_1_GPIO, GPIO.OUT) # GPIO Modus zuweisen

GPIO.output(RELAIS_1_GPIO, GPIO.LOW) # aus
time.sleep(2)
GPIO.output(RELAIS_1_GPIO, GPIO.HIGH) # an
