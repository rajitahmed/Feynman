import type {
  StartSessionReply,
  StartSessionRequest,
  SubmitTurnReply,
  SubmitTurnRequest,
} from "./types.ts";

export function startSession(
  request: StartSessionRequest,
): Promise<StartSessionReply> {
  return postJson<StartSessionReply>("/api/session/start", request);
}

export function submitTurn(
  request: SubmitTurnRequest,
): Promise<SubmitTurnReply> {
  return postJson<SubmitTurnReply>("/api/session/turn", request);
}

async function postJson<Reply>(url: string, body: object): Promise<Reply> {
  const response = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!response.ok) {
    throw new Error(`Server answered ${response.status}`);
  }
  return (await response.json()) as Reply;
}
