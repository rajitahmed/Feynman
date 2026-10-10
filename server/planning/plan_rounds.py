from models.round import MAX_KEY_POINTS_PER_ROUND, MIN_KEY_POINTS_PER_ROUND, ROUND_TYPE_GOALS
from models.rubric import Rubric
from services.language_model import LanguageModel

PLANNING_INSTRUCTIONS = f"""You plan a practice session where a learner explains a topic to a
curious kid. Read the learner's notes and plan one round per round type below, in this order.

For each round write:
- kid_question: a short, simple question a curious kid would ask to open the round.
- key_points: {MIN_KEY_POINTS_PER_ROUND} to {MAX_KEY_POINTS_PER_ROUND} short key points, taken
  only from the notes, that a good answer to this round must cover. Write each one as a general
  idea, never tied to the notes' own example or numbers, so a learner's different example counts.

Round types and what their key points check:
"""


def plan_rounds(notes: str, language_model: LanguageModel) -> Rubric:
    return language_model.generate(build_planning_prompt(notes), Rubric)


def build_planning_prompt(notes: str) -> str:
    round_type_lines = [f"- {round_type}: {goal}" for round_type, goal in ROUND_TYPE_GOALS.items()]
    return PLANNING_INSTRUCTIONS + "\n".join(round_type_lines) + f"\n\nNotes:\n{notes}"
