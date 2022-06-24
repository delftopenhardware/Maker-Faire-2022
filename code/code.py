
# Circuit Playground Sound Meter
import time
import array
import math
import audiobusio
import board
import neopixel
import adafruit_tsl2591



# Create sensor object, communicating over the board's default I2C bus
i2c = board.I2C()  # uses board.SCL and board.SDA

# Initialize the sensor.
sensor = adafruit_tsl2591.TSL2591(i2c)
sensor.gain = adafruit_tsl2591.GAIN_LOW
# Color of the peak pixel.
PEAK_COLOR = (100, 0, 255)
# Number of total pixels - 10 build into Circuit Playground
NUM_PIXELS = 100
ORDER = neopixel.RGB
pixel_pin = board.A0
brightness_level = 0.5

# Set up NeoPixels and turn them all off.
pixels = neopixel.NeoPixel(pixel_pin, NUM_PIXELS, brightness=brightness_level, auto_write=False, pixel_order=ORDER)
pixels.fill(0)
pixels.show()


def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)
    return (r, g, b) if ORDER in (neopixel.RGB, neopixel.GRB) else (r, g, b, 0)


def rainbow_cycle(wait):
    for j in range(255):
        for i in range(NUM_PIXELS):
            pixel_index = (i * 256 // NUM_PIXELS) + j
            pixels[i] = wheel(pixel_index & 255)
        pixels.show()
        time.sleep(wait)

while True:
    rainbow_cycle(0.001)  # rainbow cycle with 1ms delay per step
    time.sleep(2)
    lux = sensor.lux
    print(lux)
    leds_to_turn_on = translate(lux, 0, 1000,0,NUM_PIXELS)
    for i in range(NUM_PIXELS):
        pixels[i] = (255, 0, 0)
    pixels.show()
    time.sleep(2)


