from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_FILE_PATH = Path(__file__).parent / ".env"


class Settings(BaseSettings):
    """API keys read from server/.env. They stay on the server and never reach the browser."""

    model_config = SettingsConfigDict(env_file=ENV_FILE_PATH)

    gemini_api_key: str
    elevenlabs_api_key: str
