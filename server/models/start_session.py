from pydantic import BaseModel

from models.non_blank_text import NonBlankText


class StartSessionRequest(BaseModel):
    notes: NonBlankText


class StartSessionReply(BaseModel):
    kid_question: str
    round_count: int
    kid_audio_base64: str
