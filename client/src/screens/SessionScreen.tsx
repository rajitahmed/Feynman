import { useState } from "react";
import { submitTurn } from "../api/server.ts";
import RoundTracker from "../components/RoundTracker.tsx";
import Transcript, { type TranscriptLine } from "../components/Transcript.tsx";
import TypedAnswerBox from "../components/TypedAnswerBox.tsx";
import "./SessionScreen.css";

const FIRST_ROUND_NUMBER = 1;

type SessionScreenProps = {
  firstKidQuestion: string;
};

function SessionScreen({ firstKidQuestion }: SessionScreenProps) {
  const [transcriptLines, setTranscriptLines] = useState<TranscriptLine[]>([
    { speaker: "kid", text: firstKidQuestion },
  ]);
  const [roundNumber, setRoundNumber] = useState(FIRST_ROUND_NUMBER);
  const [isKidThinking, setIsKidThinking] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");

  function addTranscriptLine(line: TranscriptLine) {
    setTranscriptLines((previousLines) => [...previousLines, line]);
  }

  async function sendAnswer(answerText: string) {
    addTranscriptLine({ speaker: "you", text: answerText });
    setIsKidThinking(true);
    setErrorMessage("");
    try {
      const reply = await submitTurn({ answer_text: answerText });
      addTranscriptLine({ speaker: "kid", text: reply.kid_reply_text });
      setRoundNumber(reply.round_number);
    } catch (error) {
      setErrorMessage(`Could not send your answer: ${String(error)}`);
    } finally {
      setIsKidThinking(false);
    }
  }

  return (
    <main className="session-screen">
      <RoundTracker roundNumber={roundNumber} />
      <Transcript lines={transcriptLines} />
      {isKidThinking && <p role="status">The kid is thinking…</p>}
      {errorMessage && <p role="alert">{errorMessage}</p>}
      <TypedAnswerBox isDisabled={isKidThinking} onSend={sendAnswer} />
    </main>
  );
}

export default SessionScreen;
