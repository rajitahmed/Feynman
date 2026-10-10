import type {
  GapReport,
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

export function getReport(): Promise<GapReport> {
  return getJson<GapReport>("/api/session/report");
}

async function postJson<Reply>(url: string, body: object): Promise<Reply> {
  const response = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  return readReply<Reply>(response);
}

async function getJson<Reply>(url: string): Promise<Reply> {
  return readReply<Reply>(await fetch(url));
}

async function readReply<Reply>(response: Response): Promise<Reply> {
  if (!response.ok) {
    throw new Error(`Server answered ${response.status}`);
  }
  return (await response.json()) as Reply;
}
