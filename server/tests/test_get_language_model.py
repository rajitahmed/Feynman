from config import Settings
from services.fake_language_model import FakeLanguageModel
from services.gemini_language_model import GeminiLanguageModel
from services.get_language_model import pick_language_model

PLACEHOLDER_KEY = "not-a-real-key"


def test_uses_the_fake_language_model_by_default() -> None:
    # Skips server/.env so the test doesn't depend on the team's local switch.
    settings = Settings(
        _env_file=None, gemini_api_key=PLACEHOLDER_KEY, elevenlabs_api_key=PLACEHOLDER_KEY
    )

    assert isinstance(pick_language_model(settings), FakeLanguageModel)


def test_uses_gemini_only_when_explicitly_switched_on() -> None:
    settings = Settings(
        _env_file=None,
        gemini_api_key=PLACEHOLDER_KEY,
        elevenlabs_api_key=PLACEHOLDER_KEY,
        should_use_real_gemini=True,
    )

    assert isinstance(pick_language_model(settings), GeminiLanguageModel)
