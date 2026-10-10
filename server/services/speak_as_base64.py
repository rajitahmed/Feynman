import base64

from services.text_to_speech import TextToSpeech


def speak_as_base64(text: str, text_to_speech: TextToSpeech) -> str:
    # JSON can't carry raw bytes, so the kid's audio travels as a base64 string.
    return base64.b64encode(text_to_speech.speak(text)).decode("ascii")
