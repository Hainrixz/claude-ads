#!/usr/bin/env python3
"""Ad-platform source configuration for /ads update.

Defines the per-platform source set (subreddits, official changelog URLs,
WebSearch fallback queries, optional YouTube channels and X handles) used
by run_update.py to fetch the last 30 days of changes.

Sources are deliberately curated:
- Reddit subs: where practitioners actually discuss platform changes
- Changelog URLs: vendor-published release notes (ground truth)
- Search queries: phrased to surface recent industry-press coverage
- YouTube/X: optional, for users who supply API keys

Usage:
    python3 scripts/ads_sources.py --list meta
    python3 scripts/ads_sources.py --list-all
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass, field


@dataclass
class PlatformSourceSet:
    """All sources to consult for a single ad platform."""

    platform: str
    display_name: str
    subreddits: list[str] = field(default_factory=list)
    changelog_urls: list[str] = field(default_factory=list)
    search_queries: list[str] = field(default_factory=list)
    hn_keywords: list[str] = field(default_factory=list)
    youtube_channels: list[str] = field(default_factory=list)  # optional, requires YT key
    x_handles: list[str] = field(default_factory=list)  # optional, requires xAI key


PLATFORM_SOURCES: dict[str, PlatformSourceSet] = {
    "meta": PlatformSourceSet(
        platform="meta",
        display_name="Meta Ads (Facebook & Instagram)",
        subreddits=["FacebookAds", "PPC", "MarketingAutomation", "advertising"],
        changelog_urls=[
            "https://developers.facebook.com/docs/graph-api/changelog",
            "https://developers.facebook.com/docs/marketing-api/changelog",
            "https://www.facebook.com/business/news",
        ],
        search_queries=[
            "Meta Ads new feature 2026 last 30 days",
            "Facebook Ads Advantage+ update 2026",
            "Meta Marketing API deprecation 2026",
            "Instagram Ads policy change 2026",
        ],
        hn_keywords=["meta ads", "facebook ads", "instagram ads", "advantage+"],
        x_handles=["MetaforBusiness", "Meta"],
    ),
    "google": PlatformSourceSet(
        platform="google",
        display_name="Google Ads",
        subreddits=["GoogleAds", "PPC", "bigseo", "googleads"],
        changelog_urls=[
            "https://support.google.com/google-ads/answer/2375475",  # What's new in Google Ads
            "https://developers.google.com/google-ads/api/docs/release-notes",
            "https://blog.google/products/ads-commerce/",
        ],
        search_queries=[
            "Google Ads new feature 2026 last 30 days",
            "Google Ads PMax update 2026",
            "Google Ads API deprecation 2026",
            "Google Ads Smart Bidding change 2026",
        ],
        hn_keywords=["google ads", "performance max", "pmax", "google adwords"],
        x_handles=["adsliaison", "GoogleAds"],
    ),
    "tiktok": PlatformSourceSet(
        platform="tiktok",
        display_name="TikTok Ads",
        subreddits=["TikTokAds", "marketing", "PPC"],
        changelog_urls=[
            "https://business-api.tiktok.com/portal/docs?id=1740626878662658",
            "https://www.tiktok.com/business/en/blog",
        ],
        search_queries=[
            "TikTok Ads new feature 2026 last 30 days",
            "TikTok Smart+ campaign update 2026",
            "TikTok Ads API change 2026",
            "TikTok Shop Ads policy 2026",
        ],
        hn_keywords=["tiktok ads", "tiktok marketing", "tiktok shop"],
        x_handles=["TikTokForBiz"],
    ),
    # NOTE: LinkedIn / Microsoft / Apple / YouTube source sets removed in v2.3.0
    # alongside the platform scope reduction (Meta / Google / TikTok only).
    # YouTube changes are surfaced through the Google source set since they
    # share the Google Ads API and announcement channels.
}


SUPPORTED_PLATFORMS: list[str] = list(PLATFORM_SOURCES.keys())


def get_sources(platform: str) -> PlatformSourceSet:
    """Look up a platform's source set. Raises KeyError on unknown platform."""
    if platform not in PLATFORM_SOURCES:
        raise KeyError(
            f"Unknown platform '{platform}'. Supported: {', '.join(SUPPORTED_PLATFORMS)}"
        )
    return PLATFORM_SOURCES[platform]


def main() -> None:
    p = argparse.ArgumentParser(description="Inspect ad-platform source configuration.")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--list", help="Print sources for one platform (e.g. meta)")
    g.add_argument("--list-all", action="store_true", help="Print all platforms")
    args = p.parse_args()

    if args.list_all:
        out = {k: asdict(v) for k, v in PLATFORM_SOURCES.items()}
        print(json.dumps(out, indent=2))
        return

    try:
        sources = get_sources(args.list)
    except KeyError as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(1)
    print(json.dumps(asdict(sources), indent=2))


if __name__ == "__main__":
    main()
