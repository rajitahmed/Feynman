from pydantic import BaseModel, Field

from models.round import Round, RoundType

ROUND_COUNT = len(RoundType)


class Rubric(BaseModel):
    """The hidden checklist planned from the notes. Never shown during the session."""

    rounds: list[Round] = Field(min_length=ROUND_COUNT, max_length=ROUND_COUNT)
