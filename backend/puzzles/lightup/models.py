from pydantic import BaseModel
from typing import List, Optional

class Given(BaseModel):
    r: int
    c: int
    black: Optional[int] = None  # None=white, -1=black no number, 0..4 numbered

class Puzzle(BaseModel):
    puzzleType: str = "LightUp"
    rows: int
    cols: int
    givens: List[Given]
    source: Optional[str] = None
    external_id: Optional[str] = None

class Solution(BaseModel):
    bulbs: List[List[bool]]
