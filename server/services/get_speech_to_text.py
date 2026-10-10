from services.fake_speech_to_text import FakeSpeechToText
from services.speech_to_text import SpeechToText


def get_speech_to_text() -> SpeechToText:
    # ponytail: the fake until the real ElevenLabs adapter lands (#12), so local runs are free.
    return FakeSpeechToText()
