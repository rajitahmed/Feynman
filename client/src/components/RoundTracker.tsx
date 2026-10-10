import "./RoundTracker.css";

const ROUND_COUNT = 4;

type RoundTrackerProps = {
  roundNumber: number;
};

function RoundTracker({ roundNumber }: RoundTrackerProps) {
  return (
    <p className="round-tracker">
      Round {roundNumber} of {ROUND_COUNT}
    </p>
  );
}

export default RoundTracker;
