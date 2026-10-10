from fastapi import Request

from config import Settings
from services.elevenlabs_speech_to_text import ElevenLabsSpeechToText
from services.fake_speech_to_text import FakeSpeechToText
from services.speech_to_text import SpeechToText


def get_speech_to_text(request: Request) -> SpeechToText:
    return pick_speech_to_text(request.app.state.settings)


def pick_speech_to_text(settings: Settings) -> SpeechToText:
    # Fake unless switched on, so a forgotten setting never spends credits.
    if settings.should_use_real_elevenlabs:
        return ElevenLabsSpeechToText(settings.elevenlabs_api_key)
    return FakeSpeechToText()
