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

    def validate_message(self) -> bytearray:
        header = self.Header._make(struct.unpack('>BHB', self.message[:struct.calcsize('>BHB')]))
        assert header.sof == self.SOF, f"SOF not present"
        assert header.len == len(self.message) - len(header), f"length of message is {len(self.message)}"
        return self.message[4:]

    def append(self, raw):
        for b in raw:
            if b == self.ESC:
                self.last_byte_was_escape = True
                continue

            if self.last_byte_was_escape:
                self.last_byte_was_escape = False
                
                if b == self.SOF:
                    print("data transfer cancelled by sender")
                    self.message = bytearray()
                    return
                
                self.message.append(b ^ self.XOR)
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
    