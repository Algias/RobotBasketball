import pygame
import socket
import os
from pygame import image
import numpy as np
import math
from xbox360controller import Xbox360Controller 
from collections import deque
import datetime
from simple_pid import PID
import serial
from moviepy.editor import VideoFileClip
import RPi.GPIO as GPIO
import time

sensor = serial.Serial('/dev/ttyACM0','9600')
lights = serial.Serial('/dev/ttyACM1','9600')


UDP_IP1 = "127.0.0.1"
UDP_PORT1 = 5000
sock1 = socket.socket(socket.AF_INET, # Internet
					socket.SOCK_DGRAM) # UDP
sock1.bind((UDP_IP1, UDP_PORT1))
sock1.setblocking(0)

UDP_PORT2 = 3000
sock2 = socket.socket(socket.AF_INET, # Internet
					socket.SOCK_DGRAM) # UDP

UDP_PORT3 = 4000
lightSock = socket.socket(socket.AF_INET,
						socket.SOCK_DGRAM)
lightSock.bind((UDP_IP1, UDP_PORT3))
lightSock.setblocking(0)

invert_x = 1
invert_y = 1
hardmode = False
stageX = 1300
stageY = 720

blk = (0,0,0)
red = (255,0,0)
green = (0,255,0)
orange = (255,165,0)
movements = deque()

qRumb = .25
hRumb = .5
tqRumb = .75
fRumb = 1

controllerMap = pygame.image.load(os.path.realpath(os.path.join(os.getcwd(),'ControllerNew.png')))
controllerMap = pygame.transform.scale(controllerMap, (850,600))
courtImage = pygame.image.load(os.path.realpath(os.path.join(os.getcwd(),'CourtImage.png')))
courtImage = pygame.transform.scale(courtImage, (stageX-120,stageY-75))
robotImage = pygame.image.load(os.path.realpath(os.path.join(os.getcwd(),'RobotImage.png')))
#handled negative values as well

xMap = (stageX-120)/565
yMap = (stageY-75)/475

xRob = stageX/2/xMap
yRob = (stageY-60)/2/yMap
angleRob = 0
circX = 0
circY = 0

theRealestX = 0
theRealestY = 0

ui = 0.0
uj = 0.0

hoop = [0, 15 + (stageY-75)/2]
#516
hoopCV = [540,209]

intake = {
	"0" : False,
	"50" : True,
	"100" : False
}

menuSound = None

replay = False
play = False
aligning = False
alignNum = datetime.datetime.now()

alignTime = datetime.datetime.now()
firstAligning = False


pid = PID(0.5,0.0,0.0,setpoint=0)
# pid.sample_time = 0.075
pid.output_limits = (-100, 100)

steadyStateTime = datetime.datetime.now()
firstSteadyState = False
launchOut = 0
appRPM = 0

repOff = False

clip = VideoFileClip('Making_a_Basket.gif')

# GPIO Button interrupt pin (D18)
# but_pin = 12

# RawScoreCounter = 0

# def LimitCallback(channel):
# 	global RawScoreCounter
# 	RawScoreCounter = RawScoreCounter + 1
# 	print("Score counter: ", RawScoreCounter)
# 	time.sleep(0.3)

intakePress = 0

def avg(array):
	resX = 0
	resY = 0
	for i in array:
		resX += i[0]
		resY += i[1]
	
	resX /= len(array)
	resY /= len(array)
	return round(resX,3),round(resY,3)

#project vector z onto vector u
def project(zx,zy,ux,uy):

	xout = (zx*ux) + (zx*uy)
	yout = (zy*ux) + (zy*uy)

	return (xout,yout)	

def yeetComponents(vx,vy,ui,uj):

	zx1,zy1 = project(vx,vy,ui,uj)
	zx2,zy2 = project(vx,vy,0,1)

	vmag = math.sqrt(vx*vx +vy*vy)

	# if(vmag != 0):
	# 	vxunit = vx/vmag
	# 	vyunit = vy/vmag

	# 	ox,oy = project(zx1,zy1,vxunit,vyunit)
	# 	print("ox,oy",(ox,oy))
	# else:
	# 	print("no existo")
	# 	ox = vx
	# 	oy = vy
	# zx = zx1+zx2
	# zy = zy1+zy2

	xcomp = -vx
	ycomp = vy

	theta = np.radians(angleRob + 90)
	c, s = np.cos(theta), np.sin(theta)

	R_mat = np.array(((c,-s), (s, c)))
	# v = np.array([-xcomp,-ycomp]).shape(2,1)
	# rotated = np.multiply(R_mat,v)

	rx = xcomp*c + ycomp*s
	ry = -xcomp*s + ycomp*c
	# print("R_Mag:", math.sqrt(rotated[0]*rotated[0] + rotated[1]*rotated[1]))
	
	if((angleRob >= 0 and angleRob <= 90) or (angleRob >= 270 and angleRob <= 360)):
		if(theRealestX < 60):
			# print("RUMBLE")
			if(rx < 0):
				rx = 0
		elif(theRealestX < 80):
			# print("RUMBLE")
			if(rx < 0):
				rx = int(rx/3)
	else:
		if(theRealestX < 60):
			# print("RUMBLE")
			if(rx < 0):
				rx = 0
		elif(theRealestX < 80):
			# print("RUMBLE")
			if(rx < 0):
				rx = int(rx/3)
	if(theRealestX > 500): #.90*stageX/xMap
		if(rx > 0):
			rx = 0
	elif(theRealestX > 450):
		if(rx > 0):
			rx = int(rx/3)
	
		


	if(theRealestY < .09*450):
		if(ry < 0):
			ry = 0
	elif(theRealestY < .25*450):
		if(ry < 0):
			ry = int(ry/2)

	elif(theRealestY > .85*450):
		if(ry > 0):
			ry = 0

	elif(theRealestY > .75*450):
		if(ry > 0):
			ry = int(ry/2)
	
	
	c, s = np.cos(-theta), np.sin(-theta)
	R_mat = np.array(((c,-s), (s, c)))

	# print("rx,ry",(rx,ry))

	xcomp = rx*c + ry*s
	ycomp = -rx*s + ry*c
	# print("xcomp,ycomp",(xcomp,ycomp))
	# print("robot angle:", angleRob)
	# out = R_mat.dot(np.array((-rotated[0],-rotated[1])))

	# ox,oy = project(zx,zy,ui,uj)
	# return out[0],out[1]
	return -xcomp,ycomp

