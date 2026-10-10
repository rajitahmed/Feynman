import { useState, type FormEvent } from "react";
import Button from "./Button.tsx";
import "./TypedAnswerBox.css";

type TypedAnswerBoxProps = {
  isDisabled: boolean;
  onSend: (answerText: string) => Promise<boolean>;
};

function TypedAnswerBox({ isDisabled, onSend }: TypedAnswerBoxProps) {
  const [answerText, setAnswerText] = useState("");

  async function sendAnswer(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    // Keep the text after a failed send, so retrying is one click.
    const isSent = await onSend(answerText);
    if (isSent) {
      setAnswerText("");
    }
  }

  return (
    <form className="typed-answer-box" onSubmit={sendAnswer}>
      <input
        className="typed-answer-box__input"
        aria-label="Your answer"
        placeholder="Type your answer..."
        value={answerText}
        disabled={isDisabled}
        onChange={(event) => setAnswerText(event.target.value)}
      />
      <Button type="submit" disabled={isDisabled || answerText.trim() === ""}>
        Send
      </Button>
    </form>
  );
}

export default TypedAnswerBox;
