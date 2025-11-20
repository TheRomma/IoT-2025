from wifi import connect_wifi
from delay_server import DelayServer
from bmp import BMP280Reader

from machine import Pin, I2C
from time import ticks_ms, ticks_diff

SSID = "maksamakkara"
PASS = "joulupukki123"

wlan = connect_wifi(SSID, PASS)
print("Device IP:", wlan.ifconfig()[0])

i2c = I2C(0, sda=Pin(20), scl=Pin(21))
sensor = BMP280Reader(i2c, mode="sleep")

server = DelayServer(initial_delay=1.0)
server.start()
print("Web UI ready at: http://{}".format(wlan.ifconfig()[0]))

last = ticks_ms()

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
            )
        )