def toHex(val, nbits):
	#[2:] slices off the 0x prefix from the hex string
  return hex((val + (1 << nbits)) % (1 << nbits))[2:].zfill(2).upper()

def fromHex(hexstr,bits):
	value = int(hexstr,16)
	if value & (1 << (bits-1)):
		value -= 1 << bits
	return value
# print tohex(-199703103, 64)
# print tohex(199703103, 64)

def readData(data):
	splits = data.split(','.encode())
	ui = splits[0].decode()
	uj = splits[1].decode()
	x = splits[2].decode()
	y = splits[3].decode()
	# print("xrob:", x)
	# print("yrob:", y)
	theta = splits[4].decode()
	circleX = splits[5].decode()
	circleY = splits[6].decode()
	# print("CircX,circY: ",circleX,",",circleY)
	return float(ui),float(uj),float(x),float(y),float(circleX),float(circleY),float(theta)
	# print(f"Data split is {int(float(x))} and {int(float(y))}")
# def unit_vector(vector):

#     # """ Returns the unit vector of the vector.  """
#     return vector / np.linalg.norm(vector)

def angle_between(v1, v2):
    # """ Returns the angle in radians between vectors 'v1' and 'v2'::
    return np.arccos(np.clip(np.dot(v1, v2), -1.0, 1.0))

def getTextObjects(text,font,x,y,active,bgColor):

	nonActive = (255,255,255)
	Active = (255,255,0)
	if(active):
		textOut = font.render(text,True,Active,bgColor)
	else:
		textOut = font.render(text,True,nonActive,bgColor)
	textRect = textOut.get_rect()
	textRect.center = (x,y)
	return textOut,textRect

def formPacket(inp,count):
	global ui,uj,aB,aligning,appRPM,alignNum,firstSteadyState,steadyStateTime,firstAligning, alignTime
	# these numbers are different from windows to linux
	# outString = f'^000000,{inp[10]},{inp[11]},{inp[14]},{inp[15].zfill(2)}' --- Windows
	# all buttons added to input first, then axes

	#calculate launcher speed here using current x and y pos
	#then feed into outStrings below in inp17 spot

	xvect = abs(xRob - hoopCV[0])
	yvect = abs(yRob - hoopCV[1])

	vectMag = math.sqrt((xvect*xvect) + (yvect*yvect))
	# rpm = 1419.8 * pow(2.71828,.0413*vectMag/100)
	rpm = 2.2*vectMag + 1200
	rpm /= 32
	appRPM = rpm

	botunit = np.array([-float(ui),float(-uj)])

	hoop2bot = np.array([xRob-hoopCV[0],yRob-hoopCV[1]])
	hoop2BotMAG = (math.sqrt(math.pow(hoop2bot[0],2)+ math.pow(hoop2bot[1],2)))
	hoop2bot[0] /= hoop2BotMAG
	hoop2bot[1] /= hoop2BotMAG

		
	# aB = angle_between(hoop2bot, botunit)
	aBdot = np.dot(hoop2bot, botunit)
	aBdet = np.linalg.det([hoop2bot, botunit])
	aB = math.atan2(aBdet,aBdot)

	degreeRatio = np.degrees(aB)/180
	aBdeg = np.degrees(aB)
	

	
	

	if(aligning and play):
		print("Robot Angle:", angleRob)
		print("angle2hoop:", np.degrees(aB))
		print("Time in Align: ", (datetime.datetime.now() - alignTime).microseconds/100000)
		if firstAligning:
			firstAligning = False
			alignTime = datetime.datetime.now()

		elif (datetime.datetime.now() - alignTime).microseconds > 5000000:
			print("IN TIMEOUT")
			aligning = False
			firstAligning = True
			
		# if(abs(aBdeg) > 45):
		# 	aligning = False
		# 	outString = f'^{toHex(count%255,8)}0000,00,00,00,{toHex(int(rpm),8).zfill(2)},{toHex(60,8).zfill(2)},00,00,00'
		# 	pid.set_auto_mode(False, last_output=0.0)
		if (abs(aBdeg) >= 15):
			pid.Kp = .50
		elif(abs(aBdeg) >= 5):
			pid.Kp = 1.0
		else:
			pid.Kp = 2.0
		if(abs(aBdeg) > 2.0):
			pid.set_auto_mode(True)
			firstSteadyState = False
			# print("OUTPUT:",-degreeRatio)

			speed = int(pid(aBdeg))
			outString = f'^{toHex(count%255,8)}0000,00,00,{toHex(-speed,8)},{toHex(int(rpm),8).zfill(2)},{toHex(60,8).zfill(2)},00,00,00'
		else:
			if not firstSteadyState:
				pid.set_auto_mode(True, last_output=0.0)
				firstSteadyState = True
				steadyStateTime = datetime.datetime.now()
			elif (datetime.datetime.now() - steadyStateTime).microseconds > 250000:
				aligning = False
				
				firstAligning = True
				pid.set_auto_mode(False, last_output=0.0)
			speed = 0
			outString = f'^{toHex(count%255,8)}0000,00,00,{toHex(-speed,8)},{toHex(int(rpm),8).zfill(2)},{toHex(60,8).zfill(2)},00,00,00'

	elif(play):
		if(hardmode):
			rpm = launchOut
			appRPM = rpm

		ox,oy = yeetComponents(int(fromHex(inp[11],8)),int(fromHex(inp[12],8)),ui,uj)
		if(intake["100"]):
			outString = f'^{toHex(count%255,8)}0000,{toHex(int(ox),8)},{toHex(int(oy),8)},{inp[14]},{toHex(int(rpm),8).zfill(2)},{toHex(100,8).zfill(2)},00,00,00' # --- Linux
			# outString = f'^{toHex(count%255,8)}0000,{inp[11]},{inp[12]},{inp[14]},{toHex(int(rpm),8).zfill(2)},{toHex(100,8).zfill(2)},00,00,00' # --- Linux
		elif(intake["50"]):
			outString = f'^{toHex(count%255,8)}0000,{toHex(int(ox),8)},{toHex(int(oy),8)},{inp[14]},{toHex(int(rpm),8).zfill(2)},{toHex(60,8).zfill(2)},00,00,00' # --- Linux
			# outString = f'^{toHex(count%255,8)}0000,{inp[11]},{inp[12]},{inp[14]},{toHex(int(rpm),8).zfill(2)},{toHex(60,8).zfill(2)},00,00,00' # --- Linux
		elif(intake["0"]):
			outString = f'^{toHex(count%255,8)}0000,{toHex(int(ox),8)},{toHex(int(oy),8)},{inp[14]},{toHex(int(rpm),8).zfill(2)},{toHex(0,8).zfill(2)},00,00,00' # --- Linux
			# outString = f'^{toHex(count%255,8)}0000,{inp[11]},{inp[12]},{inp[14]},{toHex(int(rpm),8).zfill(2)},{toHex(0,8).zfill(2)},00,00,00' # --- Linux
		# print("Approximate RPM: ", rpm*32)
		# print("x,y: ",xRob,",",yRob)
	else:
		outString = "^000000,00,00,00,00,00,00,00,00"

	sock2.sendto(outString.encode(), (UDP_IP1, UDP_PORT2))
	# print(outString)
	
	


