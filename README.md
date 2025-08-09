# Solver

Multi-puzzle solving framework. Plugins live under `backend/puzzles/*`.

## Run

```bash
docker compose build
docker compose up -d
# Frontend: http://<ip>:3000
# Backend:  http://<ip>:8000/docs
```

## Add a puzzle

Create `backend/puzzles/<name>/` with `plugin.py` implementing `PuzzlePlugin`, then register it in `backend/puzzles/registry.py`.
