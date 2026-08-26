# CLAUDE.md — Discography Archive

Instructions for generating annotated discography reports for this repository.
Written for Claude Code, but usable by any capable LLM.

---

## What this repo is

A collection of self-contained HTML discography reports. Each report covers one
artist's catalog, organized by creative era, with personnel, instrumentation,
producers, labels, and context. The landing page (`index.html`) auto-lists
everything in `htmls/` via the GitHub API — no manual linking needed.

```
/
├── index.html          # landing page (auto-lists htmls/ via GitHub API)
├── README.md
├── CLAUDE.md           # this file
└── htmls/
    ├── arcade_fire_discography.html
    ├── james_brown_discography.html
    └── ...
```

**Naming:** `<artist_name_snake_case>_discography.html`, all lowercase.
`of_montreal_discography.html`, `mars_volta_discography.html`. The landing page
prettifies these into display titles automatically.

---

## The task

> Create a discography report for **[ARTIST]**.
> Highlight these albums: **[LIST]** (optional — may be none).
> Include side projects/other bands: **[yes/no]** (default: no, unless the
> artist's work is genuinely spread across multiple bands).

Deliverable: one HTML file in `htmls/`. PDF only if asked.

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

Self-contained: inline `<style>`, no external assets, no JavaScript.

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ARTIST - Studio Albums, Musicians &amp; Instrumentation</title>
<style>
    body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        margin: 20px; background-color: #f5f5f5; color: #333;
    }
    .container {
        max-width: 1500px; margin: 0 auto; background-color: white;
        padding: 30px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    h1 { text-align: center; color: #1a1a1a; margin-bottom: 10px; font-size: 28px; }
    .subtitle { text-align: center; color: #666; margin-bottom: 30px; font-size: 14px; }

    .synopsis {
        margin-bottom: 35px; padding: 20px 25px; background-color: #f9f9f9;
        border-left: 4px solid #2c3e50; border-radius: 4px;
        font-size: 13px; line-height: 1.75;
    }
    .synopsis p { margin-bottom: 12px; }
    .synopsis p:last-child { margin-bottom: 0; }
    .scope-note {
        font-size: 11px; color: #95a5a6; font-style: italic;
        margin-top: 20px; line-height: 1.6;
    }

    table { width: 100%; border-collapse: collapse; font-size: 12px; margin-bottom: 30px; }
    thead { background-color: #2c3e50; color: white; position: sticky; top: 0; }
    th { padding: 12px 8px; text-align: left; font-weight: 600; border-bottom: 2px solid #34495e; }
    td { padding: 10px 8px; border-bottom: 1px solid #ecf0f1; vertical-align: top; }
    tbody tr:hover { background-color: #f9f9f9; }
    .year-album { font-weight: 600; color: #2c3e50; width: 175px; }

    /* One era-* class per era; pick distinct colors from the palette below */
    .era-one   { border-left: 4px solid #8e44ad; }
    .era-two   { border-left: 4px solid #c0392b; }
    .era-three { border-left: 4px solid #2980b9; }
    .era-four  { border-left: 4px solid #e67e22; }
    .era-five  { border-left: 4px solid #27ae60; }
    .era-six   { border-left: 4px solid #16a085; }

    .era-label {
        display: inline-block; padding: 2px 8px; border-radius: 3px;
        font-size: 11px; font-weight: 600; margin-bottom: 8px;
    }
    .era-label.one   { background-color: #f4ecf7; color: #6c3483; }
    .era-label.two   { background-color: #fadbd8; color: #922b21; }
    .era-label.three { background-color: #d6eaf8; color: #1b4965; }
    .era-label.four  { background-color: #fef5e7; color: #b8680b; }
    .era-label.five  { background-color: #d5f4e6; color: #186a3b; }
    .era-label.six   { background-color: #d1f2eb; color: #0b5345; }

    .musician-role { display: block; margin-bottom: 2px; font-weight: 500; }
    .instrument { color: #7f8c8d; font-size: 11px; font-style: italic; }

    .highlight-masterpiece {
        background-color: #fff9e6;
        box-shadow: inset 0 0 8px rgba(230,200,50,0.3);
        border-left: 6px solid #f39c12 !important;
    }

    /* Only include when a report mixes album formats */
    .fmt {
        display: inline-block; font-size: 10px; letter-spacing: 0.06em;
        text-transform: uppercase; color: #7f8c8d; border: 1px solid #d5dbdb;
        border-radius: 3px; padding: 1px 5px; margin-top: 4px;
    }

    /* Only for multi-band artists organized by project */
    .project-header {
        background-color: #34495e; color: white; padding: 14px 18px;
        border-radius: 5px 5px 0 0; margin: 10px 0 0; font-size: 17px;
    }
    .project-desc {
        background-color: #ecf0f1; padding: 10px 18px; font-size: 12px;
        color: #555; margin-bottom: 15px; border-left: 4px solid #34495e;
        line-height: 1.6;
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

Assign era colors in order; any distinct subset is fine.

| Color | Border | Label bg | Label text |
|---|---|---|---|
| Purple | `#8e44ad` | `#f4ecf7` | `#6c3483` |
| Red | `#c0392b` | `#fadbd8` | `#922b21` |
| Blue | `#2980b9` | `#d6eaf8` | `#1b4965` |
| Orange | `#e67e22` | `#fef5e7` | `#b8680b` |
| Green | `#27ae60` | `#d5f4e6` | `#186a3b` |
| Teal | `#16a085` | `#d1f2eb` | `#0b5345` |
| Gold (highlight) | `#f39c12` | `#fff9e6` | — |

---

## Before committing

- [ ] HTML validates — tags balanced, no stray `</div>`
- [ ] Filename is `<artist>_discography.html`, lowercase, in `htmls/`
- [ ] Synopsis is 3–4 narrative paragraphs, ending with a scope note
- [ ] No leftover legend or footer after the final table
- [ ] Every requested highlight has both `highlight-masterpiece` and `⭐`
- [ ] Era count is 3–7 and each era is meaningfully named
- [ ] Album years, labels, and personnel verified against sources
- [ ] Special characters HTML-escaped (`&amp;`, `&mdash;`, `&ndash;`, accents)
- [ ] Renders correctly when opened in a browser

Commit, push, and the landing page picks it up automatically.
