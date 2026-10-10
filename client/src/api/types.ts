// Hand-mirrored from the Pydantic models in server/models/, only the ones the browser sends or
// receives. Field names stay snake_case so the JSON needs no converting. Change both sides together.

export type RoundType = "what" | "how" | "why" | "example";

export type ParrotingMatch = {
  user_phrase: string;
  note_line: string;
};

export type RoundStatus = "covered" | "partly_covered" | "fuzzy";

export type KeyPointMark = {
  key_point: string;
  is_covered: boolean;
};

export type RoundCard = {
  round_number: number;
  round_type: RoundType;
  status: RoundStatus;
  key_point_marks: KeyPointMark[];
};

export type RecapAnswer = {
  answer_text: string;
  covered_key_points: string[];
  kid_reply_text: string;
};

export type RoundRecap = {
  round_number: number;
  kid_question: string;
  answers: RecapAnswer[];
};

export type GapReport = {
  round_cards: RoundCard[];
  missed_key_points: string[];
  parroting_flags: ParrotingMatch[];
  re_explain_prompts: string[];
  round_recaps: RoundRecap[];
};

export type StartSessionRequest = {
  notes: string;
};

export type StartSessionReply = {
  kid_question: string;
  round_count: number;
  kid_audio_base64: string;
};

// One answer per turn: typed text, or a recording the server transcribes.
export type SubmitTurnRequest =
  { answer_text: string } | { answer_audio_base64: string };

export type SubmitTurnReply = {
  answer_text: string;
  kid_reply_text: string;
  round_number: number;
  is_session_finished: boolean;
  kid_mood: "confused" | "got_it";
  kid_audio_base64: string;
};

export type KidGreeting = {
  kid_greeting_text: string;
};
