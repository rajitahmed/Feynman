import { useState } from "react";
import { submitTurn } from "../api/server.ts";
import RoundTracker from "../components/RoundTracker.tsx";
import Transcript, { type TranscriptLine } from "../components/Transcript.tsx";
import TypedAnswerBox from "../components/TypedAnswerBox.tsx";
import "./SessionScreen.css";

const FIRST_ROUND_NUMBER = 1;

type SessionScreenProps = {
  firstKidQuestion: string;
  roundCount: number;
};

function SessionScreen({ firstKidQuestion, roundCount }: SessionScreenProps) {
  const [transcriptLines, setTranscriptLines] = useState<TranscriptLine[]>([
    { speaker: "kid", text: firstKidQuestion },
  ]);
  const [roundNumber, setRoundNumber] = useState(FIRST_ROUND_NUMBER);
  const [isKidThinking, setIsKidThinking] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");

  async function sendAnswer(answerText: string): Promise<boolean> {
    setIsKidThinking(true);
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
      return true;
    } catch (error) {
      setErrorMessage(`Could not send your answer: ${String(error)}`);
      return false;
    } finally {
      setIsKidThinking(false);
    }
  }

  return (
    <main className="session-screen">
      <RoundTracker roundNumber={roundNumber} roundCount={roundCount} />
      <Transcript lines={transcriptLines} />
      {isKidThinking && <p role="status">The kid is thinking…</p>}
      {errorMessage && <p role="alert">{errorMessage}</p>}
      <TypedAnswerBox isDisabled={isKidThinking} onSend={sendAnswer} />
    </main>
  );
}

export default SessionScreen;
