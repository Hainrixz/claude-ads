# Advertising Compliance & Privacy — Index

Compliance content is split into three focused files to stay within the 200-line reference budget. Load only what you need for the audit at hand:

| Topic | File |
|-------|------|
| Per-platform ad policies (Google strike system, Meta Special Ad Categories, LinkedIn restricted industries, TikTok native rules, Microsoft import notes, Copilot) | [`compliance-platforms.md`](compliance-platforms.md) |
| Privacy regulations (GDPR, CCPA/CPRA, 20 US state laws, Consent Mode v2, ATT, healthcare/finance rules, compliance decision tree) | [`compliance-privacy.md`](compliance-privacy.md) |
| 2025-2026 change log (Consent Mode deadline, Meta link-clicks redefinition, Meta Shops checkout phase-out, Google Call Ads sunset, Apple rebrand, ECPC removal, attribution model deprecations) | [`compliance-changes-2025-2026.md`](compliance-changes-2025-2026.md) |

## Quick-lookup decision

- **Special Ad Category required?** → housing, employment, credit, or financial products (since Jan 2025 Meta) → `compliance-platforms.md`
- **Audit covers EU/EEA traffic?** → Consent Mode v2 mandatory; check `compliance-privacy.md`
- **Audit covers California or any of 20 US state laws?** → CCPA/CPRA + state-specific → `compliance-privacy.md`
- **Healthcare or financial services account?** → category-specific rules in both `compliance-platforms.md` and `compliance-privacy.md`
- **Finding a deprecated feature still in use** (ECPC, rule-based attribution, Call Ads, native Shops checkout, EU Message Ads)? → `compliance-changes-2025-2026.md` for current migration guidance
