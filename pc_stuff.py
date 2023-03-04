import socket

# set up the TCP socket
HOST = '192.168.0.203'
PORT = 5000
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

# send data to the server
s.send(b'\x00\x00\x0F')

# close the connection
s.close()