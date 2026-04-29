# Advertising Compliance & Privacy Reference

<!-- Updated: 2026-04-13 | v1.5 -->
<!-- Sources: Claude Research, Gemini Research -->

## Google Ads Policies

### Enforcement System: Three-Strike Policy
| Strike | Consequence | Duration |
|--------|------------|----------|
| Strike 1 | 90-day probation | Warning period |
| Strike 2 | 90-day restriction | Limited functionality |
| Strike 3 | Permanent suspension | Account terminated |

### Prohibited Content (Immediate Disapproval)
- Counterfeit goods
- Dangerous products or services
- Dishonest behavior enablement
- Inappropriate content (hate speech, violence, shocking content)

### Restricted Categories (Certification Required)
| Category | Requirement |
|----------|-------------|
| Online pharmacies | Google certification + LegitScript |
| Telemedicine | Platform certification |
| Health insurance | Certification in applicable regions |
| Gambling | State/country-specific licensing |
| Political ads | Identity verification + disclosures |
| Cryptocurrency | Certification required |
| Financial services | Clear APR/fee/terms disclosures |
| Alcohol | Age-gating + regional restrictions |
| Adult content | Age restriction + limited placements |

### Common Disapprovals
- Misleading claims (superlatives without evidence)
- Missing landing page content (404s, under construction)
- Destination mismatch (ad promise ≠ landing page)
- Prohibited content in ad text
- Trademark infringement
- Restricted healthcare claims

### Recommendations Tab: What to Accept/Reject

**Safe to accept:**
- Optimized ad rotation
- Relevant extensions
- Fix disapproved ads

**Usually reject:**
- "Raise your budget"
- "Add broad match keywords"
- "Add new keywords" (auto-suggested)
- Auto-created RSAs
- Bidding strategy switches
- Turn off Optimization Score auto-apply

---

## Meta Ads Policies

### Special Ad Categories (Restricted Targeting)
| Category | Restrictions |
|----------|-------------|
| Housing | No ZIP code, age must be 18-65+, no lookalike |
| Employment | Same restrictions as Housing |
| Credit | Same restrictions as Housing |
| **Financial Products** | **New Jan 2025**, enforced as Special Category |

All Special Ad Categories:
- Cannot target by age (18-65+ only range)
- Cannot target by ZIP code / postal code
- Cannot use Lookalike Audiences
- Must declare category before campaign creation

### Enforcement Scale
- Over 1.3 billion ads rejected or removed in 2024
- Account restrictions escalate with repeated violations
- Appeal process available but slow

### Detailed Targeting Exclusions (Removed)
- Removed from new ad sets: March 31, 2025
- Removed from boosted posts: June 10, 2025
- Existing campaigns with old exclusions stopped: January 15, 2026
- Meta cites 22.6% lower median cost per conversion without exclusions

### Content Rules
- No misleading health/weight loss claims
- Before/after images: heavily restricted
- Cryptocurrency: certification required
- Political ads: "Paid for by" disclosure required
- Personal attributes: cannot imply user has specific condition
- Sensational content: no clickbait tactics

---

## LinkedIn Ads Policies

### Restricted Industries
- Gambling and betting
- Tobacco and related products
- Weapons and ammunition
- Adult content
- Multi-level marketing
- Cryptocurrency (restricted, not prohibited)

### Professional Standards
- B2B focus expected; casual/misleading content penalized
- Thought Leader Ads must come from genuine employees
- Lead Gen Forms must have clear privacy policy
- Job postings must comply with employment laws

---

## TikTok Ads Policies

### Platform Requirements
- Content must feel native (not overly polished/corporate)
- Audio required (TikTok is sound-on)
- Must comply with music licensing for commercial use
- Creator content (Spark Ads) requires creator approval

### Restricted Categories
- Age-restricted products (alcohol, gambling): geo-gated
- Health claims: evidence required
- Financial products: risk disclosures required
- Political ads: banned in many markets

### TikTok Shop Policies
- Products must meet marketplace standards
- No counterfeit or restricted goods
- Seller verification required
- Available in 11 countries (US, UK, key Asian/European markets)

---

## Microsoft Ads Policies

### Import Considerations
- Google Ads policy approvals don't transfer
- Microsoft has separate review process
- Some Google-approved ads may be disapproved on Microsoft
- Bing audience skews older/more conservative; creative should match

### Copilot Placement Policies
- Ads in Copilot must be clearly labeled
- Copilot Checkout (Jan 2026): commerce within conversations
- Higher quality standards for conversational context

---

## Privacy Regulations (February 2026)

### Global Privacy Landscape

