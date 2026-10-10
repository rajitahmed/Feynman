from models.session import Session


class SessionStore:
    """Holds the live session in server memory. One session at a time is enough for the demo."""

    def __init__(self) -> None:
        self.current_session: Session | None = None


session_store = SessionStore()
