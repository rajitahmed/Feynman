import httpx

TEXT_TO_SPEECH_URL = "https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
# MP3 matches the audio/mpeg label the client plays the kid's reply with.
OUTPUT_FORMAT = "mp3_44100_128"
REQUEST_TIMEOUT_SECONDS = 30
API_KEY_HEADER = "xi-api-key"


class ElevenLabsTextToSpeech:
    """The real TextToSpeech. The only file that knows ElevenLabs text-to-speech exists."""

    def __init__(self, api_key: str, kid_voice_id: str, model_name: str) -> None:
        self.api_key = api_key
        # One fixed voice and model, so the kid sounds like the same character all session.
        self.kid_voice_id = kid_voice_id
        self.model_name = model_name

    def speak(self, text: str) -> bytes:
        response = httpx.post(
            TEXT_TO_SPEECH_URL.format(voice_id=self.kid_voice_id),
            headers={API_KEY_HEADER: self.api_key},
            params={"output_format": OUTPUT_FORMAT},
            json={"text": text, "model_id": self.model_name},
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        return response.content
