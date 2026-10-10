# Polar Notes

Learn and Q&A about Python Polars. I already know R's tidyverse.

This is a Quarto Book. Prose chapters live under `contents/<topic>/*.qmd`; the
table of contents is `book.chapters` in `_quarto.yml` — a chapter is not part of
the book until it is listed there.

- `notebooks/`: Jupyter Notebooks for exploration. Not render in Quarto.

## Writing a chapter

- Targets Polars 2.x. Render one chapter with `uv run quarto render <file>`, the
  book with `uv run quarto render`.
- Parts are folders: `core/`, `transform/`, `types/`, `scale/` (later `program/`,
  `ecosystem/`, `qa/`). A stub has a `🚧 Stub` callout listing its planned
  scope; replace the callout when writing the chapter.
- Anatomy: **In tidyverse** (R code in ```` ```r ````, shown, never run) →
  **Mental model** (ASCII diagram) → **Mechanics** (runnable Polars, small to
  realistic) → **Where it bites** → **Recipes** → **See also**.
- Headings: YAML `title:` plus `##` sections. A `#` heading is numbered like a
  chapter.
- Data: `from pl_notes import datasets`, then `datasets.penguins()`,
  `datasets.flights()`, `airlines()`, `airports()`, `planes()`, `weather()`.
  Name frames `<subject>_df[_<stage>]`.
- Section IDs are global across the book, so prefix them per chapter
  (`{#sec-expr-*}`). Cheatsheet sections are `#sec-cs-*`.
- Go deeper than the cheatsheet, don't repeat it: link the cheatsheet section
  instead of copying its table.
- Error demos: `#| error: true`, plus a hidden `%xmode Minimal` cell so each
  error shows as one line.
- Back every claim about Polars behaviour with an executed cell, or verify it
  before writing.