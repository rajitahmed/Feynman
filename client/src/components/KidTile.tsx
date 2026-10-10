import KidAvatar from "./KidAvatar.tsx";
import {
  KID_MOOD_LABELS,
  KID_SPRITE_ROW_BY_MOOD,
  type KidMood,
} from "./kidMood.ts";
import { KID_NAME } from "./kidName.ts";
import SelfTile from "./SelfTile.tsx";
import SpeechBubble from "./SpeechBubble.tsx";
import ThinkingDots from "./ThinkingDots.tsx";
import "./KidTile.css";

type KidTileProps = {
  mood: KidMood;
  isTalking: boolean;
  latestKidLine: string;
};

function KidTile({ mood, isTalking, latestKidLine }: KidTileProps) {
  const talkingClass = isTalking ? "kid-tile--talking" : "";
  const isThinking = mood === "thinking";
  return (
    <section
      className={`kid-tile kid-tile--${mood} ${talkingClass}`}
      aria-label="Call"
    >
      {/* Keys remount on change, which replays the bubble's pop-in and the avatar's crossfade.
          Listening and thinking share a sprite row, so switching between them doesn't flicker. */}
      <SpeechBubble key={isThinking ? "thinking" : latestKidLine}>
        {isThinking ? <ThinkingDots /> : latestKidLine}
      </SpeechBubble>
      <KidAvatar key={KID_SPRITE_ROW_BY_MOOD[mood]} mood={mood} />
      <p className="kid-tile__name-tag">
        {KID_NAME} · {KID_MOOD_LABELS[mood]}
      </p>
      <SelfTile />
    </section>
  );
}

export default KidTile;
