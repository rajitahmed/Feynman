from pydantic import BaseModel


class FakeLanguageModel:
    """Stands in for Gemini with canned replies, so tests and local runs spend no credits."""

    def __init__(self, canned_replies: list[BaseModel]) -> None:
        self.canned_replies = canned_replies
        # Lets tests check what was asked without a real model.
        self.received_prompts: list[str] = []

    def generate[ReplyShape: BaseModel](
        self, prompt: str, reply_shape: type[ReplyShape]
    ) -> ReplyShape:
        self.received_prompts.append(prompt)
        for canned_reply in self.canned_replies:
            if isinstance(canned_reply, reply_shape):
                return canned_reply
        raise LookupError(f"No canned reply of shape {reply_shape.__name__}")
