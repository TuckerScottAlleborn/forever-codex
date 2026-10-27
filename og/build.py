"""Builds the link-preview images, the class share pages and the icons.

  python og/build.py

Writes, relative to the site root:
  og.png                              the codex home's preview (from og/card.html)
  lore/og.png                         book I's preview (from og/lore-card.html)
  classes/og.png                      book II's preview (from og/classes-card.html)
  races/og.png                        book III's preview (from og/races-card.html)
  companions/og.png                   book IV's preview (from og/companions-card.html)
  appendix/og.png                     the appendix's preview (from og/appendix-card.html)
  classes/<class>/index.html          share page with its own Discord/OG embed, forwards to classes/#<class>
  classes/<class>/og.png              that class's preview (from og/class-card.html)
  favicon.ico, apple-touch-icon.png   raster copies of the hand-written favicon.svg
Rendering uses headless Edge; icons use Pillow.
"""
import html
import json
import shutil
import subprocess
import tempfile
import time
import urllib.parse
import uuid
from pathlib import Path

from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SITE = "https://tuckerscottalleborn.github.io/forever-codex/"
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

CLASSES = [
    dict(id="warrior", key=1, name="Warrior", color="#C69B6D", specs="Arms · Fury · Protection", dist=1.5, level="Low–moderate",
         card="The safest pick for Classic, just better."),
    dict(id="paladin", key=2, name="Paladin", color="#F48CBA", specs="Holy · Protection · Retribution", dist=4, level="Very high",
         card="One of the biggest overhauls in the game. A real healer, tank or Ret."),
    dict(id="hunter", key=3, name="Hunter", color="#AAD372", specs="Beast Mastery · Marksmanship · Survival", dist=3, level="High",
         card="Three trees that are now different ways to play. Survival is close to a new spec."),
    dict(id="rogue", key=4, name="Rogue", color="#FFF468", specs="Assassination · Combat · Subtlety", dist=2, level="Moderate",
         card="Classic Rogue with clearer specs, not a reinvention."),
    dict(id="priest", key=5, name="Priest", color="#FFFFFF", specs="Discipline · Holy · Shadow", dist=3, level="High",
         card="All three specs become much more complete. Disc is the one to relearn."),
    dict(id="shaman", key=6, name="Shaman", color="#0070DD", specs="Elemental · Enhancement · Restoration", dist=4, level="Very high",
         card="New to the Alliance as Dwarf Shaman, and heavily redesigned besides."),
    dict(id="mage", key=7, name="Mage", color="#3FC7EB", specs="Arcane · Fire · Frost", dist=3, level="High",
         card="The same Classic control chassis, now with an engine for each spec."),
    dict(id="warlock", key=8, name="Warlock", color="#8788EE", specs="Affliction · Demonology · Destruction", dist=3, level="High",
         card="The cleanest three-way spec split among the pure casters."),
    dict(id="druid", key=9, name="Druid", color="#FF7C0A", specs="Balance · Feral · Restoration", dist=4, level="Very high",
         card="Perhaps the deepest Classic-plus redesign. The changes reach the engine level."),
]


def render(src: Path, out: Path, fragment: str = "") -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    out.unlink(missing_ok=True)
    # not tempfile.mkdtemp: on Windows its owner-only ACL locks Edge's sandboxed child out of the
    # profile, and the screenshot is never written
    profile = Path(tempfile.gettempdir()) / f"og-edge-{uuid.uuid4().hex}"
    profile.mkdir()
    args = ["--headless=new", f"--user-data-dir={profile}", "--no-first-run", "--disable-gpu",
            "--hide-scrollbars", "--force-device-scale-factor=1", "--window-size=1200,630",
            "--virtual-time-budget=5000", f"--screenshot={out}", src.as_uri() + fragment]
    try:
        subprocess.run([EDGE] + args, check=True, capture_output=True, timeout=90)
        # msedge.exe can return before its headless child has written the file
        for _ in range(40):
            if out.exists():
                break
            time.sleep(0.5)
    finally:
        shutil.rmtree(profile, ignore_errors=True)
    if not out.exists():
        raise SystemExit(f"render failed: {out}")
    print("rendered", out.relative_to(ROOT))


