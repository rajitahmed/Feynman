import httpx
from pydantic import BaseModel

SPEECH_TO_TEXT_URL = "https://api.elevenlabs.io/v1/speech-to-text"
SPEECH_TO_TEXT_MODEL_NAME = "scribe_v1"
# ElevenLabs reads the format from the audio itself; the name only labels the upload.
RECORDING_FILE_NAME = "answer.webm"
REQUEST_TIMEOUT_SECONDS = 30
API_KEY_HEADER = "xi-api-key"


class ElevenLabsTranscript(BaseModel):
    """The one field we use from ElevenLabs' transcription reply."""

    text: str


class ElevenLabsSpeechToText:
    """The real SpeechToText. The only file that knows ElevenLabs speech-to-text exists."""

    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

    def transcribe(self, audio: bytes) -> str:
        response = httpx.post(
            SPEECH_TO_TEXT_URL,
            headers={API_KEY_HEADER: self.api_key},
            data={"model_id": SPEECH_TO_TEXT_MODEL_NAME},
            files={"file": (RECORDING_FILE_NAME, audio)},
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        return ElevenLabsTranscript.model_validate_json(response.content).text
