# Discography Archive

A growing collection of annotated discography reports — musicians, instrumentation, producers, labels, and the context behind the records.

**Live site:** `https://<your-username>.github.io/<your-repo>/`

## What's inside

Each report is a self-contained HTML page covering an artist's studio albums, organized by era, with full personnel and instrumentation credits. Reports currently include Weather Report, Stevie Wonder, Ween, of Montreal, and Arcade Fire — with more on the way.

## How it works

- All report pages live in the [`html/`](html/) folder.
- The landing page (`index.html`) queries the GitHub API at load time and **automatically lists every `.html` file** in `htmls/`. No manual link editing needed.
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
