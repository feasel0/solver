"use client";
import { useEffect, useState } from "react";
import { listPuzzles, ingest, render } from "../lib/api";

export default function PuzzleForm() {
  const [types, setTypes] = useState<string[]>([]);
  const [type, setType] = useState("LightUp");
  const [eParam, setEParam] = useState("MDo5LDQ0Niw5MDY");
  const [puzzle, setPuzzle] = useState<any>(null);
  const [svg, setSvg] = useState<string>("");

  useEffect(() => {
    listPuzzles().then(d => setTypes(d.puzzles.map((p:any)=>p.type)));
  }, []);

  const doIngest = async () => {
    const data = await ingest(type, type === "LightUp" ? { e: eParam } : {});
    setPuzzle(data.puzzle);
  };

  const doRender = async () => {
    if (!puzzle) return;
    const out = await render(type, puzzle);
    setSvg(out);
  };

  return (
    <div className="space-y-3">
      <div>
        <label className="block mb-1">Puzzle Type</label>
        <select className="border p-2"
          value={type}
          onChange={(e)=>setType(e.target.value)}>
          {types.map(t => <option key={t} value={t}>{t}</option>)}
        </select>
      </div>

      {type === "LightUp" && (
        <div>
          <label className="block mb-1">LightUp ?e= parameter or full URL</label>
          <input className="border p-2 w-full"
            value={eParam}
            onChange={(ev)=>setEParam(ev.target.value.replace(/^.*[?&]e=/,'').trim())}
            placeholder="MDo5LDQ0Niw5MDY" />
        </div>
      )}

      <div className="flex gap-2">
        <button className="bg-black text-white px-4 py-2 rounded" onClick={doIngest}>Ingest</button>
        <button className="bg-blue-600 text-white px-4 py-2 rounded" onClick={doRender} disabled={!puzzle}>Solve & Render</button>
      </div>

      {puzzle && (
        <pre className="bg-gray-100 p-3 text-xs overflow-x-auto">
          {JSON.stringify(puzzle, null, 2)}
        </pre>
      )}

      {svg && <div className="border p-2" dangerouslySetInnerHTML={{__html: svg}} />}
    </div>
  );
}
