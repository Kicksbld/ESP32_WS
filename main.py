from joystick import *
from button import *
from rfid import *
from ledstrip import *
from sensor import *
from ochestrator import *
from wsclient import WSClient
from Message import Message, MessageType, SensorId
from time import sleep
from lightSensor import *

CLIENT_NAME = "ESP_Killian"

def on_connect():
    print("WS connected")

def handle_led_command(value):
    """Traite une commande LED reçue de l'IA."""
    try:
        # value peut être un dict ou une string JSON
        if isinstance(value, str):
            import json
            data = json.loads(value)
        else:
            data = value

        led_id = data.get("led_id")
        state = data.get("state", "").lower()

        # Convertir de 1-indexed (utilisateur) à 0-indexed (array)
        if led_id is not None:
            led_id = led_id - 1

        print(f"LED command: led_id={led_id}, state={state}")

        if state == "on":
            # Clignotement 3 fois puis éteint
            for _ in range(3):
                if led_id is not None and 0 <= led_id < leds.num:
                    leds.set(led_id, 255, 255, 255)
                else:
                    leds.white()
                sleep(0.2)
                if led_id is not None and 0 <= led_id < leds.num:
                    leds.set(led_id, 0, 0, 0)
                else:
                    leds.off()
                sleep(0.2)
        elif state == "off":
            if led_id is not None and 0 <= led_id < leds.num:
                leds.set(led_id, 0, 0, 0)
            else:
                leds.off()

        print(f"LED {led_id} -> {state}")
    except Exception as e:
        print(f"Erreur handle_led_command: {e}")

def on_message(msg):
    print("message reçu:", msg)
    try:
        received = Message.from_json(msg)

        # Traiter les messages SENSOR de type LED
        if received.message_type == MessageType.RECEPTION.SENSOR:
            if received.sensor_id == SensorId.LED:
                handle_led_command(received.value)
    except Exception as e:
        print(f"Erreur parsing message: {e}")

def on_close():
    print("WS closed")

ws = WSClient(
    "ws://192.168.4.230:9000",
    on_message=on_message,
    on_connect=on_connect,
    on_close=on_close
)

# Déclaration après connexion
declaration = Message(MessageType.DECLARATION, "", CLIENT_NAME)
ws.send(declaration.to_json())

def on_button_clicked(btn: Sensor):
    msg = Message.sensor(CLIENT_NAME, SensorId.BUTTON, btn.state.to_json(), "Sacha")
    ws.send(msg.to_json())

def on_joystick_change(joystick: Sensor, state):
    msg = Message.sensor(CLIENT_NAME, SensorId.JOYSTICK, state.to_json(), "Sacha")
    ws.send(msg.to_json())

def on_light_change(sensor: Sensor, state):
    msg = Message.sensor(CLIENT_NAME, SensorId.LIGHT, state.to_json(), "Sacha")
    ws.send(msg.to_json())

button = Button(ButtonWirings.default(), on_button_clicked)
joystick = Joystick(JoystickWirings.default(), on_joystick_change)
rfid = RFID(RFIDWirings.default())
leds = LedStrip(LedStripWirings(pinDin=13, numLeds=27))
light = LightSensor(LightSensorWirings(pinData=32), on_light_change)

# Test LED au démarrage
print("Test LED...")
leds.red()
sleep(0.3)
leds.green()
sleep(0.3)
leds.blue()
sleep(0.3)
leds.off()
print("Test LED OK")

def update_leds_from_light():
    state = light.state
    num_leds_on = int(state.percentage * leds.num / 100)
    for i in range(leds.num):
        if i < num_leds_on:
            leds.np[i] = (255, 0, 0)  # Rouge
        else:
            leds.np[i] = (0, 0, 0)
    leds.np.write()
    

o = Orchestrator() \
    .add_sensor(button) 
    #.add_sensor(joystick) \
    #.add_sensor(light)
    #.add_sensor(rfid) \

while True:
    ws.poll()
    # update_leds_from_light()  # Désactivé pour permettre le contrôle via @IA
    o.update(0.2)

