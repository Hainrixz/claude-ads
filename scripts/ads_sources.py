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
    "linkedin": PlatformSourceSet(
        platform="linkedin",
        display_name="LinkedIn Ads",
        subreddits=["LinkedInAds", "B2BMarketing", "marketing"],
        changelog_urls=[
            "https://learn.microsoft.com/en-us/linkedin/marketing/whats-new/",
            "https://www.linkedin.com/business/marketing/blog",
        ],
        search_queries=[
            "LinkedIn Ads new feature 2026 last 30 days",
            "LinkedIn Marketing API change 2026",
            "LinkedIn Thought Leader Ads update 2026",
            "LinkedIn ABM new feature 2026",
        ],
        hn_keywords=["linkedin ads", "linkedin marketing"],
        x_handles=["LinkedInMktg"],
    ),
    "microsoft": PlatformSourceSet(
        platform="microsoft",
        display_name="Microsoft Advertising (Bing Ads)",
        subreddits=["MicrosoftAds", "PPC", "bigseo"],
        changelog_urls=[
            "https://about.ads.microsoft.com/en-us/resources/whats-new",
            "https://learn.microsoft.com/en-us/advertising/guides/release-notes",
        ],
        search_queries=[
            "Microsoft Advertising new feature 2026 last 30 days",
            "Bing Ads Copilot update 2026",
            "Microsoft Ads API change 2026",
            "Microsoft Audience Network 2026",
        ],
        hn_keywords=["bing ads", "microsoft advertising", "microsoft ads"],
        x_handles=["MSFTAdvertising"],
    ),
    "apple": PlatformSourceSet(
        platform="apple",
        display_name="Apple Search Ads",
        subreddits=["aso", "AppBusiness", "iOSProgramming"],
        changelog_urls=[
            "https://searchads.apple.com/whats-new",
            "https://developer.apple.com/news/?id=adattributionkit",
        ],
        search_queries=[
            "Apple Search Ads new feature 2026 last 30 days",
            "Apple Search Ads Custom Product Pages 2026",
            "AdAttributionKit update 2026",
            "Apple Search Ads Maximize Conversions 2026",
        ],
        hn_keywords=["apple search ads", "adattributionkit", "skadnetwork"],
    ),
    "youtube": PlatformSourceSet(
        platform="youtube",
        display_name="YouTube Ads",
        subreddits=["GoogleAds", "PPC", "youtubers"],
        changelog_urls=[
            "https://support.google.com/youtube/answer/2375475",
            "https://blog.youtube/news-and-events/",
            "https://blog.google/products/ads-commerce/",
        ],
        search_queries=[
            "YouTube Ads new feature 2026 last 30 days",
            "YouTube Shorts Ads update 2026",
            "YouTube Demand Gen campaign 2026",
            "YouTube CTV Ads 2026",
        ],
        hn_keywords=["youtube ads", "youtube shorts ads", "youtube ctv"],
        x_handles=["YouTube"],
    ),
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
