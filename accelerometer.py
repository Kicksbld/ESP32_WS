from machine import Pin, I2C
from sensor import *
import struct


class AccelerometerWirings:

    def __init__(self, pinSDA, pinSCL, address=0x68):
        self.pinSDA = pinSDA
        self.pinSCL = pinSCL
        self.address = address

    @staticmethod
    def default():
        return AccelerometerWirings(pinSDA=23, pinSCL=22)


class AccelerometerState(SensorState):

    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return "Accel: X={}, Y={}, Z={}".format(self.x, self.y, self.z)

    def to_json(self):
        return {
            "x": self.x,
            "y": self.y,
            "z": self.z
        }


class Accelerometer(Sensor):

    def __init__(self, wiring: AccelerometerWirings, on_change=None):
        self.i2c = I2C(0, scl=Pin(wiring.pinSCL), sda=Pin(wiring.pinSDA), freq=400000)
        self.address = wiring.address
        self.state = AccelerometerState()
        self.on_change = on_change

        # Wake up le MPU6050 (registre power management = 0)
        self.i2c.writeto_mem(self.address, 0x6B, b'\x00')

    def read(self):
        # Lire 6 octets a partir du registre 0x3B (ACCEL_XOUT_H)
        data = self.i2c.readfrom_mem(self.address, 0x3B, 6)
        x = struct.unpack('>h', data[0:2])[0]
        y = struct.unpack('>h', data[2:4])[0]
        z = struct.unpack('>h', data[4:6])[0]

        new_state = AccelerometerState(x, y, z)

        if self.on_change:
            self.on_change(self, new_state)

        self.state = new_state
        return self.state
