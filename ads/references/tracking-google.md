# Google Ads Conversion Tracking

## Required Stack

```
1. Global Site Tag (gtag.js) → all pages
2. Enhanced Conversions → hashed first-party data (email, phone, address, name)
3. Consent Mode v2 → MANDATORY for EU/EEA since March 2024
4. Server-Side GTM → recommended for data durability
5. Offline Conversion Import → for lead gen (CRM → Google Ads)
```

## Enhanced Conversions

- Sends SHA-256 hashed first-party data
- Improves measurement by ~10% more measured conversions
- Required for smart bidding accuracy in cookie-degraded environments
- Setup via gtag.js or Google Tag Manager
- Works alongside standard conversion tracking

## Consent Mode v2

```javascript
// Default (before consent)
gtag('consent', 'default', {
  'ad_storage': 'denied',
  'ad_user_data': 'denied',
  'ad_personalization': 'denied',
  'analytics_storage': 'denied'
});

// After user grants consent
gtag('consent', 'update', {
  'ad_storage': 'granted',
  'ad_user_data': 'granted',
  'ad_personalization': 'granted',
  'analytics_storage': 'granted'
});
```

- Enforcement began July 21, 2025 for EEA/UK. Requires 700+ ad clicks/day over 7 days per country/domain for behavioral modeling to activate. Advanced mode mandatory (Basic = huge data loss). Combined with Enhanced Conversions + server-side tagging, recovers 30-50% of lost conversions.
- Enables conversion modeling for unconsented users
- Without implementation: 90-95% metric drops (enforcement tightened July 2025)
- ~31% of users accept tracking cookies globally

## Attribution

- **DDA (Data-Driven Attribution) is now MANDATORY default** (September 2025)
- Only two models remain: DDA and Last Click
- All rule-based models deprecated (first-click, linear, time decay, position-based)
- No minimum data threshold for DDA
- Windows: Click 1/3/7/30(default)/60/90 days; Engaged-view 3d; View-through 1d

## Customer Match

- Requires 90 days of account history and $50,000+ lifetime spend for full access
- Maximum membership duration: 540 days (changed April 7, 2025; previously infinite)
- Use for RLSA, similar audiences, and Customer Match lists
- First-party data source: CRM emails, phone numbers, addresses

## Conversion Setup Rules

- Use Google Ads native tracking as PRIMARY for bidding (real-time data)
- Import GA4 conversions for observation only
- Never count both (double-counting)
- Separate micro (AddToCart, TimeOnSite) from macro (Purchase, Lead) conversions
- Only macro conversions as "Primary" for bidding optimization

## Duplicate Detection Accuracy

- Only check **ENABLED** conversion actions for duplicates; exclude HIDDEN and REMOVED actions (they cannot cause double-counting)
- Exclude Smart Campaign system-managed conversions (e.g., 'Smart campaign map clicks to call') from DDA and counting-type checks; their attribution model and counting type are locked by Google
