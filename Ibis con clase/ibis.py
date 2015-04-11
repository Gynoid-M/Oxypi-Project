from bluetoothRead import *
from connection import *
import threading

#This is the main call to the ibis controller application for Oxypi Health System .
#In this new version, we store the data in a .txt instead of a mysql database. However, we will need
#to send data from a sms to the Hospital Center Server (in a real case)


if __name__ =="__main__":
	
	conn = Connection();
	blue = bluetoothRead();
	th_Con = threading.Thread(Connection.conn_SerialPort(conn))


	th_Read = threading.Thread(bluetoothRead.read(blue,conn))

	
	th_Con.start()
		
	time.sleep(3)
	th_Read.start()	