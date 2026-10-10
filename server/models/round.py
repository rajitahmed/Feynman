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


# What each round's key points should check. Adding a round type means adding an entry here.
ROUND_TYPE_GOALS: dict[RoundType, str] = {
    RoundType.WHAT: "a plain definition of the topic",
    RoundType.HOW: "how it works, step by step, or how it relates to something familiar",
    RoundType.WHY: "what it is for and why it matters",
    RoundType.EXAMPLE: "one concrete example of it in action",
}


class Round(BaseModel):
    round_type: RoundType
    kid_question: str
    key_points: list[str] = Field(
        min_length=MIN_KEY_POINTS_PER_ROUND, max_length=MAX_KEY_POINTS_PER_ROUND
    )