def run(width,height,fps):
	global courtImage,robotImage,menuSound,controllerMap
	
	pygame.init()
	pygame.mixer.pre_init(44100, 16, 2, 4096) 
	pygame.mixer.init()

	menuSound = pygame.mixer.Sound('bensound-endlessmotion.wav')

	gameDisplay = pygame.display.set_mode((width, height))
	clock = pygame.time.Clock()
	cursor = CustomCursor(width/2,height/2,pygame.image.load(os.path.realpath(os.path.join(os.getcwd(),'icons8-cursor-30.png'))))
	pygame.mouse.set_visible(False)
	courtImage = courtImage.convert()

	


	robotImage = pygame.transform.scale(robotImage,(110,110))
	robotRect = robotImage.get_rect()
	robotRect.center = (55,55)
	alpha = 0
	robotImage.set_colorkey((255,255,255))
	robotImage = robotImage.convert_alpha()

	# controllerMap.set_colorkey((255,255,255))
	# controllerMap = controllerMap.convert_alpha()
	# robotImage.fill((255, 255, 255, alpha), None, pygame.BLEND_RGBA_MULT)
	
	


	active_scene = MainMenu(width,height,gameDisplay)
	
	inputs = InputManager(active_scene,cursor,active_scene.ms)
	js = inputs.init_joystick()


# Initialize the GPIO
# Pin Setup:
	# GPIO.setmode(GPIO.BOARD)  # BOARD pin-numbering scheme
	# GPIO.setup(but_pin, GPIO.IN)  # button pin set as input
	# GPIO.add_event_detect(but_pin, GPIO.RISING, callback=LimitCallback, bouncetime=300)


	while active_scene != None:
		pressed_keys = pygame.key.get_pressed()
		filtered_events = inputs.get_events()
		
		active_scene.ProcessInput(filtered_events, pressed_keys,inputs.ms.currentActiveButton())
		active_scene.Update()
		active_scene.Render(gameDisplay)

		active_scene = active_scene.next
		if(active_scene == None):
			break
		inputs.active_scene = active_scene
		inputs.ms = active_scene.ms
		pygame.display.flip()
		clock.tick(fps)

