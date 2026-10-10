import { useState } from "react";
import { getReport, submitTurn } from "../api/server.ts";
import type { GapReport } from "../api/types.ts";
import KidTile from "../components/KidTile.tsx";
import type { KidMood } from "../components/kidMood.ts";
import { KID_NAME } from "../components/kidName.ts";
import RoundTracker from "../components/RoundTracker.tsx";
import Transcript, { type TranscriptLine } from "../components/Transcript.tsx";
import TypedAnswerBox from "../components/TypedAnswerBox.tsx";
import "./SessionScreen.css";

const FIRST_ROUND_NUMBER = 1;

type SessionScreenProps = {
  firstKidQuestion: string;
  roundCount: number;
  onReportReady: (report: GapReport) => void;
};

function SessionScreen({
  firstKidQuestion,
  roundCount,
  onReportReady,
}: SessionScreenProps) {
  const [transcriptLines, setTranscriptLines] = useState<TranscriptLine[]>([
    { speaker: "kid", text: firstKidQuestion },
  ]);
  const [roundNumber, setRoundNumber] = useState(FIRST_ROUND_NUMBER);
  const [kidMood, setKidMood] = useState<KidMood>("listening");
  const [errorMessage, setErrorMessage] = useState("");
  const [isSessionFinished, setIsSessionFinished] = useState(false);

  async function sendAnswer(answerText: string): Promise<boolean> {
    const moodBeforeAnswer = kidMood;
    setKidMood("thinking");
    setErrorMessage("");
    try {
      const reply = await submitTurn({ answer_text: answerText });
      // Both lines are added only on success, so a failed send never leaves a stray line.
      setTranscriptLines((previousLines) => [
        ...previousLines,
        { speaker: "you", text: answerText },
        { speaker: "kid", text: reply.kid_reply_text },
      ]);
      setRoundNumber(reply.round_number);
      setKidMood(reply.kid_mood);
      setIsSessionFinished(reply.is_session_finished);
      if (reply.is_session_finished) {
        void loadReport();
      }
      return true;
    } catch (error) {
      setErrorMessage(`Could not send your answer: ${String(error)}`);
      setKidMood(moodBeforeAnswer);
      return false;
    }
  }

  async function loadReport() {
    try {
      onReportReady(await getReport());
    } catch (error) {
      setErrorMessage(`Could not load your report: ${String(error)}`);
    }
  }

  const isKidThinking = kidMood === "thinking";
  const latestKidLine = transcriptLines.findLast(
    (line) => line.speaker === "kid",
  );

  return (
    <main className="session-screen">
      <RoundTracker roundNumber={roundNumber} roundCount={roundCount} />
      <div className="session-screen__call">
        <KidTile mood={kidMood} latestKidLine={latestKidLine?.text ?? ""} />
        <Transcript lines={transcriptLines} />
      </div>
      <footer className="session-screen__control-bar">
        {isKidThinking && <p role="status">{KID_NAME} is thinking…</p>}
        {errorMessage && <p role="alert">{errorMessage}</p>}
        {isSessionFinished ? (
          <p role="status">
            That's all {roundCount} rounds. Writing your report…
          </p>
        ) : (
          <TypedAnswerBox isDisabled={isKidThinking} onSend={sendAnswer} />
        )}
      </footer>
    </main>
  );
}

export default SessionScreen;
