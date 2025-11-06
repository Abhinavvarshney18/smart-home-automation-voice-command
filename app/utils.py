import os
from pydub import AudioSegment

def ensure_wav_16k_mono(src_path: str, dst_path: str):
    """Convert src audio to WAV PCM 16k mono and write to dst_path."""
    audio = AudioSegment.from_file(src_path)
    audio = audio.set_frame_rate(16000).set_channels(1).set_sample_width(2)
    audio.export(dst_path, format="wav")
    return dst_path

def write_bytes_to_file(b: bytes, path: str):
    with open(path, "wb") as f:
        f.write(b)
    return path
