import struct
import time
from collections import namedtuple

class MessageException(Exception):
    pass

class Message:

    SOF = b'\x7E'
    EOF = b'\x7C'
    ESC = b'\x7D'
    XOR = b'\x20'

    Header = namedtuple("Header", "sof len cmd")

    TIMEOUT_MS = 5000

    def __init__(self, tcp_conn) -> None:
        self.message = bytearray()
        self.last_byte_was_escape = False
        self.new_messages = 0
        self.conn = tcp_conn

    def validate_message(self) -> bytearray:
        header = self.Header(*struct.unpack('>BHB', self.message[:struct.calcsize('>BHB')]))
        assert header.sof == int.from_bytes(self.SOF, 'big'), "SOF not present"
        assert header.len == len(self.message) - len(header) - 1, "length of message is {}".format(len(self.message))
        assert self.message[-1] == int.from_bytes(self.EOF, 'big'), "EOF not present"
        self.data = self.message[struct.calcsize('>BHB'):]
        return header.cmd

    def get_message(self):

        tick = time.ticks_ms()
        while time.ticks_ms() - tick < self.TIMEOUT_MS:

            b = self.conn.recv(1)
            if b is None:
                continue

            if self.last_byte_was_escape:
                self.last_byte_was_escape = False
                
                if b == self.SOF:
                    self.message = bytearray()
                    raise MessageException("data transfer cancelled")
                else:
                    self.message += (b ^ self.XOR)
            
            elif b == self.SOF:
                self.message = bytearray()
                self.message += b
                self.new_messages += 1

            elif b == self.EOF:
                self.message += b
                return
            
            elif b == self.ESC:
                self.last_byte_was_escape = True

            else:
                self.message += b

        raise MessageException("Get message timeout")

    @classmethod
    def construct(cls, data):
        input = bytearray(int.to_bytes(len(data), 2, 'big'))
        input += data

        message = bytearray()
        message += cls.SOF

        for i in input:
            if i == cls.SOF or i == cls.ESC:
                message.append(cls.ESC)
                message.append(i ^ cls.XOR)
            else:
                message.append(i)

        message += cls.EOF
        return message
    

if __name__ == "__main__":

    data = b'\x04\x7e\x78\x7D\x7D'

    raw = Message.construct(data)
    
    print([hex(x) for x in raw])

    message = Message()
    message.append(raw)
    print([hex(x) for x in message.message])

    message.validate_message()
    