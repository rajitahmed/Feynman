from services.fake_text_to_speech import FakeTextToSpeech
from services.text_to_speech import TextToSpeech


def get_text_to_speech() -> TextToSpeech:
    # ponytail: the fake until the real ElevenLabs adapter lands (#12), so local runs are free.
    return FakeTextToSpeech()
