from judging.judge_answer import judge_answer
from models.judgment import Decision, Judgment
from models.round import Round
from models.session import JudgedAnswer, Session
from models.submit_turn import KidMood, SubmitTurnReply
from services.language_model import LanguageModel
from services.speak_as_base64 import speak_as_base64
from services.text_to_speech import TextToSpeech

# The server enforces the cap, not the language model, so the learner can never get stuck.
MAX_FOLLOW_UPS_PER_ROUND = 2
FUZZY_KID_LINE = "I'm still a bit fuzzy on that, but let's try the next part!"
# A fuzzy round still follows a follow-up decision, so the kid stays confused there too.
KID_MOOD_BY_DECISION = {Decision.FOLLOW_UP: KidMood.CONFUSED, Decision.MOVE_ON: KidMood.GOT_IT}


def take_turn(
    session: Session,
    answer_text: str,
    language_model: LanguageModel,
    text_to_speech: TextToSpeech,
) -> SubmitTurnReply:
    judgment = judge_answer(session.notes, find_current_round(session), answer_text, language_model)
    record_judged_answer(session, answer_text, judgment)
    kid_mood = KID_MOOD_BY_DECISION[judgment.decision]
    kid_reply_text = judgment.kid_reply_text
    if judgment.decision == Decision.FOLLOW_UP:
        if session.follow_up_count < MAX_FOLLOW_UPS_PER_ROUND:
            session.follow_up_count += 1
            return build_reply(session, kid_reply_text, kid_mood, text_to_speech)
        session.fuzzy_round_numbers.append(session.current_round_number)
        kid_reply_text = FUZZY_KID_LINE
    if session.current_round_number == len(session.rubric.rounds):
        session.is_finished = True
    else:
        advance_round(session)
        kid_reply_text += f" {find_current_round(session).kid_question}"
    return build_reply(session, kid_reply_text, kid_mood, text_to_speech)


def build_reply(
    session: Session, kid_reply_text: str, kid_mood: KidMood, text_to_speech: TextToSpeech
) -> SubmitTurnReply:
    return SubmitTurnReply(
        kid_reply_text=kid_reply_text,
        round_number=session.current_round_number,
        is_session_finished=session.is_finished,
        kid_mood=kid_mood,
        kid_audio_base64=speak_as_base64(kid_reply_text, text_to_speech),
    )


def find_current_round(session: Session) -> Round:
    # Round numbers start at 1 for people; list positions start at 0.
    return session.rubric.rounds[session.current_round_number - 1]


def record_judged_answer(session: Session, answer_text: str, judgment: Judgment) -> None:
    session.judged_answers.append(
        JudgedAnswer(
            round_number=session.current_round_number,
            answer_text=answer_text,
            judgment=judgment,
        )
    )
    # A follow-up answer often repeats a point the learner already made; count it once.
    for key_point in judgment.covered_key_points:
        if key_point not in session.covered_key_points:
            session.covered_key_points.append(key_point)


def advance_round(session: Session) -> None:
    session.current_round_number += 1
    # The follow-up cap counts per round, so a new round starts from zero.
    session.follow_up_count = 0
