import os
import json
import time
from influxdb_client import InfluxDBClient
import paho.mqtt.client as mqtt

# Environment variables
INFLUX_URL = os.getenv("INFLUX_URL", "http://influxdb:8086")
INFLUX_TOKEN = os.getenv("INFLUX_TOKEN", "your-token")
INFLUX_ORG = os.getenv("INFLUX_ORG", "your-org")
INFLUX_BUCKET = os.getenv("INFLUX_BUCKET", "your-bucket")

MQTT_HOST = os.getenv("MQTT_HOST", "mosquitto")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
MQTT_TOPIC = os.getenv("MQTT_TOPIC", "control/temperature")

INTERVAL = int(os.getenv("INTERVAL", 60))

time.sleep(4)

# Initialize InfluxDB client
client = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG)
query_api = client.query_api()

def get_average_temperature():
    query = f'''
    from(bucket: "{INFLUX_BUCKET}")
      |> range(start: -10s)
      |> filter(fn: (r) => r._field == "temperature")
      |> group(columns: [])
      |> mean()
    '''
    tables = query_api.query(query)
    for table in tables:
        for record in table.records:
            return record.get_value()

    return None

def send_control_message(avg_temp):
    if avg_temp != None:
        control_value = 1 if avg_temp and avg_temp > 30 else 0
        payload = json.dumps({"control": control_value})
        mqtt_client = mqtt.Client()
        mqtt_client.username_pw_set('mqttuser', 'mqttpass')
        mqtt_client.connect(MQTT_HOST, MQTT_PORT, 60)
        mqtt_client.publish(MQTT_TOPIC, payload)
        mqtt_client.disconnect()
        print(f"Sent MQTT message: {payload}")

# Run every minute
while True:
    avg_temp = get_average_temperature()
    print(f"Average temperature: {avg_temp}")
    send_control_message(avg_temp)
    time.sleep(INTERVAL)
