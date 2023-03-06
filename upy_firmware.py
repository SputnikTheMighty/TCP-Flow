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

    message = Message(conn)
    completed_messages = 0
    total_write_time = 0
    total_read_time = 0

    try:

        while True:

            try:
                tick_read = time.ticks_us()
                message.get_message()
                command = message.validate_message()
                completed_messages += 1
                tock_read = time.ticks_us()
                total_read_time += (tock_read - tick_read)

                values = message.data

                tick_write = time.ticks_us()
                while len(values) > 3:
                    if values[0] < NUM_LEDS:
                        np[values[0]] = (values[1], values[2], values[3])
                    values = values[4:]
                np.write()
                tock_write = time.ticks_us()
                total_write_time += (tock_write - tick_write)
            
            except KeyboardInterrupt:
                raise
           
            except Exception as e:
                print("exception in main: {}".format(e))

    finally:
        print("messages: {}".format(message.new_messages))
        print("completed messages: {}".format(completed_messages))
        print("average write time: {}".format(total_write_time/completed_messages))
        print("average read time: {}".format(total_read_time/completed_messages))
        conn.close()
