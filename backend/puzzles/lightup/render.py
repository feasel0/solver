import svgwrite
from typing import Dict, Any
from .models import Puzzle, Solution

def render_lightup(puzzle_dict: Dict[str, Any], solution_dict: Dict[str, Any]) -> str:
    puz = Puzzle(**puzzle_dict)
    sol = Solution(**solution_dict)
    s = 40
    R, C = puz.rows, puz.cols
    dwg = svgwrite.Drawing(size=(C*s, R*s))

    # board
    for r in range(R):
        for c in range(C):
            x,y = c*s, r*s
            cell = next((g for g in puz.givens if g.r==r and g.c==c and g.black is not None), None)
            if cell is not None:
                dwg.add(dwg.rect(insert=(x,y), size=(s,s), fill="#222"))
                if cell.black is not None and cell.black >= 0:
                    dwg.add(dwg.text(str(cell.black), insert=(x+s/2,y+s*0.65),
                                     text_anchor="middle", fill="white", font_size=20, font_family="monospace"))
            else:
                dwg.add(dwg.rect(insert=(x,y), size=(s,s), fill="#fff", stroke="#aaa"))

    # bulbs
    for r in range(R):
        for c in range(C):
            if sol.bulbs[r][c]:
                x,y = c*s+s/2, r*s+s/2
                dwg.add(dwg.circle(center=(x,y), r=s*0.25))
    return dwg.tostring()
