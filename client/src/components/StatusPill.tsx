import type { RoundStatus } from "../api/types.ts";
import "./StatusPill.css";

// Every status has text and an icon, so color is never the only signal.
const STATUS_LABELS: Record<RoundStatus, string> = {
  covered: "Covered",
  partly_covered: "Partly covered",
  fuzzy: "Fuzzy",
};

const STATUS_ICONS: Record<RoundStatus, string> = {
  covered: "✓",
  partly_covered: "◐",
  fuzzy: "?",
};

type StatusPillProps = {
  status: RoundStatus;
};

function StatusPill({ status }: StatusPillProps) {
  return (
    <span className={`status-pill status-pill--${status}`}>
      <span aria-hidden="true">{STATUS_ICONS[status]}</span>
      {STATUS_LABELS[status]}
    </span>
  );
}

export default StatusPill;
