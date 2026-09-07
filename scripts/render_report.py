#!/usr/bin/env python3
"""
Render a discography report from YAML to HTML.

Claude writes the YAML -- research, structure and prose. This owns everything
else: the stylesheet, era colours, HTML escaping, format tags, and matching the
club's chosen albums to the rows that should be highlighted.

That split exists because every failure this pipeline has had was a formatting
instruction going wrong rather than research going wrong. Here, the pre-commit
checklist stops being a checklist: escaping, tag balance, colour order and the
star/class pairing are structural rather than things to remember.

    render_report.py data/reports/dolly_parton.yaml
    render_report.py <yaml> --highlight "Jolene; Coat of Many Colors"
    render_report.py <yaml> --validate-only
"""

from __future__ import annotations

import argparse
import difflib
import html
import re
import sys
import unicodedata
from pathlib import Path

import yaml

SCRIPTS = Path(__file__).resolve().parent
REPO = SCRIPTS.parent
TEMPLATE_CSS = SCRIPTS / "report_template.css"
REPORT_DIR = REPO / "html"

# Slot order is fixed: these seven are validated against the dark background for
# contrast and colour-blind separation, and the order keeps adjacent eras apart.
ERA_SLOTS = ["one", "two", "three", "four", "five", "six", "seven"]

FUZZY_THRESHOLD = 0.85          # 'eruope 72' -> 'Europe 72' scores 0.90


class ReportError(RuntimeError):
    """The YAML does not describe a report we can render."""


# --------------------------------------------------------------------------
# Text
# --------------------------------------------------------------------------

def inline(text) -> str:
    """Escape HTML, then allow a tiny markdown subset: **bold** and *italic*.

    Authoring prose as markdown rather than HTML means a report cannot ship
    malformed tags, and unconverted literal asterisks -- which two hand-written
    reports shipped with -- become impossible.
    """
    s = html.escape("" if text is None else str(text), quote=False)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s, flags=re.S)
    s = re.sub(r"(?<!\*)\*([^*\n]+?)\*(?!\*)", r"<em>\1</em>", s)
    return s


def normalize_title(s) -> str:
    """Fold an album title for comparison.

    Spreadsheet cells carry band attributions in parentheses, curly
    apostrophes, stray case and the odd typo; report titles do not.
    """
    s = unicodedata.normalize("NFKD", str(s))
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.replace("’", "'").replace("…", "...")
    s = re.sub(r"\([^)]*\)", " ", s)
    s = re.sub(r"[^a-z0-9']+", " ", s.lower()).strip()
    return re.sub(r"^(the|a)\s+", "", s)


# --------------------------------------------------------------------------
# Loading and validation
# --------------------------------------------------------------------------

def load(path: Path) -> dict:
    try:
        with open(path, encoding="utf-8") as fh:
            data = yaml.safe_load(fh)
    except yaml.YAMLError as exc:
        raise ReportError(f"{path.name} is not valid YAML: {exc}") from exc
    if not isinstance(data, dict):
        raise ReportError(f"{path.name} should contain a mapping, got {type(data).__name__}")
    return data


