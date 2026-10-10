import base64
from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient

from main import app
from models.judgment import Decision, Judgment
from services.canned_rubric import CANNED_RUBRIC
from services.fake_language_model import FakeLanguageModel
from services.fake_speech_to_text import CANNED_TRANSCRIPT, FakeSpeechToText
from services.fake_text_to_speech import PLACEHOLDER_CLIP, FakeTextToSpeech
from services.get_language_model import get_language_model
from services.get_speech_to_text import get_speech_to_text
from services.get_text_to_speech import get_text_to_speech
from session.session_store import session_store
from session.take_turn import FINISHED_KID_LINE, FUZZY_KID_LINE, MAX_FOLLOW_UPS_PER_ROUND

# The test client skips startup, so there are no settings to pick the voice services from.
app.dependency_overrides[get_speech_to_text] = FakeSpeechToText
app.dependency_overrides[get_text_to_speech] = FakeTextToSpeech

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
FIRST_KEY_POINT = CANNED_RUBRIC.rounds[0].key_points[0]
PARTLY_COVERED_JUDGMENT = Judgment(
    covered_key_points=[FIRST_KEY_POINT],
    parroting=None,
    decision=Decision.FOLLOW_UP,
    kid_reply_text="Okay, but why does it use itself?",
)

PLACEHOLDER_CLIP_BASE64 = base64.b64encode(PLACEHOLDER_CLIP).decode("ascii")
RECORDED_AUDIO = b"pretend this is a recording"
RECORDED_AUDIO_BASE64 = base64.b64encode(RECORDED_AUDIO).decode("ascii")

client = TestClient(app)


def start_session_with_judgment(
    judgment: Judgment, monkeypatch: pytest.MonkeyPatch
) -> FakeLanguageModel:
    fake_language_model = FakeLanguageModel(canned_replies=[CANNED_RUBRIC, judgment])
    monkeypatch.setitem(app.dependency_overrides, get_language_model, lambda: fake_language_model)
    client.post("/session/start", json={"notes": RECURSION_NOTES})
    return fake_language_model


def test_moves_to_next_round_and_asks_its_question_when_judge_says_move_on(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    start_session_with_judgment(MOVE_ON_JUDGMENT, monkeypatch)

    response = client.post("/session/turn", json={"answer_text": ANSWER_TEXT})

    next_kid_question = CANNED_RUBRIC.rounds[1].kid_question
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "answer_text": ANSWER_TEXT,
        "kid_reply_text": f"{MOVE_ON_JUDGMENT.kid_reply_text} {next_kid_question}",
        "round_number": 2,
        "is_session_finished": False,
        "kid_mood": "got_it",
        "kid_audio_base64": PLACEHOLDER_CLIP_BASE64,
    }


