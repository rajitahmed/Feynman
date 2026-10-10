from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from config import Settings


@asynccontextmanager
async def load_settings_on_startup(app: FastAPI) -> AsyncIterator[None]:
    # Read at startup so a missing key fails before the demo, not mid-session.
    # Tests that don't start the app this way never need a real .env.
    app.state.settings = Settings()
    yield


app = FastAPI(title="Feynman", lifespan=load_settings_on_startup)


@app.get("/health")
def check_health() -> dict[str, str]:
    return {"status": "ok"}
