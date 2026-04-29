# Microsoft Ads Audit Checklist

<!-- Updated: 2026-04-13 | v1.5 -->
<!-- Sources: Google Research PDF 1 (MS01-MS20), Claude Research, Gemini Research, Seer Interactive -->
<!-- Total Checks: 24 | Categories: 6 | See scoring-system.md for weights and algorithm -->

## Quick Reference

| Category | Weight | Check Count |
|----------|--------|-------------|
| Technical Setup | 25% | MS01-MS03 (3 checks) |
| Syndication & Bidding | 20% | MS04-MS07 (4 checks) |
| Structure & Audience | 20% | MS08-MS10 (3 checks) |
| Creative & Extensions | 20% | MS11-MS13 + MS19-MS20 (5 checks) |
| Settings & Performance | 15% | MS14-MS18 (5 checks) |
| Import Safety, Compliance & Video (v1.5) | N/A | MS-SI1, MS-CM1, MS-CT1, MS-VD1 (4 checks) |

---

## Technical Setup (25% weight)

| ID | Check | Severity | Pass | Warning | Fail |
|----|-------|----------|------|---------|------|
| MS01 | UET tag installed | Critical | Universal Event Tracking tag firing on all pages | Firing on most pages (>90%) | UET tag not installed or broken |
| MS02 | Enhanced conversions | High | Enhanced conversions enabled for improved matching | N/A | Not enabled |
| MS03 | Google Ads import validation | High | If imported: all settings verified (URLs, extensions, bids). Scheduled auto-imports deactivated after initial setup | Minor discrepancies found | Import errors not resolved (broken URLs, missing goals). Scheduled imports still active without monitoring |

### Import Validation Critical Note
Google Ads imports are the most common Microsoft Ads setup method. Common import issues:
- Conversion goals often break during import
- Tracking templates may not transfer
- Extensions may be partially imported
- Bid adjustments may not match
- **Scheduled auto-imports can re-enable paused campaigns** (a common billing surprise)
- ALWAYS validate conversion tracking after import
- **Deactivate auto-imports immediately after initial setup** to prevent silent campaign re-enablement and overwritten manual bid/budget changes

---

## Syndication & Bidding (20% weight)

| ID | Check | Severity | Pass | Warning | Fail |
|----|-------|----------|------|---------|------|
| MS04 | Brand syndication control | Critical | Brand campaigns excluded from syndicated partners OR low-performers excluded | Partners enabled, monitored regularly | Brand campaigns on syndicated partners, never reviewed (massive budget waste risk) |
| MS05 | Audience Network settings | High | Audience Network enabled only if testing intentionally. Run Website URL publisher reports weekly and maintain account-level exclusion lists | Audience Network enabled with regular publisher report monitoring | Audience Network ON by default without review. B2B clients see CPA 2-4x higher from Audience Network than search alone (Seer Interactive). Microsoft auto-includes it by default |
| MS06 | Bid strategy alignment | High | Strategy matches goal + conversion volume; targets 20-35% lower than Google | Strategy matches but targets not adjusted for Bing | Mismatched strategy for conversion volume |
| MS07 | Target New Customers (PMax) | Medium | "Target New Customers" enabled for growth campaigns (Beta 2026) | N/A | Not tested for eligible PMax campaigns |

---

## Structure & Audience (20% weight)

| ID | Check | Severity | Pass | Warning | Fail |
|----|-------|----------|------|---------|------|
| MS08 | Campaign structure | High | Mirrors Google structure (if imported) or follows best practices | Minor structural issues | Disorganized structure, no naming convention |
| MS09 | Budget allocation | Medium | Budget proportional to Bing search volume (typically 20-30% of Google) | Slightly over/under-allocated | Budget >50% of Google budget (over-investment) |
| MS10 | LinkedIn profile targeting | High | LinkedIn targeting utilized for B2B: up to 16% greater CTR and 64% greater conversion rate vs non-audience-targeted ads. Available across Search, DSA, Shopping, PMax, and Multimedia ads. Dimensions: Company (80,000+), Industry (148), Job Function (26). Use Observation (Bid Only) mode first. CPCs 30-70% cheaper than LinkedIn Ads directly | Partial LinkedIn targeting | No LinkedIn targeting for B2B campaigns (unique advantage missed) |

---

## Creative & Extensions (20% weight)

| ID | Check | Severity | Pass | Warning | Fail |
|----|-------|----------|------|---------|------|
| MS11 | RSA asset count | High | ≥8 headlines, ≥3 descriptions per RSA | 3-7 headlines, 2 descriptions | <3 headlines (minimum) |
| MS12 | Multimedia Ads | Medium | Multimedia Ads tested (unique rich visual format) | N/A | Not tested |
| MS13 | Ad copy uniqueness | Medium | Ad copy optimized for Bing demographics (older, affluent, educated) | Same copy as Google, untested | N/A |
| MS19 | Action Extension | Medium | Action Extension utilized (unique to Microsoft) | N/A | Not tested |
| MS20 | Filter Link Extension | Medium | Filter Link Extension tested for product/service categories | N/A | Not tested |

### Microsoft-Unique Formats
These extensions are ONLY available on Microsoft Ads:
- **Action Extension**: Predefined action buttons (clickable CTAs)
- **Filter Link Extension**: Category-based deep links (product filters)
- **Multimedia Ads**: Rich visual search ads (image + headline + description)
- **Review Extension**: Third-party review quotes in ads

---

