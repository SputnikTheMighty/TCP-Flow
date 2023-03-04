import socket
from enum import IntEnum, auto
import time

colours = [b'\x00\x00\x0F', b'\x00\x0F\x00', b'\x0F\x00\x00']

# set up the TCP socket
HOST = '192.168.0.203'
PORT = 301

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    # send data to the server
    while True:

        b = bytearray()
        i = 0
        while i < 16:
            for c in colours:
                b += bytearray((i,))
                b += bytearray(c)
                i += 1
                if i > 15:
                    break

        s.send(b)
        time.sleep(0.1)
        temp = colours[0]
        colours[0] = colours[1]
        colours[1] = colours[2]
        colours[2] = temp