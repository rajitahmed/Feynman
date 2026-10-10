import { useState } from "react";
import { getReport, submitTurn } from "../api/server.ts";
import type { GapReport, SubmitTurnRequest } from "../api/types.ts";
import KidTile from "../components/KidTile.tsx";
import type { KidMood } from "../components/kidMood.ts";
import { KID_NAME } from "../components/kidName.ts";
import MicButton from "../components/MicButton.tsx";
import RoundTracker from "../components/RoundTracker.tsx";
import Transcript, { type TranscriptLine } from "../components/Transcript.tsx";
import TypedAnswerBox from "../components/TypedAnswerBox.tsx";
import "./SessionScreen.css";

const FIRST_ROUND_NUMBER = 1;
// ElevenLabs speaks mp3, sent from the server as base64.
const KID_AUDIO_URL_PREFIX = "data:audio/mpeg;base64,";

type SessionScreenProps = {
  firstKidQuestion: string;
  firstKidAudioBase64: string;
  roundCount: number;
  onReportReady: (report: GapReport) => void;
};

function SessionScreen({
  firstKidQuestion,
  firstKidAudioBase64,
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
  const [kidAudioBase64, setKidAudioBase64] = useState(firstKidAudioBase64);
  const [isKidTalking, setIsKidTalking] = useState(false);

  // Typed and spoken answers share this one turn flow; only the request differs.
  async function sendAnswer(request: SubmitTurnRequest): Promise<boolean> {
    const moodBeforeAnswer = kidMood;
    setKidMood("thinking");
    setErrorMessage("");
    try {
      const reply = await submitTurn(request);
      // Both lines are added only on success, so a failed send never leaves a stray line.
      setTranscriptLines((previousLines) => [
        ...previousLines,
        // The server's transcript, so the learner sees what the app heard.
        { speaker: "you", text: reply.answer_text },
        { speaker: "kid", text: reply.kid_reply_text },
      ]);
      setKidAudioBase64(reply.kid_audio_base64);
      setRoundNumber(reply.round_number);
      setKidMood(reply.kid_mood);
      setIsSessionFinished(reply.is_session_finished);
      return true;
    } catch (error) {
      setErrorMessage(`Could not send your answer: ${String(error)}`);
      setKidMood(moodBeforeAnswer);
      return false;
    }
  }

  function finishKidLine() {
    setIsKidTalking(false);
    // Waits for the kid's last line, because leaving the screen would cut its audio off.
    if (isSessionFinished) {
      void loadReport();
    }
  }

  async function loadReport() {
    try {
      onReportReady(await getReport());
    } catch (error) {
      setErrorMessage(`Could not load your report: ${String(error)}`);
    }
  }

  function showMicError(error: unknown) {
    setErrorMessage(`Could not use the mic, try typing: ${String(error)}`);
  }

  // Null while the kid waits for an answer; the mic shows it as its disabled label.
  function describeKidStatus(): string | null {
    if (kidMood === "thinking") {
      return `${KID_NAME} is thinking…`;
    }
    return isKidTalking ? `${KID_NAME} is talking…` : null;
  }

  const kidStatus = describeKidStatus();
  const latestKidLine = transcriptLines.findLast(
    (line) => line.speaker === "kid",
  );

  return (
    <main className="session-screen">
      <RoundTracker roundNumber={roundNumber} roundCount={roundCount} />
      <div className="session-screen__call">
        <KidTile
          mood={kidMood}
          isTalking={isKidTalking}
          latestKidLine={latestKidLine?.text ?? ""}
        />
        {/* The key remounts the player for every kid line, so a repeated clip still plays. */}
        <audio
          key={transcriptLines.length}
          src={`${KID_AUDIO_URL_PREFIX}${kidAudioBase64}`}
          autoPlay
          onPlay={() => setIsKidTalking(true)}
          onEnded={finishKidLine}
          onError={finishKidLine}
        />
        <Transcript lines={transcriptLines} />
      </div>
      <footer className="session-screen__control-bar">
        {errorMessage && <p role="alert">{errorMessage}</p>}
        {isSessionFinished ? (
          <p role="status">
            That's all {roundCount} rounds. Writing your report…
          </p>
        ) : (
          <>
            <MicButton
              waitingLabel={kidStatus}
              onRecorded={(audioBase64) =>
                void sendAnswer({ answer_audio_base64: audioBase64 })
              }
              onMicError={showMicError}
            />
            {/* Always visible, so typing still works if the mic or the room fails. */}
            <TypedAnswerBox
              isDisabled={kidStatus !== null}
              onSend={(answerText) => sendAnswer({ answer_text: answerText })}
            />
          </>
        )}
      </footer>
    </main>
  );
}

export default SessionScreen;
