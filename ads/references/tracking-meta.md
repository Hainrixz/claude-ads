# Meta Ads Conversion Tracking

## Required Stack

```
1. Meta Pixel → base code on all pages + standard events
2. Conversions API (CAPI) → server-side event forwarding
3. Event Deduplication → event_id matching between Pixel and CAPI
4. EMQ Optimization → pass email, phone, fbp, fbc, external_id
```

## Event Match Quality (EMQ) Scoring

| Score | Rating | Action |
|-------|--------|--------|
| <4.0 | Critical | Severe data loss; urgent fix needed |
| 4.0-5.9 | Warning | Significant signal gaps |
| 6.0-7.9 | Acceptable | Some optimization possible |
| 8.0-10.0 | Excellent | Maximum signal strength |

**Key parameters by impact:**

- Email: +4.0 points
- Phone: +3.0 points
- External ID: significant
- fbp (browser ID): important
- fbc (click ID): important

**87% of advertisers have poor EMQ**; fixing it improves performance 20-40%.

**Tiered EMQ Targets by Event:**

- Purchase: 8.5+
- AddToCart: 6.5+
- PageView: 5.5+

## Event Deduplication

```
Same event_id + same event_name = deduplicated (correct)
Missing event_id = potential double-counting (broken)

Check: Events Manager > Overview > Deduplication Rate
Target: 90%+ deduplication rate
```

## CAPI Performance Impact

- Without CAPI: 30-40% data loss post-iOS 14.5 (pixel-only tracking is critically insufficient)
- With CAPI: 15-20% performance increase over pixel-only
- Bypasses ad blockers and iOS ATT limitations
- 87% of advertisers have poor Event Match Quality; fixing CAPI improves performance 20-40%
- Offline Conversions API permanently discontinued May 2025. All offline tracking now uses CAPI with `action_source='physical_store'`.

## Standard Events (Use These, Not Custom)

```
Purchase, AddToCart, InitiateCheckout, AddPaymentInfo,
Lead, CompleteRegistration, Subscribe, ViewContent,
Search, AddToWishlist, Contact, CustomizeProduct,
FindLocation, Schedule, StartTrial, SubmitApplication
```

## Attribution

- 7-day click / 1-day view (default and recommended)
- Top 8 events configured in AEM (Aggregated Event Measurement)
- Domain verification required in Business Manager
- Financial Products & Services = new Special Ad Category (Jan 2025)

## MCP-First Path

When `ad_account_id` is supplied, the `audit-meta` agent queries Meta MCP tools rather than reading these definitions back to the user. See [`mcp-meta-integration.md`](mcp-meta-integration.md) for the check↔tool mapping (M01-M10 are largely live-data lookups now).
