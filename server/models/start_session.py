from typing import Annotated

from pydantic import BaseModel, StringConstraints


class StartSessionRequest(BaseModel):
    notes: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]


class StartSessionReply(BaseModel):
    kid_question: str
