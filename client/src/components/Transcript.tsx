import "./Transcript.css";

export type Speaker = "kid" | "you";

export type TranscriptLine = {
  speaker: Speaker;
  text: string;
};

const SPEAKER_NAMES: Record<Speaker, string> = {
  kid: "Kid",
  you: "You",
};

type TranscriptProps = {
  lines: TranscriptLine[];
};

function Transcript({ lines }: TranscriptProps) {
  return (
    <section className="transcript">
      <h2 className="transcript__label">Transcript</h2>
      <ol className="transcript__lines" aria-live="polite">
        {lines.map((line, lineIndex) => (
          // Lines are only ever appended, so their position is a stable key.
          <li key={lineIndex} className="transcript__line">
            <strong>{SPEAKER_NAMES[line.speaker]}:</strong> {line.text}
          </li>
        ))}
      </ol>
    </section>
  );
}

export default Transcript;
