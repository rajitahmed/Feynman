from http import HTTPStatus

from fastapi.testclient import TestClient

from main import app
from routes.get_kid_greeting import KID_GREETING_TEXT

client = TestClient(app)


def test_greeting_is_the_kid_line_the_server_owns() -> None:
    response = client.get("/kid/greeting")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"kid_greeting_text": KID_GREETING_TEXT}
