"""Simple Story dataclass — replaces the upstream schema.SourceItem.

Used by signals/dedupe to score and cluster items fetched from any source
(Reddit, Hacker News, official changelog, web search).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Story:
    """A single fetched item from any source."""

    source: str  # "reddit", "hackernews", "official_changelog", "web", etc.
    title: str
    url: str
    published_at: Optional[str] = None  # YYYY-MM-DD
    body: str = ""
    author: str = ""
    container: str = ""  # subreddit name, domain, etc.
    snippet: str = ""
    engagement: dict = field(default_factory=dict)
    metadata: dict = field(default_factory=dict)

    # Computed scores (filled by signals.annotate_stream)
    freshness: int = 0
    engagement_score: Optional[int] = None
    source_quality: float = 0.0
    rank_score: float = 0.0
