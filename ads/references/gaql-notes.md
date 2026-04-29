# GAQL Compatibility & Accuracy Notes

<!-- Added: 2026-04-01 -->
<!-- Source: akarls-web fork audit accuracy improvements (44 commits) -->
<!-- Purpose: Prevent false positives when analyzing Google Ads data via GAQL or exports -->

## Known GAQL Field Incompatibilities (API v20+)

| Resource | Incompatible Field | Error | Fix |
|----------|-------------------|-------|-----|
| `search_term_view` | `campaign.status`, `ad_group.status` | INVALID_ARGUMENT | Filter status in application layer, not GAQL |
| `search_term_view` | `search_term_view.status` | INVALID_ARGUMENT | Field deprecated/removed in v20 |
| `asset_group_signal` | `audience_signal` | UNRECOGNIZED_FIELD | Use `resource_name` instead |
| DURING clause | `LAST_90_DAYS` | INVALID_VALUE_WITH_DURING_OPERATOR | Use `LAST_30_DAYS` for search terms |

## Keyword Deduplication

**Problem:** `keyword_view + segments.date DURING LAST_30_DAYS` returns one row per keyword per day. A keyword active 5 days = 5 rows. Same keyword with BROAD + PHRASE = 2 rows per day = 10 total.

**Fix:** Deduplicate by `(ad_group_id + keyword_text + match_type)` at fetch time. Aggregate metrics (impressions, clicks, cost, conversions) across duplicate rows.

**Alternative:** Remove `segments.date` from GAQL queries entirely to eliminate date-level duplication at source.

**Impact:** All downstream keyword-dependent checks (G03, G05, G07, G-PM3, G17, G21, G25, G-KW1, and ~10 others) automatically use correct unique counts.

## Filter Scope Best Practices

For active audits, filter to ENABLED resources only:
- **Campaigns:** `campaign.status = 'ENABLED'` (not `!= 'REMOVED'`, which includes PAUSED)
- **Ad groups:** ENABLED campaigns + non-removed groups
- **Keywords:** ENABLED campaigns + non-removed groups + non-removed keywords
- **Search terms:** Extended from `LAST_30_DAYS` to `LAST_90_DAYS` for deeper analysis, ordered by cost DESC

**Why:** Including paused campaigns/ad groups causes false positives. Paused ad groups can have ENABLED keywords at criterion level but aren't visible in the UI; auditing them confuses users.

## Error Handling

Track which data fetches failed and why. Report as a G-SYS1 diagnostic:
- List all failed data sources with error messages
- Provide per-check context on which checks were skipped due to missing data
- Never silently skip checks; always explain why data is unavailable

## Legacy BMM (Broad Match Modified) Detection

Google stripped '+' prefixes during the 2021 migration but kept `matchType='BROAD'` in the API.

**Heuristic:** True intentional broad match is ALWAYS paired with Smart Bidding (tCPA, tROAS, Maximize Conversions/Value). BROAD + Manual CPC = legacy BMM (behaves as phrase match).

**Impact:** Without this heuristic, accounts with legacy BMM keywords generate hundreds of false failures on G17.
