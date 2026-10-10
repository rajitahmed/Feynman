from pathlib import Path

from models.rubric import Rubric

# Checked into git: the hand-checked recursion rubric the demo falls back on if planning fails.
DEMO_RUBRIC_FILE_PATH = Path(__file__).parent.parent / "demo_rubric.json"


def load_demo_rubric() -> Rubric:
    return Rubric.model_validate_json(DEMO_RUBRIC_FILE_PATH.read_text(encoding="utf-8"))
