from typing import Annotated

from pydantic import BaseModel, StringConstraints


class SubmitTurnRequest(BaseModel):
    answer_text: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]


class SubmitTurnReply(BaseModel):
    kid_reply_text: str
    round_number: int
