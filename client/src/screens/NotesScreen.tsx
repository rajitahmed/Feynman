import { useEffect, useState, type FormEvent } from "react";
import {
  getKidGreeting,
  startDemoSession,
  startSession,
} from "../api/server.ts";
import type { StartSessionReply, StartSessionRequest } from "../api/types.ts";
import Button from "../components/Button.tsx";
import KidAvatar from "../components/KidAvatar.tsx";
import SpeechBubble from "../components/SpeechBubble.tsx";
import "./NotesScreen.css";

const NOTES_BOX_LINES = 12;

type NotesScreenProps = {
  onSessionStarted: (reply: StartSessionReply) => void;
};

function NotesScreen({ onSessionStarted }: NotesScreenProps) {
  const [notes, setNotes] = useState("");
  const [isPreparing, setIsPreparing] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");
  const [kidGreeting, setKidGreeting] = useState("");

  useEffect(() => {
    // The greeting is a nicety; without it the kid just waits quietly.
    getKidGreeting()
      .then((greeting) => setKidGreeting(greeting.kid_greeting_text))
      .catch(() => setKidGreeting(""));
  }, []);

  function submitNotes(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    void beginSession(startSession);
  }

  async function beginSession(
    start: (request: StartSessionRequest) => Promise<StartSessionReply>,
  ) {
    setIsPreparing(true);
    setErrorMessage("");
    try {
      const reply = await start({ notes });
      onSessionStarted(reply);
    } catch (error) {
      setErrorMessage(`Could not start the session: ${String(error)}`);
      setIsPreparing(false);
    }
  }

  if (isPreparing) {
    return (
      <main className="notes-screen">
        <KidAvatar mood="thinking" />
        <p aria-hidden="true">• • •</p>
        <p className="notes-screen__preparing" role="status">
          Preparing your session…
        </p>
      </main>
    );
  }

  return (
    <main className="notes-screen">
      {kidGreeting && <SpeechBubble>{kidGreeting}</SpeechBubble>}
      <KidAvatar mood="listening" />
      <form className="notes-screen__card" onSubmit={submitNotes}>
        <label className="notes-screen__label" htmlFor="notes">
          Your notes
        </label>
        <textarea
          id="notes"
          className="notes-screen__notes"
          rows={NOTES_BOX_LINES}
          placeholder="Paste your study notes here..."
          value={notes}
          onChange={(event) => setNotes(event.target.value)}
        />
        {errorMessage && <p role="alert">{errorMessage}</p>}
        <Button type="submit" disabled={notes.trim() === ""}>
          Start
        </Button>
        {/* Backup if live planning fails on stage; also rehearses without spending credits. */}
        <button
          type="button"
          className="notes-screen__demo-link"
          disabled={notes.trim() === ""}
          onClick={() => void beginSession(startDemoSession)}
        >
          Use demo rubric
        </button>
      </form>
    </main>
  );
}

export default NotesScreen;
