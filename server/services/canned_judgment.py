from models.judgment import Decision, Judgment
from services.canned_rubric import CANNED_RUBRIC

# Claims every key point and always moves on, so a local run reaches a gap-free report
# without spending credits.
CANNED_JUDGMENT = Judgment(
    covered_key_points=[
        key_point
        for planned_round in CANNED_RUBRIC.rounds
        for key_point in planned_round.key_points
    ],
    parroting=None,
    decision=Decision.MOVE_ON,
    kid_reply_text="Oh, I get it!",
)
