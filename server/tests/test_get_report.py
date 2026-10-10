from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient

from main import app
from models.judgment import Decision, Judgment, ParrotingMatch
from models.session import JudgedAnswer, Session
from services.canned_re_explain_prompts import CANNED_RE_EXPLAIN_PROMPTS
from services.canned_rubric import CANNED_RUBRIC
from services.fake_language_model import FakeLanguageModel
from services.get_language_model import get_language_model
from session.session_store import session_store

RECURSION_NOTES = "A function that calls itself until it reaches a base case."
EVERY_KEY_POINT = [
    key_point for planned_round in CANNED_RUBRIC.rounds for key_point in planned_round.key_points
]
WHAT_ROUND, HOW_ROUND, WHY_ROUND, EXAMPLE_ROUND = CANNED_RUBRIC.rounds
# Round 1 fully, round 2 partly, round 3 not at all (it went fuzzy), round 4 fully.
COVERED_KEY_POINTS = WHAT_ROUND.key_points + HOW_ROUND.key_points[:1] + EXAMPLE_ROUND.key_points
FUZZY_ROUND_NUMBER = 3
PARROTING = ParrotingMatch(
    user_phrase="a function that calls itself until it reaches a base case",
    note_line=RECURSION_NOTES,
)
PARROTED_ANSWER = JudgedAnswer(
    round_number=1,
    answer_text="It's a function that calls itself until it reaches a base case.",
    judgment=Judgment(
        covered_key_points=WHAT_ROUND.key_points,
        parroting=PARROTING,
        decision=Decision.MOVE_ON,
        kid_reply_text="Oh, I get it!",
    ),
)

client = TestClient(app)


def finish_session(
    covered_key_points: list[str],
    fuzzy_round_numbers: list[int],
    monkeypatch: pytest.MonkeyPatch,
) -> FakeLanguageModel:
    finished_session = Session(
        notes=RECURSION_NOTES,
        rubric=CANNED_RUBRIC,
        current_round_number=len(CANNED_RUBRIC.rounds),
        is_finished=True,
        covered_key_points=covered_key_points,
        judged_answers=[PARROTED_ANSWER],
        fuzzy_round_numbers=fuzzy_round_numbers,
    )
    monkeypatch.setattr(session_store, "current_session", finished_session)
    fake_language_model = FakeLanguageModel(canned_replies=[CANNED_RE_EXPLAIN_PROMPTS])
    monkeypatch.setitem(app.dependency_overrides, get_language_model, lambda: fake_language_model)
    return fake_language_model


def test_missed_points_are_the_rubric_points_that_were_never_covered(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    finish_session(COVERED_KEY_POINTS, [FUZZY_ROUND_NUMBER], monkeypatch)

    response = client.get("/session/report")

    assert response.status_code == HTTPStatus.OK
    assert response.json()["missed_key_points"] == [
        key_point for key_point in EVERY_KEY_POINT if key_point not in COVERED_KEY_POINTS
    ]


def test_each_round_card_shows_covered_partly_covered_or_fuzzy(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    finish_session(COVERED_KEY_POINTS, [FUZZY_ROUND_NUMBER], monkeypatch)

    round_cards = client.get("/session/report").json()["round_cards"]

    assert [round_card["status"] for round_card in round_cards] == [
        "covered",
        "partly_covered",
        "fuzzy",
        "covered",
    ]
    assert round_cards[1]["bullets"] == HOW_ROUND.key_points[:1]


def test_a_parroted_answer_shows_the_phrase_next_to_the_note_line(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    finish_session(COVERED_KEY_POINTS, [FUZZY_ROUND_NUMBER], monkeypatch)

    response = client.get("/session/report")

    assert response.json()["parroting_flags"] == [PARROTING.model_dump()]


def test_a_fuzzy_round_gets_a_re_explain_prompt(monkeypatch: pytest.MonkeyPatch) -> None:
    fake_language_model = finish_session(COVERED_KEY_POINTS, [FUZZY_ROUND_NUMBER], monkeypatch)

    response = client.get("/session/report")

    assert response.json()["re_explain_prompts"] == CANNED_RE_EXPLAIN_PROMPTS.prompts
    [re_explain_request] = fake_language_model.received_prompts
    assert WHY_ROUND.kid_question in re_explain_request


def test_asks_for_no_re_explain_prompts_when_nothing_was_missed(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fake_language_model = finish_session(EVERY_KEY_POINT, [], monkeypatch)

    response = client.get("/session/report")

    assert response.json()["re_explain_prompts"] == []
    assert response.json()["missed_key_points"] == []
    assert fake_language_model.received_prompts == []


def test_the_report_has_no_score(monkeypatch: pytest.MonkeyPatch) -> None:
    finish_session(COVERED_KEY_POINTS, [FUZZY_ROUND_NUMBER], monkeypatch)

    report = client.get("/session/report").json()

    assert not any("score" in field_name for field_name in report)


def test_rejects_a_report_before_the_session_is_finished(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    finish_session(COVERED_KEY_POINTS, [], monkeypatch)
    assert session_store.current_session is not None
    monkeypatch.setattr(session_store.current_session, "is_finished", False)

    response = client.get("/session/report")

    assert response.status_code == HTTPStatus.CONFLICT
