from typing import Protocol

from pydantic import BaseModel


class LanguageModel(Protocol):
    def generate[ReplyShape: BaseModel](
        self, prompt: str, reply_shape: type[ReplyShape]
    ) -> ReplyShape:
        """Answer the prompt with structured output parsed into reply_shape."""
        ...
