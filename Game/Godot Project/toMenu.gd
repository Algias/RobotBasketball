extends Button

# Declare member variables here. Examples:
# var a = 2
# var b = "text"

# Called when the node enters the scene tree for the first time.
func _ready():
	#wont function if you dont have connect here
	connect("pressed",self,"on_pressed")
	pass


func on_pressed():
	get_tree().change_scene("res://MainScreen.tscn")
	global.hardmode = true