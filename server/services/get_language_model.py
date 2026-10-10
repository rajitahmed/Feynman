from services.canned_judgment import CANNED_JUDGMENT
from services.canned_re_explain_prompts import CANNED_RE_EXPLAIN_PROMPTS
from services.canned_rubric import CANNED_RUBRIC
from services.fake_language_model import FakeLanguageModel
from services.language_model import LanguageModel


def get_language_model() -> LanguageModel:
    # ponytail: the fake until the real Gemini adapter lands (#11), so local runs are free.
    return FakeLanguageModel(
        canned_replies=[CANNED_RUBRIC, CANNED_JUDGMENT, CANNED_RE_EXPLAIN_PROMPTS]
    )
