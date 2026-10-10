from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_FILE_PATH = Path(__file__).parent / ".env"


class Settings(BaseSettings):
    """Settings read from server/.env. The keys stay on the server and never reach the browser."""

    model_config = SettingsConfigDict(env_file=ENV_FILE_PATH)

    gemini_api_key: str
    elevenlabs_api_key: str
    # Off by default so tests and local runs never spend Gemini credits.
    should_use_real_gemini: bool = False
    # Off by default so tests and local runs never spend ElevenLabs credits.
    should_use_real_elevenlabs: bool = False
    # Pasted in rather than looked up, so the key needs no Voices or Models permission.
    elevenlabs_kid_voice_id: str = "wtQQHWfMy9WeIYuth5ga"
    elevenlabs_text_to_speech_model_name: str = "eleven_flash_v2_5"
