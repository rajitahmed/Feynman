CANNED_TRANSCRIPT = "It's when a function calls itself on a smaller piece of the problem."


class FakeSpeechToText:
    """Stands in for ElevenLabs with a fixed transcript, so tests and local runs are free."""

    def __init__(self, canned_transcript: str = CANNED_TRANSCRIPT) -> None:
        self.canned_transcript = canned_transcript
        # Lets tests check which recording was sent without real audio.
        self.heard_audio: list[bytes] = []

    def transcribe(self, audio: bytes) -> str:
        self.heard_audio.append(audio)
        return self.canned_transcript
