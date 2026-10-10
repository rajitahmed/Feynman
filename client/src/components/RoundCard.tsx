import type { RoundCard as RoundCardData } from "../api/types.ts";
import StatusPill from "./StatusPill.tsx";
import "./RoundCard.css";

type RoundCardProps = {
  roundCard: RoundCardData;
};

function RoundCard({ roundCard }: RoundCardProps) {
  return (
    <article className="round-card">
      <p className="round-card__label">Round {roundCard.round_number}</p>
      <h3 className="round-card__type">{roundCard.round_type}</h3>
      <StatusPill status={roundCard.status} />
      <ul className="round-card__bullets">
        {roundCard.bullets.map((bullet) => (
          <li key={bullet}>{bullet}</li>
        ))}
      </ul>
    </article>
  );
}

export default RoundCard;
