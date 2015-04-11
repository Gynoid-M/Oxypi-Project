import serial
import time
import ctypes
import thread
import binascii
from connection import *

class bluetoothRead: 
	data = range(6)

	def find(self,ser):
		found = False
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

		return found                

	def read(self,connection):
		loop = 0

		while loop == 0:


			ser = Connection.conn_socketSerialPort(connection);

			found = False
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

			if (found == True):
				bytePulso = data[2] #The second byte of the data packet recovered, is the pulse. 
				ultimo_bit = int(bytePulso[1], 16) #Conversion hexadecimal to integer.

				if ultimo_bit%2 == 1:

					pulso = int(data[3], 16)
					pulso = pulso + 1
				else:
					pulso = int(data[3],16)

				#Temporary test of correct read data.

				print "Su pulso es : "
				print pulso
				print "Su cantidad de oxigeno es: "
				oxigeno = int(data[4], 16)
				print oxigeno

				#This write the data in a DB. Then doctors or healthcare workers can visualize and check the clinical information of the patient.
				if(crearhilo == 0):
					hiloEs = threading.Thread(target = store, args=(self,oxygen, pulse)) #First thread
					hiloEs.setDaemon(True) #Don't block the main thread
					hiloEs.start()
					crearhilo = 1

				if(hiloEs.isAlive() == False): #Won't create more threads until the first ends
					hiloEs = threading.Thread(target = store, args=(self,oxygen, pulse))
					hiloEs.setDaemon(True) #Don't block the main thread
					hiloEs.start()


				ser.flushInput();
				ser.flushOutput();


				ser.close()

	def store(self,oxigeno, pulso):
		#Principally, we need to store the data in a file which will be read by a daemon who sends the sms to the 
		#doctor's phone
		#We stop the thread a few minutes if the case is not so serious. Therefore we avoid to store data that is not
		#necessary to store (because is repetitive)

		if(oxigeno == 99 or oxigeno == 98 or oxigeno == 97):
				time.sleep(300) #Update after 5 minutes.
		elif(oxigeno == 96 or oxigeno == 95):
				time.sleep(180) #Update after 3 minutes.
		elif (oxigeno<95):
				time.sleep(3) #Exists danger. Cronical 

		#We write a file with the data. Then, with a cron task, we send the message to the Server. 		
		f = open('data.txt', 'r+')

		f.write(time.strftime('%c')+ '\n')
		f.write("SPO2: " + oxigeno + '\t')
		f.write("RPM: " + pulso + '\n')

		#For more security, we store the data into an internal DB 
		query = "INSERT INTO DATOS(FECHA,SPO2, RPM) VALUES ('%s','%d', '%d')"%(time.strftime("%c"), oxigeno, pulso) #Insert data in DB.
		runQuery(query)
			
		