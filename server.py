import socket
import subprocess


# create socket
def socket_create():
	try:
		global host
		global port
		global server_socket
		host = ''
		port = 8000
		server_socket = socket.socket()
	except socket.error as msg:
		print "socket creation failed: "+str(msg)

def socket_bind():
	try:
		global host
		global port 
		global server_socket
		print ("Binding socket to port: " + str(port))
		server_socket.bind((host, port))
		server_socket.listen(5)
	except socket.error as msg:
		print "socket binding failed: " + str(msg) + "Retrying"
		socket_bind()
 
def socket_accept():
	global server_socket
	connection = server_socket.accept()[0].makefile('rb')
	video_receiver(connection)
	connection.close()
	#server_socket.close()

# video receiver
def video_receiver(connection):
	#while True:
		try:
			 cmdline = ['mplayer', '-fps', '25', '-cache', '1024', '-']
	                 player = subprocess.Popen(cmdline, stdin=subprocess.PIPE)
         	         while True:
                        # Repeatedly read 1k of data from the connection and write it to
                        # the media player's stdin
                         	data = connection.read(1024)
                       		if not data:
                                	break
                        	player.stdin.write(data)

		finally:
	    		#connection.close()
    			player.terminate()

def main():
	socket_create()
	socket_bind()
	while True:
		socket_accept()

# if this script is run directly on the terminal using command line
# run the main() function of the code
if __name__== "__main__":
        main()

