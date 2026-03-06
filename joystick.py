from machine import Pin, ADC
from sensor import *


class JoystickWirings:

    def __init__(self, pinX, pinY, pinButton):
        self.pinX = pinX
        self.pinY = pinY
        self.pinButton = pinButton

    @staticmethod
    def default():
        return JoystickWirings(pinX=34, pinY=35, pinButton=25)


class JoystickDirection:
    CENTER = "CENTER"
    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"
    UP_LEFT = "UP_LEFT"
    UP_RIGHT = "UP_RIGHT"
    DOWN_LEFT = "DOWN_LEFT"
    DOWN_RIGHT = "DOWN_RIGHT"


class JoystickState(SensorState):

    def __init__(self, direction="CENTER", button=False):
        self.direction = direction
        self.button = button

    def __str__(self):
        return "Direction: {}, Button: {}".format(self.direction, self.button)

    def __eq__(self, other):
        if not isinstance(other, JoystickState):
            return False
        return self.direction == other.direction and self.button == other.button

    def to_json(self):
        return {
            "direction": self.direction,
            "button": self.button
        }


class Joystick(Sensor):

    THRESHOLD_LOW = 1200
    THRESHOLD_HIGH = 2800

    def __init__(self, wiring: JoystickWirings, on_change=None):
        # Axes
        self.x = ADC(Pin(wiring.pinX))
        self.y = ADC(Pin(wiring.pinY))

        # Config ADC
        self.x.atten(ADC.ATTN_11DB)
        self.y.atten(ADC.ATTN_11DB)
        self.x.width(ADC.WIDTH_12BIT)
        self.y.width(ADC.WIDTH_12BIT)

        # Bouton
        self.btn = Pin(wiring.pinButton, Pin.IN, Pin.PULL_UP)

        self.state = JoystickState()
        self.on_change = on_change

    def _get_direction(self, x_val, y_val):
        up = y_val < self.THRESHOLD_LOW
        down = y_val > self.THRESHOLD_HIGH
        left = x_val < self.THRESHOLD_LOW
        right = x_val > self.THRESHOLD_HIGH

        if up and left:
            return JoystickDirection.UP_LEFT
        if up and right:
            return JoystickDirection.UP_RIGHT
        if down and left:
            return JoystickDirection.DOWN_LEFT
        if down and right:
            return JoystickDirection.DOWN_RIGHT
        if up:
            return JoystickDirection.UP
        if down:
            return JoystickDirection.DOWN
        if left:
            return JoystickDirection.LEFT
        if right:
            return JoystickDirection.RIGHT

        return JoystickDirection.CENTER

    def read(self):
        x_val = self.x.read()
        y_val = self.y.read()
        btn_val = not self.btn.value()

        direction = self._get_direction(x_val, y_val)
        new_state = JoystickState(direction, btn_val)

        if self.on_change and new_state != self.state:
            self.on_change(self, new_state)

        self.state = new_state
        return self.state
