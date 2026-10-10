from planning.load_demo_rubric import load_demo_rubric

# The fake planner hands back the hand-checked demo rubric, so the recursion rubric lives in
# one place (demo_rubric.json) and local runs rehearse the real demo rounds.
CANNED_RUBRIC = load_demo_rubric()
