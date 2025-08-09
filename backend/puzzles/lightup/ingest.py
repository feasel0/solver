import base64, re
from typing import Any, Dict
from playwright.async_api import async_playwright
from .models import Puzzle, Given

def _decode_e(e: str) -> str:
    pad = '=' * (-len(e) % 4)
    return base64.b64decode((e + pad).encode()).decode()  # e.g. "0:9,446,906"

async def ingest_lightup(query: Dict[str, Any]) -> Dict[str, Any]:
    e = query.get("e")
    if not e:
        raise ValueError("Missing 'e' parameter for LightUp ingest")
    decoded = _decode_e(e)
    url = f"https://www.puzzle-light-up.com/?e={e}"

    async with async_playwright() as pw:
        br = await pw.chromium.launch()
        page = await br.new_page()
        await page.goto(url, wait_until="domcontentloaded")

        grid = await page.evaluate("""
            () => {
              const res = [];
              const tbl = document.querySelector('table, #board, .board');
              if (!tbl) return res;
              const trs = tbl.querySelectorAll('tr');
              for (const tr of trs) {
                const row = [];
                const tds = tr.querySelectorAll('td');
                for (const td of tds) {
                  const cl = td.className || '';
                  const m = cl.match(/black-(\d)/);
                  if (cl.includes('black')) row.push(m ? parseInt(m[1],10) : -1);
                  else row.push(null);
                }
                if (row.length) res.push(row);
              }
              return res;
            }
        """)
        html = await page.content()
        await br.close()

    rows, cols = 7, 7
    m = re.search(r'(\d+)\s*x\s*(\d+)', html)
    if m:
        rows, cols = int(m.group(1)), int(m.group(2))

    givens = []
    if grid and len(grid) and len(grid[0]):
        rows, cols = len(grid), len(grid[0])
        for r in range(rows):
            for c in range(cols):
                val = grid[r][c]
                if val is not None:
                    givens.append(Given(r=r, c=c, black=val))
    return Puzzle(rows=rows, cols=cols, givens=givens, source=url, external_id=decoded).model_dump()
