extends CheckButton

# Declare member variables here. Examples:
# var a = 2
# var b = "text"

# Called when the node enters the scene tree for the first time.
func _ready():
	#wont function if you dont have connect here
	connect("toggled",self,"on_toggled")
	
	pass

func on_toggled(pressed):
	if(pressed):
		global.inverty = true;
		print("inverted y")
	else:
		global.inverty = false;
		print("uninverted y")