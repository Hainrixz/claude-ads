# Adapted from last30days-skill (https://github.com/mvanhorn/last30days-skill)
# Original author: Matt Van Horn
# License: MIT
# Vendored: 2026-04-28
# Modifications:
#   - Replaced schema.SourceItem dependency with local story.Story dataclass
#   - Removed text-overlap relevance scoring (not needed; ad-platform queries
#     are pre-filtered by source/keyword upstream in ads_sources.py)
#   - Added official_changelog source (2x quality boost: ground-truth vendor docs)
#   - Adapted SOURCE_QUALITY for ad-domain sources (web blog, search)
# Full upstream license preserved at scripts/lib/THIRD_PARTY_NOTICES.md

"""Per-source engagement weighting and freshness/quality scoring."""

from __future__ import annotations

import math
from typing import Optional

from . import dates
from .story import Story


# Source quality multipliers. Official changelog is ground-truth (boosted
# above the 1.0 baseline). Reddit/HN are practitioner discussion (good signal,
# noisier). Web search results are uncurated (lowest).
SOURCE_QUALITY: dict[str, float] = {
    "official_changelog": 2.0,
    "hackernews": 0.8,
    "reddit": 0.6,
    "web": 0.5,
}


def source_quality(source: str) -> float:
    return SOURCE_QUALITY.get(source, 0.5)


# Per-source engagement weights for sources with structured engagement metrics.
# Reddit gets a custom function below to include the upvote-ratio signal.
ENGAGEMENT_WEIGHTS: dict[str, list[tuple[str, float]]] = {
    "hackernews": [("points", 0.55), ("comments", 0.45)],
}


def log1p_safe(value) -> float:
    if value is None:
        return 0.0
    try:
        numeric = float(value)
    except (TypeError, ValueError):
        return 0.0
    if numeric <= 0:
        return 0.0
    return math.log1p(numeric)


def _weighted_engagement(item: Story, weights: list[tuple[str, float]]) -> Optional[float]:
    values = [(log1p_safe(item.engagement.get(field)), weight) for field, weight in weights]
    if not any(v for v, _ in values):
        return None
    return sum(v * w for v, w in values)


def _reddit_engagement(item: Story) -> Optional[float]:
    score = log1p_safe(item.engagement.get("score"))
    comments = log1p_safe(item.engagement.get("num_comments"))
    ratio = float(item.engagement.get("upvote_ratio") or 0.0)
    if not any([score, comments, ratio]):
        return None
    return (0.55 * score) + (0.40 * comments) + (0.05 * (ratio * 10.0))


def _generic_engagement(item: Story) -> Optional[float]:
    if not item.engagement:
        return None
    values = [logged for v in item.engagement.values() if (logged := log1p_safe(v)) > 0]
    if not values:
        return None
    return sum(values) / len(values)


def engagement_raw(item: Story) -> Optional[float]:
    if item.source == "reddit":
        return _reddit_engagement(item)
    weights = ENGAGEMENT_WEIGHTS.get(item.source)
    if weights:
        return _weighted_engagement(item, weights)
    return _generic_engagement(item)


def freshness(item: Story) -> int:
    """Recency-weighted score (0-100)."""
    return dates.recency_score(item.published_at, max_days=30)


def normalize(values: list[Optional[float]]) -> list[Optional[int]]:
    valid = [v for v in values if v is not None]
    if not valid:
        return [None for _ in values]
    low, high = min(valid), max(valid)
    if math.isclose(low, high):
        return [50 if v is not None else None for v in values]
    return [
        None if v is None else int(((v - low) / (high - low)) * 100)
        for v in values
    ]


def annotate_stream(items: list[Story]) -> list[Story]:
    """Score every item and return sorted by rank_score descending.

    rank_score = 0.45 * freshness + 0.35 * engagement + 0.20 * source_quality
    Heavily favors recent, well-engaged content from authoritative sources —
    exactly what we want for "what changed in the last 30 days."
    """
    eng_scores = normalize([engagement_raw(item) for item in items])
    for item, eng in zip(items, eng_scores):
        item.freshness = freshness(item)
        item.engagement_score = eng
        item.source_quality = source_quality(item.source)
        item.rank_score = (
            0.45 * (item.freshness / 100.0)
            + 0.35 * ((eng or 0) / 100.0)
            + 0.20 * (item.source_quality / 2.0)  # normalize against changelog max
        )
    return sorted(items, key=lambda i: i.rank_score, reverse=True)
