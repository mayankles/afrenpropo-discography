# CLAUDE.md — Discography Archive

Instructions for writing annotated discography reports for this repository.

**You write YAML. A script renders the HTML.** Everything about how a report
*looks* — the stylesheet, era colours, escaping, star highlighting — belongs to
`scripts/render_report.py`, not to you. Your job is the research, the structure,
and the prose.

---

## What this repo is

A collection of discography reports. Each covers one artist's catalog, organized
by creative era, with personnel, instrumentation, producers, labels, and context.
`archive.html` auto-lists everything in `html/` via the GitHub API.

```
/
├── index.html          # Hit List: stats, current artist, sortable session table
├── archive.html        # auto-lists html/ via the GitHub API
├── stats.html          # ratings dashboard
├── data/
│   ├── ratings.json    # generated -- do not hand-edit
│   └── reports/        # YOU WRITE HERE: <artist_slug>.yaml
├── scripts/
│   ├── render_report.py    # YAML -> HTML. Owns all presentation.
│   ├── report_template.css # the stylesheet, one copy for every report
│   ├── club.py             # reads the club spreadsheet
│   └── artists.json        # artist name -> report slug
└── html/                   # GENERATED -- do not hand-edit
    └── <artist_slug>_discography.html
```

Reports are usually written by a scheduled GitHub Action and arrive as a pull
request, never merged unreviewed.

**Naming.** Write `data/reports/<artist_slug>.yaml`, lowercase snake_case:
`of_montreal.yaml`, `mars_volta.yaml`. The renderer derives
`html/<artist_slug>_discography.html` from that name.

**Legacy reports.** Eleven reports predate this format and exist only as
hand-written HTML in `html/`. Leave them alone unless asked to migrate one.

---

## The task

