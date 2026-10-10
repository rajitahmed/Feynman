from models.judgment import Decision, Judgment

# Always moves on, so a local run can click through every round without spending credits.
CANNED_JUDGMENT = Judgment(
    covered_key_points=[],
    parroting=None,
    decision=Decision.MOVE_ON,
    kid_reply_text="Oh, I get it!",
)
