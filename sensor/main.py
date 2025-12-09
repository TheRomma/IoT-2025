from wifi import connect_wifi
from delay_server import DelayServer
from sensor_reader import BMP280Reader
from mqtt_sender import MQTTSender

from machine import Pin, I2C
from time import ticks_ms, ticks_diff
import json

SSID = "TW-EAV510AC_2.4G_3E80"
PASS = "84b602b976c59b56"

MQTT_SERVER = "192.168.0.100"
MQTT_USER = "mqttuser"
MQTT_PASS = "mqttpass"
MQTT_TOPIC = "sensors/measurements"

CLIENT_ID = "sensor_0"
LOCATION = "olohuone"

LED = machine.Pin('LED', machine.Pin.OUT)

def control_callback(topic, msg):
	print('Received: ', msg)
	data = json.loads(msg)
	control_val = data.get('control', 0)
	if control_val == 1:
		LED.value(1)
	else:
		LED.value(0)

mqtt = MQTTSender(
    server=MQTT_SERVER,
    user=MQTT_USER,
    password=MQTT_PASS,
    topic=MQTT_TOPIC,
    client_id=CLIENT_ID
)

wlan = connect_wifi(SSID, PASS)
print("Device IP:", wlan.ifconfig()[0])

i2c = I2C(0, sda=Pin(20), scl=Pin(21))
sensor = BMP280Reader(i2c, mode="sleep")

server = DelayServer(initial_delay=1.0)
server.start()
print("Web UI ready at: http://{}".format(wlan.ifconfig()[0]))

last = ticks_ms()

# Start MQTT connection
mqtt.connect()

while True:

    server.poll()

    now = ticks_ms()
    interval = int(server.get_delay() * 1000)

    if ticks_diff(now, last) >= interval:
        last = now

        t, p = sensor.measure_once()
        print("Temp: {:.2f} C  Pressure: {:.2f} hPa   Delay: {}".format(
            t, p, server.get_delay()
        ))

        mqtt.publish(
            sensor_id=CLIENT_ID,
            location=LOCATION,
            temperature=t,
            pressure=p
        )
