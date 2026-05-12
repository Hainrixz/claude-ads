# Conversion Tracking Setup & Requirements — Index

Tracking content is split per-platform to stay under the 200-line reference budget. Load only the files the audit needs.

| File | Covers |
|------|--------|
| [`tracking-google.md`](tracking-google.md) | gtag.js stack, Enhanced Conversions, Consent Mode v2, DDA, Customer Match, duplicate-detection rules |
| [`tracking-meta.md`](tracking-meta.md) | Meta Pixel + CAPI stack, EMQ scoring, event deduplication, standard events, AEM. MCP-first via `mcp-meta-integration.md` |
| [`tracking-tiktok.md`](tracking-tiktok.md) | TikTok Pixel + Events API + ttclid passback, learning phase, standard events, Events API Gateway |
| [`tracking-cross.md`](tracking-cross.md) | Cross-platform health checklist, server-side tracking priority logic, incrementality (Meridian) |

## Quick decision

- Auditing Meta? CAPI + EMQ are critical post-iOS 14.5. → `tracking-meta.md`
- Auditing TikTok? ttclid passback is the most common attribution failure. → `tracking-tiktok.md`
- Serving EU/EEA traffic on any platform? Consent Mode v2 advanced is mandatory. → `tracking-google.md` (gtag example) + `compliance-privacy.md`
- E-commerce on any platform? Offline conversion import + dynamic values are the highest-leverage upgrades.
