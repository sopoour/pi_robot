#!/usr/bin/env python

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

try:
        name = input('Please type in your Name: ')
        print("Now place your key to write")
        reader.write(name)
        print("Written: " + name)
finally:
        GPIO.cleanup()