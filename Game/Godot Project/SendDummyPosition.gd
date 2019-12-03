extends Button
var rng = RandomNumberGenerator.new()
# Declare member variables here. Examples:
# var a = 2
# var b = "text"
var socket = PacketPeerUDP.new()
var socket2 = PacketPeerUDP.new()



# Called when the node enters the scene tree for the first time.

func _init():
	socket.set_dest_address("127.0.0.1",4242)
	socket2.set_dest_address("127.0.0.1",3000)
func _ready():
	pass # Replace with function body.

# Called every frame. 'delta' is the elapsed time since the previous frame.
#func _process(delta):
#	pass


func _on_SendDummyPosition_pressed():
	var randX = rng.randf_range(200,1000)
	var randY = rng.randf_range(100,500)
	
	var output = str(randX) + "," + str(randY) 
	
	socket.put_packet(output.to_ascii())
	
	socket2.put_packet(output.to_ascii())
	
	print(global.hexOut(global.count))
	global.count += 1
	
	pass # Replace with function body.
