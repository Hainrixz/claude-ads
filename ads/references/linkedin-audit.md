# LinkedIn Ads Audit Checklist

<!-- Updated: 2026-04-13 | v1.5 -->
<!-- Sources: Google Research PDF 1 (L01-L25), Claude Research, Gemini Research -->
<!-- Total Checks: 27 | Categories: 6 | See scoring-system.md for weights and algorithm -->

> **Note:** LinkedIn renamed Campaign Groups to Campaigns and Campaigns to Ad Sets in October 2025.

## Quick Reference

| Category | Weight | Check Count |
|----------|--------|-------------|
| Technical Setup | 25% | L01-L02 (2 checks) |
| Audience Quality | 25% | L03-L09 (7 checks) |
| Creative & Formats | 20% | L10-L13 (4 checks) |
| Lead Gen Forms | 15% | L14-L15 (2 checks) |
| Bidding & Budget | 15% | L16-L17 (2 checks) |
| Structure & Performance | N/A | L18-L25 (8 checks, scored across categories) |
| CRM & Compliance | 10% | L-CRM1, L-EU1 (2 checks) |

---

## Technical Setup (25% weight)

| ID | Check | Severity | Pass | Warning | Fail |
|----|-------|----------|------|---------|------|
| L01 | Insight Tag installed | Critical | LinkedIn Insight Tag firing on all pages | Firing on most pages (>90%) | Tag not installed or broken |
| L02 | Conversions API (CAPI) | High | Server-side conversion tracking active (launched 2025) | Planned but not deployed | No server-side tracking |

---

## Audience Quality (25% weight)

| ID | Check | Severity | Pass | Warning | Fail |
|----|-------|----------|------|---------|------|
| L03 | Job title targeting precision | High | Specific job titles matching ICP (not just functions) | Broad function targeting only | No job title targeting |
| L04 | Company size filtering | Medium | Company size matches ICP | Includes all sizes | N/A |
| L05 | Seniority level targeting | High | Seniority appropriate for offer (C-suite for enterprise, Manager for mid-market) | Broad seniority targeting | Mismatched seniority level |
| L06 | Matched Audiences | High | Website retargeting + contact list audiences active | One type active | No matched audiences |
| L07 | ABM company lists | Medium | Target company lists uploaded (up to 300,000) for ABM | Partial list uploaded | No ABM lists for enterprise campaigns |
| L08 | Audience expansion setting | Medium | OFF for precise targeting, ON for scale (intentional). **CRITICAL: Always uncheck Audience Expansion for ABM campaigns.** ABM budget distribution can be wildly uneven. One case showed 96% of budget going to just 3 accounts out of 400 targeted (AJ Wilcox, B2Linked) | N/A | Default ON without review |
| L09 | Predictive audiences | Medium | Predictive audiences tested (replaced Lookalike Audiences 2024; 21% CPL reduction). Now accepts company lists and retargeting sources as inputs (March 2025) | N/A | Not tested for eligible campaigns |

---

## Creative & Formats (20% weight)

| ID | Check | Severity | Pass | Warning | Fail |
|----|-------|----------|------|---------|------|
| L10 | Thought Leader Ads (TLAs) | High | TLAs active, receiving ≥30% of budget for B2B. TLAs expanded to non-employee members March 2025 (customer testimonial UGC possible). Engagement 2-5x higher than standard | TLAs tested but <30% budget | No TLAs (CPC $2.29-4.14 vs $13.23 standard) |
| L11 | Ad format diversity | High | ≥2 formats tested (single image, video, document, carousel) | 1 format only | N/A |
| L12 | Video ads present | Medium | Video ads tested | N/A | No video tested |
| L13 | Creative refresh cadence | Medium | Creative refreshed every 4-6 weeks | Refreshed every 6-10 weeks | Same creative >10 weeks |

---

## Lead Gen Forms (15% weight)

| ID | Check | Severity | Pass | Warning | Fail |
|----|-------|----------|------|---------|------|
| L14 | Lead Gen Form optimization | High | ≤5 fields (reduce friction); 13% CVR benchmark | 6-8 fields | >8 fields (high friction) |
| L15 | Lead Gen Form CRM integration | High | Form synced to CRM in real-time | Synced within 24hrs | Manual CSV download only |

---

## Bidding & Budget (15% weight)

| ID | Check | Severity | Pass | Warning | Fail |
|----|-------|----------|------|---------|------|
| L16 | Bid strategy appropriate | High | Manual CPC or Cost Cap for cost control; start manual, then test automated bidding with established data | N/A | Maximum Delivery left as default without cost analysis (most expensive option) |
| L17 | Budget sufficiency | High | Daily budget ≥$50 for Sponsored Content | $25-$50/day | <$25/day ($10 minimum, insufficient for learning) |

---

