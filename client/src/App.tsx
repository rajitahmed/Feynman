import { useState } from "react";
import type { GapReport, StartSessionReply } from "./api/types.ts";
import NotesScreen from "./screens/NotesScreen.tsx";
import ReportScreen from "./screens/ReportScreen.tsx";
import SessionScreen from "./screens/SessionScreen.tsx";

function App() {
  const [startedSession, setStartedSession] =
    useState<StartSessionReply | null>(null);
  const [report, setReport] = useState<GapReport | null>(null);

  if (startedSession === null) {
    return <NotesScreen onSessionStarted={setStartedSession} />;
  }

  if (report !== null) {
    return <ReportScreen report={report} />;
  }

  return (
    <SessionScreen
      firstKidQuestion={startedSession.kid_question}
      roundCount={startedSession.round_count}
      onReportReady={setReport}
    />
  );
}

export default App;
