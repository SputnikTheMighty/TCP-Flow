import struct
from collections import namedtuple

class Message:

    SOF = 0x7E
    ESC = 0x7D
    XOR = 0x20

    Header = namedtuple("Header", "sof len cmd")

    def __init__(self) -> None:
        self.message = bytearray()
        self.last_byte_was_escape = False
        self.new_messages = 0

    def validate_message(self) -> bytearray:
        header = self.Header(*struct.unpack('>BHB', self.message[:struct.calcsize('>BHB')]))
        assert header.sof == self.SOF, "SOF not present"
        assert header.len == len(self.message) - len(header), "length of message is {}".format(len(self.message))
        self.data = self.message[struct.calcsize('>BHB'):]
        return header.cmd

    def append(self, raw):
        for b in raw:

            if self.last_byte_was_escape:
                self.last_byte_was_escape = False
                
                if b == self.SOF:
                    print("data transfer cancelled by sender")
                    self.message = bytearray()
                else:
                    self.message.append(b ^ self.XOR)
            
            elif b == self.SOF:
                self.message = bytearray()
                self.message.append(b)
                self.new_messages += 1
            
            elif b == self.ESC:
                self.last_byte_was_escape = True

            else:
                self.message.append(b)

    @classmethod
    def construct(cls, data):
        input = bytearray(int.to_bytes(len(data), 2, 'big'))
        input += data

        message = bytearray()
        message.append(cls.SOF)

        for i in input:
            if i == cls.SOF or i == cls.ESC:
                message.append(cls.ESC)
                message.append(i ^ cls.XOR)
            else:
                message.append(i)

        return message
    

if __name__ == "__main__":

    data = b'\x04\x7e\x78\x7D\x7D'

    raw = Message.construct(data)
    
    print([hex(x) for x in raw])

    message = Message()
    message.append(raw)
    print([hex(x) for x in message.message])

    message.validate_message()
    