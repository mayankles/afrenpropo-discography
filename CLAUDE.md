# CLAUDE.md — Discography Archive

Instructions for generating annotated discography reports for this repository.
Written for Claude Code, but usable by any capable LLM.

---

## What this repo is

A collection of self-contained HTML discography reports. Each report covers one
artist's catalog, organized by creative era, with personnel, instrumentation,
producers, labels, and context. The landing page (`index.html`) auto-lists
everything in `html/` via the GitHub API — no manual linking needed.

```
/
├── index.html          # landing page (auto-lists html/ via GitHub API)
├── stats.html          # ratings dashboard, renders data/ratings.json
├── README.md
├── CLAUDE.md           # this file
├── data/
│   └── ratings.json    # generated -- do not hand-edit
├── scripts/
│   ├── club.py         # reads the club spreadsheet
│   └── artists.json    # artist name -> report slug
└── html/
    ├── arcade_fire_discography.html
    ├── james_brown_discography.html
    └── ...
```

Reports are sometimes written by a scheduled GitHub Action (see the README)
rather than by hand. Either way the spec below is the whole contract: filename,
structure, and the pre-commit checklist apply identically. An automated report
arrives as a pull request and is never merged unreviewed.

**Naming:** `<artist_name_snake_case>_discography.html`, all lowercase.
`of_montreal_discography.html`, `mars_volta_discography.html`. The landing page
prettifies these into display titles automatically.

---

## The task

