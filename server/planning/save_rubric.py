from pathlib import Path

from models.rubric import Rubric

# Outside git (see .gitignore) so the team can open it and check the key points before the demo.
RUBRIC_FILE_PATH = Path(__file__).parent.parent / "planned_rubric.json"
JSON_INDENT = 2


def save_rubric(rubric: Rubric) -> None:
    rubric_json = rubric.model_dump_json(indent=JSON_INDENT)
    RUBRIC_FILE_PATH.write_text(rubric_json, encoding="utf-8")
    print(f"Planned rubric saved to {RUBRIC_FILE_PATH}:\n{rubric_json}")
