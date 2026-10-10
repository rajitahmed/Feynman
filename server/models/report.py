from enum import StrEnum

from pydantic import BaseModel

from models.judgment import ParrotingMatch
from models.round import RoundType


class RoundStatus(StrEnum):
    COVERED = "covered"
    PARTLY_COVERED = "partly_covered"
    FUZZY = "fuzzy"


class KeyPointMark(BaseModel):
    key_point: str
    is_covered: bool


class RoundCard(BaseModel):
    round_number: int
    round_type: RoundType
    status: RoundStatus
    key_point_marks: list[KeyPointMark]


class RecapAnswer(BaseModel):
    answer_text: str
    covered_key_points: list[str]
    kid_reply_text: str


class RoundRecap(BaseModel):
    round_number: int
    kid_question: str
    answers: list[RecapAnswer]


class GapReport(BaseModel):
    """What the learner sees after round 4. Deliberately has no score."""

    round_cards: list[RoundCard]
    missed_key_points: list[str]
    parroting_flags: list[ParrotingMatch]
    re_explain_prompts: list[str]
    round_recaps: list[RoundRecap]


class ReExplainPrompts(BaseModel):
    """The language model's only job in the report: one retry question per gap."""

    prompts: list[str]
