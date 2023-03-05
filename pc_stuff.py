import socket
from enum import IntEnum, auto
import time
from message import Message

colours = [b'\x00\x00\x0F', b'\x00\x0F\x00', b'\x0F\x00\x00']

# set up the TCP socket
HOST = '192.168.0.203'
PORT = 301

class Np:

    NUM_DATA_BYTES = 3

    def __init__(self, number) -> None:
        self.number = number
        self.array = [[0 for y in range(self.NUM_DATA_BYTES)] for x in range(number)]
    
    def to_bytearray(self):
        b = bytearray()
        for i, d in enumerate(self.array):
            b += bytearray(([i] + d))
        return b

if __name__ == "__main__":

    np = Np(16)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        # send data to the server
        while True:

            for i in range(16):

                for j in range(16):
                    np.array[j] = [0x00, 0x00, 0x00]

                np.array[i] = [0x0F, 0x00, 0x00]
                m = bytearray([0x04])
                m += np.to_bytearray()

                s.send(Message.construct(m))
                time.sleep(0.1)
