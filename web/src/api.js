// Single API client. Talks to the FastAPI backend (proxied at /api in dev).
export async function getHealth() {
  const r = await fetch("/api/health");
  if (!r.ok) throw new Error("health failed");
  return r.json();
}

export async function analyze(params) {
  const r = await fetch("/api/analyze", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(params),
  });
  if (!r.ok) throw new Error(`analyze failed (${r.status})`);
  return r.json();
}
