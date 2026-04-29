# `/ads update` — Cost & Credit Warning

> **Read this before running `/ads update`. It is the most credit-intensive command in claude-ads.**

`/ads update` refreshes per-platform reference files with the last 30 days of changes by aggregating sources from:

- **Reddit JSON API** (free, no key) — practitioner subreddits per platform
- **Hacker News Algolia API** (free, no key) — keyword-filtered to ad-tech topics
- **Official platform changelogs** — vendor release notes (Google Ads, Meta Marketing API, TikTok / LinkedIn / Microsoft / Apple Ads)
- **Web search** — industry press fallback (Search Engine Land, AdWeek, etc.)

For each platform, this means **20–50 outbound HTTP requests** plus LLM synthesis to produce the digest.

## Estimated cost per run

| Mode | Platforms covered | Approx. tokens | Approx. minutes |
|---|---|---|---|
| `/ads update <one platform>` | 1 | ~50,000–150,000 | 2–5 min |
| `/ads update all` | 7 (loops sequentially) | ~500,000+ | 15–30 min |

Estimates assume `--depth default`. Quick mode (`--depth quick`) is roughly **40% of the above**; deep mode (`--depth deep`) is roughly **2× the above**.

## Recommendations

1. **If you're on a low-credit plan**, run per platform — never `all`.
2. **Use Sonnet, not Opus**, for `/ads update` runs. Opus is overkill for synthesis-from-citations work and costs ~5× more.
3. **Refresh monthly, not daily.** The reference data is dated `Last 30 Days`; rerunning the next day produces near-identical output and burns credits for nothing.
4. **Cancel is always safe.** The skill writes per-platform files atomically — interrupting mid-`all` leaves earlier platforms' digests intact.

## Confirmation

The skill will ask for explicit confirmation before fetching. You can:

- **Proceed** — run the requested mode at the cost estimated above
- **Switch to quick depth** — same coverage, ~40% of the cost
- **Cancel** — abort with no fetches made

Pick **Cancel** if you're unsure. References are still fully usable without an `/ads update` run.
