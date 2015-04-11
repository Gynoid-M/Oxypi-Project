
'''
The aim of this class is to provide an easy interface for the Rpi's connection,
and make the connection authomatic. 	
'''


import os
import bluetooth
import serial


class Connection: 



	def conn_SerialPort(self):
		os.system( "rfcomm connect 0" )	



	def conn_socketSerialPort(self):
		ser = serial.Serial('/dev/rfcomm0', timeout=2)		
		return ser

