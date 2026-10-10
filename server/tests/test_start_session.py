import json
from http import HTTPStatus
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from main import app
from models.rubric import Rubric
from services.canned_rubric import CANNED_RUBRIC
from services.fake_language_model import FakeLanguageModel
from services.get_language_model import get_language_model

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
    }


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
