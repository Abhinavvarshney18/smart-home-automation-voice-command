from fastapi import FastAPI
from pydantic import BaseModel
import os

from .intent_classifier import IntentClassifier
from .mqtt_client import MqttClient

app = FastAPI(title="AbhiRaj Backend: Intent + MQTT")
classifier = IntentClassifier()
mqtt = MqttClient()

class PredictRequest(BaseModel):
    text: str

class PredictResponse(BaseModel):
    text: str
    intent: dict

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    text = req.text or ""
    result = classifier.predict(text)
    # publish mapped command
    topic = os.getenv("MQTT_TOPIC", "home/commands")
    payload = {"intent": result["intent"], "text": text}
    mqtt.publish_device(topic, payload)
    return {"text": text, "intent": result}
