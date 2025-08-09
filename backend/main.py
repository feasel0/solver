from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import ORJSONResponse, PlainTextResponse
from typing import Dict, Any
from core.models import SolveEnvelope, SolveResult, RenderEnvelope
from puzzles.registry import list_puzzles, get_plugin

app = FastAPI(
    default_response_class=ORJSONResponse,
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
    redoc_url=None,
)

@app.get("/api/health")
def health():
    return {"ok": True}

@app.get("/api/puzzles")
def puzzles():
    return {"puzzles": list_puzzles()}

@app.get("/api/ingest")
async def ingest(type: str = Query(...), **query):
    try:
        plugin = get_plugin(type)
    except KeyError:
        raise HTTPException(status_code=400, detail=f"Unknown puzzle type '{type}'")
    data = await plugin.ingest(query)  # e.g., LightUp needs e=<...>
    return {"type": type, "puzzle": data}

@app.post("/api/solve")
def solve(body: SolveEnvelope) -> SolveResult:
    try:
        plugin = get_plugin(body.type)
    except KeyError:
        raise HTTPException(status_code=400, detail=f"Unknown puzzle type '{body.type}'")
    res = plugin.solve(body.puzzle)
    return SolveResult(**res)

@app.post("/api/render", response_class=PlainTextResponse)
def render(body: RenderEnvelope):
    try:
        plugin = get_plugin(body.type)
    except KeyError:
        raise HTTPException(status_code=400, detail=f"Unknown puzzle type '{body.type}'")
    if not body.solution:
        res = plugin.solve(body.puzzle)
        if res.get("status") != "solved":
            return "<svg><!-- unsolved/unsat --></svg>"
        body.solution = res["solution"]
    svg = plugin.render(body.puzzle, body.solution)
    return svg
