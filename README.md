# Forever Codex

A codex to *World of Warcraft: Forever* for returning Warcraft veterans: what's different, set against the Vanilla they remember. Alliance side only, in books that share one design system. Static HTML, no build step for the pages themselves.

| Path | What it is |
| --- | --- |
| `index.html` | The landing page: who it's for, the calendar, what's different area by area (Vanilla beside Forever, each row pointing at its book), a "coming back as…" briefing for every Alliance class and race, then each book's table of contents |
| `lore/` | Book I, **The Lore**: what's canon, what's new and what's still unwritten, in three parts, plus an epilogue and reading stack |
| `classes/` | Book II, **The Classes**: how Forever changes the nine Alliance classes compared with Vanilla, with a narrated episode |
| `classes/<class>/` | Share pages with their own Discord/Open Graph embed; they forward to that class's sheet |
| `races/` | Book III, **The Races**: the five Alliance races against Vanilla after Blizzard's final October 26 racial pass, with race leans for every class and spec. The class sheets link into its leans |
| `companions/` | Book IV, **The Companions**: every companion pet within an Alliance character's reach, as a checklist (checks are kept in the browser's `localStorage` only), with the beta's drop counts, a collecting route, difficulty tiers and the unsolved ones |
| `world/` | Book V, **The World**: everything outside classes and races against Vanilla: the nine new dungeons and the old ones' keys and levels, the December raid tier, gear and stats, professions and camping, Legacy, transmog, regions and rulesets, what costs money, and PvP |
| `appendix/` | **The Appendix**: a dated patch log, a filterable glossary of every new and changed name against Vanilla, and common questions |
| `codex.css`, `codex.js` | What every page shares: tokens (both themes), type, frames, the masthead, the sticky bar's shell and reading progress, action-bar slots, the "vs Vanilla" tags, the "next book" card, the footer |

Each page links `codex.css` and keeps only its own layout inline. To add a book, add a folder with its own `index.html`, a link in every page's `.mast-books`, an `<article class="book">` and a row in `.diffs` on the landing page, and its date in the appendix's "how current" ledger.

Research briefs for ChatGPT deep research, and the reports they return, live in `research/`, which git ignores: working files, not site content.

## Building

- `python og/build.py` (needs Edge and Pillow) regenerates the preview images (`og.png`, `lore/og.png`, `classes/og.png`, `races/og.png`, `companions/og.png`, `world/og.png`, `appendix/og.png`, `classes/<class>/og.png`), the class share pages, and `favicon.ico` / `apple-touch-icon.png` from the hand-written `favicon.svg`.
- `python podcast/build.py` turns `podcast/script.md` into the chaptered episode at `classes/audio/forever-codex-classes.mp3`. It uses [Kokoro](https://github.com/thewh1teagle/kokoro-onnx) (voice `af_heart`, run on the CPU from `%LOCALAPPDATA%\kokoro-tts`), and writes the chapter timings into `classes/audio/chapters.json` and the `#podcast-data` block in `classes/index.html`. Each `## Title {#id}` heading in the script is a chapter whose id matches a section on the classes page. `--samples <voice> ...` renders short voice samples to `podcast/samples/`.

The race colors (`.c-human` and the rest in `codex.css`) are the codex's own, not Blizzard's. Racial values follow the October 26 pass; where an older guide disagrees, that pass wins.

Merged from the earlier Forever Lore Codex and Forever Class Codex sites.
