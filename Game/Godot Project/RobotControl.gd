extends Area2D

var startingPos = self.position
# Dead zone is the area around the center of the control when it is at rest
var deadZone = 0.2

# Speed Multiplier is what you would use to implement a sensitivity setting.  Higher == more movement per press
var speedMultiplier = 3
var socket = PacketPeerUDP.new()

func _init():
	if(socket.listen(4242,"127.0.0.1") != OK):
		print("An error occurred listening on port 4242")
	else:
		print("Listening on port 4242 on localhost")
	


func _ready():
	# Register event to monitor if joystick connected or disconnected
	Input.connect("joy_connection_changed",self,"joy_con_changed")

func _draw():
	draw_rect((Rect2(-25,-25,50,50)),Color.blue, true)

func _process(delta):
	update()
	if(socket.get_available_packet_count() > 0):
		var data = socket.get_packet().get_string_from_ascii()
		print(data)
		
		var splits = data.split(",",true)
		#print(splits[0])
		#print(splits[1])
		
		self.position = Vector2(float(splits[0]),float(splits[1]))
		
	#Make sure at least one Joystick is connected
#	if Input.get_connected_joypads().size() > 0:
#		var xAxis = Input.get_joy_axis(0,JOY_AXIS_0)
#		var yAxis = Input.get_joy_axis(0,JOY_AXIS_1)
#
#		if(abs(xAxis) > deadZone):    
#			# xAxis is a value from +/0 0-1 depending on how hard the stick is being pressed
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