from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient

from main import app
from models.session import Session
from planning.load_demo_rubric import load_demo_rubric
from services.fake_text_to_speech import FakeTextToSpeech
from services.get_text_to_speech import get_text_to_speech
from session.session_store import session_store

RECURSION_NOTES = "Recursion is when a function calls itself until it reaches a base case."

client = TestClient(app)


def test_start_demo_session_opens_a_session_from_the_demo_rubric(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # Faked explicitly so this test stays free once the real ElevenLabs adapter lands.
    monkeypatch.setitem(app.dependency_overrides, get_text_to_speech, FakeTextToSpeech)
    demo_rubric = load_demo_rubric()

    response = client.post("/session/start-demo", json={"notes": RECURSION_NOTES})

    assert response.status_code == HTTPStatus.OK
    assert response.json()["kid_question"] == demo_rubric.rounds[0].kid_question
    assert response.json()["round_count"] == len(demo_rubric.rounds)
    assert session_store.current_session is not None
    assert session_store.current_session.rubric == demo_rubric


def test_starting_again_replaces_the_finished_session_so_its_report_is_gone(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setitem(app.dependency_overrides, get_text_to_speech, FakeTextToSpeech)
    finished_session = Session(notes=RECURSION_NOTES, rubric=load_demo_rubric(), is_finished=True)
    monkeypatch.setattr(session_store, "current_session", finished_session)

    start_response = client.post("/session/start-demo", json={"notes": RECURSION_NOTES})
    report_response = client.get("/session/report")

    assert start_response.status_code == HTTPStatus.OK
    assert report_response.status_code == HTTPStatus.CONFLICT
