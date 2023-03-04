import socket

# set up the TCP socket
HOST = '192.168.0.203'
PORT = 5000
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

# send data to the server
s.send(b'\x00\x0F\x00')

# receive data from the server
response = s.recv(1024)
print(response)

# close the connection
s.close()