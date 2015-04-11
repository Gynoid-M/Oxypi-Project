import threading
import serial
import binascii
import time
import os
import ctypes
import MySQLdb
import Queue 

DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASS = 'marina'
DB_NAME = 'ibis_database'



data = range(6)		
ser = serial.Serial('/dev/rfcomm0', 115200, timeout=2) #We open the socket to serial comunications.
i=0		
while i == 0: #We need the first 6 bytes of the data packet. 

	data =binascii.b2a_hex(ser.read(6))#Conversion ascii to hexadecimal.
	byte_check = data[1]

	bit=((int(byte_check,16) >> 7) & 1) 		
	print bit	 
	
	if(bit == 1)
		print "datos"


	time.sleep(3)			
