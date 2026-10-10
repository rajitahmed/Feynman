from typing import Annotated

from fastapi import APIRouter, Depends

from models.session import Session
from models.start_session import StartSessionReply, StartSessionRequest
from planning.plan_rounds import plan_rounds
from planning.save_rubric import save_rubric
from services.get_language_model import get_language_model
from services.language_model import LanguageModel
from session.session_store import session_store

router = APIRouter()


@router.post("/session/start")
def start_session(
    request: StartSessionRequest,
    language_model: Annotated[LanguageModel, Depends(get_language_model)],
) -> StartSessionReply:
    rubric = plan_rounds(request.notes, language_model)
    save_rubric(rubric)
    session_store.current_session = Session(notes=request.notes, rubric=rubric)
    return StartSessionReply(
        kid_question=rubric.rounds[0].kid_question, round_count=len(rubric.rounds)
    )
