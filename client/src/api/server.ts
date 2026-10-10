import type { StartSessionReply, StartSessionRequest } from "./types.ts";

export async function startSession(
  request: StartSessionRequest,
): Promise<StartSessionReply> {
  const response = await fetch("/api/session/start", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(request),
  });
  if (!response.ok) {
    throw new Error(`Server answered ${response.status}`);
  }
  return (await response.json()) as StartSessionReply;
}