## Structure & Performance (scored across categories)

| ID | Check | Severity | Pass | Warning | Fail |
|----|-------|----------|------|---------|------|
| L18 | Ad Set objective alignment | High | Objective matches funnel stage | N/A | Objective mismatched to goal |
| L19 | A/B testing active | Medium | Active A/B test on creative or audience | Test planned | No testing |
| L20 | Frequency monitoring | High | Message frequency ≤1 per 30-45 days per user | 1 per 20-30 days | >1 per 20 days (inbox fatigue) |
| L21 | CTR benchmark | High | Sponsored Content CTR ≥0.44% | CTR 0.30-0.44% | CTR <0.30% |
| L22 | CPC benchmark | Medium | CPC within industry benchmark ($5-7 avg, senior $6.40+) | CPC 20-50% above benchmark | CPC >50% above benchmark |
| L23 | Lead quality tracking | High | Lead-to-opportunity rate tracked (not just CPL) | CPL tracked only | No lead quality metrics |
| L24 | Conversion tracking attribution | Medium | 30-day click / 7-day view window configured | Default window without review | Attribution not configured |
| L25 | Demographics report review | Medium | Job title and company breakdown reviewed monthly | Reviewed quarterly | Never reviewed |

---

## CRM & Compliance (v1.5)

| ID | Check | Severity | Pass | Warning | Fail |
|----|-------|----------|------|---------|------|
| L-CRM1 | CRM integration for revenue attribution | High | Salesforce or HubSpot CRM integration configured (launched June 2025) enabling closed-loop reporting from impression to revenue | CRM available but not integrated with LinkedIn | No CRM integration despite having Salesforce/HubSpot (missing revenue attribution loop) |
| L-EU1 | EU Sponsored Messaging compliance | Medium | No Message Ads or Conversation Ads targeting EU audiences (EU Sponsored Messaging discontinued since January 2022) | N/A | Message/Conversation Ads targeting EU audiences (will not deliver; discontinued) |

---

## Quick Wins (LinkedIn)

| Check | Fix | Time |
|-------|-----|------|
| L01: Insight Tag | Install/verify Insight Tag on all pages | 10 min |
| L10: Thought Leader Ads | Create TLA using employee organic posts | 10 min |
| L14: Lead Gen Form fields | Reduce form to ≤5 fields | 5 min |
| L08: Audience expansion | Review and set intentionally (OFF for precision) | 2 min |
| L20: Message frequency | Set frequency cap to 1 per 30-45 days | 2 min |
| L24: Attribution window | Configure 30-day click / 7-day view | 2 min |

---

## Context Notes

- **October 2025 naming**: Campaign Groups renamed to "Campaigns"; Campaigns renamed to "Ad Sets"
- **CRM integration (June 2025)**: Salesforce/HubSpot closed-loop reporting from impression to revenue
- **TLA expansion (March 2025)**: Non-employee members can now be featured in Thought Leader Ads
- **Predictive Audiences (March 2025)**: Now accept company lists and retargeting sources
- **LinkedIn Audience Network**: Expert consensus (AJ Wilcox, $200M+ spend): turn it OFF. Quality is poor. It's enabled by default
- **Document Ads**: 7.00% engagement rate (14% YoY increase), leading all LinkedIn content formats
- **Conversation Ads**: 50-60% open rates, 2-5% CTR (far exceeds feed benchmarks of 0.3-0.5%)
- **Connected TV Ads (2025)**: LinkedIn extended reach to CTV inventory via partnerships, allowing B2B brand campaigns on streaming platforms.
- **BrandLink (2025)**: Premium video placement alongside trusted publisher content on LinkedIn. Ideal for awareness-stage B2B campaigns.
- **Live Event Ads (2025)**: Sponsored LinkedIn Live events with built-in registration and reminder flows. Effective for webinar-driven lead gen.
- **Accelerate ad sets**: LinkedIn's AI-optimized ad set type delivers 42% lower CPA and 21% lower CPL on average. Recommended for advertisers with sufficient conversion history.

---

## LinkedIn-Specific Context

| Fact | Value |
|------|-------|
| Minimum audience for delivery | 500 members |
| Recommended audience size | 50,000-300,000 |
| Predictive Audiences seed | 300+ members |
| Company list upload limit | 300,000 |
| Lookalike audiences | Discontinued Feb 29, 2024 |
| Lead Gen Form CVR benchmark | 13% (3.25x landing pages) |
| B2B ROAS benchmark | 113% ($1.13 per $1 spent) |
| Accelerate ad sets | 42% lower CPA, 21% lower CPL |
| TLA CPC advantage | $2.29-4.14 vs $13.23 standard |
| Hierarchy naming (Oct 2025) | "Campaigns" (formerly Campaign Groups) → "Ad Sets" (formerly Campaigns) |
