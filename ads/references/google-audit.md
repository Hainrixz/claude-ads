# Google Ads Audit Checklist

Total checks: 80. Categories: 7. See `scoring-system.md` for weights and algorithm. See `google-audit-notes.md` for per-check methodology nuances and edge cases.

## Quick Reference

| Category | Weight | Check Count |
|----------|--------|-------------|
| Conversion Tracking | 25% | G42-G49 (8) + G-CT1 through G-CT3 (3) + G-CTV1 (1) = 12 |
| Wasted Spend / Negatives | 20% | G13-G19 (7) + G-WS1 (1) = 8 |
| Account Structure | 15% | G01-G12 (12) |
| Keywords & Quality Score | 15% | G20-G25 (6) + G-KW1, G-KW2 (2) = 8 |
| Ads & Assets | 15% | G26-G35 (10) + G-AD1, G-AD2 (2) = 12 |
| Settings & Targeting | 10% | G50-G61 (12) |
| Performance Max | N/A | G-PM1 through G-PM6 (6, scored within Ads & Assets) |
| AI & Demand Gen | N/A | G-AI1 (1) + G-DG1 through G-DG3 (3, scored within Ads & Assets) |

## Conversion Tracking (25% weight)

| ID | Check | Severity | Pass | Warning | Fail |
|----|-------|----------|------|---------|------|
| G42 | Conversion actions defined | Critical | ≥1 primary conversion action configured | N/A | No active conversion actions |
| G43 | Enhanced conversions enabled | Critical | Enhanced conversions active AND verified for primary conversions (~10% uplift) **[Quick Win: 5 min]** | Enabled but not verified | Not enabled |
| G44 | Server-side tracking | High | Server-side GTM or Google Ads API conversion import active | Planned but not deployed | No server-side tracking |
| G45 | Consent Mode v2 | Critical | Advanced Consent Mode v2 implemented (enforcement July 21, 2025 EEA/UK). Recovers 15-25% of lost conversions | Basic mode only | Not implemented |
| G46 | Conversion window appropriate | Medium | Window matches sales cycle (7d ecom, 30-90d B2B, 30d lead gen) | Default 30d without validation | Window mismatched to sales cycle |
| G47 | Micro vs macro separation | High | Only macro conversions (Purchase, Lead) set as "Primary" for bidding | Some micro events as Primary | All events including micro as Primary |
| G48 | Attribution model | Medium | Data-driven attribution (DDA) selected | Last Click (intentional) | Rule-based model active (see notes) |
| G49 | Conversion value assignment | High | Dynamic values for ecom; value rules for lead gen | Static values assigned | No conversion values |
| G-CT1 | No duplicate counting | Critical | GA4 + Google Ads not double-counting same conversion | N/A | Both GA4 import and native tag counting same action |
| G-CT2 | GA4 linked and flowing | High | GA4 property linked, data flowing correctly | Linked but data discrepancies | Not linked |
| G-CT3 | Google Tag firing | Critical | gtag.js or GTM firing correctly on all pages | Firing on most pages (>90%) | Tag missing or broken on key pages |

## Wasted Spend / Negatives (20% weight)

| ID | Check | Severity | Pass | Warning | Fail |
|----|-------|----------|------|---------|------|
| G13 | Search term audit recency | Critical | Reviewed within last 14 days | Reviewed within 30 days | Not reviewed in >30 days |
| G14 | Negative keyword lists exist | Critical | ≥3 theme-based lists (Competitor, Jobs, Free, Irrelevant) | 1-2 lists exist | No negative keyword lists |
| G15 | Account-level negatives applied | High | Negative lists applied at account or all-campaign level | Applied to some campaigns only | Not applied |
| G16 | Wasted spend on irrelevant terms | Critical | <5% of spend on irrelevant search terms (last 30d, >$10 spend & 0 conv) | 5-15% | >15% |
| G17 | Broad match + smart bidding pairing | Critical | No Broad Match keywords running on Manual CPC (excluding legacy BMM — see notes) | N/A | Broad Match + Smart Bidding without negative hygiene |
| G18 | Close variant pollution | High | Exact/Phrase match not triggering irrelevant close variants | Minor close variant issues | Significant irrelevant close variant spend |
| G19 | Search term visibility | Medium | >60% of search term spend visible | 40-60% visible | <40% visible |
| G-WS1 | Zero-conversion keywords | High | No keywords with >100 clicks and 0 conversions | 1-3 such keywords | >3 keywords with >100 clicks, 0 conv |

## Account Structure (15% weight)

