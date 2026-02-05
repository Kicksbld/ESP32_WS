from machine import Pin
import dht
from sensor import *


class TemperatureWirings:

    def __init__(self, pinData):
        self.pinData = pinData

    @staticmethod
    def default():
        return TemperatureWirings(pinData=4)


class TemperatureState(SensorState):

    def __init__(self, temperature=0, humidity=0):
        self.temperature = temperature
        self.humidity = humidity

    def __str__(self):
        return "Temp: {}°C, Humidity: {}%".format(self.temperature, self.humidity)


class Temperature(Sensor):

    def __init__(self, wiring: TemperatureWirings):
        self.dht = dht.DHT11(Pin(wiring.pinData))

    def read(self):
        try:
            self.dht.measure()
            return TemperatureState(
                temperature=self.dht.temperature(),
                humidity=self.dht.humidity()
            )
        except:
            return TemperatureState()
