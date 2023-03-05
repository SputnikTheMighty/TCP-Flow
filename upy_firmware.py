import machine
import neopixel
import socket
import struct
import network
import time
import vars
from message import Message

SSID = vars.WIFI_SSID
PASSWORD = vars.WIFI_PASS
NUM_LEDS = 16

# Create a neopixel object on pin GP2
np = neopixel.NeoPixel(machine.Pin(0), NUM_LEDS)

wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(SSID, PASSWORD)

while not wifi.isconnected():
    time.sleep(1)

# Create a TCP server on port 5000
server = socket.socket()
server.bind(('0.0.0.0', 301))
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.listen(1)

while True: 
    
    print('Waiting for connection...')
    conn, addr = server.accept()
    print('Connected by', addr)

    message = Message()
    completed_messages = 0

    try:

        while True:

            try:
                # Receive data from the client
                data = conn.recv(1024)
                message.append(data)
                command = message.validate_message()
                completed_messages += 1

                values = message.data

                while len(values) > 3:
                    if values[0] < NUM_LEDS:
                        np[values[0]] = (values[1], values[2], values[3])
                    values = values[4:]

                # Update the LEDs
                np.write()
            
            except KeyboardInterrupt:
                raise
           
            except Exception as e:
                print(e)

    finally:
        print("messages: {}".format(message.new_messages))
        print("completed messages: {}".format(completed_messages))
        conn.close()
