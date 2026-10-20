# enroll_voice.py
import sounddevice as sd
import numpy as np
from voice_authenticator import VoiceAuthenticator

DURATION = 5  # seconds
SAMPLE_RATE = 16000

def record_voice(duration=5, sr=16000):
    print(f"🎙️ Recording for {duration} seconds...")
    audio = sd.rec(int(duration * sr), samplerate=sr, channels=1, dtype=np.int16)
    sd.wait()
    print("✅ Recording finished.")
    return audio.tobytes()

if __name__ == "__main__":
    audio_data = record_voice(DURATION, SAMPLE_RATE)
    va = VoiceAuthenticator()
    success = va.enroll(audio_data)
    if success:
        print("✅ Voice enrolled successfully.")
    else:
        print("❌ Voice enrollment failed.")
