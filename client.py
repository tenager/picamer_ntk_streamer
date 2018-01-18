# -*- coding: utf-8 -*-
import socket
import time
import picamera
import RPi.GPIO as GPIO
import SocketServer
# define motion sensor pin
PIR_PIN = 4

# define your hostname /IP address
my_server = "192.168.1.177"

#client_socket = socket.socket()
#client_socket.connect((my_server, 8000))

# Make a file-like object out of the connection
#connection = client_socket.makefile('wb')


class MyTCPHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        while 1:
            self.data = self.request.recv(1024)
            if not self.data:
                break
            self.data = self.data.strip()
            print str(self.client_address[0]) + " wrote: "
            print self.data
            self.request.send(self.data.upper())


# Callback function
def my_callback(PIR_PIN):
        print " motion detected!"
        print "\n Initializing video stream ..."
        time.sleep(1)
        stream()

def stream():
	client_socket = socket.socket()
	client_socket.connect((my_server, 8000))

	# Make a file-like object out of the connection
	connection = client_socket.makefile('wb')
	try:
    		with picamera.PiCamera() as camera:
			camera.resolution = (640, 480)
        		camera.framerate = 24
        		# Start a preview and let the camera warm up for 2 seconds
        		#camera.start_preview()
			camera.annotate_text = 'Unauthorized person detected!'
        		time.sleep(2)
        		# Start recording, sending the output to the connection for 60
        		# seconds, then stop
       			camera.start_recording(connection, format='h264')
       			camera.wait_recording(60)
        		camera.stop_recording()
	finally:
		connection.close()
		client_socket.close()
def main():
	print "Surveillance application using PIR sensor and camera module."
        print "Press CTRL+C to exit"
        print "Waiting for motion ..."
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(PIR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        # inser a bouncetime of more than 10 sconds
        GPIO.add_event_detect(PIR_PIN, GPIO.RISING, callback=my_callback, bouncetime=12000)
        #GPIO.add_event_callback(PIR_PIN, my_callback)
        while 1:
                time.sleep(100)
        GPIO.cleanup()

# if this script is run directly on the terminal using command line
# run the main() function of the code
if __name__== "__main__":
        main()
