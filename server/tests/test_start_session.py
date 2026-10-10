import base64
import json
from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient
from pydantic import BaseModel

import planning.save_rubric as save_rubric_module
from main import app
from models.rubric import Rubric
from services.canned_rubric import CANNED_RUBRIC
from services.fake_language_model import FakeLanguageModel
from services.fake_text_to_speech import PLACEHOLDER_CLIP, FakeTextToSpeech
from services.get_language_model import get_language_model
from services.get_text_to_speech import get_text_to_speech
from services.language_model import InvalidReplyError

RECURSION_NOTES = "Recursion is when a function calls itself until it reaches a base case."

app.dependency_overrides[get_language_model] = lambda: FakeLanguageModel(
    canned_replies=[CANNED_RUBRIC]
)
# The test client skips startup, so there are no settings to pick the voice service from.
app.dependency_overrides[get_text_to_speech] = FakeTextToSpeech
client = TestClient(app)


def test_start_session_returns_the_first_round_question() -> None:
    response = client.post("/session/start", json={"notes": RECURSION_NOTES})

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "kid_question": CANNED_RUBRIC.rounds[0].kid_question,
        "round_count": len(CANNED_RUBRIC.rounds),
        "kid_audio_base64": base64.b64encode(PLACEHOLDER_CLIP).decode("ascii"),
    }


def test_start_session_speaks_the_first_round_question(monkeypatch: pytest.MonkeyPatch) -> None:
    fake_text_to_speech = FakeTextToSpeech()
    monkeypatch.setitem(app.dependency_overrides, get_text_to_speech, lambda: fake_text_to_speech)

    client.post("/session/start", json={"notes": RECURSION_NOTES})

    assert fake_text_to_speech.spoken_texts == [CANNED_RUBRIC.rounds[0].kid_question]


def test_start_session_saves_the_planned_rubric_to_a_file() -> None:
    client.post("/session/start", json={"notes": RECURSION_NOTES})

    # conftest.py points this at a temporary file for every test.
    rubric_file_path = save_rubric_module.RUBRIC_FILE_PATH
    saved_rubric = Rubric.model_validate(json.loads(rubric_file_path.read_text(encoding="utf-8")))
    assert saved_rubric == CANNED_RUBRIC


def test_start_session_rejects_blank_notes() -> None:
    response = client.post("/session/start", json={"notes": "   "})

    assert response.status_code == HTTPStatus.UNPROCESSABLE_CONTENT


class MisshapenLanguageModel:
    """Answers every prompt with a reply that doesn't fit the shape asked for."""

    def generate[ReplyShape: BaseModel](
        self, prompt: str, reply_shape: type[ReplyShape]
    ) -> ReplyShape:
        raise InvalidReplyError(f"Reply didn't fit {reply_shape.__name__}")


def test_start_session_reports_a_misshapen_plan_as_a_bad_gateway(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setitem(app.dependency_overrides, get_language_model, MisshapenLanguageModel)

    response = client.post("/session/start", json={"notes": RECURSION_NOTES})

    assert response.status_code == HTTPStatus.BAD_GATEWAY
    assert response.json() == {"detail": "Reply didn't fit Rubric"}
