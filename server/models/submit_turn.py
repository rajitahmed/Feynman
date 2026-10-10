from enum import StrEnum
from typing import Annotated

from pydantic import BaseModel, StringConstraints


class SubmitTurnRequest(BaseModel):
    answer_text: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]


class KidMood(StrEnum):
    """How the kid reacts to an answer. Listening and thinking are client-only states."""

    CONFUSED = "confused"
    GOT_IT = "got_it"


class SubmitTurnReply(BaseModel):
    kid_reply_text: str
    round_number: int
    is_session_finished: bool
    kid_mood: KidMood
    kid_audio_base64: str
