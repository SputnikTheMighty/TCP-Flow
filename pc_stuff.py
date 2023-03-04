import socket
from enum import IntEnum, auto

class ColourChoice(IntEnum):
    BLUE = auto()
    RED = auto()
    GREEN = auto()

print("\n".join("\t{}: {}".format(x, x.name) for x in ColourChoice))
choice = int(input("Choose a colour: "))

if choice == ColourChoice.BLUE:
    data = b'\x00\x00\x0F'
elif choice == ColourChoice.RED:
    data = b'\x0F\x00\x00'
elif choice == ColourChoice.GREEN:
    data = b'\x00\x0F\x00'

# set up the TCP socket
HOST = '192.168.0.203'
PORT = 301

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    # send data to the server
    s.send(data)