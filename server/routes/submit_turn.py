from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from models.submit_turn import SubmitTurnReply, SubmitTurnRequest
from services.get_language_model import get_language_model
from services.get_speech_to_text import get_speech_to_text
from services.get_text_to_speech import get_text_to_speech
from services.language_model import LanguageModel
from services.speech_to_text import SpeechToText
from services.text_to_speech import TextToSpeech
from session.session_store import session_store
from session.take_turn import take_turn

router = APIRouter()


@router.post("/session/turn")
def submit_turn(
    request: SubmitTurnRequest,
    language_model: Annotated[LanguageModel, Depends(get_language_model)],
    speech_to_text: Annotated[SpeechToText, Depends(get_speech_to_text)],
    text_to_speech: Annotated[TextToSpeech, Depends(get_text_to_speech)],
) -> SubmitTurnReply:
    if session_store.current_session is None:
        raise HTTPException(status.HTTP_409_CONFLICT, "Start a session before answering")
    if session_store.current_session.is_finished:
        raise HTTPException(status.HTTP_409_CONFLICT, "This session is finished")
    answer_text = read_answer_text(request, speech_to_text)
    return take_turn(session_store.current_session, answer_text, language_model, text_to_speech)


def read_answer_text(request: SubmitTurnRequest, speech_to_text: SpeechToText) -> str:
    # A typed answer skips speech-to-text, so the fallback still works if the mic fails.
    if request.answer_text is not None:
        return request.answer_text
    # The request validator guarantees audio whenever text is missing.
    assert request.answer_audio_base64 is not None
    answer_text = speech_to_text.transcribe(request.answer_audio_base64).strip()
    # Silence transcribes to nothing; judging an empty answer would waste a turn.
    if answer_text == "":
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_CONTENT, "Didn't catch that, try again")
    return answer_text
