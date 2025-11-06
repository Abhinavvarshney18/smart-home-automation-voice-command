from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
import tempfile
import os

from .utils import write_bytes_to_file, ensure_wav_16k_mono
from .stt import transcribe_wav, VOSK_AVAILABLE, VOSK_MODEL_PATH
from .nlu import NLUEvaluator
from .mqtt_client import MqttClient

app = FastAPI(title="Prithvi NLU Service")
nlu = NLUEvaluator()
mqtt = MqttClient()

class TextReq(BaseModel):
    text: str

class IntentResp(BaseModel):
    text: str
    intent: dict

@app.get("/health")
def health():
    return {"status":"ok", "vosk_available": VOSK_AVAILABLE, "vosk_model_path": VOSK_MODEL_PATH}

@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(400, "No file provided")
    tmp_in = tempfile.mktemp(suffix=os.path.splitext(file.filename)[1] or ".wav")
    data = await file.read()
    write_bytes_to_file(data, tmp_in)
    tmp_wav = tempfile.mktemp(suffix=".wav")
    try:
        ensure_wav_16k_mono(tmp_in, tmp_wav)
        text = transcribe_wav(tmp_wav)
    finally:
        for p in (tmp_in, tmp_wav):
            try:
                os.remove(p)
            except Exception:
                pass
    return {"text": text}

@app.post("/intent", response_model=IntentResp)
def intent(req: TextReq):
    text = req.text or ""
    res = nlu.predict(text)
    mqtt.publish_intent(res, text)
    return {"text": text, "intent": res}

@app.post("/intent_audio", response_model=IntentResp)
async def intent_audio(file: UploadFile = File(...)):
    tmp_in = tempfile.mktemp(suffix=os.path.splitext(file.filename)[1] or ".wav")
    data = await file.read()
    write_bytes_to_file(data, tmp_in)
    tmp_wav = tempfile.mktemp(suffix=".wav")
    try:
        ensure_wav_16k_mono(tmp_in, tmp_wav)
        text = transcribe_wav(tmp_wav)
    finally:
        for p in (tmp_in, tmp_wav):
            try:
                os.remove(p)
            except Exception:
                pass
    res = nlu.predict(text)
    mqtt.publish_intent(res, text)
    return {"text": text, "intent": res}
