import { useState, type FormEvent } from "react";
import { startSession } from "../api/server.ts";
import Button from "../components/Button.tsx";
import "./NotesScreen.css";

const KID_GREETING = "Hi! What are you teaching me today?";
const NOTES_BOX_LINES = 12;

type NotesScreenProps = {
  onSessionStarted: (kidQuestion: string) => void;
};

function NotesScreen({ onSessionStarted }: NotesScreenProps) {
  const [notes, setNotes] = useState("");
  const [isPreparing, setIsPreparing] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");

  async function submitNotes(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setIsPreparing(true);
    setErrorMessage("");
    try {
      const reply = await startSession({ notes });
      onSessionStarted(reply.kid_question);
    } catch (error) {
      setErrorMessage(`Could not start the session: ${String(error)}`);
      setIsPreparing(false);
    }
  }

  if (isPreparing) {
    return (
      <main className="notes-screen">
        <p className="notes-screen__preparing" role="status">
          Preparing your session…
        </p>
      </main>
    );
  }

  return (
    <main className="notes-screen">
      <p className="notes-screen__greeting">{KID_GREETING}</p>
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
      </form>
    </main>
  );
}

export default NotesScreen;
