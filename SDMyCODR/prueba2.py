import serial
import threading
import binascii
import time
import os
import ctypes
import Queue 


def conexion():
		
	os.system( "rfcomm connect 0" )	

def lectura():
		
	data = range(10)
	
	loop = 0
	crearhilo = 0
	ser = 0

	while loop == 0:
		
		found = False
		ser = serial.Serial('/dev/rfcomm0',115200)		
		while found == False:
		
			byte_check = binascii.b2a_hex(ser.read())
	
			bitSync = (int(byte_check,16)>>7)&1 

			if(bitSync == 1): #We already know that this is the correct packet. 
			
				data[0] = byte_check
				i = 1

				while i < 7: #Once we know that is correct, we continue reading.
					data[i] = binascii.b2a_hex(ser.read()) 
					i= i + 1
				found = True
					
		bytePulso = data[2] #The second byte of the data packet recovered, is the pulse. 
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
	
				
		ser.close()
		ser = serial.Serial('/dev/rfcomm0',115200)		
		
		time.sleep(5)
				
	
			



if __name__ =="__main__":
	
	
	

	hiloCon = threading.Thread(target = conexion)


	hiloLec = threading.Thread(target = lectura)

	try :	
		hiloCon.start()
		
		time.sleep(3)
		hiloLec.start()		
	
	except (KeyboardInterrupt, SystemExit):
		hiloLec.Stop();
		hiloCon.Stop();
		sys.exit()


