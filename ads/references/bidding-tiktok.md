# TikTok Ads Bidding

## Strategy Selection

```
DEFAULT:
  → Lowest Cost (volume maximization)
  → Most common, good starting point

IF margin protection needed:
  → Cost Cap
  → Set target CPA, system tries to stay near

IF strict cost control needed:
  → Bid Cap
  → Controls maximum bid per auction (not average CPA)
  → Set at 2-3x target CPA initially
  → Best for: retargeting, competitive niches (Q4/BFCM)
  → Risk: significant under-delivery if set too aggressively

IF Smart+ campaign:
  → Modular automation (choose per module)
  → Up to 30 ad groups, 50 creatives per asset group
  → Smart+ now supports modular control (2025). Lock
    targeting/creative/budget/placement independently
    while automating others

GMV Max (TikTok Shop):
  → Default/only for Shop campaigns (July 2025)
  → Optimizes for Gross Merchandise Value
```

## Budget Rules

- Campaign minimum: $50/day
- Ad group minimum: $20/day
- Budget should be ≥50× target CPA per ad group (provides sufficient learning room)
- Learning phase: ~50 conversions in 7 days

## Cross-Platform Bidding Red Flags

| Red Flag | Severity | Platform | Action |
|----------|----------|----------|--------|
| Broad Match + Manual CPC | Critical | Google | Switch to Smart Bidding or Exact Match |
| tCPA <50% of actual CPA | Critical | Google | Unrealistic target; set at 1.1-1.2× historical |
| Smart Bidding with <15 conv/month | High | Google | Use Manual CPC or Maximize Clicks |
| >50% ad sets "Learning Limited" | Critical | Meta | Consolidate, broaden audience, increase budget |
| Cost Cap below historical CPA | High | Meta | Set at 1.2-1.5× target, not below |
| Daily budget <5× CPA | High | Meta | Increase budget or switch to higher-funnel event |
| Budget < $50/day campaign | High | TikTok | Increase to minimum or consolidate |
| No negative keywords with Broad Match | Critical | Google | Add themed negative lists immediately |
| No Portfolio strategy for low-vol campaigns | Medium | Google | Group <15 conv campaigns into portfolio |
