from models.rubric import Rubric
from models.session import Session
from models.start_session import StartSessionReply
from services.speak_as_base64 import speak_as_base64
from services.text_to_speech import TextToSpeech
from session.session_store import session_store


def open_session(notes: str, rubric: Rubric, text_to_speech: TextToSpeech) -> StartSessionReply:
    session_store.current_session = Session(notes=notes, rubric=rubric)
    first_kid_question = rubric.rounds[0].kid_question
    return StartSessionReply(
        kid_question=first_kid_question,
        round_count=len(rubric.rounds),
        kid_audio_base64=speak_as_base64(first_kid_question, text_to_speech),
    )
