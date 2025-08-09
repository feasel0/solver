"use client";
import PuzzleForm from "../components/PuzzleForm";

export default function Page() {
  return (
    <main className="p-6 max-w-3xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">Solver</h1>
      <p className="mb-4">Choose a puzzle type, ingest it, and solve.</p>
      <PuzzleForm />
    </main>
  );
}
