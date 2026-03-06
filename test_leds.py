from machine import Pin
import neopixel
from time import sleep

PIN = 13
NUM_LEDS = 8

print("Test LEDs - GPIO {} - {} leds".format(PIN, NUM_LEDS))

try:
    np = neopixel.NeoPixel(Pin(PIN, Pin.OUT), NUM_LEDS)
    print("NeoPixel initialisé")

    print("Rouge...")
    for i in range(NUM_LEDS):
        np[i] = (255, 0, 0)
    np.write()
    sleep(1)

    print("Vert...")
    for i in range(NUM_LEDS):
        np[i] = (0, 255, 0)
    np.write()
    sleep(1)

    print("Bleu...")
    for i in range(NUM_LEDS):
        np[i] = (0, 0, 255)
    np.write()
    sleep(1)

    print("Extinction")
    for i in range(NUM_LEDS):
        np[i] = (0, 0, 0)
    np.write()

    print("Test terminé OK")

except Exception as e:
    print("ERREUR:", e)
