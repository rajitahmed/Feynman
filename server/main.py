from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from config import Settings
from models.health_check import HealthCheck
from routes.start_session import router as start_session_router
from routes.submit_turn import router as submit_turn_router


@asynccontextmanager
async def load_settings_on_startup(app: FastAPI) -> AsyncIterator[None]:
    # Read at startup so a missing key fails before the demo, not mid-session.
    # Tests that don't start the app this way never need a real .env.
    app.state.settings = Settings()
    yield


app = FastAPI(title="Feynman", lifespan=load_settings_on_startup)
app.include_router(start_session_router)
app.include_router(submit_turn_router)


@app.get("/health")
def check_health() -> HealthCheck:
    return HealthCheck(status="ok")
