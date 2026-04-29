# Adapted from last30days-skill (https://github.com/mvanhorn/last30days-skill)
# Original author: Matt Van Horn
# License: MIT
# Vendored: 2026-04-28
# Modifications:
#   - Replaced schema.SourceItem dependency with local story.Story dataclass
#   - Kept hybrid trigram+token Jaccard with 0.7 threshold (proven default)
# Full upstream license preserved at scripts/lib/THIRD_PARTY_NOTICES.md

"""Cross-source near-duplicate detection via hybrid Jaccard similarity."""

from __future__ import annotations

import re

from .story import Story

STOPWORDS = frozenset({
    "the", "a", "an", "to", "for", "how", "is", "in", "of", "on",
    "and", "with", "from", "by", "at", "this", "that", "it", "what",
    "are", "do", "can",
})


def normalize_text(text: str) -> str:
    text = re.sub(r"[^\w\s]", " ", text.lower())
    return re.sub(r"\s+", " ", text).strip()


def _ngrams_of_normalized(norm: str, n: int = 3) -> set[str]:
    if len(norm) < n:
        return {norm} if norm else set()
    return {norm[i:i + n] for i in range(len(norm) - n + 1)}


def _tokens(normalized: str) -> frozenset[str]:
    return frozenset(
        tok for tok in normalized.split()
        if len(tok) > 1 and tok not in STOPWORDS
    )


def jaccard(a: set[str] | frozenset[str], b: set[str] | frozenset[str]) -> float:
    if not a or not b:
        return 0.0
    union = a | b
    return len(a & b) / len(union) if union else 0.0


class _Prepared:
    __slots__ = ("ngrams", "tokens")

    def __init__(self, raw: str) -> None:
        norm = normalize_text(raw)
        self.ngrams = _ngrams_of_normalized(norm)
        self.tokens = _tokens(norm)


def _prepared_similarity(a: _Prepared, b: _Prepared) -> float:
    return max(jaccard(a.ngrams, b.ngrams), jaccard(a.tokens, b.tokens))


def _item_text(item: Story) -> str:
    parts = [item.title, item.body, item.author, item.container]
    return " ".join(p for p in parts if p).strip()


def dedupe_items(items: list[Story], threshold: float = 0.7) -> list[Story]:
    """Remove near-duplicates while keeping earlier (higher-ranked) items."""
    kept: list[Story] = []
    kept_prepared: list[_Prepared] = []
    for item in items:
        text = _item_text(item)
        if not text:
            kept.append(item)
            continue
        prep = _Prepared(text)
        if any(_prepared_similarity(prep, ex) >= threshold for ex in kept_prepared):
            continue
        kept.append(item)
        kept_prepared.append(prep)
    return kept
