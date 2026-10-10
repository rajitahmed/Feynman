from typing import Annotated

from fastapi import APIRouter, Depends

from models.start_session import StartSessionReply, StartSessionRequest
from planning.plan_rounds import plan_rounds
from planning.save_rubric import save_rubric
from services.get_language_model import get_language_model
from services.language_model import LanguageModel

router = APIRouter()


@router.post("/session/start")
def start_session(
    request: StartSessionRequest,
    language_model: Annotated[LanguageModel, Depends(get_language_model)],
) -> StartSessionReply:
    rubric = plan_rounds(request.notes, language_model)
    save_rubric(rubric)
    return StartSessionReply(kid_question=rubric.rounds[0].kid_question)
