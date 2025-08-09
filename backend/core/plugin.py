from typing import Protocol, Any, Dict

class PuzzlePlugin(Protocol):
    """Each puzzle plugin implements these three."""
    type_name: str  # e.g., "LightUp"

    async def ingest(self, query: Dict[str, Any]) -> Dict[str, Any]:
        """Return canonical puzzle JSON for this type (async for scraper)."""

    def solve(self, puzzle: Dict[str, Any]) -> Dict[str, Any]:
        """Return {status, solution, log}."""

    def render(self, puzzle: Dict[str, Any], solution: Dict[str, Any]) -> str:
        """Return SVG string."""
