from machine import Pin
from neopixel import NeoPixel
import time

pin = Pin(0, Pin.OUT)   # set GPIO0 to output to drive NeoPixels
np = NeoPixel(pin, 16)   # create NeoPixel driver on GPIO0 for 8 pixels
np.write()              # write data to all pixels

while True:
    for i in range(16):
        for j in range(16):
            np[j] = (0, 0, 0)
        np[i] = (70, 0, 0)
        np.write()
        time.sleep(0.1)
