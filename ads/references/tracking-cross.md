# Cross-Platform Tracking Health Audit

## Critical Checks (Run for All Platforms)

| Check | Severity | Pass Criteria |
|-------|----------|---------------|
| Primary conversion action exists | Critical | ≥1 active conversion per platform |
| Server-side tracking active | Critical | CAPI/Server GTM/Events API configured |
| Event deduplication | Critical | event_id matching (Meta), no double-counting |
| Consent Mode v2 (EU) | Critical | Implemented if serving EU/EEA |
| Enhanced Conversions / EMQ | High | Google: enabled; Meta: EMQ ≥6.0 |
| Micro vs macro separation | High | Only macro conversions set as Primary |
| Attribution model appropriate | Medium | DDA (Google), 7d/1d (Meta) |
| Conversion window matches cycle | Medium | 7d (ecom), 30-90d (B2B), 30d (lead gen) |
| Offline conversion import | Medium | Active for lead gen / B2B accounts |
| First-party data utilization | High | Customer Match / Custom Audiences from CRM |

## Server-Side Tracking Priority

```
IF business_type IN [ecommerce, lead_gen, saas]:
  server_side_tracking = CRITICAL

IF platform == "Meta":
  CAPI = CRITICAL (30-40% data loss without post-iOS 14.5)

IF region == "EU/EEA":
  consent_mode_v2 = CRITICAL (90-95% metric drops without)

server_side_recovery = 10-30% accuracy improvement
```

## General Note: Incrementality Measurement

Meridian (2025): Google's open-source Marketing Mix Model for incrementality measurement. Useful for advanced accounts evaluating cross-channel contribution.