> Create a discography report for **[ARTIST]**.
> Highlight these albums: **[LIST]** (optional — may be none).
> Include side projects/other bands: **[yes/no]** (default: no, unless the
> artist's work is genuinely spread across multiple bands).

Deliverable: one YAML file in `data/reports/`.

---

## What you write

```yaml
artist: Talking Heads
subtitle: Musicians & Instrumentation (1977–1988)
synopsis:
  - >
    Paragraph 1 — origins, formation, who the creative core is.
  - >
    Paragraph 2 — the arc: eras, lineup changes, key collaborators.
  - >
    Paragraph 3 — later career, personal history where it shaped the work.
scope_note: >
  Scope: what's included and what's excluded, and why.
eras:
  - name: THE ENO TRILOGY
    years: 1978–1980
    descriptor: Funk, Paranoia & Polyrhythm
    columns: [Album / Year, Core Members, Collaborators / Producers, Label / Notes]
    albums:
      - title: Remain in Light
        year: 1980
        cells:
          - players:
              - {name: David Byrne, instrument: "vocals, guitar"}
              - {name: Chris Frantz, instrument: drums}
          - Brian Eno, producer; Adrian Belew (guitar)
          - Sire. Built at Compass Point from studio jams…
```

`data/reports/talking_heads.yaml` is a complete worked example — read it before
writing your first report.

### Field rules

- **`artist`** — the name as it should read, properly spelled and accented.
- **`subtitle`** — one line, e.g. `Musicians & Instrumentation (1997–2024)`.
- **`title`** — optional. Defaults to `<artist>: Studio Albums Discography`.
  Override only when that's wrong (e.g. `James Brown: Landmark Albums`).
- **`synopsis`** — a list of 3–4 paragraphs. See below.
- **`scope_note`** — required. See below.
- **`eras`** — 3–7 of them, in chronological order.

### Cells

`columns` lists every column header, including `Album / Year`. The first column
is built for you from `title`, `year` and `format`, so **`cells` has one fewer
entry than `columns`**, in the same order.

A cell is either prose, or a list of players:

```yaml
cells:
  - players:
      - {name: Tina Weymouth, instrument: "bass, keyboards"}
      - {name: Jerry Harrison}          # instrument optional
  - Sire. Context, sound, chart facts, notable tracks.
```

### Prose formatting

Write **markdown**, never HTML. `**bold**` for key names on first mention,
`*italic*` for album titles. Ampersands, angle brackets and accents are escaped
for you — type them literally. Never write `&amp;` or `<em>`.

---

## Report structure

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

`name` holds the era name, `years` the range, and `descriptor` a short tag that
reads after it — `descriptor: "The One" & Black Pride`.

Era colours are assigned automatically in order. Don't ask for one.

### Tables

Columns vary by artist — use what serves the material. Common shapes:

| Use case | Columns |
|---|---|
| Band with stable lineup | Album/Year · Core Members · Collaborators/Producers · Label/Notes |
| Solo artist | Album/Year · Artist's Role · Producers & Key Musicians · Label/Notes |
| Large ensemble (jazz) | Album/Year · Key Personnel · Notes |
| Multi-band artist | one era block per band/project |

Columns may differ between eras when the material calls for it — Weather Report
uses one column per instrument.

**Notes column** is where the value is. 1–4 sentences: what the record sounds
like, what happened during its making, chart/award facts, why it matters,
lineup changes, notable tracks. Be specific — "recorded in a Montreal church"
beats "atmospheric production."

---

## Special cases

**Highlighting is not your job.** The renderer matches the club's chosen albums
against your titles and applies the star and the highlight class. Never add
stars or highlight markers yourself. Just make sure every album the club is
listening to actually appears in the report — a missing one fails the build.

**Non-studio albums.** If a requested album is a live record, compilation or
side-project release, include it — don't refuse or drop it. Set `format:`:

```yaml
- title: Live at the Apollo
  year: 1963
  format: Live
```

Values: `Studio`, `Live`, `Live + Studio`, `Compilation`, `Soundtrack`, or a
credit line like `Fred Wesley & The J.B.'s`. **A tag renders wherever you set
`format`, and nowhere else.** Set it for anything that isn't a plain studio
album, and for collaborative billing. Don't put `format: Studio` on every row
unless the report genuinely needs that distinction drawn throughout.

`format` is the only place a badge can appear. Don't try to mark up the notes
prose — it's markdown, and any HTML in it will be escaped and shown literally.

**Multi-band artists.** For someone like Nick Cave, organize by project rather
than era. Set `project: true` on the section and give it a `description`:

```yaml
- name: The Birthday Party
  project: true
  description: One of post-punk's most violent, confrontational bands.
  columns: [Album / Year, Core Lineup, Notes]
```

**Enormous catalogs.** For artists with 50+ releases (James Brown, Miles Davis),
cover the landmarks rather than everything, and say so explicitly in the scope
note. Completeness is not the goal; usefulness is.

**Side projects.** Include them when the artist's work is genuinely distributed
across multiple bands. Otherwise mention them in the scope note and leave them
out.

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

---

## Voice

- Confident and specific. Assume a reader who knows music and wants detail.
- Warm, not academic. These are read aloud in listening groups.
- No hedging filler ("it could be argued that…"), no hype ("legendary
  masterpiece that changed everything forever").
- Concrete beats abstract: name the studio, the year, the person, the gear.

---

---

## Before you finish

Run the validator. It refuses to render until it's happy, and reports every
problem at once:

```
python3 scripts/render_report.py data/reports/<slug>.yaml --validate-only
```

**The renderer guarantees these — don't spend effort on them:** HTML escaping,
balanced tags, era colours and their order, star and highlight-class pairing,
format-tag suppression in single-format reports, the stylesheet.

**These are yours, and nothing can check them for you:**

- [ ] Album years, labels, personnel and producers verified against sources
- [ ] Synopsis is 3–4 narrative paragraphs with a point of view, not a summary
- [ ] Scope note states what was excluded *and why*
- [ ] Eras reflect real shifts and are named meaningfully
- [ ] Every album the club is listening to appears in the report
- [ ] Notes columns say something specific about each record
- [ ] Nothing invented — gaps written as "details limited"
