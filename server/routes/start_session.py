from typing import Annotated

from fastapi import APIRouter, Depends

from models.session import Session
from models.start_session import StartSessionReply, StartSessionRequest
from planning.plan_rounds import plan_rounds
from planning.save_rubric import save_rubric
from services.get_language_model import get_language_model
from services.get_text_to_speech import get_text_to_speech
from services.language_model import LanguageModel
from services.speak_as_base64 import speak_as_base64
from services.text_to_speech import TextToSpeech
from session.session_store import session_store

router = APIRouter()


@router.post("/session/start")
def start_session(
    request: StartSessionRequest,
    language_model: Annotated[LanguageModel, Depends(get_language_model)],
    text_to_speech: Annotated[TextToSpeech, Depends(get_text_to_speech)],
) -> StartSessionReply:
    rubric = plan_rounds(request.notes, language_model)
    save_rubric(rubric)
    session_store.current_session = Session(notes=request.notes, rubric=rubric)
    first_kid_question = rubric.rounds[0].kid_question
    return StartSessionReply(
        kid_question=first_kid_question,
        round_count=len(rubric.rounds),
        kid_audio_base64=speak_as_base64(first_kid_question, text_to_speech),
    )
