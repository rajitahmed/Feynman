from enum import StrEnum
from typing import Annotated, Self

from pydantic import Base64Bytes, BaseModel, StringConstraints, model_validator

NonBlankText = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]


class SubmitTurnRequest(BaseModel):
    """One answer: typed text, or a recording the server transcribes. Never both."""

    answer_text: NonBlankText | None = None
    answer_audio_base64: Base64Bytes | None = None

    @model_validator(mode="after")
    def check_exactly_one_answer(self) -> Self:
        if (self.answer_text is None) == (self.answer_audio_base64 is None):
            raise ValueError("Send either answer_text or answer_audio_base64")
        return self


class KidMood(StrEnum):
    """How the kid reacts to an answer. Listening and thinking are client-only states."""

    CONFUSED = "confused"
    GOT_IT = "got_it"


class SubmitTurnReply(BaseModel):
    # What the app heard, so the learner can check a spoken answer was transcribed right.
    answer_text: str
    kid_reply_text: str
    round_number: int
    is_session_finished: bool
    kid_mood: KidMood
    kid_audio_base64: str
