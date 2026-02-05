# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()
import network
import time

print("In Boot")

def wifi_connect(ssid, psd):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if not wlan.isconnected():
        print('Connecting to WiFi...')
        wlan.connect(ssid, psd)
        while not wlan.isconnected():
            print('.', end='')
            time.sleep(0.5)
    print('WiFi connected:', wlan.ifconfig())
    
wifi_connect("Salle-de-creation", "animation")


