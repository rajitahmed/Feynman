from models.report import GapReport, ReExplainPrompts, RoundCard, RoundStatus
from models.round import Round
from models.session import Session
from services.language_model import LanguageModel

MAX_BULLETS_PER_CARD = 2
# A fuzzy round can have every key point ticked yet still need practice.
NO_MISSED_POINTS_TEXT = "nothing specific"

RE_EXPLAIN_INSTRUCTIONS = """A learner just explained a topic to a curious kid. Below are the rounds
where their explanation had gaps. Write exactly one short "try re-explaining this" prompt per round.

Each prompt is a question the learner could answer out loud to practice, for example "How would
you explain why recursion needs a place to stop?". Never include the answer or any fact from the
missed points; only point at what to explain again.
"""


def build_gap_report(session: Session, language_model: LanguageModel) -> GapReport:
    round_cards = [
        build_round_card(session, round_number, planned_round)
        for round_number, planned_round in enumerate(session.rubric.rounds, start=1)
    ]
    return GapReport(
        round_cards=round_cards,
        missed_key_points=[
            key_point
            for planned_round in session.rubric.rounds
            for key_point in find_missed_key_points(session, planned_round)
        ],
        parroting_flags=[
            judged_answer.judgment.parroting
            for judged_answer in session.judged_answers
            if judged_answer.judgment.parroting is not None
        ],
        re_explain_prompts=write_re_explain_prompts(session, round_cards, language_model),
    )


def build_round_card(session: Session, round_number: int, planned_round: Round) -> RoundCard:
    covered_key_points = [
        key_point
        for key_point in planned_round.key_points
        if key_point in session.covered_key_points
    ]
    return RoundCard(
        round_number=round_number,
        round_type=planned_round.round_type,
        status=find_round_status(session, round_number, planned_round),
        bullets=covered_key_points[:MAX_BULLETS_PER_CARD],
    )


def find_round_status(session: Session, round_number: int, planned_round: Round) -> RoundStatus:
    if round_number in session.fuzzy_round_numbers:
        return RoundStatus.FUZZY
    if find_missed_key_points(session, planned_round):
        return RoundStatus.PARTLY_COVERED
    return RoundStatus.COVERED


def find_missed_key_points(session: Session, planned_round: Round) -> list[str]:
    return [
        key_point
        for key_point in planned_round.key_points
        if key_point not in session.covered_key_points
    ]


def write_re_explain_prompts(
    session: Session, round_cards: list[RoundCard], language_model: LanguageModel
) -> list[str]:
    gap_lines = [
        describe_gap_round(session, session.rubric.rounds[round_card.round_number - 1])
        for round_card in round_cards
        if round_card.status != RoundStatus.COVERED
    ]
    # No gaps means nothing to practice, so skip the language model call entirely.
    if not gap_lines:
        return []
    prompt = RE_EXPLAIN_INSTRUCTIONS + "\nRounds with gaps:\n" + "\n".join(gap_lines)
    return language_model.generate(prompt, ReExplainPrompts).prompts


def describe_gap_round(session: Session, gap_round: Round) -> str:
    missed_key_points = find_missed_key_points(session, gap_round)
    missed_text = "; ".join(missed_key_points) if missed_key_points else NO_MISSED_POINTS_TEXT
    return (
        f"- {gap_round.round_type} round, kid asked: {gap_round.kid_question} Missed: {missed_text}"
    )
