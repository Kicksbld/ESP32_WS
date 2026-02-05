from machine import Pin, ADC
from sensor import *


class LightSensorWirings:

    def __init__(self, pinData):
        self.pinData = pinData

    @staticmethod
    def default():
        return LightSensorWirings(pinData=34)


class LightSensorState(SensorState):

    def __init__(self, value=0, percentage=0):
        self.value = value
        self.percentage = percentage

    def __str__(self):
        return "Light: {}% ({})".format(self.percentage, self.value)

    def to_json(self):
        return {
            "raw": self.value,
            "percentage": self.percentage
        }


class LightSensor(Sensor):

    def __init__(self, wiring: LightSensorWirings, on_change=None):
        self.adc = ADC(Pin(wiring.pinData))
        self.adc.atten(ADC.ATTN_11DB)
        self.adc.width(ADC.WIDTH_12BIT)
        self.state = LightSensorState()
        self.on_change = on_change

    def read(self):
        value = self.adc.read()
        percentage = int(value * 100 / 4095)
        new_state = LightSensorState(value=value, percentage=percentage)

        if self.on_change:
            self.on_change(self, new_state)

        self.state = new_state
        return self.state
