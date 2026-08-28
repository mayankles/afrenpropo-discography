# Discography Archive

A growing collection of annotated discography reports — musicians, instrumentation, producers, labels, and the context behind the records.

**Live site:** https://mayankles.github.io/afrenpropo-discography/ 

## What's inside

Each report is a self-contained HTML page covering an artist's studio albums, organized by era, with full personnel and instrumentation credits. Reports currently include Weather Report, Stevie Wonder, Ween, of Montreal, and Arcade Fire — with more on the way.

There's also a [Stats Lab](stats.html) page: ratings, taste correlations, genre averages, and every session ranked, rebuilt from the club's spreadsheet.

## How it works

- All report pages live in the [`html/`](html/) folder.
- The landing page (`index.html`) queries the GitHub API at load time and **automatically lists every `.html` file** in `html/`. No manual link editing needed.
- The [Stats Lab](stats.html) renders `data/ratings.json`, which is regenerated from the spreadsheet.
- Hosted free via GitHub Pages.

## Adding a new report

1. Drop the new `.html` file into the `html/` folder.
2. Commit and push (e.g. via GitHub Desktop).
3. The new report appears on the landing page automatically within a minute or two.

That's it — the landing page rebuilds its catalog every time someone visits.

## Enabling GitHub Pages (one-time setup)

1. Go to your repo's **Settings → Pages**.
2. Under **Source**, select the `main` branch and the `/ (root)` folder.
3. Save. Your site goes live at `https://<your-username>.github.io/<your-repo>/`.

## Notes

- The repo must be **public** for the GitHub API listing and Pages to work on a free account.
- Anonymous GitHub API calls are limited to 60/hour per visitor; for a personal archive this is plenty.
- Using a custom domain? Open `index.html` and set `MANUAL.owner` / `MANUAL.repo` near the top of the script.

## Automation

A scheduled GitHub Action keeps the archive in step with the club's spreadsheet.
It runs daily, and can be triggered by hand from the **Actions** tab.

Each run:

1. Downloads the spreadsheet as `.xlsx` — Google's export preserves manual cell
   fills, so no API key or service account is needed, only a link-viewable sheet.
2. Finds the row filled bright green (`#00FF00`), which is how the club marks the
   artist currently being listened to.
3. Recomputes every statistic from the raw per-member scores and commits
   `data/ratings.json` straight to `main`.
4. If that artist has no report in `html/`, asks Claude to write one and opens a
   **pull request**.

Reports arrive as pull requests rather than commits on purpose. They make factual
claims about real people, and generated prose needs a human to check it before it
goes on a public site. Statistics land directly because they're arithmetic.

The green row stays green for a fortnight, so the workflow skips the run if a
`report/<slug>` branch already exists — otherwise a daily schedule would open the
same pull request fourteen times.

### Setup

Two repository secrets, under **Settings → Secrets and variables → Actions**:

| Secret | What it is |
|---|---|
| `CLUB_SHEET_ID` | The spreadsheet's document id — the long string in its URL between `/d/` and `/edit`. A secret rather than a hardcoded value so the link isn't published with the repo. |
| `CLAUDE_CODE_OAUTH_TOKEN` | A Claude subscription token. Generate with `claude setup-token`; works on Pro. No API credits or Console account needed. |

You also need the [Claude GitHub App](https://github.com/apps/claude) installed on
the repo. Running `/install-github-app` from Claude Code does that and stores the
token for you.

Note that GitHub disables scheduled workflows on public repos after 60 days of
inactivity. If the club takes a break, re-run the workflow by hand from the
Actions tab to wake it up.

## Working with the data locally

```bash
pip install -r scripts/requirements.txt
```

Then, with `CLUB_SHEET_ID` set in your environment (or `--file some.xlsx` to read
a downloaded copy):

| Command | What it does |
|---|---|
| `python3 scripts/club.py check` | Prints the current artist and whether a report exists |
| `python3 scripts/club.py current` | The green-highlighted session, as JSON |
| `python3 scripts/club.py stats` | Regenerates `data/ratings.json` |
| `python3 scripts/club.py audit` | Every artist, its slug, and which have reports |

`audit` is the one to run when a report doesn't get picked up. Artist names in the
spreadsheet are messy — `The Mars Volta` has to resolve to `mars_volta`, `Béyonce`
to `beyonce` — and `scripts/artists.json` maps the awkward ones. Names not listed
there are slugified automatically: accents stripped, parentheticals dropped, a
leading "The" removed.

To preview the site locally, serve the folder and open `stats.html`:

```bash
python3 -m http.server 8899
```
