import base64
import json
from http import HTTPStatus
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from main import app
from models.rubric import Rubric
from services.canned_rubric import CANNED_RUBRIC
from services.fake_language_model import FakeLanguageModel
from services.fake_text_to_speech import PLACEHOLDER_CLIP, FakeTextToSpeech
from services.get_language_model import get_language_model
from services.get_text_to_speech import get_text_to_speech

RECURSION_NOTES = "Recursion is when a function calls itself until it reaches a base case."

app.dependency_overrides[get_language_model] = lambda: FakeLanguageModel(
    canned_replies=[CANNED_RUBRIC]
)
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


def test_start_session_saves_the_planned_rubric_to_a_file(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # Keeps the team's real planned_rubric.json from being overwritten by test runs.
    rubric_file_path = tmp_path / "planned_rubric.json"
    monkeypatch.setattr("planning.save_rubric.RUBRIC_FILE_PATH", rubric_file_path)

    client.post("/session/start", json={"notes": RECURSION_NOTES})

    saved_rubric = Rubric.model_validate(json.loads(rubric_file_path.read_text(encoding="utf-8")))
    assert saved_rubric == CANNED_RUBRIC


def test_start_session_rejects_blank_notes() -> None:
    response = client.post("/session/start", json={"notes": "   "})

    assert response.status_code == HTTPStatus.UNPROCESSABLE_CONTENT