| Regulation | Region | Status | Key Requirement |
|-----------|--------|--------|-----------------|
| GDPR | EU/EEA | Active | Consent before tracking; data minimization |
| UK GDPR | UK | Active | Similar to EU GDPR |
| CCPA/CPRA | California | Active | Right to opt out; mandatory audits |
| 20 State Laws | US (various) | Active Jan 2026 | Indiana, Kentucky, Rhode Island newest |
| LGPD | Brazil | Active | Consent and transparency |
| PIPL | China | Active | Consent and data localization |

### Key Privacy Facts (2026)

**Privacy Sandbox is DEAD:**
- Google officially retired October 2025
- Third-party cookies remain in Chrome (~67% browser share)
- Safari and Firefox already block third-party cookies
- No separate consent prompt coming

**iOS App Tracking Transparency (ATT):**
- Average opt-in rate: ~35% (Q2 2025, up from 29% in 2022)
- Gaming highest: 37-50%
- Education lowest: 7-14%
- Apps with <30% opt-in lose 58% of ad revenue on average

**Consent Mode v2 (Mandatory for EU/EEA):**
- Enforcement tightened July 2025
- Without: 90-95% metric drops
- Advanced mode recovers 30-50% of lost conversions
- ~31% of users globally accept tracking cookies

**US State Privacy:**
- 20 state laws active by January 2026
- Texas AG: $1.4 billion settlement for tracking violations
- California CPPA: mandatory cybersecurity audits + data processing risk assessments
- Server-side tracking now architecturally necessary for compliance

### Compliance Decision Tree

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

### Healthcare-Specific Compliance

| Rule | Enforcement |
|------|-------------|
| No remarketing/retargeting for health services | Google policy: account suspension risk |
| No targeting by health conditions | Google, Meta, all platforms |
| Online pharmacy certification | Google: LegitScript required |
| Telemedicine certification | Google: platform certification |
| HIPAA considerations | US: no PHI in tracking pixels |
| Use contextual targeting | Instead of audience targeting |

### Financial Services Compliance

| Rule | Enforcement |
|------|-------------|
| Clear APR/fee/terms disclosures | Google, Meta: ad disapproval |
| Lending certification | Google: account level |
| Crypto certification | Google: account level |
| Risk disclosures | All platforms |
| Financial Products Special Category | Meta (Jan 2025): restricted targeting |
| No misleading income claims | All platforms: account suspension |

---

## 2025-2026 Changes

### Microsoft Consent Mode Deadline
- **May 5, 2025**: Consent Mode required for all campaigns targeting EEA, UK, and Switzerland
- Without implementation, conversion tracking in these regions will be severely degraded

### Meta Link Clicks Redefinition (Feb 2025)
- "Link clicks" metric now **excludes social engagement clicks** (likes, comments, shares)
- Only counts clicks that navigate away from Meta surfaces
- Affects historical benchmarking: year-over-year comparisons will show apparent drops
- Use "outbound clicks" or "landing page views" for continuity

### Meta Shops Native Checkout Phase-Out (June-August 2025)
- Native in-app checkout phased out between June and August 2025
- All checkout flows now redirect to the advertiser's website
- Update any campaigns relying on Shops checkout conversion events

### Google Call Ads Deprecation
- **February 2026**: No new call-only ad creation permitted
- **February 2027**: Existing call ads stop serving entirely
- **Migration path**: Use call assets (extensions) within Responsive Search Ads (RSAs)

### Apple Ads Rebrand (April 2025)
- "Apple Search Ads" officially renamed to **"Apple Ads"**
- Reflects expanded inventory beyond App Store search (Today tab, Search tab, product pages)
- Update all client-facing reports and documentation to use new branding

### EU Sponsored Messaging: LinkedIn (Discontinued Jan 2022)
- Message Ads and Conversation Ads **cannot be delivered to EU members** since January 2022
- LinkedIn removed EU targeting for these formats due to ePrivacy Directive
- **Never recommend Message/Conversation Ads for EU-targeting campaigns**
- Use alternative formats: Sponsored Content, Lead Gen Forms, or InMail via Sales Navigator

### Google Enhanced CPC (ECPC): Fully Deprecated (March 2025)
- ECPC bidding strategy **fully removed** as of March 2025
- Existing ECPC campaigns auto-migrated to Manual CPC (no bid adjustments)
- Recommended migration: Target CPA or Maximize Conversions with optional target

### Google Rule-Based Attribution Models (Deprecated)
- First click, linear, time decay, and position-based attribution models all removed
- All campaigns using these models were **auto-upgraded to Data-Driven Attribution (DDA)**
- DDA is now the only multi-touch attribution option in Google Ads
- Audit note: flag any client reports still referencing legacy attribution models
