from typing import Any, Dict, List
from z3 import Bool, Solver, Implies, And, Or, Not, Sum, If
from .models import Puzzle, Solution

def solve_lightup(puzzle_dict: Dict[str, Any]) -> Dict[str, Any]:
    puz = Puzzle(**puzzle_dict)
    R, C = puz.rows, puz.cols
    bulb = [[Bool(f"b_{r}_{c}") for c in range(C)] for r in range(R)]
    s = Solver()

    black = [[None]*C for _ in range(R)]
    numbered = {}
    for g in puz.givens:
        if g.black is not None:
            black[g.r][g.c] = g.black
            if g.black >= 0:
                numbered[(g.r,g.c)] = g.black

    # No bulbs on black
    for r in range(R):
        for c in range(C):
            if black[r][c] is not None:
                s.add(Not(bulb[r][c]))

    # Numbered blacks adjacency constraint
    for (r,c), k in numbered.items():
        adj = []
        for (rr,cc) in [(r-1,c),(r+1,c),(r,c-1),(r,c+1)]:
            if 0 <= rr < R and 0 <= cc < C and black[rr][cc] is None:
                adj.append(bulb[rr][cc])
        s.add(Sum([If(x,1,0) for x in adj]) == k)

    # No two bulbs see each other
    for r in range(R):
        for c in range(C):
            if black[r][c] is not None: 
                continue
            seen = []
            cc = c-1
            while cc >= 0 and black[r][cc] is None:
                seen.append(bulb[r][cc]); cc -= 1
            cc = c+1
            while cc < C and black[r][cc] is None:
                seen.append(bulb[r][cc]); cc += 1
            s.add(Implies(bulb[r][c], And([Not(x) for x in seen])))

    # Every white cell is lit
    for r in range(R):
        for c in range(C):
            if black[r][c] is not None: 
                continue
            rays = [bulb[r][c]]
            rr = r-1
            while rr >= 0 and black[rr][c] is None:
                rays.append(bulb[rr][c]); rr -= 1
            rr = r+1
            while rr < R and black[rr][c] is None:
                rays.append(bulb[rr][c]); rr += 1
            cc = c-1
            while cc >= 0 and black[r][cc] is None:
                rays.append(bulb[r][cc]); cc -= 1
            cc = c+1
            while cc < C and black[r][cc] is None:
                rays.append(bulb[r][cc]); cc += 1
            s.add(Or(rays))

    if s.check().r == 1:
        m = s.model()
        grid: List[List[bool]] = [[bool(m.eval(bulb[r][c], model_completion=True)) for c in range(C)] for r in range(R)]
        sol = Solution(bulbs=grid).model_dump()
        return {"status":"solved", "solution": sol, "log":[]}
    return {"status":"unsat", "solution":{}, "log":[{"rule":"UNSAT"}]}
