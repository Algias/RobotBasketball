import RPi.GPIO as GPIO
import time
import socket

import datetime

UDP_IP1 = "127.0.0.1"
UDP_PORT1 = 4000
sock1 = socket.socket(socket.AF_INET, # Internet
					socket.SOCK_DGRAM) # UDP
# sock1.bind((UDP_IP1, UDP_PORT1))
# sock1.setblocking(0)




but_pin = 12

curTime = 0.0
# curTime = datetime.datetime.now()
# lastPress = None
lastPress = 0.0

def LimitCallback(channel):
    # global lastPress
    # curTime = datetime.datetime.now().microsecond
    #pressTime = datetime.datetime.now().microsecond
    # print(curTime - lastPress)
    # print("Pressed")
    # if(lastPress == None):
    #     print("Limit switch pressed!")
    #     sock1.sendto("1".encode(), (UDP_IP1, UDP_PORT1))
    #     lastPress = datetime.datetime.now()
    
    lastPress = datetime.datetime.now()
    #if((datetime.datetime.now() - lastPress).microseconds > 700000):
    if((curTime - lastPress) > 10.0):
        print(curTime - lastPress)
        print("Limit switch pressed!")
        sock1.sendto("1".encode(), (UDP_IP1, UDP_PORT1))
        # lastPress = datetime.datetime.now()
    
       
    

def main():
    
    # Pin Setup:
    GPIO.setmode(GPIO.BOARD)  # BOARD pin-numbering scheme
    # GPIO.setup([led_pin_1, led_pin_2], GPIO.OUT)  # LED pins set as output
    GPIO.setup(but_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    # GPIO.setup(but_pin, GPIO.IN)  # button pin set as input
    curTime = datetime.datetime.now()
    GPIO.add_event_detect(but_pin, GPIO.FALLING, callback=LimitCallback)
    print("Starting demo now! Press CTRL+C to exit")

    

    try:
        while True:
            pass
            # print(curTime)
            # # blink LED 1 slowly
            # time.sleep(.15)
    finally:
        GPIO.cleanup()  # cleanup all GPIOs

if __name__ == '__main__':
    main()