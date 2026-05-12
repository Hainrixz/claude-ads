# Google Ads Audit — Accuracy Notes

Methodology notes that supplement the check tables in `google-audit.md`. Load this file alongside it when you need to know *why* a check is scored a particular way.

## G03 — Theme coherence

When evaluating theme coherence:
1. Only count keywords with impressions > 0; dormant zero-impression keywords don't affect ad serving and shouldn't inflate counts.
2. Exclude paused ad groups: `ENABLED` ad groups only (paused groups can have enabled keywords at criterion level but aren't visible in UI).
3. Deduplicate keywords by text per ad group; the same keyword with BROAD + PHRASE match types is one keyword, not two.
4. Exclude stopword-only keywords (e.g., 'attorney', 'lawyers') from coherence scoring; they carry no thematic signal and dilute coherence scores.

## G04 — Campaign count per objective

For multi-location businesses, strip geographic identifiers (city names, state abbreviations, zip codes, metro areas, directional qualifiers like "North"/"South") from campaign names before counting unique objectives. A firm running "Divorce - Chicago", "Divorce - Schaumburg", "Divorce - Naperville" has 1 objective across 3 geos, not 3 separate objectives. Preserve PPC-meaningful terms (brand, nonbrand, pmax, remarketing, etc.).

## G05 / G07 / G-PM3 — Brand detection

Don't rely solely on campaign naming conventions. Derive brand tokens from the account/business name and scan actual keyword text for brand terms. Classify campaigns by keyword composition: >50% brand keywords = brand campaign. This catches mislabeled campaigns and provides accurate brand vs. non-brand separation.

## G12 — Network settings

Search Partners typically provides incremental reach at comparable CPA. Flag Search Partners OFF as a missed opportunity (Warning), not ON. Display Network on Search campaigns remains a Fail.

## G14 / G15 — Negative coverage

Count both campaign-level negatives AND Shared Negative Keyword Lists when evaluating coverage. Campaigns covered by shared lists should NOT be flagged as "missing negatives." Report per-campaign breakdown showing direct negatives vs. shared list assignments for clear remediation paths.

## G16 / G-WS1 — Wasted spend

Only flag search terms as "wasted" if they have >$10 spend AND 0 conversions. Long-tail terms with minimal spend (<$10) are normal exploration, not waste. When reporting, show top 10 wasters with spend and click details.

## G17 / FL04 — Legacy BMM heuristic

Google stripped '+' prefixes from Broad Match Modified keywords during the 2021 migration but kept `matchType=BROAD` in the API. BROAD + Manual CPC almost always indicates legacy BMM (behaves as phrase match), NOT intentional broad match. True intentional broad match is always paired with Smart Bidding (tCPA, tROAS, Maximize Conversions/Value). Only flag BROAD keywords in Smart Bidding campaigns as needing review. Skip BROAD + Manual CPC; these are legacy BMM and should not be flagged as failures.

## G19 — Search term visibility

When computing `totalVisibleSpend`, use ALL fetched search terms before any truncation or top-N limiting. A common error is summing cost from a truncated subset (e.g., top 500 of 2000 terms) which understates visibility. Fetch terms ordered by cost descending to ensure the highest-spend terms are captured first.

## G48 / CT-FL5 — Attribution & counting

Exclude Smart Campaign system-managed conversions (e.g., 'Smart campaign map clicks to call') from DDA and counting-type checks. Their attribution model and counting type are locked by Google; advertisers cannot change them. Only evaluate advertiser-controlled conversion actions.

## G-CT1 — Duplicate counting

Only check ENABLED conversion actions for duplicates. Exclude HIDDEN and REMOVED conversion actions; these are already disabled and cannot cause double-counting. When reporting duplicates, include the conversion action ID, type, origin, category, status, primary/secondary flag, counting type, and attribution model for easy resolution.
