import socket
import subprocess

# Start a socket listening for connections on 0.0.0.0:8000 (0.0.0.0 means
# all interfaces)
server_socket = socket.socket()
server_socket.bind(('0.0.0.0', 8000))
server_socket.listen(0)

# Accept a single connection and make a file-like object out of it
connection = server_socket.accept()[0].makefile('rb')
def main():
	try:
    		# Run a viewer with an appropriate command line. Uncomment the mplayer
    		# version if you would prefer to use mplayer instead of VLC
    		# cmdline = ['vlc', '--demux', 'h264', '-']
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
    		connection.close()
    		server_socket.close()
    		player.terminate()

# if this script is run directly on the terminal using command line
# run the main() function of the code
if __name__== "__main__":
        main()

