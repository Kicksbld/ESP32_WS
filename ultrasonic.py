from machine import Pin, time_pulse_us
import time


class UltrasonicWirings:

    def __init__(self, pinTrig, pinEcho):
        self.pinTrig = pinTrig
        self.pinEcho = pinEcho

    @staticmethod
    def default():
        return UltrasonicWirings(pinTrig=32, pinEcho=33)


class UltrasonicState:

    def __init__(self, distance_cm=0):
        self.distance_cm = distance_cm

    def __str__(self):
        return "Distance: {:.1f} cm".format(self.distance_cm)


class Ultrasonic:

    def __init__(self, wiring: UltrasonicWirings):
        self.trig = Pin(wiring.pinTrig, Pin.OUT)
        self.echo = Pin(wiring.pinEcho, Pin.IN)
        self.trig.value(0)

    def read(self):
        # Envoyer une impulsion de 10µs sur TRIG
        self.trig.value(0)
        time.sleep_us(2)
        self.trig.value(1)
        time.sleep_us(10)
        self.trig.value(0)

        # Mesurer la durée de l'impulsion ECHO
        duration = time_pulse_us(self.echo, 1, 30000)  # Timeout 30ms

        if duration < 0:
            # Timeout ou erreur
            return UltrasonicState(-1)

        # Calculer la distance (vitesse du son = 343 m/s)
        # distance = (durée * 0.0343) / 2
        distance_cm = (duration * 0.0343) / 2

        return UltrasonicState(distance_cm)

    def get_distance(self):
        return self.read().distance_cm
