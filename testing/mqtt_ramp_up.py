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
count = 1
while True:
	for i in range(count):
		client.publish(
			"sensors/measurements",
			'{"sensor_id": "sensor_'+str(i)+'", "location": "room_'+str(i)+'", ' + '"temperature": {}, "pressure": {}, "ts_sent": {}'.format(
				random.randrange(10.0, 30.0),
				random.randrange(1000.0, 1050.0),
				time.time() * 1000
			)+'}'
		)

	count += 1
	time.sleep(1.0)

# Disconnect client.
client.disconnect()
