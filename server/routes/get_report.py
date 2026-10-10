from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from models.report import GapReport
from report.build_gap_report import build_gap_report
from services.get_language_model import get_language_model
from services.language_model import LanguageModel
from session.session_store import session_store

router = APIRouter()


@router.get("/session/report")
def get_report(
    language_model: Annotated[LanguageModel, Depends(get_language_model)],
) -> GapReport:
    if session_store.current_session is None or not session_store.current_session.is_finished:
        raise HTTPException(status.HTTP_409_CONFLICT, "Finish the session before the report")
    return build_gap_report(session_store.current_session, language_model)
