import paho.mqtt.client as mqtt
import random
import time

# Create a client.
client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)

# Set credentials.
client.username_pw_set("mqttuser", "mqttpass");

# Connect to the broker.
client.connect(
	"127.0.0.1",
	1883,
	60
)

# Publish measurements.
while True:
	client.publish(
		"sensors/measurements",
		'{"sensor_id": "sensor_0", "location": "olohuone", ' + '"temperature": {}, "pressure": {}'.format(
			random.randrange(10.0, 20.0),
			random.randrange(0.0, 5.0)
		)+'}'
	)
	time.sleep(1.0)

# Disconnect client.
client.disconnect()
