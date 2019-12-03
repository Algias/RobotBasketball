import socket
import serial

#Lights--------------------------------------------------------
UDP_IP = "127.0.0.1"
UDP_PORT2 = 4000
lightReceive = socket.socket(socket.AF_INET, # Internet
					socket.SOCK_DGRAM) # UDP
lightReceive.bind((UDP_IP, UDP_PORT2))
lightReceive.setblocking(0)


lights = serial.Serial('/dev/ttyACM0','9600')

def defaultAnimation():
	lights.write('D'.encode()) # main menu and normal play
   
def revMotorAnimation():
	lights.write('R'.encode()) #when you first start 

def throwAnimation():
	lights.write('T'.encode()) #when you shoot

def hitAnimation():
	lights.write('H'.encode()) #when you make it

def missAnimation():
	lights.write('E'.encode()) #when you don't/ last 10 seconds

#----------------------------------------------------------

while True:
	try:
		data, addr = sock1.recvfrom(1024)
		if(data is not None):
			pass
	except:
		
		pass