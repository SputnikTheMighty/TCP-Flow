import machine
import neopixel
import socket
import struct
import network
import time

SSID = "TP-Link_DA66"
PASSWORD = ""
NUM_LEDS = 16

# Create a neopixel object on pin GP2
np = neopixel.NeoPixel(machine.Pin(0), NUM_LEDS)


while True:
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    wifi.connect(SSID, PASSWORD)

    while not wifi.isconnected():
        time.sleep(1)

    while True:

        # Create a TCP server on port 5000
        server = socket.socket()
        server.bind(('0.0.0.0', 5000))
        server.listen(1)

        print('Waiting for connection...')
        conn, addr = server.accept()
        print('Connected by', addr)

        # Loop until the client disconnects
        while True:
            # Receive data from the client
            data = conn.recv(1024)
            print(data)

            # If the client disconnected, break out of the loop
            if not data:
                break

            # Convert the data to a list of integers
            values = struct.unpack('B'*len(data), data)
            print(values)

            # Set the color of the WS2815 LEDs
            for i in range(NUM_LEDS):
                np[i] = (values[0], values[1], values[2])

            # Update the LEDs
            np.write()

        # Close the connection
        conn.close()
