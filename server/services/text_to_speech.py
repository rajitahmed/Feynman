from typing import Protocol


class TextToSpeech(Protocol):
    def speak(self, text: str) -> bytes:
        """Turn the text into audio the browser can play."""
        ...
