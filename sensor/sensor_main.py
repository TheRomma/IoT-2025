from wifi import connect_wifi
from delay_server import DelayServer
from sensor_reader import BMP280Reader
from mqtt_sender import MQTTSender

from machine import Pin, I2C
from time import ticks_ms, ticks_diff

SSID = ""
PASS = ""

MQTT_SERVER = "127.0.0.1"
MQTT_USER = "mqttuser"
MQTT_PASS = "mqttpass"
MQTT_TOPIC = "sensors/measurements"

mqtt = MQTTSender(
    server=MQTT_SERVER,
    user=MQTT_USER,
    password=MQTT_PASS,
    topic=MQTT_TOPIC,
    client_id="pico_0"
)

wlan = connect_wifi(SSID, PASS)
print("Device IP:", wlan.ifconfig()[0])

i2c = I2C(0, sda=Pin(20), scl=Pin(21))
sensor = BMP280Reader(i2c, mode="sleep")

server = DelayServer(initial_delay=1.0)
server.start()
print("Web UI ready at: http://{}".format(wlan.ifconfig()[0]))

last = ticks_ms()

mqtt.connect()

while True:
    server.poll()

    now = ticks_ms()
    interval = int(server.get_delay() * 1000)

    if ticks_diff(now, last) >= interval:
        last = now

        t, p = sensor.measure_once()
        print(
            "Temp: {:.2f} C  Pressure: {:.2f} hPa   Delay: {}".format(
                t, p, server.get_delay()
            ))

        mqtt.publish(
            sensor_id="sensor_pico_0",
            location="olohuone",
            temperature=t,
            pressure=p
        )