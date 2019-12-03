import bluetooth
import time
import binascii
import datetime

import serial
import socket
#Sparkfun Bluetooth Addr
#devboard address
#Dev Board
# bd_addr = "00:06:66:C0:5C:E0"
# New board
bd_addr = '00:06:66:F3:1D:98'
#PCB Bluetooth Addr
# bd_addr = "00:06:66:18:40:87"#Onboard robot address	
#CommunicationMethod = "Wired"
CommunicationMethod = "Bluetooth"


if CommunicationMethod is "Bluetooth":
	global sock
	try:
		port = 1
		sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
		sock.connect((bd_addr, port))
		time.sleep(1)
	except:
		print("Bluetooth unavailable")
		exit()

elif CommunicationMethod is "Wired":
	global ser
	try:
		ser = serial.Serial('/dev/ttyUSB0',115200)
	except:
		print("serial unavailable")
		exit()



UDP_IP = "127.0.0.1"
UDP_PORT = 3000

sockReceive = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sockReceive.bind((UDP_IP, UDP_PORT))



# sockReceive.setblocking(0)
#data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
time.sleep(.5)
vX = -100
vY = -100
backlog = 1
motor = "M1"
Name = "RO-SHAQ"

buffer = ""
buffer2 = ""
dataToGame = ""

msgDisp = ""



def waitforMsg(buffer, sockIn):
	data= sockIn.recv(32)	
		
	if(data):
		dataString = data.decode()
		if(dataString.endswith('\n')):
			buffer += dataString
			print("function: ",buffer)
			# buffer = ""
		else:
			buffer += dataString
	return buffer
	
RobotReadyForData = False


if CommunicationMethod == "Bluetooth":
	try:
		while True:
			data = ""
			fromRobot = ""

			# try:
			data,addr = sockReceive.recvfrom(1024)
			# sockReceive.recvfrom(1024)

			if data:
				print("Received from Game")
				if RobotReadyForData:
					print("Sending Data")
					data = data.decode() + "\n"
					print("Data Sent: ", data)
					sock.send(data.encode())
			try:
				# fromRobot = sock.recv(32)
				fromRobot = sock.recv(1024)
			except:
				print("Error in from Robot")
			
			if fromRobot:
				print("From Robot:", fromRobot.decode())
			if "G" in fromRobot.decode():
				print("Robot ready for data")
				RobotReadyForData = True
			fromRobot = sock.recv(1024)
			# except:
				# print("Inner Error")
	except KeyboardInterrupt:
		sendString = "^000000,00,00,00,00,00,00,00,00\n"
		sock.send(sendString.encode())
		sockReceive.close()
		time.sleep(.04)
		sock.close



elif CommunicationMethod == "Wired":
	try:
		while True:
			data = ""
			fromRobot = ""
			
			try:
				# Read data from the game buffer
				data, addr = sockReceive.recvfrom(32) # buffer size is 1024 bytes
				#Flush the rest of the buffer????
				sockReceive.recvfrom(1024)
				# If data is available
				if data:
					# If the robot is ready for data, send the data
					if RobotReadyForData:
						print("Sending data")
						data = data.decode() + "\n"
						ser.write(data.encode())
				# Read data from the robot
				fromRobot = ser.readline().decode()

				if fromRobot:
					print("from Serial: ", fromRobot)

				# If robot data contains a G, then the robot is ready to receive data
				if "G" in fromRobot:
					RobotReadyForData = True
					
			except:
				print("If you see this, you messed up")
	except KeyboardInterrupt:
		sendString = "^000000,00,00,00,00,00,00,00,00\n"
		ser.write(sendString.encode())
		# sock.send(sendString)
		sockReceive.close()
		time.sleep(.04)
		# sock.close()