import "./RoundTracker.css";

type RoundTrackerProps = {
  roundNumber: number;
  roundCount: number;
};

function RoundTracker({ roundNumber, roundCount }: RoundTrackerProps) {
  return (
    <p className="round-tracker">
      Round {roundNumber} of {roundCount}
    </p>
  );
}

export default RoundTracker;
