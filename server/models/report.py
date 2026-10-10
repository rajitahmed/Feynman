from enum import StrEnum

from pydantic import BaseModel

from models.judgment import ParrotingMatch
from models.round import RoundType


class RoundStatus(StrEnum):
    COVERED = "covered"
    PARTLY_COVERED = "partly_covered"
    FUZZY = "fuzzy"


class RoundCard(BaseModel):
    round_number: int
    round_type: RoundType
    status: RoundStatus
    bullets: list[str]


class GapReport(BaseModel):
    """What the learner sees after round 4. Deliberately has no score."""

    round_cards: list[RoundCard]
    missed_key_points: list[str]
    parroting_flags: list[ParrotingMatch]
    re_explain_prompts: list[str]