def share_page(c: dict) -> str:
    url = f"{SITE}classes/{c['id']}/"
    title = f"{c['name']} · The Classes · Forever Codex"
    desc = f"{c['card']} Distance from Vanilla: {c['level']}. How WoW: Forever changes the {c['name']} compared with Vanilla."
    target = f"../#{c['id']}"
    e = html.escape
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:type" content="article">
<meta property="og:site_name" content="Forever Codex">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{url}og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{e(c['name'])}: {e(c['card'])}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:image" content="{url}og.png">
<meta name="theme-color" content="{c['color']}">
<link rel="icon" href="../../favicon.svg" type="image/svg+xml">
<link rel="icon" href="../../favicon.ico" sizes="32x32">
<link rel="apple-touch-icon" href="../../apple-touch-icon.png">
<meta http-equiv="refresh" content="0; url={target}">
<script>location.replace("{target}")</script>
<style>body{{margin:0;background:#0d0c14;color:#ece3cc;font:18px/1.5 Georgia,serif;display:grid;place-items:center;min-height:100vh;padding:16px;box-sizing:border-box}}a{{color:#f4c76b}}</style>
</head>
<body>
<p>Opening the <a href="{target}">{e(c['name'])} sheet in the Forever Codex</a>…</p>
</body>
</html>
"""


def bez(p0, p1, p2, p3, n=24):
    """Points along a cubic Bezier, for drawing favicon.svg's curves with Pillow."""
    pts = []
    for i in range(n + 1):
        t = i / n
        a, b, c, e = (1 - t) ** 3, 3 * (1 - t) ** 2 * t, 3 * (1 - t) * t ** 2, t ** 3
        pts.append((a * p0[0] + b * p1[0] + c * p2[0] + e * p3[0], a * p0[1] + b * p1[1] + c * p2[1] + e * p3[1]))
    return pts


def icons() -> None:
    # same geometry as favicon.svg (a 64-unit box)
    glass = (bez((18.5, 14), (18.5, 25), (29.5, 27.5), (29.5, 32)) + bez((29.5, 32), (29.5, 36.5), (18.5, 39), (18.5, 50))
             + bez((45.5, 50), (45.5, 39), (34.5, 36.5), (34.5, 32)) + bez((34.5, 32), (34.5, 27.5), (45.5, 25), (45.5, 14)))
    sand_top = [(22.5, 20), (41.5, 20)] + bez((41.5, 20), (39.5, 25), (34, 27.5), (32, 31.5)) + bez((32, 31.5), (30, 27.5), (24.5, 25), (22.5, 20))
    sand_bottom = bez((21.5, 50), (22.5, 43.5), (28, 40.5), (32, 39.7)) + bez((32, 39.7), (36, 40.5), (41.5, 43.5), (42.5, 50))

    def draw(size: int) -> Image.Image:
        k = size * 4 / 64
        s = round(64 * k)
        im = Image.new("RGBA", (s, s), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        pts = lambda ps: [(x * k, y * k) for x, y in ps]
        d.rounded_rectangle([0, 0, s - 1, s - 1], radius=12 * k, fill="#0d0c14")
        d.rectangle(pts([(14, 9), (50, 14)]), fill="#f4c76b")
        d.rectangle(pts([(14, 50), (50, 55)]), fill="#f4c76b")
        d.line(pts(glass + glass[:1]), fill="#cf9a52", width=round(3 * k), joint="curve")
        d.polygon(pts(sand_top), fill="#f4c76b")
        d.polygon(pts(sand_bottom), fill="#f4c76b")
        d.line(pts([(32, 31), (32, 40)]), fill="#f4c76b", width=max(1, round(1.6 * k)))
        return im.resize((size, size), Image.LANCZOS)

    draw(180).save(ROOT / "apple-touch-icon.png")
    draw(64).save(ROOT / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])
    print("wrote favicon.ico, apple-touch-icon.png")


def main() -> None:
    icons()
    render(HERE / "card.html", ROOT / "og.png")
    render(HERE / "lore-card.html", ROOT / "lore" / "og.png")
    render(HERE / "classes-card.html", ROOT / "classes" / "og.png")
    render(HERE / "races-card.html", ROOT / "races" / "og.png")
    render(HERE / "companions-card.html", ROOT / "companions" / "og.png")
    render(HERE / "appendix-card.html", ROOT / "appendix" / "og.png")
    for c in CLASSES:
        render(HERE / "class-card.html", ROOT / "classes" / c["id"] / "og.png", "#" + urllib.parse.quote(json.dumps(c)))
        (ROOT / "classes" / c["id"] / "index.html").write_text(share_page(c), encoding="utf-8", newline="\n")
        print("wrote", f"classes/{c['id']}/index.html")


if __name__ == "__main__":
    main()