| ID | Check | Severity | Pass | Warning | Fail |
|----|-------|----------|------|---------|------|
| G01 | Campaign naming convention | Medium | Consistent pattern (e.g., [Brand]_[Type]_[Geo]_[Target]) | Partially consistent | No naming convention |
| G02 | Ad group naming convention | Medium | Matches campaign naming pattern | Partially consistent | No naming convention |
| G03 | Single theme ad groups | High | Each ad group targets 1 keyword theme (≤10 keywords with impressions) | 11-20 keywords with consistent theme | 20+ unrelated keywords (theme drift) |
| G04 | Campaign count per objective | High | ≤5 campaigns per funnel stage/objective (strip geos before counting) | 6-8 | >8 (fragmented) |
| G05 | Brand vs Non-Brand separation | Critical | Brand and non-brand in separate campaigns | N/A | Mixed in same campaign |
| G06 | PMax present for eligible accounts | Medium | PMax active for accounts with conversion history | PMax tested but paused | No PMax tested despite eligibility |
| G07 | Search + PMax overlap | High | Brand exclusions configured in PMax when Search brand campaign exists | Partial brand exclusions | No brand exclusions |
| G08 | Budget allocation matches priority | High | Top performers not budget-limited | Minor budget constraints | Severely budget-limited |
| G09 | Campaign daily budget vs spend | Medium | No campaigns hitting budget cap before 6PM | 1-2 capped early | Multiple capped before noon |
| G10 | Ad schedule configured | Low | Schedule set if business has operating hours | N/A | No schedule despite clear hours |
| G11 | Geographic targeting accuracy | High | "People in" (not "Presence or Interest") for local | N/A | "Presence or Interest" for local business |
| G12 | Network settings | High | Search Partners ON; Display Network OFF for Search | Search Partners OFF | Display Network ON for Search |

## Keywords & Quality Score (15% weight)

| ID | Check | Severity | Pass | Warning | Fail |
|----|-------|----------|------|---------|------|
| G20 | Average Quality Score | High | Impression-weighted QS ≥7 | QS 5-6 | QS ≤4 |
| G21 | Critical QS keywords | Critical | <10% with QS ≤3 | 10-25% | >25% |
| G22 | Expected CTR component | High | <20% Below Average | 20-35% | >35% |
| G23 | Ad relevance component | High | <20% Below Average | 20-35% | >35% |
| G24 | Landing page experience | High | <15% Below Average | 15-30% | >30% |
| G25 | Top keyword QS | Medium | Top 20 spend keywords all QS ≥7 | Some at QS 5-6 | Top keywords with QS ≤4 |
| G-KW1 | Zero-impression keywords | Medium | No 0-impression keywords in last 30 days | <10% zero-imp | >10% zero-imp |
| G-KW2 | Keyword-to-ad relevance | High | Headlines contain primary keyword variants | Partial inclusion | No variants in headlines |

## Ads & Assets (15% weight)

| ID | Check | Severity | Pass | Warning | Fail |
|----|-------|----------|------|---------|------|
| G26 | RSA per ad group | High | ≥1 RSA per ad group (≥2 rec) | 1 RSA | Ad groups without any RSA |
| G27 | RSA headline count | High | ≥8 unique headlines (ideal 12-15) | 3-7 | <3 |
| G28 | RSA description count | Medium | ≥3 descriptions (ideal 4) | 2 | <2 |
| G29 | RSA Ad Strength | High | All RSAs "Good" or "Excellent" | Some "Average" | Any "Poor" |
| G30 | RSA pinning strategy | Medium | Strategic (1-2 positions, 2-3 variants each) | Over-pinned all positions | N/A |
| G31 | PMax asset density | Critical | ≥20 images, ≥5 logos, ≥5 native videos. PMax needs 30-50+ conv/mo | 5-19 images / <30 conv/mo | <5 images OR 0 logos OR 0 video |
| G32 | PMax video assets present | High | Native video in all formats (16:9, 1:1, 9:16) | 1-2 formats only | No native video |
| G33 | PMax asset group count | Medium | ≥2 asset groups (intent-segmented) | 1 asset group | N/A |
| G34 | PMax final URL expansion | High | Configured intentionally | N/A | Default ON without review |
| G35 | Ad copy relevance to keywords | High | Headlines contain primary variants | Partial | No relevance |
| G-AD1 | Ad freshness | Medium | New copy tested within 90 days | N/A | No new ads in >90 days |
| G-AD2 | CTR vs industry benchmark | High | CTR ≥ industry average | 50-100% of avg | <50% of avg |

## Settings & Targeting (10% weight)

