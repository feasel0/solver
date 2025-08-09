from typing import Any, Dict
from core.plugin import PuzzlePlugin
from .ingest import ingest_lightup
from .solver import solve_lightup
from .render import render_lightup

class _LightUpPlugin(PuzzlePlugin):
    type_name = "LightUp"

    async def ingest(self, query: Dict[str, Any]) -> Dict[str, Any]:
        return await ingest_lightup(query)

    def solve(self, puzzle: Dict[str, Any]) -> Dict[str, Any]:
        return solve_lightup(puzzle)

    def render(self, puzzle: Dict[str, Any], solution: Dict[str, Any]) -> str:
        return render_lightup(puzzle, solution)

plugin = _LightUpPlugin()