## Settings & Performance (15% weight)

| ID | Check | Severity | Pass | Warning | Fail |
|----|-------|----------|------|---------|------|
| MS14 | Copilot placement | Medium | Copilot chat placement enabled for PMax campaigns. CTV ads now serve on Netflix, Max, Hulu, Roku, discovery+. Auto-generated RSA assets enabled by default globally Jan 2026 (5% CTR increase). Image Animation via Copilot pilot (Nov 2025): static images converted to video assets | N/A | Not enabled (73% higher CTR opportunity) |
| MS15 | Conversion goals | High | Goals configured natively (not relying on Google-imported goals) | Imported goals verified and working | Imported goals not verified |
| MS16 | CPC vs Google comparison | Medium | Microsoft CPC 20-40% lower than Google for same keywords | CPC within 0-20% of Google | CPC equal to or higher than Google |
| MS17 | Conversion rate comparison | Medium | Microsoft CVR comparable to Google | CVR 25-50% lower | CVR >50% lower than Google |
| MS18 | Impression share | Medium | IS tracked for brand and top non-brand terms | Partially tracked | Not tracked |

---

## Quick Wins (Microsoft)

| Check | Fix | Time |
|-------|-----|------|
| MS10: LinkedIn targeting | Enable LinkedIn profile targeting for B2B campaigns | 5 min |
| MS14: Copilot placement | Enable Copilot chat placement in PMax settings | 2 min |
| MS04: Partner network | Review syndicated partner performance, exclude low-performers | 10 min |
| MS19: Action Extension | Add Action Extension to campaigns | 5 min |
| MS12: Multimedia Ads | Create Multimedia Ad from existing assets | 10 min |
| MS03: Import validation | Verify conversion goals and tracking post-import | 10 min |

---

## Microsoft-Specific Context

| Fact | Value |
|------|-------|
| Average CPC | $1.20-$1.55 (20-35% discount vs Google) |
| Average CTR | 2.83-3.1% (higher than Google's ~2.0%) |
| US desktop share | 16.75-17.58%; with partners ~25% |
| Copilot CTR lift | 73% higher than traditional search |
| Copilot CVR lift | 16% stronger conversion rates |
| Copilot journey | 33% shorter customer journeys |
| Purchase intent | 194% more likely to purchase in Copilot |
| Copilot Checkout | Launched Jan 2026 (in-conversation commerce) |
| 37% of advertisers | Report higher ROAS vs Google |
| Bing users click paid ads | 25% more often than Google users |
| Audience skew | Affluent (~50% top 25% HHI), educated (34% degrees), older (45-64: 38%) |
| Import options | Quick Import, Smart Import, Advanced Import (Feb 2025) |
| API version | v13 stable, SOAP-based with REST emerging |

---

## Copilot Integration (2026)

Microsoft's Copilot represents the biggest unique advantage:

1. **Copilot Chat Placement**: Ads appear within conversational search
2. **Copilot Checkout** (Jan 2026); Full commerce within conversations
3. **Higher engagement**: 73% CTR lift, 16% CVR lift, 33% shorter journeys
4. **Shopping intent**: Users 194% more likely to purchase
5. **Launch partners**: Urban Outfitters, Etsy, Ashley Furniture

Ensure PMax campaigns have Copilot placement enabled to capture this growing channel.

---

## Import Safety, Compliance & Video (v1.5)

| ID | Check | Severity | Pass | Warning | Fail |
|----|-------|----------|------|---------|------|
| MS-SI1 | Scheduled import status | Critical | Scheduled Google Ads imports disabled or closely monitored. Auto-imports can silently re-enable paused campaigns and overwrite manual bid/budget changes | Imports active with manual review schedule | Scheduled imports running unmonitored (risk of re-enabling paused campaigns and unexpected spend) |
| MS-CM1 | Consent Mode compliance (EEA/UK) | High | Consent Mode implemented by May 5, 2025 deadline for EEA/UK/Switzerland audiences. Required for behavioral modeling and conversion recovery | Implementation in progress | Not implemented for EEA/UK/CH audiences (non-compliant since May 2025) |
| MS-CT1 | CTV ad inventory coverage | Medium | CTV placements evaluated for brand/awareness campaigns. Microsoft CTV now serves on Netflix, Max, Hulu, Roku, discovery+. 30-second non-skippable format available | N/A | CTV not evaluated despite brand awareness objectives |
| MS-VD1 | Video ad inventory utilization | Medium | Video formats tested: 9:16 vertical video (available since Apr 2025), up to 90-second duration. Copilot Image Animation (Nov 2025 pilot) evaluated for static-to-video conversion | N/A | No video assets despite available inventory and video-capable campaigns |

---

## Context Notes

- **PMax on Microsoft**: Up to 300 campaigns per account (vs 100 on Google). LinkedIn profile data integration. No video placements. Self-serve negative keywords in open beta (Feb 2026)
- **Scheduled imports danger**: Can re-enable paused campaigns silently. Deactivate after initial setup
- **CTV inventory (2025-2026)**: Netflix, Max, Hulu, Roku, discovery+. 30-second non-skippable on CTV
- **Auto-generated RSA (Jan 2026)**: Enabled by default globally. 5% CTR increase
- **Smart Shopping to PMax (Aug 2025)**: All Smart Shopping auto-upgraded
- **Copilot ads**: Show beneath AI responses with "Sponsored" labels in Copilot conversations
- **9:16 vertical video (Apr 2025)**: 90-second duration support added