class InputManager:
	def __init__(self,active_scene,cursor,ms):
		global launchOut
		self.init_joystick()
		self.active_scene = active_scene 
		self.buttons = ['A', 'B', 'X', 'Y', 'LB', 'RB', 'Menu', 'Start', 'LS', 'RS', 'R']
		self.hats = ['Up','Down','Left','Right']
		# If you would like there to be a keyboard fallback configuration, fill those out
		# here in this mapping.
		self.key_map = {
			pygame.K_UP : 'up',
			pygame.K_DOWN : 'down',
			pygame.K_LEFT : 'left',
			pygame.K_RIGHT : 'right',
			pygame.K_RETURN : 'start',
			pygame.K_a : 'A',
			pygame.K_b : 'B',
			pygame.K_x : 'X',
			pygame.K_y : 'Y',
			pygame.K_l : 'L',
			pygame.K_r : 'R'
		}

		self.cursor = cursor
		self.speed = 75
		self.lastPacketSendTime = datetime.datetime.now()
		# This dictionary will tell you which logical buttons are pressed, whether it's
		# via the keyboard or joystick
		self.keys_pressed = {}
		
		self.intakeTimer = pygame.time.get_ticks()

		for button in self.buttons:
			self.keys_pressed[button] = False

		self.quit_attempt = False
		self.launchSpeed = 0
		self.launchTime = pygame.time.get_ticks()
		launchOut = 0 

		self.decay = False
		self.count = 0
		self.ms = ms
		self.controller = Xbox360Controller(0)
		self.ballpos = deque()
		self.robpos = deque()
		self.vectors = deque()

		# self.controller.info()
		# with Xbox360Controller() as controller:
		# 	controller.info()
	# button is a string of the designation in the list above
	def is_pressed(self, button):
		return self.keys_pressed[button]
	
	#parses through events
	def get_events(self):
		
		global xRob,yRob,ui,uj,circX,circY,movements,replay,intake,angleRob,launchOut
		global theRealestX, theRealestY, replay,intakePress
		self.count = self.count + 1
		
		if(sensor.in_waiting > 0):
			senseData = sensor.readline()
			print(senseData.decode())
			if(isinstance(self.active_scene, Arena)):
				print((pygame.time.get_ticks() - intakePress))
				if('1' in senseData.decode() and (pygame.time.get_ticks() - intakePress < 3000)):
					lights.write('H'.encode())
					pygame.mixer.Channel(1).play(pygame.mixer.Sound('mlg-airhorn.wav'), 0)
					self.active_scene.score += 1
					replay = True

				self.active_scene.curTime = pygame.time.get_ticks()
				# while(pygame.time.get_ticks() - self.active_scene.curTime < 1000):

				# 	repText, repRect = getTextObjects("Replay",self.active_scene.font, stageX/2,(stageY-60)/2, False, blk)
				# 	self.active_scene.gameDisplay.fill(blk)
				# 	self.active_scene.gameDisplay.blit(repText,repRect)
				# 	pygame.display.flip()
				# 	pygame.time.Clock().tick(60)
				


		# try:
		# 	lData, laddr = lightSock.recvfrom(1024)
		# 	if(isinstance(self.active_scene, Arena)):
		# 		if('1' in lData.decode()):
		# 			lights.write('H'.encode())
		# 			pygame.mixer.Channel(1).play(pygame.mixer.Sound('mlg-airhorn.wav'), 0)
		# 			self.active_scene.score += 1
		# except:
		# 	pass
		
		events = []
		outputs = []
		for event in pygame.event.get():
			if(event.type == pygame.QUIT or 
			(event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE)):
				self.active_scene.Terminate()
				self.quit_attempt = True
			
			if(event.type == pygame.JOYBUTTONDOWN):
				events.append(event)
			# This is where the keyboard events are checked
			if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
				key_pushed_down = event.type == pygame.KEYDOWN
				button = self.key_map.get(event.key)
				if button != None:
					self.keys_pressed[button] = key_pushed_down
			if(event.type == pygame.MOUSEBUTTONDOWN):
				events.append(event)
		


		if(play):
			numButtons = self.joystick.get_numbuttons()
			axes = self.joystick.get_numaxes()
			for i in range(numButtons):
				curButt = self.joystick.get_button(i)
				if(curButt):
					if(isinstance(self.active_scene, Arena)):
						
						if(pygame.time.get_ticks() - self.active_scene.initTime > 100):
							if(pygame.time.get_ticks() - self.intakeTimer > 75):
								#close
								if(i == 0):
									intake["0"] = False
									intake["50"] = False
									intake["100"] = True
									intakePress = pygame.time.get_ticks()
									self.intakeTimer = pygame.time.get_ticks()
									if(self.active_scene.timeLeft > 10):
										lights.write('T'.encode())
								#hold
								elif(i == 2):
									intake["0"] = False
									intake["50"] = True
									intake["100"] = False
									self.intakeTimer = pygame.time.get_ticks()
								#open
								elif(i == 3):
									intake["0"] = True
									intake["50"] = False
									intake["100"] = False
									self.intakeTimer = pygame.time.get_ticks()
									if(self.active_scene.timeLeft > 10):
										lights.write('R'.encode())

							if(pygame.time.get_ticks() - self.launchTime > 75):
								if(i == 4):
									launchOut -= 2
									if(launchOut < 0):
										launchOut = 0
									self.launchTime = pygame.time.get_ticks()
								if(i == 5):
									launchOut += 2
									if(launchOut > 100):
										launchOut = 100
									self.launchTime = pygame.time.get_ticks()

					outputs.append('0'+(str(curButt)))
				else:
					outputs.append('00')
			deadzone = .2

			# launchOut = self.launchSpeed


			self.decay = True
			for i in range(axes):
				axis = self.joystick.get_axis(i)
				if(i == 5):
					# self.launchSpeed = int((axis+1)*50)
					pass

				if(abs(axis) > .2):
					if(i == 0):

						outputs.append(toHex(int(axis*self.speed*invert_x),8))

						if(isinstance(self.active_scene, Arena)):
							
							# # print("xRob:",xRob + self.speed*invert_x*axis)
							# if(xRob + self.speed*invert_x*axis > 0 and xRob + self.speed*invert_x*axis < stageX/xMap):
							# 	xRob += self.speed*invert_x*axis
							pass

					elif(i == 1):
						# print(toHex(int(axis*100),8))
						outputs.append(toHex(int(axis*-self.speed*invert_y),8))
						
						# print(self.controller.info())
						if(isinstance(self.active_scene, Arena)):
							pass
							
								
					# rotation
					elif(i == 3):
						outputs.append(toHex(int(axis*-self.speed),8))
					#triggers
					elif(i == 2):
						outputs.append(toHex(int(axis*100),8))

					elif(i == 4):
						outputs.append(toHex(int(axis*100),8))

					# right trigger on linux
					elif(i == 5):
						outputs.append(toHex(int(axis*100),8))
					# print("Axis {} value: {:>6.3f}".format(i, axis))
				else:
					outputs.append('00')

			outputs.append(toHex(self.launchSpeed,8))

		#menu functinality here
		axes = self.joystick.get_numaxes()
		for i in range(axes):
			axis = self.joystick.get_axis(i)
			if(abs(axis) > .2):

				if(i == 1):
					if(self.count >= 15):
						self.count = 0
						if(axis < 0):
							self.ms.updateActiveMenuButton(-1)
						if(axis > 0):
							self.ms.updateActiveMenuButton(1)
		# if(isinstance(self.active_scene, Arena)):
		# 	if(yRob*yMap  < (stageY-60)*.125 or yRob*yMap > (stageY-60)*.875):
		# 		self.controller.set_rumble(tqRumb, tqRumb, 500)

			# try:
				
			# 	if(xRob*xMap  < stageX*.125 or xRob*xMap > stageX*.875):
			# 		print("RUMBLE RUMBLE")
			# 		self.controller.set_rumble(tqRumb, tqRumb, 500)
			# except:
			# 	pass


		try:
			data, addr = sock1.recvfrom(1024) # buffer size is 1024 bytes
			ui, uj, xRob, yRob,circX,circY,angleRob = readData(data)
			
			theRealestX = xRob
			theRealestY = yRob

			# self.robpos.append((int(xRob),int(yRob)))
			# self.vectors.append((ui,uj))

			if(circX > 0 and circY > 0):
				self.ballpos.append((circX,circY))

			# if(len(self.robpos) > 4):
			# 	self.robpos.popleft()
			# 	# self.vectors.popleft()
			# 	xRob,yRob = avg(self.robpos)
			# 	# ui,uj = avg(self.vectors)

			if(len(self.ballpos) > 5):
				self.ballpos.popleft()
				circX,circY = avg(self.ballpos)

			
		except:
			# print("issue")
			pass
		
		if(not replay and isinstance(self.active_scene, Arena)):
			movements.append((xRob,yRob,ui,uj,circX,circY))
			if(len(movements) > 150):
				movements.popleft()

		if (datetime.datetime.now() - self.lastPacketSendTime).microseconds > 75000:
			formPacket(outputs,self.count)
			self.lastPacketSendTime = datetime.datetime.now()

		return events        
	
	# Set joystick information.
	# The joystick needs to be plugged in before this method is called (see main() method)
	def init_joystick(self):
		joystick = pygame.joystick.Joystick(0)
		joystick.init()
		self.joystick = joystick
		self.joystick_name = joystick.get_name()