> Create a discography report for **[ARTIST]**.
> Highlight these albums: **[LIST]** (optional — may be none).
> Include side projects/other bands: **[yes/no]** (default: no, unless the
> artist's work is genuinely spread across multiple bands).

Deliverable: one HTML file in `html/`. PDF only if asked.

---

## Report structure

Every report follows this order:

1. **`<h1>` title** — `Artist: Studio Albums Discography`
2. **`.subtitle`** — one line, e.g. `Musicians & Instrumentation (1997–2024)`
3. **`.synopsis`** — 3–4 paragraphs of narrative (see below) ending with a
   `.scope-note`
4. **Era sections** — an `<h3>` era header followed by a `<table>`, repeated
5. Nothing after the last table. No footer, no bottom legend.

### The synopsis (most important part)

This replaced an older format where context lived in a legend at the bottom.
Putting it up top means the reader gets the story *before* the data.

- **3–4 paragraphs**, roughly 120–200 words each.
- **Narrative, not bullet points.** Write it like good liner notes or a strong
  encyclopedia entry — specific, confident, warm, with a point of view about
  why the artist matters.
- Cover: origins and formation; who the creative core is and how the band
  actually works; the key collaborators and lineup changes that shaped the
  sound; the artistic arc across eras; the personal history where it's
  relevant to the music (deaths, breakups, illness, addiction, politics);
  and where things stand now.
- **Bold** key names on first mention. Use `<em>` for album titles.
- Don't sanitize. Deaths, breakups, addiction, allegations, and controversy
  belong in the story when they shaped the work — stated plainly and without
  sensationalism. Keep the focus on the music and the people who made it.
- Don't editorialize into hagiography either. "Widely regarded as" and
  "critically divisive" are more useful than "the greatest ever."

### The scope note

Last element inside `.synopsis`, styled small and italic. States exactly what
was included and excluded, and why. Non-negotiable — it's what makes the
reports trustworthy. Examples of decisions worth surfacing:

- Live albums, compilations, soundtracks, EPs, remix albums
- Collaborations and co-billed releases
- Albums credited to a side project or band member rather than the artist
- Posthumous or archival releases
- Anything with a contested classification

### Era sections

Group albums into **3–7 named eras** that reflect real creative or biographical
shifts — label changes, lineup changes, stylistic pivots, hiatuses. Name them
meaningfully (`THE QUINCY JONES TRILOGY`, `POST-WILL ERA`, `REUNION / CLOUDS
HILL ERA`), not generically (`PERIOD 2`).

Header format:

```html
<h3><span class="era-label funk">THE FUNK REVOLUTION (1965–1969)</span> "The One" &amp; Black Pride</h3>
```

The `era-label` span holds the era name and years; the text after it is a short
descriptive tag.

### Tables

Columns vary by artist — use what serves the material. Common shapes:

| Use case | Columns |
|---|---|
| Band with stable lineup | Album/Year · Core Members · Collaborators/Producers · Label/Notes |
| Solo artist | Album/Year · Artist's Role · Producers & Key Musicians · Label/Notes |
| Large ensemble (jazz) | Album/Year · Key Personnel · Notes |
| Multi-band artist | one table per band/project |

**Notes column** is where the value is. 1–4 sentences: what the record sounds
like, what happened during its making, chart/award facts, why it matters,
lineup changes, notable tracks. Be specific — "recorded in a Montreal church"
beats "atmospheric production."

---

## Highlighting

When albums are specified for highlighting:

1. Add `highlight-masterpiece` to the row's class list, after the era class:
   `<tr class="era-funk highlight-masterpiece">`
2. Prefix the album title with `⭐ `

```html
<tr class="era-funk highlight-masterpiece">
    <td class="year-album">⭐ The Payback<br/>1973</td>
```

The CSS uses `!important` on `border-left` so the gold bar overrides the era
color. If no albums are specified, omit the class entirely (the CSS can stay).

---

## Special cases

**Non-studio albums in the highlight list.** If a requested highlight is a live
album, compilation, or side-project release, include it — don't refuse or
silently drop it. Add a `.fmt` format tag under the album title so the
classification stays honest:

```html
<td class="year-album">⭐ Live at the Apollo<br/>1963<span class="fmt">Live</span></td>
```

Tags used: `Studio`, `Live`, `Live + Studio`, `Compilation`, `Soundtrack`, or a
credit line like `Fred Wesley &amp; The J.B.'s`. Only add `.fmt` tags when a
report actually mixes formats — don't clutter an all-studio report with
`Studio` on every row.

**Multi-band artists.** For someone like Nick Cave, organize by
**project rather than era** — a `.project-header` and `.project-desc` block per
band, each followed by its own table.

**Enormous catalogs.** For artists with 50+ releases (James Brown, Miles Davis),
cover the landmarks rather than everything, and say so explicitly in the scope
note. Completeness is not the goal; usefulness is.

**Side projects.** Include them when the artist's work is genuinely distributed
across multiple bands (Nick Cave, Mars Volta's J.B.'s-style spinoffs). Otherwise
mention them in the scope note and leave them out.

---

## Research standards

- **Search before writing.** Verify album years, lineups, producers, labels, and
  chart positions. Don't write from memory — catalogs get reissued,
  reclassified, and expanded, and lineup details are easy to get subtly wrong.
- **Check for recent releases.** Many of these artists are still active. Search
  for anything past your training cutoff.
- **Get the personnel right.** Who played what, who produced, who left when, and
  who guested. This is the core value of the reports.
- **Flag contested classifications** rather than quietly picking a side. If an
  album is arguably a compilation, say so in the scope note or the row's notes.
- **Never invent.** If you can't confirm a detail, write "details limited"
  rather than plausible-sounding filler. A gap is fine; a fabrication is not.
- **Don't quote reviews at length.** Paraphrase critical reception in your own
  words.

---

## Voice

- Confident and specific. Assume a reader who knows music and wants detail.
- Warm, not academic. These are read aloud in listening groups.
- No hedging filler ("it could be argued that…"), no hype ("legendary
  masterpiece that changed everything forever").
- Concrete beats abstract: name the studio, the year, the person, the gear.

---

## HTML template

Inline `<style>`, no JavaScript. The only external assets are the two Google Fonts
used across the rest of the site; every rule names a local fallback, so a report still
reads correctly offline.

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ARTIST - Studio Albums, Musicians &amp; Instrumentation</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,300;9..144,400;9..144,600;9..144,900&family=Spline+Sans+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
    :root {
        --bg: #17130f; --bg-card: #1f1a15; --bg-soft: #251f19;
        --ink: #f2e9db; --ink-dim: #a8997f; --amber: #e8b04b; --line: #3a3128;
    }
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
        font-family: 'Fraunces', Georgia, serif;
        background-color: var(--bg);
        background-image:
            radial-gradient(circle at 12% 18%, rgba(232,176,75,0.06), transparent 40%),
            radial-gradient(circle at 88% 82%, rgba(200,133,43,0.05), transparent 45%);
        background-attachment: fixed;
        color: var(--ink);
        padding: clamp(1rem, 3vw, 2.5rem);
        line-height: 1.6;
    }
    .container {
        max-width: 1500px; margin: 0 auto; background-color: var(--bg-card);
        padding: clamp(1.4rem, 3vw, 2.4rem); border: 1px solid var(--line);
        border-radius: 4px; box-shadow: 0 2px 28px rgba(0,0,0,0.45);
    }
    h1 {
        font-family: 'Fraunces', Georgia, serif; font-weight: 900; text-align: center;
        color: var(--ink); font-size: clamp(1.7rem, 4vw, 2.1rem);
        letter-spacing: -0.015em; margin-bottom: 10px; line-height: 1.1;
    }
    .subtitle {
        font-family: 'Spline Sans Mono', monospace; text-align: center;
        color: var(--ink-dim); margin-bottom: 32px; font-size: 11px;
        letter-spacing: 0.16em; text-transform: uppercase;
    }

    .synopsis {
        margin-bottom: 36px; padding: 22px 26px; background-color: var(--bg-soft);
        border-left: 4px solid var(--amber); border-radius: 4px;
        font-size: 14px; line-height: 1.85;
    }
    .synopsis p { margin-bottom: 14px; }
    .synopsis p:last-child { margin-bottom: 0; }
    .synopsis strong { color: var(--amber); font-weight: 600; }
    .synopsis em { color: var(--ink); font-style: italic; }
    .scope-note {
        font-family: 'Spline Sans Mono', monospace; font-size: 11px;
        color: var(--ink-dim); font-style: normal; margin-top: 22px; line-height: 1.7;
    }

    h3 {
        margin: 34px 0 10px; font-family: 'Fraunces', Georgia, serif;
        font-weight: 600; font-size: 17px; color: var(--ink);
    }

    table { width: 100%; border-collapse: collapse; font-size: 13px; margin-bottom: 30px; }
    thead { background-color: #2a231c; position: sticky; top: 0; }
    th {
        font-family: 'Spline Sans Mono', monospace; padding: 11px 9px; text-align: left;
        font-weight: 500; font-size: 10px; letter-spacing: 0.12em; text-transform: uppercase;
        color: var(--ink-dim); border-bottom: 1px solid var(--line);
    }
    td {
        padding: 11px 9px; border-bottom: 1px solid rgba(58,49,40,0.6);
        vertical-align: top; line-height: 1.7;
    }
    tbody tr:hover { background-color: rgba(232,176,75,0.05); }
    .year-album {
        font-family: 'Spline Sans Mono', monospace; font-weight: 500;
        color: var(--ink); width: 180px; font-size: 12px; line-height: 1.5;
    }
    .musician-role { display: block; margin-bottom: 2px; font-weight: 500; }
    .instrument {
        font-family: 'Spline Sans Mono', monospace; color: var(--ink-dim);
        font-size: 11px; font-style: normal;
    }

    .era-label {
        font-family: 'Spline Sans Mono', monospace; display: inline-block;
        padding: 3px 9px; border-radius: 3px; font-size: 10px; font-weight: 500;
        letter-spacing: 0.1em; margin-bottom: 8px; margin-right: 6px;
    }

    /* One era-* class per era, assigned in the order the eras appear.
       These seven are validated for this dark surface -- don't invent more. */
    .era-one   { border-left: 4px solid #4a93d8; }
    .era-two   { border-left: 4px solid #c9762f; }
    .era-three { border-left: 4px solid #b56fd0; }
    .era-four  { border-left: 4px solid #5aa832; }
    .era-five  { border-left: 4px solid #cf5566; }
    .era-six   { border-left: 4px solid #2aa294; }
    .era-seven { border-left: 4px solid #8f8ad4; }

    .era-label.one   { background-color: #273038; color: #96bad9; }
    .era-label.two   { background-color: #3e2b1a; color: #dbaa7c; }
    .era-label.three { background-color: #3a2937; color: #d0a6d5; }
    .era-label.four  { background-color: #2a341a; color: #9ec57e; }
    .era-label.five  { background-color: #3f2524; color: #df989b; }
    .era-label.six   { background-color: #21322c; color: #84c2b4; }
    .era-label.seven { background-color: #332e37; color: #bcb5d7; }

    .highlight-masterpiece {
        background-color: #392e1c;
        box-shadow: inset 0 0 10px rgba(232,176,75,0.12);
        border-left: 6px solid var(--amber) !important;
    }

    .fmt {
        font-family: 'Spline Sans Mono', monospace; display: inline-block;
        font-size: 9px; letter-spacing: 0.1em; text-transform: uppercase;
        color: var(--ink-dim); border: 1px solid var(--line); border-radius: 3px;
        padding: 1px 5px; margin-top: 5px;
    }

    .project-header {
        font-family: 'Fraunces', Georgia, serif; background-color: #2a231c;
        color: var(--ink); padding: 14px 18px; border-radius: 4px 4px 0 0;
        margin: 10px 0 0; font-size: 18px; font-weight: 600;
    }
    .project-desc {
        background-color: var(--bg-soft); padding: 12px 18px; font-size: 13px;
        color: var(--ink-dim); margin-bottom: 15px;
        border-left: 4px solid var(--line); line-height: 1.7;
    }

    /* Most reports still carry a legend after the final table rather than a
       synopsis at the top. Styled to match the synopsis so they read as
       deliberate; the left border is neutral rather than amber to rank it
       below a real synopsis. */
    .legend {
        margin-top: 30px; padding: 20px 24px; background-color: var(--bg-soft);
        border-left: 4px solid var(--line); border-radius: 4px;
        font-size: 13px; line-height: 1.8;
    }
    .legend > strong { color: var(--amber); font-weight: 600; }
    .legend-item { margin-bottom: 14px; }
    .legend-item:last-child { margin-bottom: 0; }
    .legend-item strong { color: var(--amber); font-weight: 600; }

    a { color: var(--amber); }

    @media (max-width: 700px) {
        body { padding: 0.6rem; }
        .container { padding: 1.1rem; }
        table { font-size: 12px; }
        .year-album { width: auto; min-width: 120px; }
    }
</style>
</head>
<body>
<div class="container">
    <h1>ARTIST: Studio Albums Discography</h1>
    <p class="subtitle">Musicians &amp; Instrumentation (YYYY&ndash;YYYY)</p>

    <div class="synopsis">
        <p>Paragraph 1 — origins, formation, who the creative core is.</p>
        <p>Paragraph 2 — the arc: eras, lineup changes, key collaborators.</p>
        <p>Paragraph 3 — later career, personal history where it shaped the work.</p>
        <p class="scope-note">Scope: what's included and what's excluded, and why.</p>
    </div>

    <h3><span class="era-label one">ERA NAME (YYYY&ndash;YYYY)</span> Short descriptor</h3>
    <table>
        <thead>
            <tr><th>Album / Year</th><th>Core Members</th><th>Collaborators / Producers</th><th>Label / Notes</th></tr>
        </thead>
        <tbody>
            <tr class="era-one">
                <td class="year-album">Album Title<br/>YYYY</td>
                <td><span class="musician-role">Name</span><span class="instrument">instrument</span></td>
                <td>Producer, guests</td>
                <td>Label. Context, sound, chart facts, notable tracks.</td>
            </tr>
        </tbody>
    </table>
</div>
</body>
</html>
```

### Palette

Assign era colors in slot order — `one` for the first era, `two` for the second, and so
on. Don't reorder them to "suit" the artist and don't invent new ones: the set is
validated against the dark background for contrast and color-blind separation, and the
order is what keeps consecutive eras distinguishable.

| Slot | Color | Border | Label bg | Label text |
|---|---|---|---|---|
| `one` | Blue | `#4a93d8` | `#273038` | `#96bad9` |
| `two` | Orange | `#c9762f` | `#3e2b1a` | `#dbaa7c` |
| `three` | Purple | `#b56fd0` | `#3a2937` | `#d0a6d5` |
| `four` | Green | `#5aa832` | `#2a341a` | `#9ec57e` |
| `five` | Rose | `#cf5566` | `#3f2524` | `#df989b` |
| `six` | Teal | `#2aa294` | `#21322c` | `#84c2b4` |
| `seven` | Periwinkle | `#8f8ad4` | `#332e37` | `#bcb5d7` |
| — | Gold (highlight) | `#e8b04b` | `#392e1c` | — |

---

## Before committing

- [ ] HTML validates — tags balanced, no stray `</div>`
- [ ] Filename is `<artist>_discography.html`, lowercase, in `html/`
- [ ] Synopsis is 3–4 narrative paragraphs, ending with a scope note
- [ ] No leftover legend or footer after the final table
- [ ] Every requested highlight has both `highlight-masterpiece` and `⭐`
- [ ] Era count is 3–7 and each era is meaningfully named
- [ ] Album years, labels, and personnel verified against sources
- [ ] Special characters HTML-escaped (`&amp;`, `&mdash;`, `&ndash;`, accents)
- [ ] Renders correctly when opened in a browser

Commit, push, and the landing page picks it up automatically.
