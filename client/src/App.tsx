import { useState } from "react";
import type { GapReport, StartSessionReply } from "./api/types.ts";
import NotesScreen from "./screens/NotesScreen.tsx";
import ReportScreen from "./screens/ReportScreen.tsx";
import SessionScreen from "./screens/SessionScreen.tsx";

function App() {
  // Kept here, above the notes screen, so "Start again" brings the last notes back.
  const [notes, setNotes] = useState("");
  const [startedSession, setStartedSession] =
    useState<StartSessionReply | null>(null);
  const [report, setReport] = useState<GapReport | null>(null);

  function startAgain() {
    setStartedSession(null);
    setReport(null);
  }

  if (startedSession === null) {
    return (
      <NotesScreen
        notes={notes}
        onNotesChange={setNotes}
        onSessionStarted={setStartedSession}
      />
    );
  }

  if (report !== null) {
    return <ReportScreen report={report} onStartAgain={startAgain} />;
  }

  return (
    <SessionScreen
      firstKidQuestion={startedSession.kid_question}
      firstKidAudioBase64={startedSession.kid_audio_base64}
      roundCount={startedSession.round_count}
      onReportReady={setReport}
    />
  );
}

export default App;
