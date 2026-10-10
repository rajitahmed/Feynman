import pytest
from pydantic import ValidationError

from models.rubric import Rubric
from services.canned_rubric import CANNED_RUBRIC


def test_rubric_rejects_rounds_out_of_fixed_order() -> None:
    reversed_rounds = list(reversed(CANNED_RUBRIC.rounds))

    with pytest.raises(ValidationError):
        Rubric(rounds=reversed_rounds)
