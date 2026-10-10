import { useEffect, useRef } from "react";
import { KID_NAME } from "./kidName.ts";
import "./Transcript.css";

export type Speaker = "kid" | "you";

export type TranscriptLine = {
  speaker: Speaker;
  text: string;
};

const SPEAKER_NAMES: Record<Speaker, string> = {
  kid: KID_NAME,
  you: "You",
};

type TranscriptProps = {
  lines: TranscriptLine[];
};

function Transcript({ lines }: TranscriptProps) {
  const linesListRef = useRef<HTMLOListElement>(null);

  // Keep the newest message in view, like a chat panel.
  useEffect(() => {
    const linesList = linesListRef.current;
    if (linesList !== null) {
      linesList.scrollTop = linesList.scrollHeight;
    }
  }, [lines]);

  return (
    <section className="transcript">
      <h2 className="transcript__label">Transcript</h2>
      <ol className="transcript__lines" aria-live="polite" ref={linesListRef}>
        {lines.map((line, lineIndex) => (
          // Lines are only ever appended, so their position is a stable key.
          <li
            key={lineIndex}
            className={`transcript__line transcript__line--${line.speaker}`}
          >
            <span className="transcript__speaker">
              {SPEAKER_NAMES[line.speaker]}
            </span>
            <p className="transcript__bubble">{line.text}</p>
          </li>
        ))}
      </ol>
    </section>
  );
}

export default Transcript;
