import type { RoundRecap as RoundRecapData } from "../api/types.ts";
import { KID_NAME } from "./kidName.ts";
import "./RoundRecap.css";

type RoundRecapProps = {
  roundRecap: RoundRecapData;
};

function RoundRecap({ roundRecap }: RoundRecapProps) {
  return (
    <article className="round-recap">
      <h3 className="card-label round-recap__label">
        Round {roundRecap.round_number}
      </h3>
      <ol className="round-recap__lines">
        <li className="round-recap__line">
          <span className="round-recap__speaker">{KID_NAME}</span>
          <p className="round-recap__bubble">{roundRecap.kid_question}</p>
        </li>
        {roundRecap.answers.map((answer, answerIndex) => (
          // Answers never reorder, so their position is a stable key.
          <li key={answerIndex} className="round-recap__exchange">
            <div className="round-recap__line round-recap__line--you">
              <span className="round-recap__speaker">You</span>
              <p className="round-recap__bubble">{answer.answer_text}</p>
              {answer.covered_key_points.length === 0 ? (
                <p className="round-recap__covered">
                  No key points in this answer
                </p>
              ) : (
                <ul className="round-recap__covered">
                  {answer.covered_key_points.map((keyPoint) => (
                    <li key={keyPoint}>✓ {keyPoint}</li>
                  ))}
                </ul>
              )}
            </div>
            <div className="round-recap__line">
              <span className="round-recap__speaker">{KID_NAME}</span>
              <p className="round-recap__bubble">{answer.kid_reply_text}</p>
            </div>
          </li>
        ))}
      </ol>
    </article>
  );
}

export default RoundRecap;