class MenuSelect:
	def __init__(self,numMenuButtons):
		self.list = [False] * int(numMenuButtons)
		self.active = 0
		self.list[0] = True
		self.numMenuButtons = int(numMenuButtons)

		if(numMenuButtons == 3):
			self.positions = [(stageX/2,stageY/4),(stageX/2,2*stageY/4),(stageX/2,3*stageY/4)]

	def updateActiveMenuButton(self, direction):
		self.list[self.active] = False
		self.active = self.active + 1*direction
		if(self.active >= self.numMenuButtons):
			self.active = 0
		elif(self.active < 0):
			self.active = self.numMenuButtons - 1
		self.list[self.active] = True

	def currentActiveButton(self):
		for i in range(self.numMenuButtons):
			if(self.list[i]):
				return i

	def updateActiveMenu(newScene):
		self.list = [False] * newScene.numMenuButtons 
		self.active = 0
		self.list[0] = True
		self.numMenuButtons = newScene.numMenuButtons





class CustomCursor():
	def __init__(self,x,y,image):
		self.x = x
		self.y = y
		self.image = image

class SceneBase:
	def __init__(self):
		self.next = self
	
	def ProcessInput(self, events, pressed_keys):
		print("didnt override ProcessInput")

	def Update(self):
		print("didnt override Update")

	def Render(self, screen):
		print("didnt override Render")

	def SwitchToScene(self, next_scene):
		self.next = next_scene
	
	def Terminate(self):
		self.SwitchToScene(None)



