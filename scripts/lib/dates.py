# Vendored from last30days-skill (https://github.com/mvanhorn/last30days-skill)
# Original author: Matt Van Horn
# License: MIT
# Vendored: 2026-04-28
# Modifications: none (verbatim copy)
# Full upstream license preserved at scripts/lib/THIRD_PARTY_NOTICES.md

"""Date utilities for time-bounded research."""

from datetime import datetime, timedelta, timezone
from typing import Optional, Tuple


def get_date_range(days: int = 30) -> Tuple[str, str]:
    """Get the date range for the last N days.

    Returns:
        Tuple of (from_date, to_date) as YYYY-MM-DD strings
    """
    today = datetime.now(timezone.utc).date()
    from_date = today - timedelta(days=days)
    return from_date.isoformat(), today.isoformat()


def parse_date(date_str: Optional[str]) -> Optional[datetime]:
    """Parse a date string in various formats.

    Supports: YYYY-MM-DD, ISO 8601, Unix timestamp
    """
    if not date_str:
        return None

    try:
        ts = float(date_str)
        return datetime.fromtimestamp(ts, tz=timezone.utc)
    except (ValueError, TypeError):
        pass

    formats = [
        "%Y-%m-%d",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%dT%H:%M:%S%z",
        "%Y-%m-%dT%H:%M:%S.%f%z",
    ]

    for fmt in formats:
        try:
            dt = datetime.strptime(date_str, fmt)
            if dt.tzinfo is not None:
                return dt.astimezone(timezone.utc)
            return dt.replace(tzinfo=timezone.utc)
        except ValueError:
            continue

    return None


def timestamp_to_date(ts: Optional[float]) -> Optional[str]:
    """Convert Unix timestamp to YYYY-MM-DD string."""
    if ts is None:
        return None
    try:
        dt = datetime.fromtimestamp(ts, tz=timezone.utc)
        return dt.date().isoformat()
    except (ValueError, TypeError, OSError):
        return None


def get_date_confidence(date_str: Optional[str], from_date: str, to_date: str) -> str:
    """Determine confidence level for a date.

    Returns: 'high', 'med', or 'low'
    """
    if not date_str:
        return "low"

    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d").date()
        start = datetime.strptime(from_date, "%Y-%m-%d").date()
        end = datetime.strptime(to_date, "%Y-%m-%d").date()
        return "high" if start <= dt <= end else "low"
    except ValueError:
        return "low"


def days_ago(date_str: Optional[str]) -> Optional[int]:
    """Calculate how many days ago a date is. Returns None if invalid."""
    if not date_str:
        return None

    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d").date()
        today = datetime.now(timezone.utc).date()
        return (today - dt).days
    except ValueError:
        return None


def recency_score(date_str: Optional[str], max_days: int = 30) -> int:
    """Calculate recency score (0-100). 0 days ago = 100, max_days+ = 0."""
    age = days_ago(date_str)
    if age is None:
        return 0
    if age < 0:
        return 100
    if age >= max_days:
        return 0
    return int(100 * (1 - age / max_days))
