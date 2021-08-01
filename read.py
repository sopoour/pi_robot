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
import app as app

#to shut-down Rpi
from subprocess import call

reader = SimpleMFRC522()
#client = mqtt.Client("SopoRFID")


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
                app.main()
                #name = name.strip()
                #if id == "863881349114":

        #rfidData = json.dumps({"carKey": carKey, "renterID": str(id), "timestamp": get_time()})
        #print("Connecting to Broker")
        #client.connect("192.168.0.25")
        #print("Publishing RFID Data" + rfidData)
        #client.publish("rfidData", rfidData)
except OSError as err:
    print("OS error: {0}".format(err))
except:
    print("Unexpected error:", sys.exc_info()[0])
    raise
finally:
        print("cleaning up RFID")
        GPIO.cleanup()