class MainMenu(SceneBase):


	def __init__(self,width,height,gameDisplay):
		SceneBase.__init__(self)

		global play,intake

		lights.write('D'.encode())
		# sound1 = pygame.mixer.Sound("mlg-airhorn.mp3")
		# pygame.mixer.music.load('mlg-airhorn.mp3')
		# print(pygame.mixer.Channel(0).get_sound())
		if(pygame.mixer.Channel(0).get_sound() != menuSound):
			pygame.mixer.Channel(0).play(menuSound, -1)
		
		# intake["0"] = True
		# intake["50"] = False
		# intake["100"] = False
		
		self.font = pygame.font.Font("freesansbold.ttf",15)
		self.width = width
		self.height = height
		self.numMenuButtons = 3
		self.ms = MenuSelect("3")

		self.titleFont = pygame.font.Font("freesansbold.ttf",30)

		self.titleText,self.titleRect = getTextObjects("Robot Basketball",self.titleFont, self.width/2,
													  50, False, (128,128,128))

		self.PlayButton = pygame.Rect((width/2)-(width*.075),
									  (height/4)-(height*.05),
									   width*.15,height*.1)
		

		self.ControlButton = pygame.Rect((width/2)-(width*.075),
									  (2*height/4)-(height*.05),
									   width*.15,height*.1)


		self.ExitButton = pygame.Rect((width/2)-(width*.075),
									  (3*height/4)-(height*.05),
									   width*.15,height*.1)


		self.gameDisplay = gameDisplay
		play = False
	

	def ProcessInput(self, events, pressed_keys,active):
		for event in events:
			# if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
			# 	# Move to the next scene when the user pressed Enter
			# 	self.Switch()
			if(event.type == pygame.MOUSEBUTTONDOWN):
				mousePos = event.pos
				if(self.PlayButton.collidepoint(mousePos)):
					self.Switch(1)
				elif(self.ControlButton.collidepoint(mousePos)):
					self.Switch(2) 
				elif(self.ExitButton.collidepoint(mousePos)):
					self.Switch(3) 
			elif(event.button == 0):
				if(active == 0):
					self.Switch(1)
				elif(active == 1):
					self.Switch(2) 
				elif(active == 2):
					self.Switch(3) 

	def Switch(self,sceneNum):
		if(sceneNum == 1):
			self.SwitchToScene(SelectMenu(self.width,self.height,self.gameDisplay))
		if(sceneNum == 2):
			self.SwitchToScene(ControlMenu(self.width,self.height,self.gameDisplay))
		if(sceneNum == 3):
			self.Terminate()

	def Update(self):
		self.playText,self.playRect = getTextObjects("Play",self.font,(self.width/2),
										  (self.height/4),self.ms.list[0],blk)
		self.controlText,self.controlRect = getTextObjects("Control",self.font,(self.width/2),
										  (2*self.height/4),self.ms.list[1],blk)
		self.exitText,self.exitRect = getTextObjects("Exit",self.font,(self.width/2),
										  (3*self.height/4),self.ms.list[2],blk)
	
	def Render(self, screen):
		screen.fill((128,128,128))

		pygame.draw.rect(self.gameDisplay,[0,0,0],self.PlayButton)
		pygame.draw.rect(self.gameDisplay,[0,0,0],self.ControlButton)
		pygame.draw.rect(self.gameDisplay,[0,0,0],self.ExitButton)

		self.gameDisplay.blit(self.playText,self.playRect)
		self.gameDisplay.blit(self.controlText,self.controlRect)
		self.gameDisplay.blit(self.exitText,self.exitRect)
		self.gameDisplay.blit(self.titleText,self.titleRect)

class SelectMenu(SceneBase):
	def __init__(self,width,height,gameDisplay):
		SceneBase.__init__(self)
		self.font = pygame.font.Font("freesansbold.ttf",15)
		self.width = width
		self.height = height
		self.numMenuButtons = 2
		self.ms = MenuSelect("2")


		self.titleFont = pygame.font.Font("freesansbold.ttf",30)

		self.titleText,self.titleRect = getTextObjects("Difficulty Selection",self.titleFont, self.width/2,
													  50, False, (128,128,128))

		self.EasyButton = pygame.Rect((self.width/2)-(self.width*.125),
									  (self.height/3)-(self.height*.05),
									   self.width*.25,self.height*.1)

		self.HardButton = pygame.Rect((self.width/2)-(self.width*.125),
									  (2*self.height/3)-(self.height*.05),
									   self.width*.25,self.height*.1)
		

		self.gameDisplay = gameDisplay
		
		
	
	def ProcessInput(self, events, pressed_keys,active):
		for event in events:
			if(event.type == pygame.MOUSEBUTTONDOWN):
				mousePos = event.pos
				if(self.EasyButton.collidepoint(mousePos)):
					self.Switch(1) 
				elif(self.HardButton.collidepoint(mousePos)):
					self.Switch(2) 
			elif(event.button == 0):
				if(active == 0):
					self.Switch(1)
				elif(active == 1):
					self.Switch(2)
			elif(event.button == 1):
				self.SwitchToScene(MainMenu(self.width,self.height,self.gameDisplay))

	def Switch(self,sceneNum):
		global hardmode 

		

		if(sceneNum == 1):
			self.SwitchToScene(Arena(self.width,self.height,self.gameDisplay,False))
			hardmode = False
		if(sceneNum == 2):
			self.SwitchToScene(Arena(self.width,self.height,self.gameDisplay,True))
			hardmode = True
	def Update(self):
		self.easyText1,self.easyRect1 = getTextObjects("Easy Mode:",self.font,
													(self.width/2),(self.height/3)-10,self.ms.list[0],blk)
		self.easyText2,self.easyRect2 = getTextObjects("Computer Assistance",self.font,
													(self.width/2),(self.height/3)+10,self.ms.list[0],blk)
		self.hardText1,self.hardRect1 = getTextObjects("Hard Mode:",self.font,
													(self.width/2),(2*self.height/3)-10,self.ms.list[1],blk)
		self.hardText2,self.hardRect2 = getTextObjects("Full Control",self.font,
													(self.width/2),(2*self.height/3)+10,self.ms.list[1],blk)
	
	def Render(self, screen):
		# The game scene is just a blank blue screen
		screen.fill((128,128,128))


		pygame.draw.rect(self.gameDisplay,[0,0,0],self.EasyButton)
		pygame.draw.rect(self.gameDisplay,[0,0,0],self.HardButton)
		

		self.gameDisplay.blit(self.easyText1,self.easyRect1)
		self.gameDisplay.blit(self.easyText2,self.easyRect2)
		self.gameDisplay.blit(self.hardText1,self.hardRect1)
		self.gameDisplay.blit(self.hardText2,self.hardRect2)
		self.gameDisplay.blit(self.titleText, self.titleRect)

