from enum import StrEnum

from pydantic import BaseModel


class Decision(StrEnum):
    MOVE_ON = "move_on"
    FOLLOW_UP = "follow_up"


class ParrotingMatch(BaseModel):
    """An answer that mirrored the notes: the learner's words next to the note line they match."""

    user_phrase: str
    note_line: str


class Judgment(BaseModel):
    """The judge's structured verdict on one answer."""

    covered_key_points: list[str]
    # None when the answer was in the learner's own words.
    parroting: ParrotingMatch | None
    decision: Decision
    kid_reply_text: str
