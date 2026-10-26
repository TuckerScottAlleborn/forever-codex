# Forever Codex

A codex to *World of Warcraft: Forever* for Warcraft veterans, in books that share one design system. Static HTML, no build step for the pages themselves.

| Path | What it is |
| --- | --- |
| `index.html` | The codex's title page: the calendar and each book's table of contents |
| `lore/` | Book I, **The Lore**: what's canon, what's new and what's still unwritten, in three parts, plus an epilogue and reading stack |
| `classes/` | Book II, **The Classes**: how Forever changes the nine Alliance classes compared with Vanilla, with a narrated episode |
| `classes/<class>/` | Share pages with their own Discord/Open Graph embed; they forward to that class's sheet |
| `races/` | Book III, **The Races**: the five Alliance races against Vanilla after Blizzard's final October 26 racial pass, with race leans for every class and spec. The class sheets link into its leans |
| `codex.css`, `codex.js` | What every page shares: tokens (both themes), type, frames, the masthead, the sticky bar's shell and reading progress, action-bar slots, the "next book" card, the footer |

Each page links `codex.css` and keeps only its own layout inline. To add a book, add a folder with its own `index.html`, a link in every page's `.mast-books`, and an `<article class="book">` on the title page.

## Building

- `python og/build.py` (needs Edge and Pillow) regenerates the preview images (`og.png`, `lore/og.png`, `classes/og.png`, `races/og.png`, `classes/<class>/og.png`), the class share pages, and `favicon.ico` / `apple-touch-icon.png` from the hand-written `favicon.svg`.
- `python podcast/build.py` turns `podcast/script.md` into the chaptered episode at `classes/audio/forever-codex-classes.mp3`. It uses [Kokoro](https://github.com/thewh1teagle/kokoro-onnx) (voice `af_heart`, run on the CPU from `%LOCALAPPDATA%\kokoro-tts`), and writes the chapter timings into `classes/audio/chapters.json` and the `#podcast-data` block in `classes/index.html`. Each `## Title {#id}` heading in the script is a chapter whose id matches a section on the classes page. `--samples <voice> ...` renders short voice samples to `podcast/samples/`.

The race colors (`.c-human` and the rest in `codex.css`) are the codex's own, not Blizzard's. Racial values follow the October 26 pass; where an older guide disagrees, that pass wins.

Merged from the earlier Forever Lore Codex and Forever Class Codex sites.
