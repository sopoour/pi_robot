#!/usr/bin/python
import RPi.GPIO as GPIO
import sys
import Adafruit_DHT
import io_wrapper as hw

sensor = Adafruit_DHT.DHT11
DHT11_pin = 16

#TODO: right not properly reading, maybe use analog rather than input? Figure out what's wrong with line 16
try: 
    state = hw.input_one_read()

    if state == 1:
        print("Ready to sense temp & humidity")
        humidity, temperature = Adafruit_DHT.read_retry(sensor, DHT11_pin)
        print("Got Data")
        if humidity is not None and temperature is not None:
            print('Temperature: {0:0.1f} C  Humidity: {1:0.1f} %'.format(temperature, humidity))
        else:
            print('Failed to get reading from the sensor. Try again!')

except OSError as err:
    print("OS error: {0}".format(err))
except:
    print("Unexpected error:", sys.exc_info()[0])
    raise
finally:
        print("cleaning up RFID")
        GPIO.cleanup()