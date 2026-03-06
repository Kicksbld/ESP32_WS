from joystick import *
from button import *
from ultrasonic import *
from accelerometer import *
from lightSensor import *
from rfid import *
from temperature import *
from sensor import *
from ochestrator import *
from wsclient import WSClient
from Message import Message, MessageType, SensorId
from time import sleep

CLIENT_NAME = "ESP_KILLIAN"

def on_connect():
    print("WS connected")

def on_message(msg):
    print("message reçu:", msg)

def on_close():
    print("WS closed")

ws = WSClient(
    "ws://192.168.10.38:9000",
    on_message=on_message,
    on_connect=on_connect,
    on_close=on_close
)

# Déclaration après connexion
declaration = Message(MessageType.DECLARATION, "", CLIENT_NAME)
ws.send(declaration.to_json())

# Déclaration des capteurs connectés
for sid in [SensorId.BUTTON, SensorId.RFID, SensorId.JOYSTICK]:
    ws.send(Message.declare_sensor(CLIENT_NAME, sid).to_json())

def on_button_clicked(btn: Sensor):
    msg = Message.sensor(CLIENT_NAME, SensorId.BUTTON, btn.state.to_json(), "MAC_KILLIAN")
    ws.send(msg.to_json())

# def on_ultrasonic_change(sensor: Sensor, state):
#     msg = Message.sensor(CLIENT_NAME, SensorId.ULTRASONIC, state.to_json(), "MAC_KILLIAN")
#     ws.send(msg.to_json())

# def on_accelerometer_change(sensor: Sensor, state):
#     msg = Message.sensor(CLIENT_NAME, SensorId.ACCELEROMETER, state.to_json(), "MAC_KILLIAN")
#     ws.send(msg.to_json())

# def on_light_change(sensor: Sensor, state):
#     msg = Message.sensor(CLIENT_NAME, SensorId.LIGHT, state.to_json(), "MAC_KILLIAN")
#     ws.send(msg.to_json())

def on_rfid_change(sensor: Sensor, state):
    msg = Message.sensor(CLIENT_NAME, SensorId.RFID, state.to_json(), "MAC_KILLIAN")
    ws.send(msg.to_json())

def on_joystick_change(sensor: Sensor, state):
    msg = Message.sensor(CLIENT_NAME, SensorId.JOYSTICK, state.to_json(), "MAC_KILLIAN")
    ws.send(msg.to_json())

# def on_temperature_change(sensor: Sensor, state):
#     msg = Message.sensor(CLIENT_NAME, SensorId.TEMPERATURE, state.to_json(), "MAC_KILLIAN")
#     ws.send(msg.to_json())


joystick = Joystick(JoystickWirings.default(), on_change=on_joystick_change)
button = Button(ButtonWirings.default(), on_button_clicked)
ultrasonic = Ultrasonic(UltrasonicWirings.default())
# accelerometer = Accelerometer(AccelerometerWirings.default())
light_sensor = LightSensor(LightSensorWirings.default())
rfid = RFID(RFIDWirings.default(), on_rfid_change)
temperature = Temperature(TemperatureWirings.default())

o = Orchestrator(verbose=True) \
    .add_sensor(button) \
    .add_sensor(rfid) \
    .add_sensor(joystick)
while True:
    ws.poll()
    o.update(0.2)

