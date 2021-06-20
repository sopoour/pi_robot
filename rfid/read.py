#!/usr/bin/env python

import RPi.GPIO as GPIO
import time
#import json
import sys
from mfrc522 import SimpleMFRC522
import os
#import paho.mqtt.client as mqtt

reader = SimpleMFRC522()
#client = mqtt.Client("SopoRFID")

#TODO: import config/io_wrapper to this file & call all the ExplorerHat functions so that it actually connects to the different pins

try:
        print("Please place your key against the reader")

        def get_time():
                """ Returns a string with the time and date """
                return time.strftime("%d %b %Y %H:%M:%S", time.gmtime())
        id, name = reader.read()
        print(id)
        print(name)
        name = name.strip()
        if id == "863881349114":
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
        GPIO.cleanup()



