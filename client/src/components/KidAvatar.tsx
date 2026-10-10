import type { CSSProperties } from "react";
import {
  KID_MOOD_LABELS,
  KID_SPRITE_ROW_BY_MOOD,
  type KidMood,
} from "./kidMood.ts";
import { KID_NAME } from "./kidName.ts";
import "./KidAvatar.css";

type KidAvatarProps = {
  mood: KidMood;
  shouldPlayOnce?: boolean;
};

function KidAvatar({ mood, shouldPlayOnce = false }: KidAvatarProps) {
  // React's style type has no slot for custom properties, hence the cast.
  const spriteRowStyle = {
    "--sprite-row": KID_SPRITE_ROW_BY_MOOD[mood],
  } as CSSProperties;

  return (
    <div
      className={
        shouldPlayOnce ? "kid-avatar kid-avatar--play-once" : "kid-avatar"
      }
      role="img"
      aria-label={`${KID_NAME}: ${KID_MOOD_LABELS[mood]}`}
      style={spriteRowStyle}
    />
  );
}

export default KidAvatar;
