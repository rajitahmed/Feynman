from models.judgment import Judgment
from models.round import Round
from models.session import JudgedAnswer
from services.language_model import LanguageModel

JUDGING_INSTRUCTIONS = """You judge a learner's latest answer in a practice session where they
explain a topic to a curious kid. Read the whole round so far, not just the latest answer: a short
answer often replies to the kid's last question.

Judge like a curious kid, not an examiner. A key point counts as covered when its idea comes across
in the learner's own words, through an analogy, or with a different example than the notes use.
Exact wording, numbers and the notes' own example are never required.

Return:
- covered_key_points: the key points covered anywhere in this round so far, copied exactly from
  the list below.
- parroting: if the latest answer mirrors the notes word for word, the learner's phrase and the
  matching note line; otherwise null.
- decision: move_on if the round so far gets the main ideas across well enough for a kid to
  understand, even if a minor detail is missing. follow_up only if a key idea is missing or wrong.
- kid_reply_text: 1-2 short sentences from the kid. For follow_up, a confused question about one
  missing key point that the learner hasn't already answered. For move_on, "Oh, I get it!" plus a
  restatement in the learner's own words.

The kid never corrects, never teaches, never adds facts from the notes, and never says the answer
sounds like the notes.
"""


def judge_answer(
    notes: str,
    current_round: Round,
    earlier_answers: list[JudgedAnswer],
    answer_text: str,
    language_model: LanguageModel,
) -> Judgment:
    prompt = build_judging_prompt(notes, current_round, earlier_answers, answer_text)
    return language_model.generate(prompt, Judgment)


def build_judging_prompt(
    notes: str, current_round: Round, earlier_answers: list[JudgedAnswer], answer_text: str
) -> str:
    key_point_lines = [f"- {key_point}" for key_point in current_round.key_points]
    return (
        JUDGING_INSTRUCTIONS
        + "\nKey points:\n"
        + "\n".join(key_point_lines)
        + f"\n\nNotes:\n{notes}"
        + "\n\nThis round so far:\n"
        + describe_round_so_far(current_round, earlier_answers)
        + f"\nLearner (latest answer): {answer_text}"
    )


def describe_round_so_far(current_round: Round, earlier_answers: list[JudgedAnswer]) -> str:
    # A short follow-up answer like "in the stack" only makes sense next to the kid's question.
    lines = [f"Kid: {current_round.kid_question}"]
    for earlier_answer in earlier_answers:
        lines.append(f"Learner: {earlier_answer.answer_text}")
        lines.append(f"Kid: {earlier_answer.judgment.kid_reply_text}")
    return "\n".join(lines)
