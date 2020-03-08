#!/usr/bin/env python
# -*- coding: utf-8 -*-

import serial
import time
ser = serial.Serial('/dev/ttyACM0', 9600) 

import hashlib
from pyfingerprint.pyfingerprint import PyFingerprint

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
			print('Wait for 3 seconds')
			time.sleep(3)

		
	except Exception as e:
		print('Operation failed!')
		print('Exception message: ' + str(e))
		
