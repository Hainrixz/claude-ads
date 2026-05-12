# Privacy Regulations (2026)

## Global Privacy Landscape

| Regulation | Region | Status | Key Requirement |
|-----------|--------|--------|-----------------|
| GDPR | EU/EEA | Active | Consent before tracking; data minimization |
| UK GDPR | UK | Active | Similar to EU GDPR |
| CCPA/CPRA | California | Active | Right to opt out; mandatory audits |
| 20 State Laws | US (various) | Active Jan 2026 | Indiana, Kentucky, Rhode Island newest |
| LGPD | Brazil | Active | Consent and transparency |
| PIPL | China | Active | Consent and data localization |

## Key Privacy Facts (2026)

### Privacy Sandbox is DEAD

- Google officially retired October 2025
- Third-party cookies remain in Chrome (~67% browser share)
- Safari and Firefox already block third-party cookies
- No separate consent prompt coming

### iOS App Tracking Transparency (ATT)

- Average opt-in rate: ~35% (Q2 2025, up from 29% in 2022)
- Gaming highest: 37-50%
- Education lowest: 7-14%
- Apps with <30% opt-in lose 58% of ad revenue on average

### Consent Mode v2 (Mandatory for EU/EEA)

- Enforcement tightened July 2025
- Without: 90-95% metric drops
- Advanced mode recovers 30-50% of lost conversions
- ~31% of users globally accept tracking cookies

### US State Privacy

- 20 state laws active by January 2026
- Texas AG: $1.4 billion settlement for tracking violations
- California CPPA: mandatory cybersecurity audits + data processing risk assessments
- Server-side tracking now architecturally necessary for compliance

## Compliance Decision Tree

```
IF serving_region INCLUDES "EU/EEA":
  → Consent Mode v2 = MANDATORY
  → Cookie consent banner = MANDATORY
  → Data Processing Agreement = MANDATORY
  → Enhanced Conversions with consent = RECOMMENDED

IF serving_region INCLUDES "California":
  → CCPA/CPRA compliance = MANDATORY
  → "Do Not Sell" link = MANDATORY
  → Data processing risk assessment = MANDATORY (2026)

IF serving_region INCLUDES any US state:
  → Check specific state law requirements
  → 20 states have active laws as of Jan 2026

FOR ALL REGIONS:
  → Server-side tracking = RECOMMENDED (bypasses most client-side issues)
  → First-party data strategy = ESSENTIAL
  → Privacy policy on landing pages = MANDATORY
```

## Healthcare-Specific Compliance

| Rule | Enforcement |
|------|-------------|
| No remarketing/retargeting for health services | Google policy: account suspension risk |
| No targeting by health conditions | Google, Meta, all platforms |
| Online pharmacy certification | Google: LegitScript required |
| Telemedicine certification | Google: platform certification |
| HIPAA considerations | US: no PHI in tracking pixels |
| Use contextual targeting | Instead of audience targeting |

## Financial Services Compliance

| Rule | Enforcement |
|------|-------------|
| Clear APR/fee/terms disclosures | Google, Meta: ad disapproval |
| Lending certification | Google: account level |
| Crypto certification | Google: account level |
| Risk disclosures | All platforms |
| Financial Products Special Category | Meta (Jan 2025): restricted targeting |
| No misleading income claims | All platforms: account suspension |
