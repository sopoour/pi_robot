#!/usr/bin/env python

import RPi.GPIO as GPIO
import time
#import json
import sys
from mfrc522 import SimpleMFRC522
import os
#import paho.mqtt.client as mqtt
#import explorer hat configs:
import io_wrapper as hw

#to shut-down Rpi
from subprocess import call

reader = SimpleMFRC522()
#client = mqtt.Client("SopoRFID")

#TODO: fix the buggy motor behavior when opening app.py via read.py or find a better way to open app.py via RFID sensor!

try:
        #read input 2 in order to call RFID on explorer hat
        state = hw.input_four_read()
        print("Please place your key against the reader")

        def get_time():
                """ Returns a string with the time and date """
                return time.strftime("%d %b %Y %H:%M:%S", time.gmtime())
        if state == 1:
                id, name = reader.read()
                print(id)
                #name = name.strip()
                #if id == "863881349114":
                os.chdir(r"/home/pi/pi_robot")
                os.system("python3 app.py")

        #rfidData = json.dumps({"carKey": carKey, "renterID": str(id), "timestamp": get_time()})
        #print("Connecting to Broker")
        #client.connect("192.168.0.25")
        #print("Publishing RFID Data" + rfidData)
        #client.publish("rfidData", rfidData)
#except:
 #       print ("Couldn't open reader!")
  #      sys.exit()
finally:
        print("cleaning up RFID")
        GPIO.cleanup()



