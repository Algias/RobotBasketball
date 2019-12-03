extends Node

#contains global variables for throughout project


#game setting variables
var hardmode = false
var invertx = false
var inverty = false

#communication variables
var driveX = 0
var driveY = 0
var driveW = 0
var launcherV = 0
var intakePosition = 0
var spare1 = 0
var spare2 = 0
var spare3 = 0

var count = 100


# Called when the node enters the scene tree for the first time.
func _ready():
	pass # Replace with function body.

# Called every frame. 'delta' is the elapsed time since the previous frame.
#func _process(delta):
#	pass


func hexOut(number):
	var hex1 = 0;
	var hex2 = 0;
	var firstHalfMask = 15 #binary 00001111
	var secondHalfMask = 240 #binary 11110000
	var stringOut = ""
	
	hex1 = (number & firstHalfMask)
	hex2 = (number >> 4) & firstHalfMask
	
	stringOut = hexChar(hex2) + hexChar(hex1)
	return stringOut
	
	# Takes in a binary value (int) and returns the decimal value (int)

func hexChar(intIn):
	var charOut = ''
	match(intIn):
		0:
			charOut = '0'
		1:
			charOut = '1'
		2:
			charOut = '2'
		3:
			charOut = '3'
		4:
			charOut = '4'
		5:
			charOut = '5'
		6:
			charOut = '6'
		7:
			charOut = '7'
		8:
			charOut = '8'
		9:
			charOut = '9'
		10:
			charOut = 'A'
		11:
			charOut = 'B'
		12:
			charOut = 'C'
		13:
			charOut = 'D'
		14:
			charOut = 'E'
		15:
			charOut = 'F'
	return charOut