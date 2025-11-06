import os
import json
import paho.mqtt.client as mqtt

MQTT_BROKER = os.getenv("MQTT_BROKER", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
MQTT_TOPIC = os.getenv("MQTT_TOPIC", "home/commands")

class MqttClient:
    def __init__(self):
        self.client = mqtt.Client()
        try:
            self.client.connect(MQTT_BROKER, MQTT_PORT, 60)
        except Exception:
            pass

    def publish_intent(self, intent: dict, text: str):
        payload = {"intent": intent, "text": text}
        try:
            self.client.publish(MQTT_TOPIC, json.dumps(payload))
        except Exception:
            pass
