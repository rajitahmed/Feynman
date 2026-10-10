import KidAvatar from "./KidAvatar.tsx";
import { KID_MOOD_LABELS, type KidMood } from "./kidMood.ts";
import { KID_NAME } from "./kidName.ts";
import SelfTile from "./SelfTile.tsx";
import SpeechBubble from "./SpeechBubble.tsx";
import "./KidTile.css";

type KidTileProps = {
  mood: KidMood;
  isTalking: boolean;
  latestKidLine: string;
};

function KidTile({ mood, isTalking, latestKidLine }: KidTileProps) {
  const talkingClass = isTalking ? "kid-tile--talking" : "";
  return (
    <section
      className={`kid-tile kid-tile--${mood} ${talkingClass}`}
      aria-label="Call"
    >
      <SpeechBubble>
        {mood === "thinking" ? (
          <span className="kid-tile__thinking-dots" aria-hidden="true">
            • • •
          </span>
        ) : (
          latestKidLine
        )}
      </SpeechBubble>
      <KidAvatar mood={mood} />
      <p className="kid-tile__name-tag">
        {KID_NAME} · {KID_MOOD_LABELS[mood]}
      </p>
      <SelfTile />
    </section>
  );
}

export default KidTile;
