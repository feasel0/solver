from typing import Dict
from core.plugin import PuzzlePlugin
from puzzles.lightup import plugin as lightup_plugin

_REGISTRY: Dict[str, PuzzlePlugin] = {
    lightup_plugin.type_name: lightup_plugin
}

def list_puzzles():
    return [{"type": k} for k in _REGISTRY.keys()]

def get_plugin(t: str) -> PuzzlePlugin:
    if t not in _REGISTRY:
        raise KeyError(f"Unknown puzzle type: {t}")
    return _REGISTRY[t]
