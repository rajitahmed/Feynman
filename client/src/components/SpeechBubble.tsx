import type { ReactNode } from "react";
import "./SpeechBubble.css";

type SpeechBubbleProps = {
  children: ReactNode;
};

function SpeechBubble({ children }: SpeechBubbleProps) {
  return <p className="speech-bubble">{children}</p>;
}

export default SpeechBubble;
