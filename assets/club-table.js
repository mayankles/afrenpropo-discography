/* Shared "every session, ranked" table.
 *
 * Used by index.html and stats.html. Sortable on every column; the Average
 * value is coloured on a diverging scale anchored at the club's own mean, so
 * the colour says "better or worse than we usually rate things" rather than
 * "high or low on an abstract 0-10". Every stop on that scale clears 4.5:1
 * against the card background.
 */
(function (global) {
  "use strict";

  const LOW = "#e0808c", MID = "#a8997f", HIGH = "#93cf6a";

  const hx = c => { c = c.replace("#", ""); return [0, 2, 4].map(i => parseInt(c.slice(i, i + 2), 16)); };
  const hs = a => "#" + a.map(v => Math.max(0, Math.min(255, Math.round(v))).toString(16).padStart(2, "0")).join("");
  const mix = (a, b, t) => { const A = hx(a), B = hx(b); return hs(A.map((v, i) => v + (B[i] - v) * t)); };

  const esc = s => String(s).replace(/[&<>"]/g, c =>
    ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));

  /* Diverging ramp: min -> mean -> max, neutral at the mean. */
  function ratingColour(v, min, mean, max) {
    if (v == null) return "var(--ink-dim)";
    if (v <= mean) {
      const span = mean - min;
      return mix(LOW, MID, span <= 0 ? 1 : Math.max(0, Math.min(1, (v - min) / span)));
    }
    const span = max - mean;
    return mix(MID, HIGH, span <= 0 ? 0 : Math.max(0, Math.min(1, (v - mean) / span)));
  }

  /* Columns are declared once; sorting reads its key straight off the row. */
  function columns(members) {
    return [
      { key: "artist",    label: "Artist",    type: "text" },
      { key: "submitter", label: "Picked by", type: "text" },
      { key: "genre",     label: "Genre",     type: "text" },
      { key: "start",     label: "Date",      type: "text" },
      { key: "average",   label: "Average",   type: "num", numeric: true },
      ...members.map(m => ({ key: "score:" + m, label: m, type: "num", numeric: true })),
      { key: "stdev",     label: "Spread",    type: "num", numeric: true }
    ];
  }

  const valueOf = (row, key) =>
    key.startsWith("score:") ? (row.scores[key.slice(6)] ?? null) : (row[key] ?? null);

  /* Nulls always sink, whichever direction the sort runs. */
  function compare(a, b, col, dir) {
    const x = valueOf(a, col.key), y = valueOf(b, col.key);
    if (x == null && y == null) return 0;
    if (x == null) return 1;
    if (y == null) return -1;
    const r = col.type === "num" ? x - y : String(x).localeCompare(String(y));
    return dir === "asc" ? r : -r;
  }

  function render(mount, data, opts) {
    const options = opts || {};
    const members = data.members;
    const cols = columns(members);
    const rated = data.ranked.filter(r => r.average != null).map(r => r.average);
    const min = Math.min(...rated), max = Math.max(...rated);
    const mean = data.overall_average ?? (min + max) / 2;

    let sortKey = options.sortKey || "average";
    let sortDir = options.sortDir || "desc";

    const scroller = document.createElement("div");
    scroller.className = "table-scroll";
    mount.appendChild(scroller);

    function draw() {
      const col = cols.find(c => c.key === sortKey) || cols[4];
      const rows = data.ranked.slice().sort((a, b) => compare(a, b, col, sortDir));
      scroller.innerHTML = `<table class="session-table">
        <thead><tr>${cols.map(c => {
          const on = c.key === sortKey;
          return `<th class="${c.numeric ? "num" : ""}${on ? " sorted" : ""}"
                      data-key="${c.key}" tabindex="0" role="button"
                      aria-sort="${on ? (sortDir === "asc" ? "ascending" : "descending") : "none"}"
                      title="Sort by ${esc(c.label)}">${esc(c.label)}<span class="arrow">${
                        on ? (sortDir === "asc" ? "↑" : "↓") : "↕"}</span></th>`;
        }).join("")}</tr></thead>
        <tbody>${rows.map(r => `<tr>
          <td class="artist-cell">${r.has_report
            ? `<a href="${options.reportBase || "./html/"}${r.slug}_discography.html">${esc(r.artist)}</a>`
            : `<span class="no-report">${esc(r.artist)}</span>`}</td>
          <td class="nowrap"><span class="who-dot" style="background:${
            options.colourOf ? options.colourOf(r.submitter) : "var(--ink-dim)"}"></span>${esc(r.submitter ?? "—")}</td>
          <td class="dim">${esc(r.genre ?? "—")}</td>
          <td class="dim nowrap">${r.start ?? "—"}</td>
          <td class="num"><b style="color:${ratingColour(r.average, min, mean, max)}">${
            r.average != null ? r.average.toFixed(2) : "—"}</b></td>
          ${members.map(m => `<td class="num">${
            r.scores[m] != null ? r.scores[m].toFixed(2) : "—"}</td>`).join("")}
          <td class="num dim">${r.stdev != null ? r.stdev.toFixed(2) : "—"}</td>
        </tr>`).join("")}</tbody></table>`;

      scroller.querySelectorAll("th").forEach(th => {
        const activate = () => {
          const key = th.dataset.key;
          // First click on a new column sorts the way that column is most
          // useful: high-to-low for numbers, A-Z for text.
          if (key === sortKey) sortDir = sortDir === "asc" ? "desc" : "asc";
          else { sortKey = key; sortDir = cols.find(c => c.key === key).type === "num" ? "desc" : "asc"; }
          draw();
        };
        th.addEventListener("click", activate);
        th.addEventListener("keydown", e => {
          if (e.key === "Enter" || e.key === " ") { e.preventDefault(); activate(); }
        });
      });
    }
    draw();
  }

  global.ClubTable = { render, ratingColour };
})(window);
