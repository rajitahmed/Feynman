import type { RoundCard as RoundCardData } from "../api/types.ts";
import StatusPill from "./StatusPill.tsx";
import "./RoundCard.css";

type RoundCardProps = {
  roundCard: RoundCardData;
};

function RoundCard({ roundCard }: RoundCardProps) {
  const coveredCount = roundCard.key_point_marks.filter(
    (keyPointMark) => keyPointMark.is_covered,
  ).length;

  return (
    <article className="card round-card">
      <p className="card-label round-card__label">
        Round {roundCard.round_number}
      </p>
      <h3 className="round-card__type">{roundCard.round_type}</h3>
      <StatusPill status={roundCard.status} />
      <p className="round-card__count">
        {coveredCount} of {roundCard.key_point_marks.length} key points
      </p>
      <ul className="round-card__key-points">
        {roundCard.key_point_marks.map((keyPointMark) => (
          <li
            key={keyPointMark.key_point}
            className={
              keyPointMark.is_covered
                ? "round-card__key-point round-card__key-point--covered"
                : "round-card__key-point"
            }
          >
            {/* A hollow circle, never an X: a missed idea is something to practice, not a mistake. */}
            <span
              role="img"
              aria-label={keyPointMark.is_covered ? "Hit" : "Missed"}
            >
              {keyPointMark.is_covered ? "✓" : "○"}
            </span>
            {keyPointMark.key_point}
          </li>
        ))}
      </ul>
    </article>
  );
}

export default RoundCard;
