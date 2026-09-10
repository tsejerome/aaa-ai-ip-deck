# AAA 個人品牌 AI 講座 — web slide deck

- `deck_template.html` — the editable source (CSS + all slides + JS). Images are `__TOKENS__`.
- `assets/` — compressed images referenced by tokens (mapping lives in `assemble.py`).
- `assemble.py` — embeds assets as data URIs and writes `deck.html`.
- `deck.html` / `index.html` — the built, self-contained deck (index.html is what GitHub Pages serves).
- `source/` — original pptx, generated illustration PNGs, agent briefs.

Build and open:

    python3 assemble.py && open -a "Brave Browser" deck.html