class ControlMenu(SceneBase):
	def __init__(self,width,height,gameDisplay):
		SceneBase.__init__(self)
		self.font = pygame.font.Font("freesansbold.ttf",25)
		self.width = width
		self.height = height
		self.numMenuButtons = 2
		self.ms = MenuSelect("2")
		self.gameDisplay = gameDisplay
		# self.font = pygame.font.Font("freesansbold.ttf",10)
		self.titleFont = pygame.font.Font("freesansbold.ttf",30)

		self.titleText,self.titleRect = getTextObjects("Controls",self.titleFont, self.width/2,
													  50, False, (128,128,128))


	def ProcessInput(self, events, pressed_keys,active):
		global invert_x
		global invert_y
		for event in events:
			if(event.type == pygame.MOUSEBUTTONDOWN):
				pass
			elif(event.button == 0):
				if(active == 0):
					invert_x *= -1
					# print("Invert X")
				elif(active == 1):
					invert_y *= -1
					# print("Invert Y")
			elif(event.button == 1):
				self.SwitchToScene(MainMenu(self.width,self.height,self.gameDisplay))

	def Switch(self,sceneNum):
		if(sceneNum == 1):
			self.SwitchToScene(Arena(self.width,self.height,self.gameDisplay,False))
		if(sceneNum == 2):
			self.SwitchToScene(Arena(self.width,self.height,self.gameDisplay,True))
	def Update(self):
		self.invXText,self.invXRect = getTextObjects("Invert X Controls:",self.font,
													(self.width*.2-50),(self.height/3)-40,self.ms.list[0],(128,128,128))

		if(invert_x == 1):
			self.xFlag,self.xFlagRect = getTextObjects("Off",self.font,self.width*.3-40,(self.height/3)-40,
														False, red)
		else:
			self.xFlag,self.xFlagRect = getTextObjects("On",self.font,self.width*.3-40,(self.height/3)-40,
														False, green)
		if(invert_y == 1):
			self.yFlag,self.yFlagRect = getTextObjects("Off",self.font,self.width*.3-40,(self.height/3)+40,
														False, red)
		else:
			self.yFlag,self.yFlagRect = getTextObjects("On",self.font,self.width*.3-40,(self.height/3)+40,
													False, green)

		self.xFlagDisp = pygame.Rect(self.xFlagRect.x-2,self.xFlagRect.y-2,40,30)
		self.yFlagDisp = pygame.Rect(self.yFlagRect.x-2,self.yFlagRect.y-2,40,30)

		self.invYText,self.invYRect = getTextObjects("Invert Y Controls:",self.font,
													(self.width*.2)-50,(self.height/3)+40,self.ms.list[1],(128,128,128))
	def Render(self,screen):
		screen.fill((128,128,128))

		if(invert_x == 1):
			pygame.draw.rect(self.gameDisplay,red,self.xFlagDisp)
		else:
			pygame.draw.rect(self.gameDisplay,green,self.xFlagDisp)

		if(invert_y == 1):
			pygame.draw.rect(self.gameDisplay,red,self.yFlagDisp)
		else:
			pygame.draw.rect(self.gameDisplay,green,self.yFlagDisp)
		
		
		self.gameDisplay.blit(controllerMap,(400,100))


		self.gameDisplay.blit(self.invXText,self.invXRect)
		self.gameDisplay.blit(self.xFlag,self.xFlagRect)


		self.gameDisplay.blit(self.invYText,self.invYRect)
		self.gameDisplay.blit(self.yFlag,self.yFlagRect)
		self.gameDisplay.blit(self.titleText,self.titleRect)

