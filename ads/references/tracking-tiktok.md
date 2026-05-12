# TikTok Ads Conversion Tracking

## Required Stack

```
1. TikTok Pixel → base code + standard events on all pages
2. Events API → server-side event forwarding
3. ttclid Passback → capture from URL params, send with events
4. Advanced Matching → hashed email/phone
```

## Key Difference: ttclid

- TikTok Click ID (ttclid) comes in landing page URL parameters.
- MUST be captured and stored on first page load (cookie or session storage).
- MUST be sent back with all conversion events to the Events API.
- Without ttclid: attribution breaks for many conversions; TikTok over-claims via modeled attribution.

## Standard Events

```
ViewContent, AddToCart, InitiateCheckout, AddPaymentInfo,
Purchase, CompleteRegistration, Lead, Subscribe
```

Match Pixel + Events API event_id between client-side and server-side to avoid double-counting.

## Learning Phase

- ~50 conversions in 7 days to exit learning.
- Budget ≥50× target CPA per ad group (provides sufficient learning room).
- Avoid edits during learning phase (resets the learning timer).

## Attribution Windows

| Window | TikTok default | Recommended |
|--------|---------------|-------------|
| Click | 7 days | 7-day click for e-commerce, 14-28 day for B2B/considered purchases |
| View | 1 day | Keep at 1 day to avoid view-through over-claim |

## Events API Gateway (2024+)

Recommended for accounts running 100+ conversions/week. Reduces data loss
from ad-blockers and iOS ATT, improves Match Rate by 15-30%.
