# Compliance Changes — 2025-2026 Timeline

Material policy and feature changes that affect audit findings and recommendations. Surface these as `WARNING`/`FAIL` when accounts still use deprecated configurations.

## Microsoft Consent Mode Deadline

- **May 5, 2025**: Consent Mode required for all campaigns targeting EEA, UK, and Switzerland
- Without implementation, conversion tracking in these regions will be severely degraded

## Meta Link Clicks Redefinition (Feb 2025)

- "Link clicks" metric now **excludes social engagement clicks** (likes, comments, shares)
- Only counts clicks that navigate away from Meta surfaces
- Affects historical benchmarking: year-over-year comparisons will show apparent drops
- Use "outbound clicks" or "landing page views" for continuity

## Meta Shops Native Checkout Phase-Out (June-August 2025)

- Native in-app checkout phased out between June and August 2025
- All checkout flows now redirect to the advertiser's website
- Update any campaigns relying on Shops checkout conversion events

## Google Call Ads Deprecation

- **February 2026**: No new call-only ad creation permitted
- **February 2027**: Existing call ads stop serving entirely
- **Migration path**: Use call assets (extensions) within Responsive Search Ads (RSAs)

## Apple Ads Rebrand (April 2025)

- "Apple Search Ads" officially renamed to **"Apple Ads"**
- Reflects expanded inventory beyond App Store search (Today tab, Search tab, product pages)
- Update all client-facing reports and documentation to use new branding

## EU Sponsored Messaging: LinkedIn (Discontinued Jan 2022)

- Message Ads and Conversation Ads **cannot be delivered to EU members** since January 2022
- LinkedIn removed EU targeting for these formats due to ePrivacy Directive
- **Never recommend Message/Conversation Ads for EU-targeting campaigns**
- Use alternative formats: Sponsored Content, Lead Gen Forms, or InMail via Sales Navigator

## Google Enhanced CPC (ECPC): Fully Deprecated (March 2025)

- ECPC bidding strategy **fully removed** as of March 2025
- Existing ECPC campaigns auto-migrated to Manual CPC (no bid adjustments)
- Recommended migration: Target CPA or Maximize Conversions with optional target

## Google Rule-Based Attribution Models (Deprecated)

- First click, linear, time decay, and position-based attribution models all removed
- All campaigns using these models were **auto-upgraded to Data-Driven Attribution (DDA)**
- DDA is now the only multi-touch attribution option in Google Ads
- Audit note: flag any client reports still referencing legacy attribution models