| ID | Check | Severity | Pass | Warning | Fail |
|----|-------|----------|------|---------|------|
| G36 | Smart bidding strategy active | High | All campaigns ≥15 conv/30d use automated bidding (ECPC removed March 2025) | Partial / ECPC remaining | Manual CPC on campaigns with sufficient data |
| G37 | Target CPA/ROAS reasonableness | Critical | Within 20% of historical | 20-50% off | <50% of actual |
| G38 | Learning phase status | High | <25% of campaigns in Learning Limited | 25-40% | >40% |
| G39 | Budget constrained campaigns | High | Top performers "Eligible" | Minor limitation | Severely budget-limited |
| G40 | Manual CPC justification | Medium | Only on campaigns <15 conv/month | 15-30 conv/mo | >30 conv/mo |
| G41 | Portfolio bid strategies | Medium | Low-volume campaigns grouped | N/A | Multiple <15 conv campaigns independent |
| G50 | Sitelink extensions | High | ≥4 sitelinks | 1-3 | None |
| G51 | Callout extensions | Medium | ≥4 callouts | 1-3 | None |
| G52 | Structured snippets | Medium | ≥1 set | N/A | None |
| G53 | Image extensions | Medium | Active for search campaigns | N/A | None |
| G54 | Call extensions (if applicable) | Medium | With call tracking for phone-based | Without tracking | None for phone-based |
| G55 | Lead form extensions | Low | Tested for lead gen | N/A | Not tested |
| G56 | Audience segments applied | High | Remarketing + in-market in Observation | Some applied | None |
| G57 | Customer Match lists | High | Uploaded, refreshed <30 days | >30 days old | None |
| G58 | Placement exclusions | High | Account-level exclusions (games, apps, MFA) | Campaign-level only | None |
| G59 | Landing page mobile speed | High | LCP <2.5s | 2.5-4.0s | >4.0s |
| G60 | Landing page relevance | High | H1/title matches ad group theme | Partial | No relevance |
| G61 | Landing page schema markup | Medium | Product/FAQ/Service schema | N/A | None |

## PMax Extended (scored within Ads & Assets)

| ID | Check | Severity | Pass | Warning | Fail |
|----|-------|----------|------|---------|------|
| G-PM1 | Audience signals configured | High | Custom signals per asset group | Generic only | None |
| G-PM2 | PMax Ad Strength | High | "Good"/"Excellent" | "Average" | "Poor" |
| G-PM3 | Brand cannibalization | High | <15% of PMax conv from brand terms | 15-30% | >30% |
| G-PM4 | Search themes | Medium | Configured (up to 50/group) | <5 | None |
| G-PM5 | Negative keywords | High | Brand + irrelevant applied (up to 10K) | Some applied | None |
| G-PM6 | PMax campaign negatives | High | Campaign-level negatives configured (now available for ALL advertisers; ~15% cost reduction) **[Quick Win: 10 min]** | Account-level only | None |

## AI Max & Demand Gen (scored within Ads & Assets)

| ID | Check | Severity | Pass | Warning | Fail |
|----|-------|----------|------|---------|------|
| G-AI1 | AI Max for Search evaluation | High | AI Max evaluated/active with negative lists ready (14% avg conv lift) | N/A | Not evaluated despite eligibility (>50 conv/mo) |
| G-DG1 | Demand Gen image assets | High | Both video AND image assets (20% more conv same CPA) | Video only | No DG campaigns despite eligibility |
| G-DG2 | VAC migration status | Critical | All migrated to Demand Gen (auto-upgraded April 2026) | In progress | VAC still active |
| G-DG3 | Demand Gen frequency capping loss | High | Alt measurement in place for former VAC frequency-cap campaigns | Not monitored | Former VAC relied on caps, no replacement |

## CTV & Video Tracking (scored within Conversion Tracking)

| ID | Check | Severity | Pass | Warning | Fail |
|----|-------|----------|------|---------|------|
| G-CTV1 | CTV Floodlight tracking limitation | High | CTV uses non-Floodlight measurement (Floodlight does NOT fire on CTV) | Active but unverified | CTV relies on Floodlight |

## Quick Wins (Google)

| Check | Fix | Time |
|-------|-----|------|
| G43: Enhanced conversions | Enable in conversion settings | 5 min |
| G11: Location targeting | Switch to "People in" | 2 min |
| G14: Negative keyword lists | Create themed lists | 10 min |
| G17: Broad + Manual CPC | Switch to Smart Bidding | 5 min |
| G12: Network settings | Disable Display Network on Search | 2 min |
| G05: Brand separation | Split brand keywords | 10 min |
| G50: Sitelink extensions | Add 4+ sitelinks | 10 min |
| G-PM6: PMax campaign negatives | Add campaign-level negatives | 10 min |
