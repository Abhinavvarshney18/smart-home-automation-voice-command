import os
import wave
import json

VOSK_AVAILABLE = False
try:
    from vosk import Model, KaldiRecognizer
    VOSK_AVAILABLE = True
except Exception:
    VOSK_AVAILABLE = False

VOSK_MODEL_PATH = os.getenv("VOSK_MODEL_PATH", "/models/vosk-model-small-en-us-0.15")

def load_vosk_model():
    if not VOSK_AVAILABLE:
        return None
    if not os.path.isdir(VOSK_MODEL_PATH):
        return None
    return Model(VOSK_MODEL_PATH)

_vosk_model = load_vosk_model()

def transcribe_wav(wav_path: str) -> str:
    """Transcribe a PCM WAV file (uses Vosk if available)."""
    if _vosk_model is None:
        return "transcription_unavailable: Vosk model not found"
    wf = wave.open(wav_path, "rb")
    rec = KaldiRecognizer(_vosk_model, wf.getframerate())
    rec.SetWords(False)
    parts = []
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            parts.append(json.loads(rec.Result()).get("text",""))
    parts.append(json.loads(rec.FinalResult()).get("text",""))
    text = " ".join(filter(None, parts)).strip()
    return text or ""
