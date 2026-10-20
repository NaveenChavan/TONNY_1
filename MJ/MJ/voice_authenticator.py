import numpy as np
import librosa
import os
from scipy.spatial.distance import cosine
import logging

logger = logging.getLogger(__name__)

class VoiceAuthenticator:
    def __init__(self, enroll_path: str = "enrolled_user/voice_mfcc.npy", sr: int = 16000):
        self.enroll_path = enroll_path
        self.sr = sr

    def _extract_mfcc_from_bytes(self, audio_bytes: bytes) -> np.ndarray | None:
        try:
            y = np.frombuffer(audio_bytes, dtype=np.int16).astype(np.float32) / 32768.0
            mfcc = librosa.feature.mfcc(y=y, sr=self.sr, n_mfcc=13)
            return np.mean(mfcc, axis=1)
        except Exception as e:
            logger.error(f"MFCC extraction failed: {e}")
            return None

    def enroll(self, audio_bytes: bytes) -> bool:
        mfcc = self._extract_mfcc_from_bytes(audio_bytes)
        if mfcc is not None:
            os.makedirs(os.path.dirname(self.enroll_path), exist_ok=True)
            np.save(self.enroll_path, mfcc)
            logger.info("✅ Voice enrolled successfully.")
            return True
        logger.warning("❌ Voice enrollment failed.")
        return False

    def authenticate(self, audio_bytes: bytes, threshold: float = 0.4) -> bool:
        mfcc_input = self._extract_mfcc_from_bytes(audio_bytes)
        if mfcc_input is None:
            return False

        if not os.path.exists(self.enroll_path):
            logger.warning("⚠️ No enrolled voice found.")
            return False

        mfcc_enrolled = np.load(self.enroll_path)
        similarity = 1 - cosine(mfcc_enrolled, mfcc_input)
        logger.info(f"🔍 Voice similarity score: {similarity:.2f}")
        return similarity >= (1 - threshold)
