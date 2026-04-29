---
name: ads-update
description: Refresh per-platform references (meta, google, tiktok, linkedin, microsoft, apple, youtube) with the last 30 days of platform changes — features, deprecations, policy updates. COSTLY; gates on confirmation.
argument-hint: "meta | google | tiktok | linkedin | microsoft | apple | youtube | all"
license: MIT
allowed-tools: Bash, Read, Write, Edit, WebFetch, WebSearch, AskUserQuestion
---

# `/ads update <platform|all>` — Self-Refreshing Platform References

This skill regenerates per-platform reference files with what has actually changed in the last 30 days across each ad platform. Sources include Reddit, Hacker News, official platform changelogs, and the open web.

**Powered by an adapted version of [last30days-skill](https://github.com/mvanhorn/last30days-skill) (MIT, by Matt Van Horn). See `scripts/lib/THIRD_PARTY_NOTICES.md` for full attribution.**

---

## Step 0 — MANDATORY: Cost confirmation gate

**Before doing anything else**, you MUST:

1. Read the contents of `references/update-cost-warning.md` and print it verbatim to the user.
2. Compute the estimated token cost for the requested platform(s):
   - Single platform: **~50,000–150,000 tokens** at default depth
   - `all`: **~500,000+ tokens** at default depth
3. Call `AskUserQuestion` with this exact question and options:
   - Question: `"Run /ads update <platform>? Estimated cost: ~<N>k tokens. Proceed?"` (substitute `<platform>` and `<N>` with actuals)
   - Options:
     - `Proceed` (default depth) — run the requested mode at full cost
     - `Switch to quick depth` — same coverage, ~40% of the cost
     - `Cancel` — abort with no fetches
4. If the user picks `Cancel` or any answer other than `Proceed` / `Switch to quick depth`, **abort immediately** with a one-line message: "Cancelled. No sources fetched, no files written."

**Do not skip this step.** It exists to protect users on low-credit plans from accidentally burning their balance.

---

## Step 1 — Argument parsing

Accept exactly one argument from this enum:

`meta | google | tiktok | linkedin | microsoft | apple | youtube | all`

If the user invokes `/ads update` with no argument, ask them which platform via `AskUserQuestion` (don't default to `all` — that's the most expensive mode). If they pass an unknown value, list valid options and exit.

For `all`, loop the seven platforms **sequentially in this order**: `meta, google, tiktok, linkedin, microsoft, apple, youtube`. Sequential matters — parallel hits rate limits on the public APIs and makes cost unpredictable.

---

## Step 2 — Load source set for the platform

Run this Bash command to fetch the source configuration:

```bash
python3 scripts/ads_sources.py --list <platform>
```

Parse the JSON output. You'll get:

- `display_name` — human-readable platform name for the digest header
- `subreddits` — list of Reddit subs to query
- `changelog_urls` — official vendor release-note pages (use `WebFetch`)
- `search_queries` — phrased to surface industry-press coverage (use `WebSearch`)
- `hn_keywords` — terms to query against Hacker News
- `youtube_channels` / `x_handles` — optional, skip if no API keys

---

## Step 3 — Fetch sources

For each enabled source, fetch the last-30-days items. Depth-mode caps how many items per source:

| Source type | Quick | Default | Deep |
|---|---|---|---|
| Reddit (per sub) | 6 | 12 | 20 |
| Hacker News (per keyword) | 3 | 6 | 10 |
| WebFetch changelog URLs | all | all | all |
| WebSearch queries (per query) | 1 | 2 | 4 |

### Reddit (free, no key)

For each subreddit, run:

```bash
curl -s "https://www.reddit.com/r/<sub>/new.json?limit=25" -H "User-Agent: claude-ads/2.0"
```

Parse the JSON, keep only posts with `created_utc` within the last 30 days. Compute `published_at` from `created_utc` (Unix timestamp → YYYY-MM-DD). Capture `title`, `permalink`, `score`, `num_comments`, `upvote_ratio`, `selftext` (first 500 chars).

### Hacker News (free, no key)

For each keyword in `hn_keywords`, run:

```bash
curl -s "https://hn.algolia.com/api/v1/search_by_date?query=<keyword>&numericFilters=created_at_i>$(date -u -v-30d +%s)&hitsPerPage=10"
```

Capture `title`, `url`, `points`, `num_comments`, `created_at`.

### Official changelogs

For each URL in `changelog_urls`, use the `WebFetch` tool with this prompt: *"Extract any release notes, changelog entries, or feature announcements from the last 30 days. Return as a list of items with: title, date (YYYY-MM-DD), one-line summary, URL anchor if available."*

### Web search (industry press)

For each query in `search_queries` (capped per depth setting), use the `WebSearch` tool. Filter results client-side: prefer hits from `searchengineland.com`, `searchenginejournal.com`, `marketingland.com`, `martech.org`, `adweek.com`, vendor blogs.

---

## Step 4 — Score and dedupe (optional but recommended)

If you fetched 30+ items, run them through the vendored scoring lib for ranking. Otherwise, skip and order by `published_at` descending.

```bash
python3 -c "
import sys, json
sys.path.insert(0, 'scripts')
from lib import signals, dedupe
from lib.story import Story

raw = json.load(sys.stdin)
items = [Story(**r) for r in raw]
items = signals.annotate_stream(items)
items = dedupe.dedupe_items(items, threshold=0.7)
print(json.dumps([{'source': i.source, 'title': i.title, 'url': i.url, 'published_at': i.published_at, 'rank_score': i.rank_score} for i in items], indent=2))
"
```

---

## Step 5 — Render the digest

Write the output to `references/<platform>-changelog-30d.md` (overwrite if it exists). Use this exact structure:

```markdown
# <Display Name> — Last 30 Days

_Generated <YYYY-MM-DD> by `/ads update <platform>` (depth: <quick|default|deep>)_

> **What this is:** the last 30 days of changes to <platform> ads — features, deprecations, policy updates — pulled from official changelogs, practitioner discussion, and industry press.

## Official Changelog Entries

- [<title>](<url>) — <YYYY-MM-DD> — <1-line summary>
- ...

## Industry Press

- [<title>](<url>) — <YYYY-MM-DD> — <publisher> — <1-line summary>
- ...

## Community Discussion (Reddit / Hacker News)

- [<title>](<url>) — <YYYY-MM-DD> — r/<sub> or HN — <1-line summary>
- ...

---

_Sources fetched: <N> Reddit, <M> HN, <P> official changelog URLs, <Q> web searches. Deduped via hybrid Jaccard at threshold 0.7._
```

If a section has no items, print: `_No items found in the last 30 days from this source class._`

---

## Step 6 — Append to existing platform audit

After writing the changelog file, **append** (do not overwrite) a "Recent Updates" appendix to `references/<platform>-audit.md`. Keep it short — top 5 most-impactful items only:

```markdown

---

## Recent Updates (Last 30 Days)

_Auto-appended by `/ads update <platform>` on <YYYY-MM-DD>. See `references/<platform>-changelog-30d.md` for the full digest._

1. <impact> — [<title>](<url>) — <YYYY-MM-DD>
2. ...
```

If the audit file already has a "Recent Updates" appendix from a prior run, **replace it** rather than stacking duplicates. Match by the marker line `## Recent Updates (Last 30 Days)`.

---

## Step 7 — Confirm to the user

Print a one-line summary:

```
✓ /ads update <platform> complete — wrote references/<platform>-changelog-30d.md (<N> items) and appended top 5 to references/<platform>-audit.md.
```

For `all` mode, print this once per platform as you complete it, and a final summary line:

```
✓ /ads update all complete — refreshed 7 platforms.
```

---

## Failure modes

- **Reddit blocked / 429**: skip that subreddit, note in output. Don't retry — public Reddit JSON is best-effort.
- **WebFetch URL 404**: skip that changelog URL, note in output.
- **WebSearch returns nothing**: skip that query.
- **All sources empty for a platform**: still write the file with "No items found in the last 30 days" sections — gives the user explicit confirmation that the run completed.
- **User cancels mid-`all`**: stop the loop. Don't roll back already-written files (those are still valid, just partial coverage).

Never silently fail. Always print which sources succeeded and which were skipped.
