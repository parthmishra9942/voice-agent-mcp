from typing import Optional
from voice_mcp.audio_stream import VoiceActivityDetector

class BargeInInterruptionManager:
    """Manages audio output cancellation when user starts speaking mid-response."""
    def __init__(self, vad: VoiceActivityDetector):
        self.vad = vad
        self.is_agent_speaking = False
        self.interrupted = False

    def on_agent_playback_start(self):
        self.is_agent_speaking = True
        self.interrupted = False

    def on_audio_frame(self, frame_energy: float) -> bool:
        """Returns True if agent playback must be immediately cancelled."""
        status = self.vad.process_frame(frame_energy)
        if self.is_agent_speaking and status == "SPEECH_START":
            self.interrupted = True
            self.is_agent_speaking = False
            return True # Cancel playback immediately
        return False
