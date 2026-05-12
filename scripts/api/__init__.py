"""Direct-API adapters for claude-ads.

Each ``<platform>_fetch.py`` in this package is a standalone CLI that pulls
ad-account data from the platform's official Marketing API and emits JSON
for the corresponding audit-* agent to consume. Pure stdlib (Python 3.10+),
no external dependencies.

Adapters in v2.3.0 cover the 3 base platforms:

- ``meta_fetch.py`` — Meta Marketing API
- ``google_fetch.py`` — Google Ads API via GAQL
- ``tiktok_fetch.py`` — TikTok Business API v1.3

See ``scripts/api/README.md`` for the full per-platform OAuth setup.

These are Capa 2 of claude-ads' 3-tier free-first integration strategy:

    Capa 1 → MCP server (when available)
    Capa 2 → this package (free, OAuth setup needed once per platform)
    Capa 3 → manual exports / screenshots (always works)
"""
