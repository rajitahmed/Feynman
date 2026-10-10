import io
import wave

# ponytail: WAV, though the client labels audio mpeg for ElevenLabs (#12); Chrome sniffs it.
PLACEHOLDER_CLIP_SECONDS = 1
SAMPLE_RATE_HERTZ = 8000
BYTES_PER_SAMPLE = 2
MONO_CHANNEL_COUNT = 1


def build_silent_clip() -> bytes:
    buffer = io.BytesIO()
    with wave.open(buffer, "wb") as clip:
        clip.setnchannels(MONO_CHANNEL_COUNT)
        clip.setsampwidth(BYTES_PER_SAMPLE)
        clip.setframerate(SAMPLE_RATE_HERTZ)
        # Zeroed samples are silence.
        clip.writeframes(bytes(PLACEHOLDER_CLIP_SECONDS * SAMPLE_RATE_HERTZ * BYTES_PER_SAMPLE))
    return buffer.getvalue()


PLACEHOLDER_CLIP = build_silent_clip()


class FakeTextToSpeech:
    """Stands in for ElevenLabs with silence, so tests and local runs spend no credits."""

    def __init__(self) -> None:
        # Lets tests check what the kid said without real audio.
        self.spoken_texts: list[str] = []

    def speak(self, text: str) -> bytes:
        self.spoken_texts.append(text)
        return PLACEHOLDER_CLIP
