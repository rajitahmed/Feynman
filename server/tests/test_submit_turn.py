from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient

from main import app
from models.judgment import Decision, Judgment
from services.canned_rubric import CANNED_RUBRIC
from services.fake_language_model import FakeLanguageModel
from services.get_language_model import get_language_model
from session.session_store import session_store

RECURSION_NOTES = "Recursion is when a function calls itself until it reaches a base case."
ANSWER_TEXT = "It's when a function uses itself to solve a smaller piece of the problem."

MOVE_ON_JUDGMENT = Judgment(
    covered_key_points=CANNED_RUBRIC.rounds[0].key_points,
    parroting=None,
    decision=Decision.MOVE_ON,
    kid_reply_text="Oh, I get it! It uses itself on a smaller piece.",
)
FOLLOW_UP_JUDGMENT = Judgment(
    covered_key_points=[],
    parroting=None,
    decision=Decision.FOLLOW_UP,
    kid_reply_text="Wait, what does it mean for a function to use itself?",
)

client = TestClient(app)


def start_session_with_judgment(judgment: Judgment, monkeypatch: pytest.MonkeyPatch) -> None:
    fake_language_model = FakeLanguageModel(canned_replies=[CANNED_RUBRIC, judgment])
    monkeypatch.setitem(app.dependency_overrides, get_language_model, lambda: fake_language_model)
    client.post("/session/start", json={"notes": RECURSION_NOTES})


def test_moves_to_next_round_and_asks_its_question_when_judge_says_move_on(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    start_session_with_judgment(MOVE_ON_JUDGMENT, monkeypatch)

    response = client.post("/session/turn", json={"answer_text": ANSWER_TEXT})

    next_kid_question = CANNED_RUBRIC.rounds[1].kid_question
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "kid_reply_text": f"{MOVE_ON_JUDGMENT.kid_reply_text} {next_kid_question}",
        "round_number": 2,
    }


def test_stays_on_round_and_counts_the_follow_up_when_judge_says_follow_up(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    start_session_with_judgment(FOLLOW_UP_JUDGMENT, monkeypatch)

    first_response = client.post("/session/turn", json={"answer_text": ANSWER_TEXT})
    second_response = client.post("/session/turn", json={"answer_text": ANSWER_TEXT})

    assert first_response.json() == {
        "kid_reply_text": FOLLOW_UP_JUDGMENT.kid_reply_text,
        "round_number": 1,
    }
    assert second_response.json()["round_number"] == 1
    assert session_store.current_session is not None
    assert session_store.current_session.follow_up_count == 2


def test_rejects_a_turn_before_any_session_started(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(session_store, "current_session", None)

    response = client.post("/session/turn", json={"answer_text": ANSWER_TEXT})

    assert response.status_code == HTTPStatus.CONFLICT


def test_rejects_a_blank_answer(monkeypatch: pytest.MonkeyPatch) -> None:
    start_session_with_judgment(MOVE_ON_JUDGMENT, monkeypatch)

    response = client.post("/session/turn", json={"answer_text": "   "})

    assert response.status_code == HTTPStatus.UNPROCESSABLE_CONTENT
