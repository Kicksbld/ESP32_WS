from machine import Pin
import neopixel
from sensor import *


class LedStripWirings:

    def __init__(self, pinDin, numLeds):
        self.pinDin = pinDin
        self.numLeds = numLeds

    @staticmethod
    def default():
        return LedStripWirings(pinDin=13, numLeds=8)


class LedStripState(SensorState):

    def __init__(self, color=(0, 0, 0)):
        self.color = color

    def __str__(self):
        return "LED: R={} G={} B={}".format(*self.color)


class LedStrip(Sensor):

    def __init__(self, wiring: LedStripWirings):
        self.num = wiring.numLeds
        self.np = neopixel.NeoPixel(Pin(wiring.pinDin, Pin.OUT), self.num)
        self.current_color = (0, 0, 0)

    def fill(self, r, g, b):
        for i in range(self.num):
            self.np[i] = (r, g, b)
        self.np.write()
        self.current_color = (r, g, b)

    def set(self, index, r, g, b):
        if 0 <= index < self.num:
            self.np[index] = (r, g, b)
            self.np.write()

    def off(self):
        self.fill(0, 0, 0)

    def red(self):
        self.fill(255, 0, 0)

    def green(self):
        self.fill(0, 255, 0)

    def blue(self):
        self.fill(0, 0, 255)

    def white(self):
        self.fill(255, 255, 255)

    def read(self):
        return LedStripState(self.current_color)
