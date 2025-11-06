import os
import json
import paho.mqtt.client as mqtt

MQTT_BROKER = os.getenv("MQTT_BROKER", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))

class MqttClient:
    def __init__(self):
        self.client = mqtt.Client()
        try:
            self.client.connect(MQTT_BROKER, MQTT_PORT, 60)
        except Exception:
            # broker may not be available at container build time
            pass

    def publish_device(self, topic: str, payload: dict):
        try:
            self.client.publish(topic, json.dumps(payload))
        except Exception:
            # best-effort publish; ignore errors for now
            pass
