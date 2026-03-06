from machine import Pin, time_pulse_us
import time
from sensor import *


class UltrasonicWirings:

    def __init__(self, pinTrig, pinEcho):
        self.pinTrig = pinTrig
        self.pinEcho = pinEcho

    @staticmethod
    def default():
        return UltrasonicWirings(pinTrig=32, pinEcho=33)


class UltrasonicState(SensorState):

    def __init__(self, distance_cm=0):
        self.distance_cm = distance_cm

    def __str__(self):
        return "Distance: {:.1f} cm".format(self.distance_cm)

    def to_json(self):
        return {
            "distance_cm": self.distance_cm
        }


class Ultrasonic(Sensor):

    def __init__(self, wiring: UltrasonicWirings, on_change=None):
        self.trig = Pin(wiring.pinTrig, Pin.OUT)
        self.echo = Pin(wiring.pinEcho, Pin.IN)
        self.trig.value(0)
        self.state = UltrasonicState()
        self.on_change = on_change

    def read(self):
        # S'assurer que ECHO est bas avant de commencer
        while self.echo.value() == 1:
            pass

        # Envoyer une impulsion de 10µs sur TRIG
        self.trig.value(0)
        time.sleep_us(5)
        self.trig.value(1)
        time.sleep_us(10)
        self.trig.value(0)

        # Mesurer la durée de l'impulsion ECHO
        duration = time_pulse_us(self.echo, 1, 30000)  # Timeout 30ms

        if duration < 0:
            distance_cm = -1
        else:
            # distance = (durée * 0.0343) / 2
            distance_cm = (duration * 0.0343) / 2

        new_state = UltrasonicState(distance_cm)

        if self.on_change:
            self.on_change(self, new_state)

        self.state = new_state
        return self.state
