extends Node2D

var startingPos = self.position
# Dead zone is the area around the center of the control when it is at rest
var deadZone = 0.2

# Speed Multiplier is what you would use to implement a sensitivity setting.  Higher == more movement per press
var speedMultiplier = 3

func _ready():
	# Register event to monitor if joystick connected or disconnected
	Input.connect("joy_connection_changed",self,"joy_con_changed")

func _process(delta):
	#Make sure at least one Joystick is connected
	if(Input.get_connected_joypads().size() > 0):

		
		var xAxis = Input.get_joy_axis(0,JOY_AXIS_0)
		var yAxis = Input.get_joy_axis(0,JOY_AXIS_1)

		if(abs(xAxis) < deadZone):
			global.driveX = 0
		else:
			global.driveX = int((xAxis/1)*100)


		if(abs(yAxis) < deadZone):
			global.driveY = 0
		else:
			global.driveY = int((yAxis/1)*100)
		
		
		var rotationAxis = Input.get_joy_axis(0,JOY_AXIS_2)
		if(abs(rotationAxis) < deadZone):
			global.driveW = 0
		else:
			global.driveW = int((rotationAxis/1)*100)
			
			
		
		if(global.hardmode == true):
			
			#if holding down shoot button, wheel velocity speeds up, cant be above 100
			if(Input.is_joy_button_pressed(0,JOY_BUTTON_7)):
				global.launcherV += .5
				if(global.launcherV > 100): 
					global.launcherV = 100
				print(global.launcherV)
			#if not holding shoot button, wheel velocity slows down. cant be below 0
			else:
				global.launcherV -= .5
				if(global.launcherV < 0):
					global.launcherV = 0
			
			
			
			#TODO
			#clicking the left trigger will disengage lock and shoot ball, position should be reset after manuever is complete
			if(Input.is_joy_button_pressed(0,JOY_BUTTON_6)):
				global.intakePosition = 1
				#need to reset position to 0 when next packet is sent out 
		
		elif(global.hardmode == false):
			pass
#		if(abs(rotationAxis) > deadZone):
#			print(int((rotationAxis/1)*100))

			# xAxis is a value from +/0 0-1 depending on how hard the stick is being pressed
			
			#get x value on joystick from 1 to 100
#			print("x:" + str(int((xAxis/1)*100)))
			#get y value on joystick from 1 to 100
#			print("y:" + str(int((yAxis/1)*100)))
#			if(xAxis < 0):
#				self.position.x -= 100*delta*(speedMultiplier * abs(xAxis))
#			if(xAxis > 0):
#				self.position.x += 100*delta*(speedMultiplier * abs(xAxis))
#
#		if(abs(yAxis) > deadZone):
#			# yAxis is a value from +/0 0-1 depending on how hard the stick is being pressed
#			if(yAxis < 0):
#				self.position.y -= 100*delta*(speedMultiplier * abs(yAxis))
#			if(yAxis > 0):
#				self.position.y += 100*delta*(speedMultiplier * abs(yAxis))

	if Input.is_joy_button_pressed(0,JOY_BUTTON_0): # Same as JOY_XBOX_A
		self.position = startingPos

    # Buttons have different meanings on different devices
    # Let's loop through and see what they are defined as
	for i in range(16):
		if(Input.is_joy_button_pressed(0,i)):
			print("Button at " + str(i) + " pressed, should be button: " + Input.get_joy_button_string(i))

#
	if(Input.is_joy_button_pressed(0,JOY_DPAD_UP)):
		position.y -= 10

func joy_con_changed(deviceid,isConnected):
	if(isConnected):
		print("Joystick " + str(deviceid) + " connected")
	if(Input.is_joy_known(0)):
		print("Recognized and compatible joystick")
		print(Input.get_joy_name(0) + " device connected")
	else:
		print("Joystick " + str(deviceid) + " disconnected")