import "./RoundTracker.css";

// The four rounds always follow the arc what, how, why, example (see docs/SPEC.md).
const ROUND_TITLES = [
  "What is it?",
  "How does it work?",
  "Why does it matter?",
  "Can you give an example?",
];

type RoundTrackerProps = {
  roundNumber: number;
  roundCount: number;
};

function RoundTracker({ roundNumber, roundCount }: RoundTrackerProps) {
  const roundNumbers = Array.from(
    { length: roundCount },
    (_, roundIndex) => roundIndex + 1,
  );

  return (
    <header className="round-tracker">
      <ol className="round-tracker__dots" aria-hidden="true">
        {roundNumbers.map((dotRoundNumber) => (
          <li
            key={dotRoundNumber}
            className={`round-tracker__dot round-tracker__dot--${findDotState(dotRoundNumber, roundNumber)}`}
          />
        ))}
      </ol>
      <h1 className="round-tracker__title">
        Round {roundNumber} of {roundCount}: {ROUND_TITLES[roundNumber - 1]}
      </h1>
    </header>
  );
}

function findDotState(dotRoundNumber: number, currentRoundNumber: number) {
  if (dotRoundNumber < currentRoundNumber) {
    return "finished";
  }
  return dotRoundNumber === currentRoundNumber ? "current" : "future";
}

export default RoundTracker;
