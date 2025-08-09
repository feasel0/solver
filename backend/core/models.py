from typing import Literal, Dict, Any, List, Optional
from pydantic import BaseModel, Field

class SolveEnvelope(BaseModel):
    type: str                      # plugin key, e.g., "LightUp"
    puzzle: Dict[str, Any]         # canonical puzzle JSON per plugin schema

class SolveResult(BaseModel):
    status: Literal["solved","unsat","error"]
    solution: Dict[str, Any] = Field(default_factory=dict)
    log: List[Dict[str, Any]] = Field(default_factory=list)

class RenderEnvelope(BaseModel):
    type: str
    puzzle: Dict[str, Any]
    solution: Optional[Dict[str, Any]] = None  # if omitted, backend may solve first
    step: Optional[int] = None
