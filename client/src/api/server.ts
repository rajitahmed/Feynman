import type { HealthCheck } from "./types.ts";

export async function checkHealth(): Promise<HealthCheck> {
  const response = await fetch("/api/health");
  if (!response.ok) {
    throw new Error(`Server answered ${response.status}`);
  }
  return (await response.json()) as HealthCheck;
}
