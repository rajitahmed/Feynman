from models.report import ReExplainPrompts

CANNED_RE_EXPLAIN_PROMPTS = ReExplainPrompts(
    prompts=[
        "How would you explain what stops a recursive function from calling itself forever?",
        "How would you explain why someone would pick recursion over a loop?",
    ]
)
