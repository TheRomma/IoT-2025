import ujson
from umqtt.simple import MQTTClient

class MQTTSender:
    def __init__(self, server, user=None, password=None,
                 topic="sensors/measurements", client_id="pico_client"):

        self.topic = topic

        self.client = MQTTClient(
            client_id=client_id,
            server=server,
            user=user,
            password=password,
            port=1883,
            keepalive=60
        )

        self.connected = False

    def connect(self):
        """Connect to the MQTT broker."""
        try:
            self.client.connect()
            self.connected = True
            print("MQTT connected!")
        except Exception as e:
            print("MQTT connection failed:", e)

    def subscribe(self, topic):
	self.client.subscribe(topic)

    def set_callback(self, callback):
	self.client.set_callback(callback)

    def check_control(self):
	self.client.check_msg()

    def publish(self, sensor_id, location, temperature, pressure):
        """Publish a JSON message."""
        if not self.connected:
            self.connect()

        payload = ujson.dumps({
            "sensor_id": sensor_id,
            "location": location,
            "temperature": round(temperature, 2),
            "pressure": round(pressure, 2)
        })

        try:
            self.client.publish(self.topic, payload)
            print("MQTT published:", payload)
        except Exception as e:
            print("MQTT publish failed:", e)

    def disconnect(self):
        try:
            self.client.disconnect()
        except:
            pass
