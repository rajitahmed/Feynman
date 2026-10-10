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
