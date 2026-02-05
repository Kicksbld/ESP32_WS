from machine import Pin
from sensor import *

class ButtonWirings:

    def __init__(self, pinButton):
        self.pinButton = pinButton

    @staticmethod
    def default():
        return ButtonWirings(pinButton=26)


class ButtonState(SensorState):

    def __init__(self, pressed=False):
        self.pressed = pressed

    def __str__(self):
        return "Pressed: {}".format(self.pressed)

    def to_json(self):
        return {
            "IsPressed": self.pressed
        }

class Button(Sensor):

    def __init__(self, wiring:ButtonWirings, on_click=None):
        self.pin = Pin(wiring.pinButton, Pin.IN, Pin.PULL_UP)
        self.state = ButtonState(pressed=False)
        self.on_click = on_click

    def read(self):
        pressed = not self.pin.value()
        was_pressed = self.state.pressed
        self.state = ButtonState(pressed)

        if pressed and not was_pressed:
            if self.on_click:
                self.on_click(self)

        return self.state
    
