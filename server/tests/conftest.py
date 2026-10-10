from pathlib import Path

import pytest


@pytest.fixture(autouse=True)
def redirect_saved_rubric(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    # Every session start saves its rubric; this keeps test runs off the team's real file.
    monkeypatch.setattr("planning.save_rubric.RUBRIC_FILE_PATH", tmp_path / "planned_rubric.json")
