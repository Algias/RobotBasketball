extends SceneTree

var done = false

var socket = PacketPeerUDP.new()

func _init():
#	set_process(true)
	if(socket.listen(3000,"127.0.0.1") != OK):
		print("An error occurred listening on port 4242")
		done = true;
	else:
		print("Listening on port 4242 on localhost")

    
#fixed to be nonblocking when waiting for packet to come through socket

#_iteration is SceneTree version of Node2Ds _process
func _iteration(delta):
	if(socket.get_available_packet_count() > 0):
		var data = socket.get_packet().get_string_from_ascii()
		if(data == "quit"):
			done = true
			socket.close()        
			print("Exiting application")    
			self.quit()
		else:
			print("Data received: " + data)

