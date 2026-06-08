import time
from typing import List, Callable, Optional

class VoiceActivityDetector:
    """Energy-based Voice Activity Detection (VAD) and barge-in detector."""
    def __init__(self, energy_threshold: float = 0.05, silence_duration_sec: float = 0.5):
        self.energy_threshold = energy_threshold
        self.silence_duration_sec = silence_duration_sec
        self.is_speaking = False
        self.last_speech_time = 0.0

    def process_frame(self, frame_energy: float) -> str:
        curr_time = time.time()
        if frame_energy > self.energy_threshold:
            self.last_speech_time = curr_time
            if not self.is_speaking:
                self.is_speaking = True
                return "SPEECH_START"
            return "SPEECH_CONTINUE"
        else:
            if self.is_speaking and (curr_time - self.last_speech_time) > self.silence_duration_sec:
                self.is_speaking = False
                return "SPEECH_END"
            return "SILENCE"
