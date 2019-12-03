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
	#get_tree().change_scene("res://PlayOptions.tscn")
	var socket = PacketPeerUDP.new()
  
	socket.set_dest_address("127.0.0.1",4242)
	socket.put_packet("quit".to_ascii())
    
	print("Exiting application")  
	get_tree().quit()

# Called every frame. 'delta' is the elapsed time since the previous frame.
#func _process(delta):
#	pass
