from typing import Annotated

from fastapi import APIRouter, Depends

from models.start_session import StartSessionReply, StartSessionRequest
from planning.plan_rounds import plan_rounds
from planning.save_rubric import save_rubric
from services.get_language_model import get_language_model
from services.get_text_to_speech import get_text_to_speech
from services.language_model import LanguageModel
from services.text_to_speech import TextToSpeech
from session.open_session import open_session

router = APIRouter()


@router.post("/session/start")
def start_session(
    request: StartSessionRequest,
    language_model: Annotated[LanguageModel, Depends(get_language_model)],
    text_to_speech: Annotated[TextToSpeech, Depends(get_text_to_speech)],
) -> StartSessionReply:
    rubric = plan_rounds(request.notes, language_model)
    save_rubric(rubric)
    return open_session(request.notes, rubric, text_to_speech)
