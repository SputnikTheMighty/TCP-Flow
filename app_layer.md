# Application Layer

| Byte | Name |
|------|------|
| 0    | SOF  |
| 1    | len  |
| 2    | cmd  |
| 3    | data |
| 4 + len(data)    | eof  |
| 5 + len(data) | crc |

Message overhead = 7 bytes (size of everything except data)

For a full update of 144 LEDs, the data would be 144*4 = 576, so a full message would be 683 bytes.

## Deliminating
As everything is sent in binary, we need a way to know where the start of a frame is.

We define an escape character: `0x7D`

SOF will be 0x7E. If 0x7E occurs in the data, it will be replaced by 0x7D and the next value will be 

The frame boundary octet is 0x7E. A "control escape octet", has the value 0x7D. If either of these two octets appears in the transmitted data, an escape octet is sent, followed by the original data octet with bit 5 inverted. For example, the byte 0x7E would be transmitted as 0x7D 0x5E ("10111110 01111010"). The byte 0x7D would be sent as 0x7D 0x5D. Other reserved octet values (such as XON or XOFF) can be escaped in the same way if necessary.

The "abort sequence" 0x7D 0x7E ends a packet with an incomplete byte-stuff sequence, forcing the receiver to detect an error. This can be used to abort packet transmission with no chance the partial packet will be interpreted as valid by the receiver.