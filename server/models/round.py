from enum import StrEnum

from pydantic import BaseModel, Field

MIN_KEY_POINTS_PER_ROUND = 2
MAX_KEY_POINTS_PER_ROUND = 4


class RoundType(StrEnum):
    """The fixed arc every session follows, in this order."""

    WHAT = "what"
    HOW = "how"
    WHY = "why"
    EXAMPLE = "example"


class Round(BaseModel):
    round_type: RoundType
    kid_question: str
    key_points: list[str] = Field(
        min_length=MIN_KEY_POINTS_PER_ROUND, max_length=MAX_KEY_POINTS_PER_ROUND
    )
