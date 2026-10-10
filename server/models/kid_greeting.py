from pydantic import BaseModel


class KidGreeting(BaseModel):
    kid_greeting_text: str