def validate(r: dict) -> list[str]:
    """Return every problem found, so one run fixes them all rather than one."""
    errs: list[str] = []
    add = errs.append

    for field in ("artist", "subtitle", "scope_note"):
        if not str(r.get(field) or "").strip():
            add(f"missing required field: {field}")

    syn = r.get("synopsis") or []
    if not isinstance(syn, list):
        add("synopsis must be a list of paragraphs")
    elif not 3 <= len(syn) <= 4:
        add(f"synopsis has {len(syn)} paragraphs, CLAUDE.md asks for 3-4")

    eras = r.get("eras") or []
    if not isinstance(eras, list) or not eras:
        add("no eras listed")
        return errs
    if not 3 <= len(eras) <= 7:
        add(f"{len(eras)} eras, CLAUDE.md asks for 3-7 "
            f"(and only {len(ERA_SLOTS)} colour slots exist)")

    seen: dict[str, str] = {}
    for i, era in enumerate(eras, 1):
        where = f"era {i} ({era.get('name', 'unnamed')!r})"
        if not str(era.get("name") or "").strip():
            add(f"{where}: missing name")
        cols = era.get("columns") or []
        if len(cols) < 2:
            add(f"{where}: needs at least 2 columns, got {len(cols)}")
        albums = era.get("albums") or []
        if not albums:
            add(f"{where}: no albums")
        for album in albums:
            title = str(album.get("title") or "").strip()
            if not title:
                add(f"{where}: an album has no title")
                continue
            key = normalize_title(title)
            if key in seen:
                add(f"{where}: {title!r} also appears in {seen[key]}")
            seen[key] = where
            year = album.get("year")
            if not isinstance(year, int) or not 1900 <= year <= 2100:
                add(f"{where}: {title!r} has year {year!r}, expected a plausible integer")
            cells = album.get("cells")
            if not isinstance(cells, list):
                add(f"{where}: {title!r} has no cells list")
            elif len(cells) != len(cols) - 1:
                add(f"{where}: {title!r} has {len(cells)} cells but "
                    f"{len(cols)} columns (expected {len(cols) - 1}, "
                    f"the first column is built from title/year)")
    return errs


def all_albums(r: dict):
    for era in r.get("eras") or []:
        for album in era.get("albums") or []:
            yield era, album


# --------------------------------------------------------------------------
# Highlight matching
# --------------------------------------------------------------------------

def match_highlights(r: dict, requested: list[str]) -> tuple[set[str], list[str]]:
    """Map the club's album strings onto report rows.

    An album the club listened to that is missing from the report is a real
    inconsistency, not a highlighting nicety, so it is reported as an error
    rather than silently skipped.
    """
    titles = {normalize_title(a["title"]): a["title"] for _, a in all_albums(r)}
    matched: set[str] = set()
    errs: list[str] = []
    for want in requested:
        key = normalize_title(want)
        if not key:
            continue
        if key in titles:
            matched.add(titles[key])
            continue
        close = difflib.get_close_matches(key, list(titles), n=1, cutoff=FUZZY_THRESHOLD)
        if close:
            matched.add(titles[close[0]])
            print(f"  matched {want!r} -> {titles[close[0]]!r} (fuzzy)", file=sys.stderr)
        else:
            best = difflib.get_close_matches(key, list(titles), n=2, cutoff=0.4)
            hint = f" Closest: {', '.join(titles[b] for b in best)}." if best else ""
            errs.append(f"album {want!r} is not in the report, so it cannot be "
                        f"highlighted.{hint}")
    return matched, errs


# --------------------------------------------------------------------------
# Rendering
# --------------------------------------------------------------------------

def render_cell(cell) -> str:
    """A cell is prose, or a list of players rendered name-over-instrument."""
    if isinstance(cell, dict) and "players" in cell:
        out = []
        for p in cell["players"] or []:
            out.append(f'<span class="musician-role">{inline(p.get("name"))}</span>')
            if p.get("instrument"):
                out.append(f'<span class="instrument">{inline(p["instrument"])}</span>')
        return "".join(out)
    if isinstance(cell, list):                       # bare list of names
        return "".join(f'<span class="musician-role">{inline(x)}</span>' for x in cell)
    return inline(cell)


