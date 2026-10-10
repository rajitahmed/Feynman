from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient

from main import app
from planning.load_demo_rubric import load_demo_rubric
from services.fake_language_model import FakeLanguageModel
from services.get_language_model import get_language_model
from session.session_store import session_store

RECURSION_NOTES = "Recursion is when a function calls itself until it reaches a base case."

client = TestClient(app)


def test_start_demo_session_uses_the_demo_rubric_without_calling_the_planner(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # No canned replies: any planner call would raise, proving the demo skips it.
    fake_language_model = FakeLanguageModel(canned_replies=[])
    monkeypatch.setitem(app.dependency_overrides, get_language_model, lambda: fake_language_model)
    demo_rubric = load_demo_rubric()

    response = client.post("/session/start-demo", json={"notes": RECURSION_NOTES})

    assert response.status_code == HTTPStatus.OK
    assert response.json()["kid_question"] == demo_rubric.rounds[0].kid_question
    assert response.json()["round_count"] == len(demo_rubric.rounds)
    assert session_store.current_session is not None
    assert session_store.current_session.rubric == demo_rubric
    assert fake_language_model.received_prompts == []
