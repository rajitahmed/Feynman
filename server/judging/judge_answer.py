from models.judgment import Judgment
from models.round import Round
from services.language_model import LanguageModel

JUDGING_INSTRUCTIONS = """You judge one answer in a practice session where a learner explains a
topic to a curious kid. Compare the answer with this round's key points and the learner's notes.

Return:
- covered_key_points: the key points the answer covered, copied exactly from the list below.
- parroting: if the answer mirrors the notes word for word, the learner's phrase and the matching
  note line; otherwise null.
- decision: move_on if every key point is covered, otherwise follow_up.
- kid_reply_text: 1-2 short sentences from the kid. For follow_up, a confused question about one
  missing key point. For move_on, "Oh, I get it!" plus a restatement in the learner's own words.

The kid never corrects, never teaches, never adds facts from the notes, and never says the answer
sounds like the notes.
"""


def judge_answer(
    notes: str, current_round: Round, answer_text: str, language_model: LanguageModel
) -> Judgment:
    prompt = build_judging_prompt(notes, current_round, answer_text)
    return language_model.generate(prompt, Judgment)


def build_judging_prompt(notes: str, current_round: Round, answer_text: str) -> str:
    key_point_lines = [f"- {key_point}" for key_point in current_round.key_points]
    return (
        JUDGING_INSTRUCTIONS
        + f"\nKid's question: {current_round.kid_question}"
        + "\nKey points:\n"
        + "\n".join(key_point_lines)
        + f"\n\nNotes:\n{notes}"
        + f"\n\nAnswer:\n{answer_text}"
    )
