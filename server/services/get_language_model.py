from fastapi import Request

from config import Settings
from services.canned_judgment import CANNED_JUDGMENT
from services.canned_re_explain_prompts import CANNED_RE_EXPLAIN_PROMPTS
from services.canned_rubric import CANNED_RUBRIC
from services.fake_language_model import FakeLanguageModel
from services.gemini_language_model import GeminiLanguageModel
from services.language_model import LanguageModel


def get_language_model(request: Request) -> LanguageModel:
    return pick_language_model(request.app.state.settings)


def pick_language_model(settings: Settings) -> LanguageModel:
    # Fake unless switched on, so a forgotten setting never spends credits.
    if settings.should_use_real_gemini:
        return GeminiLanguageModel(settings.gemini_api_key)
    return FakeLanguageModel(
        canned_replies=[CANNED_RUBRIC, CANNED_JUDGMENT, CANNED_RE_EXPLAIN_PROMPTS]
    )
