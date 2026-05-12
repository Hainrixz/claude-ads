# Meta Ads Bidding Decision Engine

## Auction Formula

```
Total Value = Bid × Estimated Action Rate + User Value
```

## Strategy Selection

```
DEFAULT (90% of campaigns):
  → Lowest Cost (no cap)
  → Best for: Most campaigns, volume maximization
  → Risk: CPA can spike during high-competition (Q4)

IF need cost predictability:
  → Cost Cap
  → Set at: 1.2x - 1.5x target CPA
  → Best for: Scaling with margin protection
  → Risk: Under-delivery if cap too aggressive

IF need strict cost control:
  → Bid Cap
  → Set at: 2x - 3x target CPA
  → Best for: Experienced advertisers with clear unit economics
  → Risk: Significant under-delivery if too low

IF e-commerce with revenue tracking:
  → ROAS Goal
  → Best for: Advantage+ Sales Campaigns
  → Requires: Purchase event + dynamic values

IF high-value diverse products:
  → Highest Value
  → Prioritizes high-value conversions
  → Best for: Wide AOV range
```

## Andromeda Context

Under Andromeda, creative diversity matters more than bid strategy. Focus budget on creative testing, not micro-optimizing bids.

## CBO vs ABO Decision

```
IF daily_budget < $100:
  → ABO (manual control for testing)

IF daily_budget $100-$500:
  → Test both; CBO if similar audiences, ABO if diverse

IF daily_budget > $500:
  → CBO (Advantage+ Campaign Budget)
  → Let Meta optimize distribution

NOTE: Advantage+ Sales/Leads auto-enable CBO
```

## Learning Phase Rules

**Exit criteria:** 50 conversions per week per ad set

**Reset triggers (avoid during learning):**
- Budget change >20%
- Any targeting change
- Creative edit (even text)
- Bid strategy change
- Pausing >7 days

**If "Learning Limited":**
1. Broaden audience
2. Increase budget
3. Switch to higher-funnel event (AddToCart instead of Purchase)
4. Consolidate ad sets
5. Ensure daily budget ≥5× target CPA
