#!/usr/bin/env python3
"""CLI helper for /ads update.

Two modes:
  --dry-run   Print the planned source list + date range + estimated cost.
              No HTTP fetches. Used for verification and the cost-warning preview.
  --prep      Write a research-plan stub to references/<platform>-changelog-30d.md
              that the SKILL.md prompt then fills in via WebFetch/WebSearch.

This script does NOT do the WebFetch/WebSearch fetching itself — those are
Claude Code tools, called from the skill prompt. This script's job is to
configure the run and emit the scaffold.

For Reddit JSON and Hacker News Algolia (which are free public APIs), see
the skill prompt for the curl commands; we don't run them here to keep this
script side-effect-free in --dry-run.

Usage:
    python3 scripts/run_update.py --platform meta --dry-run
    python3 scripts/run_update.py --platform google --depth default --prep
    python3 scripts/run_update.py --platform all --depth quick --prep
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path

# Local imports
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from ads_sources import PLATFORM_SOURCES, SUPPORTED_PLATFORMS, get_sources  # noqa: E402
from lib import dates  # noqa: E402

DEPTH_SETTINGS: dict[str, dict[str, int]] = {
    "quick":   {"reddit_per_sub": 6,  "hn_per_keyword": 3,  "search_per_query": 1},
    "default": {"reddit_per_sub": 12, "hn_per_keyword": 6,  "search_per_query": 2},
    "deep":    {"reddit_per_sub": 20, "hn_per_keyword": 10, "search_per_query": 4},
}

COST_ESTIMATES_TOKENS: dict[str, tuple[int, int]] = {
    # depth -> (per_platform_low, per_platform_high)
    "quick":   (20_000, 60_000),
    "default": (50_000, 150_000),
    "deep":    (100_000, 300_000),
}


def estimate_fetches(platform: str, depth: str) -> dict[str, int]:
    """Approximate count of outbound HTTP requests for a single platform run."""
    src = get_sources(platform)
    s = DEPTH_SETTINGS[depth]
    return {
        "reddit_requests": len(src.subreddits),  # 1 request per sub (limit=25 fits all needs)
        "hn_requests": len(src.hn_keywords),
        "webfetch_requests": len(src.changelog_urls),
        "websearch_requests": len(src.search_queries) * s["search_per_query"],
    }


def _resolve_platforms(platform_arg: str) -> list[str]:
    if platform_arg == "all":
        return list(SUPPORTED_PLATFORMS)
    if platform_arg not in SUPPORTED_PLATFORMS:
        raise SystemExit(
            f"Unknown platform '{platform_arg}'. Supported: {', '.join(SUPPORTED_PLATFORMS)} | all"
        )
    return [platform_arg]


def cmd_dry_run(platform_arg: str, depth: str) -> None:
    platforms = _resolve_platforms(platform_arg)
    fr, to = dates.get_date_range(30)
    cost_low, cost_high = COST_ESTIMATES_TOKENS[depth]

    plan = {
        "platforms": platforms,
        "date_range": {"from": fr, "to": to, "days": 30},
        "depth": depth,
        "depth_settings": DEPTH_SETTINGS[depth],
        "per_platform": {p: estimate_fetches(p, depth) for p in platforms},
        "cost_estimate_tokens": {
            "per_platform_low": cost_low,
            "per_platform_high": cost_high,
            "total_low": cost_low * len(platforms),
            "total_high": cost_high * len(platforms),
        },
        "sources": {p: asdict(get_sources(p)) for p in platforms},
    }
    print(json.dumps(plan, indent=2))


def _stub_markdown(platform: str, depth: str, today: str) -> str:
    src = get_sources(platform)
    return f"""# {src.display_name} — Last 30 Days

_Generated {today} by `/ads update {platform}` (depth: {depth}) — STUB, awaiting fetches_

> **What this is:** the last 30 days of changes to {src.display_name} — features, deprecations, policy updates — pulled from official changelogs, practitioner discussion, and industry press.

> **Note:** this file was scaffolded by `scripts/run_update.py --prep`. The skill prompt will fill in the sections below by calling WebFetch on the changelog URLs and WebSearch on the queries listed in `scripts/ads_sources.py`.

## Official Changelog Entries

<!-- Fill via WebFetch on each URL in PLATFORM_SOURCES["{platform}"].changelog_urls -->

_Pending fetch._

## Industry Press

<!-- Fill via WebSearch on each query in PLATFORM_SOURCES["{platform}"].search_queries -->

_Pending fetch._

## Community Discussion (Reddit / Hacker News)

<!-- Fill via curl https://www.reddit.com/r/<sub>/new.json (per sub) and HN Algolia (per keyword) -->

_Pending fetch._

---

_Sources planned: {len(src.subreddits)} subreddits, {len(src.hn_keywords)} HN keywords, {len(src.changelog_urls)} changelog URLs, {len(src.search_queries)} search queries._
"""


def cmd_prep(platform_arg: str, depth: str, out_dir: Path) -> None:
    platforms = _resolve_platforms(platform_arg)
    today = datetime.now(timezone.utc).date().isoformat()
    out_dir.mkdir(parents=True, exist_ok=True)
    written: list[str] = []
    for p in platforms:
        path = out_dir / f"{p}-changelog-30d.md"
        path.write_text(_stub_markdown(p, depth, today), encoding="utf-8")
        written.append(str(path))
    print(json.dumps({"written": written, "depth": depth, "date": today}, indent=2))


def main() -> None:
    p = argparse.ArgumentParser(description="Plan and scaffold /ads update runs.")
    p.add_argument(
        "--platform",
        required=True,
        help="Platform name (meta, google, tiktok, linkedin, microsoft, apple, youtube) or 'all'",
    )
    p.add_argument("--depth", choices=list(DEPTH_SETTINGS.keys()), default="default")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--dry-run", action="store_true", help="Print the plan; no files written")
    g.add_argument("--prep", action="store_true", help="Write changelog stub files for the skill prompt to fill")
    p.add_argument(
        "--out-dir",
        default="references",
        help="Output directory for stub files (default: references)",
    )
    args = p.parse_args()

    if args.dry_run:
        cmd_dry_run(args.platform, args.depth)
    elif args.prep:
        cmd_prep(args.platform, args.depth, Path(args.out_dir))


if __name__ == "__main__":
    main()
