from judging.judge_answer import judge_answer
from models.judgment import Decision, Judgment
from models.round import Round
from models.session import JudgedAnswer, Session
from models.submit_turn import SubmitTurnReply
from services.language_model import LanguageModel


def take_turn(session: Session, answer_text: str, language_model: LanguageModel) -> SubmitTurnReply:
    judgment = judge_answer(session.notes, find_current_round(session), answer_text, language_model)
    record_judged_answer(session, answer_text, judgment)
    kid_reply_text = judgment.kid_reply_text
    if judgment.decision == Decision.MOVE_ON:
        advance_round(session)
        # ponytail: past round 4 there is no next question; the finished flag comes in #5.
        if session.current_round_number <= len(session.rubric.rounds):
            kid_reply_text += f" {find_current_round(session).kid_question}"
    else:
        session.follow_up_count += 1
    return SubmitTurnReply(kid_reply_text=kid_reply_text, round_number=session.current_round_number)


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
