from fastapi import Request

from config import Settings
from services.elevenlabs_text_to_speech import ElevenLabsTextToSpeech
from services.fake_text_to_speech import FakeTextToSpeech
from services.text_to_speech import TextToSpeech


def get_text_to_speech(request: Request) -> TextToSpeech:
    return pick_text_to_speech(request.app.state.settings)


def pick_text_to_speech(settings: Settings) -> TextToSpeech:
    # Fake unless switched on, so a forgotten setting never spends credits.
    if settings.should_use_real_elevenlabs:
        return ElevenLabsTextToSpeech(
            api_key=settings.elevenlabs_api_key,
            kid_voice_id=settings.elevenlabs_kid_voice_id,
            model_name=settings.elevenlabs_text_to_speech_model_name,
        )
    return FakeTextToSpeech()
