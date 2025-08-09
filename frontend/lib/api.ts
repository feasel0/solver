export const API = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000";

export async function listPuzzles() {
  const r = await fetch(`${API}/puzzles`);
  return r.json();
}

export async function ingest(type: string, query: Record<string,string>) {
  const qs = new URLSearchParams({ type, ...query }).toString();
  const r = await fetch(`${API}/ingest?` + qs);
  return r.json();
}

export async function render(type: string, puzzle: any) {
  const r = await fetch(`${API}/render`, {
    method: "POST",
    headers: {"Content-Type":"application/json"},
    body: JSON.stringify({ type, puzzle })
  });
  return r.text();
}
