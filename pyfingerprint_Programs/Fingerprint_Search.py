#!/usr/bin/env python
# -*- coding: utf-8 -*-

import serial
import time
import RPi.GPIO as GPIO
ser = serial.Serial('/dev/ttyACM0', 9600) 

import hashlib
from pyfingerprint.pyfingerprint import PyFingerprint

control = [5,5.5,6,6.5,7,7.5,8,8.5,9,9.5,10]
servo = 22
GPIO.setmode(GPIO.BOARD)
GPIO.setup(servo,GPIO.OUT)
p=GPIO.PWM(servo,50)# 50hz frequency
p.start(2.5)# starting duty cycle ( it set the servo to 0 degree )
## Tries to initialize the sensor
try:
    f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

    if ( f.verifyPassword() == False ):
        raise ValueError('The given fingerprint sensor password is wrong!')

except Exception as e:
    print('The fingerprint sensor could not be initialized!')
    print('Exception message: ' + str(e))
    exit(1)

## Gets some sensor information
print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))


while 1:
## Tries to search the finger and calculate hash
	try:
		print('Waiting for finger...')

		## Wait that finger is read
		while ( f.readImage() == False ):
			pass

		## Converts read image to characteristics and stores it in charbuffer 1
		f.convertImage(0x01)

		## Searchs template
		result = f.searchTemplate()

		positionNumber = result[0]
		accuracyScore = result[1]

		if ( positionNumber == -1 ):
			print('No match found!')
			ser.write(b'1')
			print('Wait for 10 seconds')
			time.sleep(10)
		else:
			print('Found template at position #' + str(positionNumber))
			print('The accuracy score is: ' + str(accuracyScore))
			print('Opening')
			for x in range(11):
				p.ChangeDutyCycle(control[x])
				time.sleep(0.03)
			time.sleep(4)
			print('Closing')
			for x in range(9,0,-1):
				p.ChangeDutyCycle(control[x])
				time.sleep(0.03)
			#GPIO.cleanup()

		
	except Exception as e:
		print('Operation failed!')
		print('Exception message: ' + str(e))
		