def render(r: dict, highlights: set[str]) -> str:
    css = TEMPLATE_CSS.read_text(encoding="utf-8").rstrip()
    artist = str(r["artist"]).strip()
    title = str(r.get("title") or f"{artist}: Studio Albums Discography").strip()

    out: list[str] = []
    w = out.append
    w("<!DOCTYPE html>")
    w('<html lang="en">')
    w("<head>")
    w('<meta charset="UTF-8">')
    w('<meta name="viewport" content="width=device-width, initial-scale=1.0">')
    w(f"<title>{inline(artist)} - Studio Albums, Musicians &amp; Instrumentation</title>")
    w('<link rel="preconnect" href="https://fonts.googleapis.com">')
    w('<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>')
    w('<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,300;'
      '9..144,400;9..144,600;9..144,900&family=Spline+Sans+Mono:wght@400;500&display=swap" '
      'rel="stylesheet">')
    w(f"<style>\n{css}\n</style>")
    w("</head>")
    w("<body>")
    w('<div class="container">')
    w(f"    <h1>{inline(title)}</h1>")
    w(f'    <p class="subtitle">{inline(r["subtitle"])}</p>')

    w('\n    <div class="synopsis">')
    for para in r.get("synopsis") or []:
        w(f"        <p>{inline(str(para).strip())}</p>")
    w(f'        <p class="scope-note">{inline(str(r["scope_note"]).strip())}</p>')
    w("    </div>")

    for i, era in enumerate(r["eras"]):
        slot = ERA_SLOTS[i % len(ERA_SLOTS)]
        name, years = inline(era.get("name")), str(era.get("years") or "").strip()
        label = f"{name} ({inline(years)})" if years else name
        w("")
        if era.get("project"):
            w(f'    <h2 class="project-header">{name}</h2>')
            if era.get("description"):
                w(f'    <div class="project-desc">{inline(era["description"])}</div>')
        else:
            desc = inline(era.get("descriptor") or "")
            w(f'    <h3><span class="era-label {slot}">{label}</span> {desc}</h3>'.rstrip())
        w("    <table>")
        w("        <thead>")
        w("            <tr>" + "".join(f"<th>{inline(c)}</th>" for c in era["columns"]) + "</tr>")
        w("        </thead>")
        w("        <tbody>")
        for album in era["albums"]:
            title_txt = str(album["title"]).strip()
            starred = title_txt in highlights
            classes = f"era-{slot}" + (" highlight-masterpiece" if starred else "")
            star = "⭐ " if starred else ""
            # A tag appears only where the author set one. The field carries
            # either a format ("Live") or a credit line ("Dolly Parton, Emmylou
            # Harris & Linda Ronstadt"), and whether a distinction is worth
            # drawing is the author's call, not a heuristic's.
            fmt = (f'<span class="fmt">{inline(album["format"])}</span>'
                   if str(album.get("format") or "").strip() else "")
            w(f'            <tr class="{classes}">')
            w(f'                <td class="year-album">{star}{inline(title_txt)}'
              f'<br/>{album["year"]}{fmt}</td>')
            for cell in album.get("cells") or []:
                w(f"                <td>{render_cell(cell)}</td>")
            w("            </tr>")
        w("        </tbody>")
        w("    </table>")

    w("</div>")
    w("</body>")
    w("</html>")
    return "\n".join(out) + "\n"


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("yaml_file")
    ap.add_argument("--out", help="output path (default html/<stem>_discography.html)")
    ap.add_argument("--highlight", default="",
                    help="'; '-separated albums the club chose this session")
    ap.add_argument("--validate-only", action="store_true")
    args = ap.parse_args(argv)

    src = Path(args.yaml_file)
    try:
        report = load(src)
    except ReportError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    errs = validate(report)
    requested = [p.strip() for p in args.highlight.split(";") if p.strip()]
    highlights: set[str] = set()
    if not errs and requested:
        highlights, match_errs = match_highlights(report, requested)
        errs += match_errs

    if errs:
        print(f"{src.name}: {len(errs)} problem(s)", file=sys.stderr)
        for e in errs:
            print(f"  - {e}", file=sys.stderr)
        return 1

    albums = sum(1 for _ in all_albums(report))
    if args.validate_only:
        print(f"{src.name}: OK -- {len(report['eras'])} eras, {albums} albums, "
              f"{len(highlights)} highlighted")
        return 0

    out = Path(args.out) if args.out else REPORT_DIR / f"{src.stem}_discography.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render(report, highlights), encoding="utf-8")
    try:
        shown = out.relative_to(REPO)
    except ValueError:
        shown = out
    print(f"Wrote {shown} -- {len(report['eras'])} eras, {albums} albums, "
          f"{len(highlights)} highlighted")
    return 0


if __name__ == "__main__":
    sys.exit(main())