class Arena(SceneBase):

	def __init__(self,width,height,gameDisplay,mode):
		SceneBase.__init__(self)
		global play,intake,statString, aligning,replay

		replay = False

		pygame.mixer.Channel(0).play(pygame.mixer.Sound('Pulse.wav'), -1)
		aligning = False
		self.width = width
		self.height = height
		self.gameDisplay = gameDisplay

		lights.write('R'.encode())

		timePress = pygame.time.get_ticks()
		timeLeft = 0 
		pygame.mixer.Channel(1).play(pygame.mixer.Sound('Crowd_Cheering.wav'), 0)
		intake["0"] = True
		intake["50"] = False
		intake["100"] = False

		self.font = pygame.font.Font("freesansbold.ttf",30)
		
		self.hardMode = mode
		self.ms = MenuSelect("1")
		self.coordx = 300
		self.coordy = 100
		self.score = 0

		self.startTime = pygame.time.get_ticks()
		self.timeLeft = 75000
		self.totalTime = self.timeLeft
		
		self.launch = False
		self.paused = False	
		self.pausedTime = 0
		self.pauseDur = 0
		self.ui = 0
		self.uj = 0
		# self.stat,self.statRect = getTextObjects(statString,self.font,stageX/2,stageY - 30,False,blk)
		self.theta = 0
		self.initTime = pygame.time.get_ticks()

		self.playBuzz = True
		self.replayOff = 0

		self.startAlign = 0
		self.curAngle = 0
		self.prevAngle = 0
		self.warning = False

		self.curTime = 0
		play = True
	
	def ProcessInput(self, events, pressed_keys,active):
		global replay,aligning
		for event in events:
			# print("EVENTS")
			# print("TYPE",event.button)

			if(event.button == 7):
				if(not self.paused):
					self.pausedTime = pygame.time.get_ticks()
					self.totalTime = self.timeLeft*1000
				else:
					self.startTime = pygame.time.get_ticks()
				self.paused = not self.paused
			# if(event.button == 4):
			# 	replay = True
			if(event.button == 5 and self.hardMode == False):
				self.startAlign = pygame.time.get_ticks()
				aligning = True
			# if(event.button == 2):
			# 	self.score += 1

	def Switch(self,sceneNum):
		if(sceneNum == 1):
			self.SwitchToScene(MainMenu(self.width,self.height,self.gameDisplay))
		if(sceneNum == 2):
			self.SwitchToScene(SelectMenu(self.width,self.height,self.gameDisplay))

	def Update(self):
		global aligning
		self.coordx = xRob
		self.coordy = yRob
		self.ui = ui 
		self.uj = uj
		self.curTime = pygame.time.get_ticks()
		# time in milliseconds 
		if(not self.paused):
			self.timeLeft = (self.totalTime + (self.startTime-self.curTime))/1000 + self.replayOff
		# print(self.timeLeft)

		outString = "{}:{}".format(int(self.timeLeft/60),str(int(self.timeLeft%60)).zfill(2))

		self.timer,self.timerRect = getTextObjects(outString,self.font,
									int(60),int(stageY-30),False,blk)
		self.scoreText,self.scoreRect = getTextObjects("Score: " + str(self.score), self.font, stageX - 75, stageY-30,False,blk)
		
		if((pygame.time.get_ticks() - self.startAlign) > 5000):
			aligning = False
		if(self.timeLeft <= 10 and not self.warning):
			self.warning = True
			lights.write('M'.encode())
		if(self.timeLeft <= 1 and self.playBuzz == True):
			pygame.mixer.Channel(1).play(pygame.mixer.Sound('shotclock.wav'), 0)
			self.playBuzz = False
		if(self.timeLeft <= 0.00):
			# pygame.mixer.music.load('shotclock.mp3')
			# pygame.mixer.music.play(0)
			lights.write('D'.encode())
			intake["0"] = True
			intake["50"] = False
			intake["100"] = False
			self.Switch(1)



	def Render(self, screen):
		global replay, movements,circX,circY,angleRob,robotImage, repOff


		x = int(xRob*xMap)
		# x -= 40
		y = int(yRob*yMap)
		y += 25

		self.curAngle = angleRob

		o_rect = robotImage.get_rect()

		robotImage2 = pygame.transform.rotate(robotImage, angleRob-270)
		robRect = robotImage.get_rect()
		#  image_orig.get_rect(center=screen_rect.center)
		robRect.center = (robRect.width/2,robRect.height/2)

		
		if(intake["0"]):
			intakeString = "Intake: Open"
		elif(intake["50"]):
			intakeString = "Intake: Holding"
		else:
			intakeString = "Intake: Fired"

		intakeStatus, intakeStatusRect = getTextObjects(intakeString, self.font,stageX/3, stageY - 30, False, blk)

		rpmText, rpmRect = getTextObjects("RPM: {}".format(int(appRPM*32)), self.font, 2*stageX/3, stageY - 30, False, blk)

		
		screen.fill(blk)	
		self.gameDisplay.blit(courtImage,(60,15))
		# print("xrob:", xRob)
		# print("yrob:", yRob)
		# self.gameDisplay.blit(robotImage,(x,y))
		pygame.draw.circle(self.gameDisplay, (0,0,255), (x,y), 40)

		# print("x,y: ",xRob,",",yRob)

		if(circX > 0 and circY > 0):
			pygame.draw.circle(self.gameDisplay, orange, (int(circX*xMap),int(circY*yMap)), 15)
		xu = math.cos(np.radians(-angleRob))
		yu = math.sin(np.radians(-angleRob))

		pygame.draw.line(self.gameDisplay,red,(x,y),(x+xu*70,y+yu*70),3)
		self.gameDisplay.blit(self.timer,self.timerRect)
		self.gameDisplay.blit(self.scoreText,self.scoreRect)
		self.gameDisplay.blit(rpmText, rpmRect)
		# self.gameDisplay.blit(self.stat,self.statRect)
		self.gameDisplay.blit(intakeStatus,intakeStatusRect)
		
		# if(replay):
			# print("replay")			
			
			# try:
			# 	data, addr = sock1.recvfrom(1024) # buffer size is 1024 bytes
			# except:
			# 	pass
			

			# # while(len(movements) > 0):
			# screen.fill(blk)	
			# self.gameDisplay.blit(courtImage,(60,15))
			# pos = movements.popleft()
			# # print(pos)
			# pygame.draw.circle(self.gameDisplay, (0,0,255), (int(pos[0]*xMap), int(pos[1]*yMap)), 40)
			# pygame.draw.line(self.gameDisplay,red,(int(pos[0]*xMap), int(pos[1]*yMap)),
			# 				(int(pos[0]*xMap)+int(float(pos[2])*70),int(pos[1]*yMap)+int(float(pos[3])*70)),5)
			# pygame.draw.circle(self.gameDisplay, orange, (int(pos[4]*xMap),int(pos[5]*yMap)), 15)
			# pygame.time.wait(5)
			# pygame.display.flip()
			# pygame.time.Clock().tick(60)
			# # pygame.draw.line(self.gameDisplay,red,(pos[0],pos[1]),(x+int(float(self.ui)*70),y+int(float(self.uj)*70)),3)
			# if(len(movements) <= 0):
			# replay = False
			# w, h = pygame.display.get_surface().get_size()
			# clip.resize((w,h)).preview()
			
			# pygame.display.set_mode((w,h))

			# self.replayOff += (pygame.time.get_ticks() - self.curTime)/1000
				
			# print("READ:",(pygame.time.get_ticks() - curTime)/1000)
			

			

		self.prevAngle = self.curAngle


run(stageX,stageY,60)