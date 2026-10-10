import { useState } from "react";
import type { StartSessionReply } from "./api/types.ts";
import NotesScreen from "./screens/NotesScreen.tsx";
import SessionScreen from "./screens/SessionScreen.tsx";

function App() {
  const [startedSession, setStartedSession] =
    useState<StartSessionReply | null>(null);

  if (startedSession === null) {
    return <NotesScreen onSessionStarted={setStartedSession} />;
  }

  return (
    <SessionScreen
      firstKidQuestion={startedSession.kid_question}
      roundCount={startedSession.round_count}
    />
  );
}

export default App;
