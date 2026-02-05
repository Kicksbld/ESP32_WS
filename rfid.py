from machine import Pin, SPI
from sensor import *


class RFIDWirings:

    def __init__(self, pinSDA, pinSCK, pinMOSI, pinMISO, pinRST):
        self.pinSDA = pinSDA
        self.pinSCK = pinSCK
        self.pinMOSI = pinMOSI
        self.pinMISO = pinMISO
        self.pinRST = pinRST

    @staticmethod
    def default():
        return RFIDWirings(
            pinSDA=5,
            pinSCK=18,
            pinMOSI=23,
            pinMISO=19,
            pinRST=22
        )


class RFIDState(SensorState):

    def __init__(self, detected=False):
        self.detected = detected

    def __str__(self):
        return "Card: {}".format("Yes" if self.detected else "No")


class RFID(Sensor):

    def __init__(self, wiring: RFIDWirings):
        self.rst = Pin(wiring.pinRST, Pin.OUT)
        self.rst.value(1)

        self.spi = SPI(2, baudrate=2500000, polarity=0, phase=0,
                       sck=Pin(wiring.pinSCK),
                       mosi=Pin(wiring.pinMOSI),
                       miso=Pin(wiring.pinMISO))

        self.cs = Pin(wiring.pinSDA, Pin.OUT)
        self.cs.value(1)

        self._init()

    def _write(self, addr, val):
        self.cs.value(0)
        self.spi.write(bytes([(addr << 1) & 0x7E, val]))
        self.cs.value(1)

    def _read(self, addr):
        self.cs.value(0)
        self.spi.write(bytes([((addr << 1) & 0x7E) | 0x80]))
        val = self.spi.read(1)
        self.cs.value(1)
        return val[0]

    def _init(self):
        self._write(0x01, 0x0F)  # Reset
        self._write(0x2A, 0x8D)
        self._write(0x2B, 0x3E)
        self._write(0x2D, 30)
        self._write(0x2C, 0)
        self._write(0x15, 0x40)
        self._write(0x11, 0x3D)
        # Antenna on
        if ~(self._read(0x14) & 0x03):
            self._write(0x14, self._read(0x14) | 0x03)

    def read(self):
        # Request card
        self._write(0x0D, 0x07)
        self._write(0x01, 0x00)
        self._write(0x04, 0x7F)
        self._write(0x09, 0x26)  # REQA command
        self._write(0x01, 0x0C)  # Transceive
        self._write(0x0D, self._read(0x0D) | 0x80)

        i = 100
        while i > 0:
            if self._read(0x04) & 0x30:
                break
            i -= 1

        detected = (self._read(0x06) & 0x1B) == 0x00 and i > 0
        return RFIDState(detected)
