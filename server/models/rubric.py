from pydantic import BaseModel, field_validator

from models.round import Round, RoundType

ROUND_TYPES_IN_ORDER = list(RoundType)


class Rubric(BaseModel):
    """The hidden checklist planned from the notes. Never shown during the session."""

    rounds: list[Round]

    @field_validator("rounds")
    @classmethod
    def check_rounds_follow_fixed_order(cls, rounds: list[Round]) -> list[Round]:
        planned_round_types = [planned_round.round_type for planned_round in rounds]
        if planned_round_types != ROUND_TYPES_IN_ORDER:
            raise ValueError(f"Rounds must be exactly {ROUND_TYPES_IN_ORDER} in that order")
        return rounds
