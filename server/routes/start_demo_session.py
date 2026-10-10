from typing import Annotated

from fastapi import APIRouter, Depends

from models.start_session import StartSessionReply, StartSessionRequest
from planning.load_demo_rubric import load_demo_rubric
from services.get_text_to_speech import get_text_to_speech
from services.text_to_speech import TextToSpeech
from session.open_session import open_session

router = APIRouter()


# Skips the planner, so the demo survives a failed planning call and rehearsals spend no credits.
@router.post("/session/start-demo")
def start_demo_session(
    request: StartSessionRequest,
    text_to_speech: Annotated[TextToSpeech, Depends(get_text_to_speech)],
) -> StartSessionReply:
    return open_session(request.notes, load_demo_rubric(), text_to_speech)
