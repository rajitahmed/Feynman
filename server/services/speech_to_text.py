from typing import Protocol


class SpeechToText(Protocol):
    def transcribe(self, audio: bytes) -> str:
        """Turn the learner's recorded answer into text."""
        ...
