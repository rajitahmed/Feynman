from pydantic import BaseModel

from models.judgment import Judgment
from models.rubric import Rubric


class JudgedAnswer(BaseModel):
    round_number: int
    answer_text: str
    judgment: Judgment


class Session(BaseModel):
    notes: str
    rubric: Rubric
    current_round_number: int = 1
    follow_up_count: int = 0
    covered_key_points: list[str] = []
    judged_answers: list[JudgedAnswer] = []
