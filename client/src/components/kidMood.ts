import type { SubmitTurnReply } from "../api/types.ts";

// The server sends confused or got_it after a turn; listening and thinking are client-only.
export type KidMood = "listening" | "thinking" | SubmitTurnReply["kid_mood"];

// The sprite has three rows, so listening and thinking share the generic row and differ by overlay.
export const KID_SPRITE_ROW_BY_MOOD: Record<KidMood, number> = {
  listening: 0,
  thinking: 0,
  confused: 1,
  got_it: 2,
};

export const KID_MOOD_LABELS: Record<KidMood, string> = {
  listening: "Listening",
  thinking: "Thinking",
  confused: "Confused",
  got_it: "Gets it",
};
