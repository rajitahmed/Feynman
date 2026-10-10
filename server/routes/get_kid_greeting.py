from fastapi import APIRouter

from models.kid_greeting import KidGreeting

# The server owns every kid line, so the greeting lives here and not in the client.
KID_GREETING_TEXT = "Hi! What are you teaching me today?"

router = APIRouter()


@router.get("/kid/greeting")
def get_kid_greeting() -> KidGreeting:
    return KidGreeting(kid_greeting_text=KID_GREETING_TEXT)
