from models.round import Round, RoundType
from models.rubric import Rubric

CANNED_RUBRIC = Rubric(
    rounds=[
        Round(
            round_type=RoundType.WHAT,
            kid_question="What is recursion?",
            key_points=[
                "A function that calls itself",
                "It solves a problem by solving smaller versions of the same problem",
            ],
        ),
        Round(
            round_type=RoundType.HOW,
            kid_question="How is that different from a loop?",
            key_points=[
                "Each call works on a smaller input",
                "A base case stops the calls",
                "Results are combined as the calls return",
            ],
        ),
        Round(
            round_type=RoundType.WHY,
            kid_question="Why would anyone use it?",
            key_points=[
                "Some problems are naturally made of smaller copies of themselves",
                "It can make code shorter and clearer than a loop",
            ],
        ),
        Round(
            round_type=RoundType.EXAMPLE,
            kid_question="Can you give me an example?",
            key_points=[
                "A concrete case such as factorial or walking a folder tree",
                "The example names its base case",
            ],
        ),
    ]
)
