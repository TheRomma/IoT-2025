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
	for i in range(10):
		client.publish(
			"sensors/measurements",
			'{"sensor_id": "sensor_'+str(i+1)+'", "location": "room_'+str(i+1)+'", ' + '"temperature": {}, "pressure": {}'.format(
				random.randrange(70.0, 90.0),
				random.randrange(0.0, 5.0),
			)+'}'
		)

	time.sleep(1.0)

# Disconnect client.
client.disconnect()
