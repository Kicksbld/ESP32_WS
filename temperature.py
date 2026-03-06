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

    def to_json(self):
        return {
            "temperature": self.temperature,
            "humidity": self.humidity
        }


class Temperature(Sensor):

    def __init__(self, wiring: TemperatureWirings, on_change=None):
        self.dht = dht.DHT11(Pin(wiring.pinData))
        self.state = TemperatureState()
        self.on_change = on_change

    def read(self):
        try:
            self.dht.measure()
            new_state = TemperatureState(
                temperature=self.dht.temperature(),
                humidity=self.dht.humidity()
            )
        except:
            new_state = TemperatureState()

        if self.on_change:
            self.on_change(self, new_state)

        self.state = new_state
        return self.state
