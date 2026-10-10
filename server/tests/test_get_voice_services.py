from config import Settings
from services.elevenlabs_speech_to_text import ElevenLabsSpeechToText
from services.elevenlabs_text_to_speech import ElevenLabsTextToSpeech
from services.fake_speech_to_text import FakeSpeechToText
from services.fake_text_to_speech import FakeTextToSpeech
from services.get_speech_to_text import pick_speech_to_text
from services.get_text_to_speech import pick_text_to_speech

PLACEHOLDER_KEY = "not-a-real-key"


def test_uses_the_fake_voice_services_by_default() -> None:
    # Skips server/.env so the test doesn't depend on the team's local switch.
    settings = Settings(
        _env_file=None, gemini_api_key=PLACEHOLDER_KEY, elevenlabs_api_key=PLACEHOLDER_KEY
    )

    assert isinstance(pick_text_to_speech(settings), FakeTextToSpeech)
    assert isinstance(pick_speech_to_text(settings), FakeSpeechToText)


def test_uses_elevenlabs_only_when_explicitly_switched_on() -> None:
    settings = Settings(
        _env_file=None,
        gemini_api_key=PLACEHOLDER_KEY,
        elevenlabs_api_key=PLACEHOLDER_KEY,
        should_use_real_elevenlabs=True,
    )

    assert isinstance(pick_text_to_speech(settings), ElevenLabsTextToSpeech)
    assert isinstance(pick_speech_to_text(settings), ElevenLabsSpeechToText)
