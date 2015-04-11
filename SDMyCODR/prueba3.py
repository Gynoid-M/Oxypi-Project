import serial
import threading
import binascii
import time
import os
import ctypes


data = range(10)
ser = 0
i = 0
ser = serial.Serial('/dev/rfcomm0',115200)
byte_check = binascii.b2a_hex(ser.read())

bitSync = (int(byte_check,16)>>7)&1
data[0] = byte_check
i = 1

if(bitSync == 1):
	while i < 6:
		data[i] = binascii.b2a_hex(ser.read())
		i = i + 1
	bytePulso = data[2] #The second byte of the data packet recovered, is t$
	ultimo_bit = int(bytePulso[1], 16) #Conversion hexadecimal to integer.

	if ultimo_bit%2 == 1:

		pulso = int(data[3], 16)
        	pulso = pulso + 1
	else:
        	pulso = int(data[3],16)

	print "Su pulso es : "
	print pulso
	print "Su cantidad de oxigeno es: "
	oxigeno = int(data[4], 16)
	print oxigeno
else:
	print "dato falso"

ser.close()
ser.close()