def test_stays_on_round_and_counts_the_follow_up_when_judge_says_follow_up(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    start_session_with_judgment(FOLLOW_UP_JUDGMENT, monkeypatch)

    first_response = client.post("/session/turn", json={"answer_text": ANSWER_TEXT})

    assert first_response.json() == {
        "answer_text": ANSWER_TEXT,
        "kid_reply_text": FOLLOW_UP_JUDGMENT.kid_reply_text,
        "round_number": 1,
        "is_session_finished": False,
        "kid_mood": "confused",
        "kid_audio_base64": PLACEHOLDER_CLIP_BASE64,
    }
    assert session_store.current_session is not None
    assert session_store.current_session.follow_up_count == 1


def test_asks_only_one_follow_up_before_moving_on_fuzzy(monkeypatch: pytest.MonkeyPatch) -> None:
    start_session_with_judgment(FOLLOW_UP_JUDGMENT, monkeypatch)

    client.post("/session/turn", json={"answer_text": ANSWER_TEXT})
    second_response = client.post("/session/turn", json={"answer_text": ANSWER_TEXT})

    assert second_response.json()["round_number"] == 2
    assert second_response.json()["kid_reply_text"].startswith(FUZZY_KID_LINE)


def test_shows_the_judge_the_rounds_earlier_answers_and_follow_ups(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fake_language_model = start_session_with_judgment(FOLLOW_UP_JUDGMENT, monkeypatch)
    first_answer_text = "It's like hiring helpers for smaller jobs."

    client.post("/session/turn", json={"answer_text": first_answer_text})
    client.post("/session/turn", json={"answer_text": ANSWER_TEXT})

    second_judging_prompt = fake_language_model.received_prompts[-1]
    assert first_answer_text in second_judging_prompt
    assert FOLLOW_UP_JUDGMENT.kid_reply_text in second_judging_prompt


def test_marks_round_fuzzy_and_moves_on_when_follow_ups_pass_the_cap(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    start_session_with_judgment(FOLLOW_UP_JUDGMENT, monkeypatch)

    for _ in range(MAX_FOLLOW_UPS_PER_ROUND):
        client.post("/session/turn", json={"answer_text": ANSWER_TEXT})
    response = client.post("/session/turn", json={"answer_text": ANSWER_TEXT})

    next_kid_question = CANNED_RUBRIC.rounds[1].kid_question
    assert response.json() == {
        "answer_text": ANSWER_TEXT,
        "kid_reply_text": f"{FUZZY_KID_LINE} {next_kid_question}",
        "round_number": 2,
        "is_session_finished": False,
        "kid_mood": "confused",
        "kid_audio_base64": PLACEHOLDER_CLIP_BASE64,
    }
    assert session_store.current_session is not None
    assert session_store.current_session.fuzzy_round_numbers == [1]


def test_finishes_the_session_after_the_last_round(monkeypatch: pytest.MonkeyPatch) -> None:
    start_session_with_judgment(MOVE_ON_JUDGMENT, monkeypatch)

    for _ in range(len(CANNED_RUBRIC.rounds) - 1):
        client.post("/session/turn", json={"answer_text": ANSWER_TEXT})
    last_response = client.post("/session/turn", json={"answer_text": ANSWER_TEXT})
    late_response = client.post("/session/turn", json={"answer_text": ANSWER_TEXT})

    assert last_response.json() == {
        "answer_text": ANSWER_TEXT,
        "kid_reply_text": FINISHED_KID_LINE,
        "round_number": len(CANNED_RUBRIC.rounds),
        "is_session_finished": True,
        "kid_mood": "got_it",
        "kid_audio_base64": PLACEHOLDER_CLIP_BASE64,
    }
    assert late_response.status_code == HTTPStatus.CONFLICT


def test_thanks_the_learner_happily_when_the_last_round_ends_fuzzy(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    start_session_with_judgment(FOLLOW_UP_JUDGMENT, monkeypatch)
    answers_per_fuzzy_round = MAX_FOLLOW_UPS_PER_ROUND + 1

    for _ in range(answers_per_fuzzy_round * len(CANNED_RUBRIC.rounds) - 1):
        client.post("/session/turn", json={"answer_text": ANSWER_TEXT})
    last_response = client.post("/session/turn", json={"answer_text": ANSWER_TEXT})

    assert last_response.json()["is_session_finished"] is True
    assert last_response.json()["kid_reply_text"] == FINISHED_KID_LINE
    assert last_response.json()["kid_mood"] == "got_it"


def test_speaks_the_kid_reply_it_returns(monkeypatch: pytest.MonkeyPatch) -> None:
    start_session_with_judgment(FOLLOW_UP_JUDGMENT, monkeypatch)
    fake_text_to_speech = FakeTextToSpeech()
    monkeypatch.setitem(app.dependency_overrides, get_text_to_speech, lambda: fake_text_to_speech)

    client.post("/session/turn", json={"answer_text": ANSWER_TEXT})

    assert fake_text_to_speech.spoken_texts == [FOLLOW_UP_JUDGMENT.kid_reply_text]


def test_records_a_key_point_once_when_two_answers_cover_it(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    start_session_with_judgment(PARTLY_COVERED_JUDGMENT, monkeypatch)

    client.post("/session/turn", json={"answer_text": ANSWER_TEXT})
    client.post("/session/turn", json={"answer_text": ANSWER_TEXT})

    assert session_store.current_session is not None
    assert session_store.current_session.covered_key_points == [FIRST_KEY_POINT]


def test_rejects_a_turn_before_any_session_started(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(session_store, "current_session", None)
    # The route still resolves its language model before rejecting, so it needs a fake one.
    monkeypatch.setitem(
        app.dependency_overrides, get_language_model, lambda: FakeLanguageModel(canned_replies=[])
    )

    response = client.post("/session/turn", json={"answer_text": ANSWER_TEXT})

    assert response.status_code == HTTPStatus.CONFLICT


def test_rejects_a_blank_answer(monkeypatch: pytest.MonkeyPatch) -> None:
    start_session_with_judgment(MOVE_ON_JUDGMENT, monkeypatch)

    response = client.post("/session/turn", json={"answer_text": "   "})

    assert response.status_code == HTTPStatus.UNPROCESSABLE_CONTENT


class RefusingSpeechToText:
    """Fails the test if a typed answer ever reaches speech-to-text."""

    def transcribe(self, audio: bytes) -> str:
        raise AssertionError("A typed answer must skip speech-to-text")


def test_transcribes_a_recorded_answer_and_takes_the_turn_with_it(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    start_session_with_judgment(FOLLOW_UP_JUDGMENT, monkeypatch)
    fake_speech_to_text = FakeSpeechToText()
    monkeypatch.setitem(app.dependency_overrides, get_speech_to_text, lambda: fake_speech_to_text)

    response = client.post("/session/turn", json={"answer_audio_base64": RECORDED_AUDIO_BASE64})

    assert fake_speech_to_text.heard_audio == [RECORDED_AUDIO]
    assert response.json()["answer_text"] == CANNED_TRANSCRIPT
    assert session_store.current_session is not None
    assert session_store.current_session.judged_answers[0].answer_text == CANNED_TRANSCRIPT


def test_typed_answer_skips_speech_to_text_and_takes_the_same_turn(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    start_session_with_judgment(FOLLOW_UP_JUDGMENT, monkeypatch)
    monkeypatch.setitem(app.dependency_overrides, get_speech_to_text, RefusingSpeechToText)

    response = client.post("/session/turn", json={"answer_text": ANSWER_TEXT})

    assert response.status_code == HTTPStatus.OK
    assert response.json()["answer_text"] == ANSWER_TEXT


def test_rejects_a_recording_that_transcribes_to_nothing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    start_session_with_judgment(FOLLOW_UP_JUDGMENT, monkeypatch)
    silent_speech_to_text = FakeSpeechToText(canned_transcript="  ")
    monkeypatch.setitem(app.dependency_overrides, get_speech_to_text, lambda: silent_speech_to_text)

    response = client.post("/session/turn", json={"answer_audio_base64": RECORDED_AUDIO_BASE64})

    assert response.status_code == HTTPStatus.UNPROCESSABLE_CONTENT
    assert session_store.current_session is not None
    assert session_store.current_session.judged_answers == []


def test_rejects_a_turn_with_both_text_and_audio(monkeypatch: pytest.MonkeyPatch) -> None:
    start_session_with_judgment(MOVE_ON_JUDGMENT, monkeypatch)

    response = client.post(
        "/session/turn",
        json={"answer_text": ANSWER_TEXT, "answer_audio_base64": RECORDED_AUDIO_BASE64},
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_CONTENT
