# Google Ads Bidding Decision Engine

## Strategy Selection Flow

```
START → How many conversions in last 30 days?

┌─ < 15 conversions ──────────────────────────┐
│  → Maximize Clicks (cold start)             │
│  → Set Max CPC = Target_CPA / (CVR × 1.5)  │
│  → Learning: 3-5 days                       │
│  → Monitor until 15+ conversions achieved    │
│  → OR use Manual CPC if full control needed  │
│  → NOTE: eCPC fully removed March 2025       │
└──────────────────────────────────────────────┘

┌─ 15-29 conversions ─────────────────────────┐
│  → Maximize Conversions (uncapped)          │
│  → Learning: 7-14 days                      │
│  → Transition when CPA SD < 20% over 14d   │
│  → THEN switch to Target CPA               │
└──────────────────────────────────────────────┘

┌─ 30+ conversions, NO dynamic values ────────┐
│  → Target CPA                               │
│  → Strict: 30+ (Google says 15, but 30+     │
│    for reliable performance, 50+ ideal)      │
│  → Set at: 1.1x-1.2x historical CPA        │
│  → Adjust: Max 10% change every 14 days     │
│  → Never lower by more than 15% at once     │
└──────────────────────────────────────────────┘

┌─ 50+ conversions WITH dynamic values ───────┐
│  → Target ROAS                              │
│  → Requires dynamic conversion values        │
│  → Set at: EXACT historical ROAS            │
│  → Formula: Bid = P(conv) × Value × 1/tROAS│
│  → Adjust: Same rules as tCPA              │
└──────────────────────────────────────────────┘

┌─ Brand Protection campaigns ────────────────┐
│  → Target Impression Share                  │
│  → Target: 95-100% on brand keywords        │
│  → No conversion data requirement           │
│  → Search only (not available elsewhere)     │
└──────────────────────────────────────────────┘

SPECIAL CASES:
- PMax: Always uses Maximize Conversions or Maximize Conv Value
- Demand Gen: Supports Target CPC (new), tCPA, tROAS, Max Clicks
- Display Pay per Conversion: Eligibility required
```

## Smart Bidding Exploration (2025+)

Allows flexible ROAS targets to discover new traffic. Delivers 18% more unique search query categories + 19% more conversions.

- **How it works**: Algorithm temporarily relaxes ROAS constraints to enter auctions it would normally skip, testing new user segments
- **When to enable**: Stable tROAS campaigns with 50+ conversions/month seeking incremental growth beyond current query coverage
- **When to avoid**: Tight-margin accounts or campaigns already spending full budget (exploration adds volume, not just efficiency)
- **Available on**: Target ROAS bid strategies only

## AI Max for Search (2025+)

AI Max for Search layers broad match + keywordless targeting on existing Search campaigns. 14% avg conversion lift. DSA likely consolidated into AI Max Q2 2026. Requires strong negative keyword lists.

- **How it works**: Automatically expands keyword coverage using AI to match user intent beyond exact keyword matches
- **When to enable**: Established Search campaigns with healthy conversion volume and comprehensive negative keyword lists
- **When to avoid**: Low-budget campaigns without negative keyword hygiene; accounts with strict brand safety requirements
- **Migration note**: Begin migrating DSA campaigns to AI Max before Q2 2026

## Attribution Model

- **DDA (Data-Driven Attribution) is now MANDATORY default** (September 2025)
- Only two models remain: DDA and Last Click
- All rule-based models deprecated (first-click, linear, time decay, position-based)
- No minimum data threshold for DDA
- Impact on bidding: DDA distributes conversion credit across touchpoints, affecting Smart Bidding signals

## Portfolio Bid Strategies

When to use portfolios:
- Multiple campaigns each with <15 conv, but combined >30
- Need cross-campaign budget optimization
- **CPC Cap Hack**: Only way to set max CPC bid on tCPA/tROAS

Rules:
- Minimum 3 campaigns per portfolio for meaningful data
- Group campaigns with similar target CPAs/ROAS
- Never mix brand and non-brand in same portfolio

## Transition Triggers

| From | To | Trigger |
|------|----|---------|
| Maximize Clicks | Maximize Conversions | 15+ conversions in 30 days |
| Maximize Conversions | Target CPA | CPA SD <20% over 14 days + 30+ conv |
| Target CPA | Target ROAS | 50+ conv + dynamic values available |
| Manual CPC | Maximize Clicks | Ready to test automation |
| Any | Target Impression Share | Brand protection need identified |
