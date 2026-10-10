from google import genai
from google.genai import types
from pydantic import BaseModel, ValidationError

from services.language_model import InvalidReplyError

GEMINI_MODEL_NAME = "gemini-3.8-flash"
JSON_MIME_TYPE = "application/json"


class GeminiLanguageModel:
    """The real LanguageModel. The only file that knows Gemini exists."""

    def __init__(self, api_key: str) -> None:
        self.client = genai.Client(api_key=api_key)

    def generate[ReplyShape: BaseModel](
        self, prompt: str, reply_shape: type[ReplyShape]
    ) -> ReplyShape:
        # Passing the Pydantic model as the schema makes Gemini answer in exactly that JSON shape.
        response = self.client.models.generate_content(
            model=GEMINI_MODEL_NAME,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type=JSON_MIME_TYPE, response_schema=reply_shape
            ),
        )
        # A blocked or empty reply has no text; saying so beats a confusing JSON parse error.
        if response.text is None:
            raise InvalidReplyError(f"Gemini returned no {reply_shape.__name__}")
        # Validated by hand, because the SDK's own parsing hides why a reply was rejected.
        try:
            return reply_shape.model_validate_json(response.text)
        except ValidationError as error:
            raise InvalidReplyError(
                f"Gemini's reply didn't fit {reply_shape.__name__}: {error}"
            ) from error
