from __future__ import print_function
import logging

PORT = '/dev/ttyUSB0'
BAUDRATE = 115200
PIN = None

from gsmmodem.modem import GsmModem
from gsmmodem.modem import Sms
from gsmmodem.modem import SentSms

def text (): 
	f = open('data.txt', 'r')
	message = f.read ()

	return message; 
def main(): 
	print("Iniciando modem...")
	logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
	modem = GsmModem(PORT, BAUDRATE)
	modem.smsTextMode = True
	modem.connect(PIN)
	modem.sendSms('638070483', text())

if __name__ == '__main__':
	main()