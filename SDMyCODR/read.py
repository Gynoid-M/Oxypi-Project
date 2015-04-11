import serial
import threading
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
f = open('data.txt', 'r+')

def conexion():
		
	os.system( "rfcomm connect 0" )	

def lectura():
		
	data = range(10)
	
	loop = 0
	crearhilo = 0
	ser = 0
	count = 0
	while loop == 0:
		
		found = False
		ser = serial.Serial('/dev/rfcomm0', timeout=2)		
		if count == 1 : 
			ser = ser1
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
	
		#This write the data in a DB. Then doctors or healthcare workers can visualize and check the clinical information of the patient.
		if(crearhilo == 0):
			hiloEs = threading.Thread(target = escribir, args=(oxigeno, pulso)) #Primer hilo
			hiloEs.setDaemon(True) #No bloquea el hilo principal
			hiloEs.start()
			crearhilo = 1
			
		if(hiloEs.isAlive() == False): #Para que no se creen mas hilos, hasta que no se haya terminado el primero. 
			hiloEs = threading.Thread(target = escribir, args=(oxigeno, pulso))
			hiloEs.setDaemon(True) #No bloquea el hilo principal
			hiloEs.start()
	
				
		ser.flushInput();
		ser.flushOutput();
		time.sleep(3)
						
		ser.close()
	
			


def runQuery (query=''):
	
	
	
	
	db = MySQLdb.Connect(DB_HOST,DB_USER,DB_PASS,DB_NAME)
	cursor = db.cursor()
	cursor.execute(query)
	db.commit()
	db.close()

	

#Thread to write. Takes some time to write, depending of the recovered data. 
def escribir(oxigeno, pulso):
	
	
	if(oxigeno == 99 or oxigeno == 98 or oxigeno == 97):
				time.sleep(3) #Update after 5 minutes.
	elif(oxigeno == 96 or oxigeno == 95):
				time.sleep(180) #Update after 3 minutes.
	elif (oxigeno<95):
				time.sleep(3) #Exists danger. Cronical 

	

	f.write(time.strftime('%c')+ '\n')
	f.write("SPO2: " + str(oxigeno) + '\t')
	f.write("RPM: " + str(pulso) + '\n')			
			 
	query = "INSERT INTO DATOS(FECHA,SPO2, RPM) VALUES ('%s','%d', '%d')"%(time.strftime("%c"), oxigeno, pulso) #Insert data in DB.
	runQuery(query)
			
	
	 #When terminate, thread ends too (is daemon type).

if __name__ =="__main__":
	
	
	

	hiloCon = threading.Thread(target = conexion)


	hiloLec = threading.Thread(target = lectura)

	
	hiloCon.start()
		
	time.sleep(3)
	hiloLec.start()		


	exit()


