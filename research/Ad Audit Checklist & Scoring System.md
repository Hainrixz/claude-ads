# Algorithmic Integrity and Performance Auditing: A Technical Standard for Digital Advertising Compliance

---

## 1. Executive Summary: The Shift to Deterministic Auditing

The digital advertising landscape has undergone a fundamental architectural shift. The era of manual bid adjustments and granular keyword management has largely ceded territory to algorithmic automation---systems driven by machine learning models such as Google's Smart Bidding, Meta's Advantage+, and TikTok's Automated Creative Optimization. In this environment, the role of the account audit transforms from a subjective review of human strategy to a deterministic evaluation of algorithmic inputs. The auditor's primary function is no longer to judge creative aesthetics but to verify "Signal Integrity" and "Algorithmic Freedom."

Signal Integrity refers to the technical fidelity of the data loop feeding the ad platform. If a conversion pixel misfires, or if server-side deduplication fails, the algorithm optimizes toward a hallucination. Algorithmic Freedom refers to the structural constraints placed on the machine; hyper-segmented account structures (such as Single Keyword Ad Groups or SKAGs) often starve modern algorithms of the data density required for statistical significance, forcing them into a perpetual state of "Learning Limited."

This report establishes a rigorous technical specification for claude-ads, an automated auditing engine. It defines over 170 specific, binary, and numeric pass/fail criteria across Google, Meta, LinkedIn, TikTok, and Microsoft advertising platforms. These specifications are designed not merely as best practices but as hard-coded logic gates that determine the health of an advertising ecosystem. The methodology prioritizes the mathematical realities of auction dynamics---Impression Share, Quality Score, Event Match Quality, and Auction Overlap---over subjective marketing trends.

---

## 2. Standardized Scoring Methodology

To convert complex, multi-dimensional audit data into a singular, actionable metric, a weighted scoring algorithm is essential. This system must account for the disparate impact of various failure modes; a broken conversion tag (Critical) renders an account functionally useless, whereas a missing sitelink extension (Low) merely represents a marginal efficiency loss.

### 2.1 The Weighted Scoring Algorithm

The final account score (S_total) is derived using a category-weighted arithmetic mean, adjusted by severity multipliers. Each individual audit check (C_i) is assigned a severity tier (W_sev) and falls within a functional category (Cat_j) carrying a specific category weight (W_cat).

The severity weights are calibrated to reflect the existential risk to account performance:

- **Critical (Multiplier: 5.0):** These are "Kill Switch" issues. Their presence implies that reported data is false or that capital is being deployed with near-zero efficiency. Examples include offline conversion tracking, >90% budget wasted on irrelevant search terms, or a Meta Pixel with <3.0 Event Match Quality. A failure here triggers an automatic "F" grade for the specific section.
- **High (Multiplier: 3.0):** These issues cause significant inefficiency, volume loss, or algorithmic confusion. Examples include Quality Scores below 5, creative fatigue indices >0.6, or audience overlaps >30%.
- **Medium (Multiplier: 1.5):** These represent violations of modern best practices that hinder optimization but do not break the system. Examples include excessive keyword density per ad group (>20) or missing secondary ad extensions.
- **Low (Multiplier: 0.5):** Housekeeping, hygiene, and minor optimizations, such as inconsistent naming conventions or disorganized labels.

The algorithmic logic for the final score calculation is expressed as:

$$S_{total} = \frac{\sum(C_{pass} \times W_{sev} \times W_{cat})}{\sum(C_{total} \times W_{sev} \times W_{cat})} \times 100$$

### 2.2 Category Weight Distribution

The weights assigned to each audit category reflect the specific architectural priorities of each platform. For instance, in Google Ads, "Search Terms" and "Keywords" hold primacy because it is a pull-based intent channel. In contrast, for Meta Ads, "Creative" and "Pixel Health" are dominant because it is a push-based discovery channel reliant on signal resilience and visual engagement.

| Platform | Category | Weight (%) | Rationale |
|----------|----------|------------|-----------|
| **Google** | Conversion Tracking | 25% | Smart Bidding (tCPA/tROAS) fails fundamentally without accurate data. |
| | Wasted Spend / Negatives | 20% | Direct impact on financial efficiency and CPA. |
| | Account Structure | 15% | Determines Quality Score, Ad Rank, and data density. |
| | Keywords & Quality Score | 15% | The core mechanism of the Search auction. |
| | Ads & Assets (RSA/PMax) | 15% | Critical for CTR, Ad Rank, and inventory access. |
| | Settings & Targeting | 10% | Foundational hygiene and geo-fencing. |
| **Meta** | Pixel/CAPI Health | 30% | Post-iOS14, signal resilience is the primary determinant of success. |
| | Creative (Diversity/Fatigue) | 30% | Creative is the primary targeting lever on social platforms. |
| | Account Structure | 20% | Consolidation is required for algorithmic learning phases. |
| | Audience & Targeting | 20% | Overlap and saturation checks to prevent self-competition. |

### 2.3 Grading Thresholds and "Quick Wins"

The numeric score output (0--100) maps to qualitative performance bands. These thresholds are strict; an account in the "C" range is functioning but leaking significant budget, while an "A" account is fully optimized for machine learning.

- **A (90--100): Algorithmic Excellence.** The account operates with high signal integrity, consolidated structures, and maximal asset density.
- **B (75--89): Performant.** A solid foundation exists, likely with minor inefficiencies in asset variety or secondary extension coverage.
- **C (60--74): Compromised.** The account is functional but inefficient. It likely suffers from fragmentation (too many ad sets/groups) or creative fatigue.
- **D (40--59): At Risk.** Major fundamental errors are present. Tracking may be intermittent, or wasted spend is unchecked.
- **F (<40): Critical Failure.** The account is actively burning capital with little attributable return. Immediate pause and remediation are required.

**Quick Wins Logic:**

The system must algorithmically identify "Quick Wins" to prioritize user action. A check is classified as a Quick Win if it meets the following Boolean logic:

1. **Severity** == High OR Critical
2. **Remediation Time** == Low (<15 minutes)

Examples of Quick Wins include adding negative keywords for 0-conversion terms, enabling "Enhanced Conversions" in settings, or excluding "Audience Network" from traffic campaigns.

---

## 3. Google Ads Audit Checklist: The Intent Engine

Google Ads remains the most complex platform to audit due to its multi-layered auction dynamics involving Search, Shopping, Display, and Video. The core philosophy of a Google Ads audit is "Relevance and Hygiene." The system penalizes irrelevance (low Quality Score, wasted search terms) and rewards density (high asset counts in PMax and RSAs).

### 3.1 Account Structure and Hierarchy

The structural integrity of a Google Ads account dictates its ability to learn. In the age of Smart Bidding, the "SKAG" (Single Keyword Ad Group) structure is largely obsolete because it fragments data, preventing the bidding algorithm from achieving statistical significance. The modern standard is the "STAG" (Single Theme Ad Group) or consolidated structure, which pools data to feed the AI.

**Metric Analysis:** The "Ad Group Density" check (G02) monitors the ratio of ad groups to campaigns. An account with 100 campaigns and 1 ad group each (1:1 ratio) often fails to leverage campaign-level budget optimization. Conversely, an ad group with >20 keywords (G03) suffers from "Theme Drift," where the ad copy cannot possibly match the user intent of every keyword, degrading Ad Relevance.<sup>1</sup>

**Table 1: Google Ads Structure & Settings Audit**

| Check # | Category | Check Name | Pass Criteria | Fail Criteria | Severity |
|---------|----------|------------|---------------|---------------|----------|
| G01 | Structure | Campaign Fragmentation | < 1 Campaign per $500/mo spend | > 1 Campaign per $500/mo spend | Medium |
| G02 | Structure | Ad Group Density | 5--20 Ad Groups per Campaign | < 1 or > 50 (diluted data) | Medium |
| G03 | Structure | Keyword Density per Ad Group | ≤ 10 Keywords <sup>1</sup> | > 20 Keywords | High |
| G04 | Structure | Ad Count per Ad Group | 1--3 Active RSAs | 0 Active or > 3 Active | Critical |
| G05 | Structure | Search Network Settings | Display Network Disabled | Display Network Enabled | High |
| G06 | Structure | Search Partner Performance | CPA ≤ 1.2x Search CPA | CPA > 1.2x Search CPA & Enabled | Medium |
| G07 | Structure | Campaign Naming Hygiene | Matches Regex (e.g., `Type | Geo | Goal`) | | Low |
| G08 | Settings | Location Option | "Presence: People in..." | "Interest: People in or interested in..." | High |
| G09 | Settings | Geo Exclusions | Excluded Locations List Populated | Empty Exclusion List | Low |
| G10 | Settings | Ad Schedule (Dayparting) | Applied (Data-driven) | 24/7 (if limited by budget) | Low |
| G11 | Settings | Device Bid Adjustments | Applied to low performers | None (despite variance >20%) | Medium |
| G12 | Settings | Auto-Apply Recommendations | Harmful suggestions OFF (e.g., Broad Match) | Harmful suggestions ON | Medium |

### 3.2 Search Terms and Wasted Spend

This category represents the most direct financial impact. "Wasted Spend" is defined as budget consumed by search terms that generate clicks but zero conversions. While some exploration is necessary, algorithmic efficiency demands that this waste be capped.

**Technical Thresholds:** The audit sets a strict fail threshold for irrelevant spend. If more than 10% of the budget is allocated to search terms classified as irrelevant (via N-gram analysis or manual review logic), the account fails.<sup>1</sup> Furthermore, "Zero-Conversion Spend" is a critical efficiency metric. A threshold of 20% of the total budget spent on 0-conversion terms is the fail line.<sup>2</sup> The audit also utilizes a specific query volume check: identifying search terms with >30 clicks and 0 conversions as immediate candidates for negative keywords.<sup>3</sup>

**Table 2: Google Ads Search Terms & Negatives Audit**

| Check # | Category | Check Name | Pass Criteria | Fail Criteria | Severity |
|---------|----------|------------|---------------|---------------|----------|
| G13 | Search Terms | Irrelevant Spend Ratio | < 5% of spend | > 10% of spend <sup>1</sup> | High |
| G14 | Search Terms | Zero-Conversion Waste | < 10% of total budget | > 20% of total budget <sup>2</sup> | Critical |
| G15 | Search Terms | High-Volume Losers | 0 terms with >30 clicks & 0 conv | > 0 terms with >30 clicks & 0 conv <sup>3</sup> | High |
| G16 | Search Terms | Search Term Coverage | > 80% of volume matched to keywords | < 50% matched | Medium |
| G17 | Negatives | Negative Keyword Conflicts | 0 Conflicts | > 0 Conflicts | Critical |
| G18 | Negatives | Negative List Usage | Shared Lists Applied | Campaign-level negatives only | Low |
| G19 | Negatives | Brand Isolation | 0% Brand Imp. in Non-Brand | > 5% Brand Imp. in Non-Brand | High |

### 3.3 Quality Score and Keyword Health

Quality Score (QS) is not a vanity metric; it is a proxy for Ad Rank and Cost Per Click (CPC). A low QS forces the advertiser to pay a premium for every click. The audit analyzes the distribution of QS across the account's active keywords.

**Critical Thresholds:** A healthy account maintains a weighted Quality Score where ≥70% of keywords are QS 7 or higher.<sup>1</sup> Conversely, any account where >20% of spend goes to keywords with QS < 5 is critically inefficient.<sup>4</sup> This indicates a fundamental disconnect between keywords, ad copy, and landing pages.

**Table 3: Google Ads Keyword & Quality Score Audit**

| Check # | Category | Check Name | Pass Criteria | Fail Criteria | Severity |
|---------|----------|------------|---------------|---------------|----------|
| G20 | Quality Score | High QS Distribution | ≥ 70% keywords with QS ≥ 7 | < 50% keywords with QS ≥ 7 <sup>1</sup> | High |
| G21 | Quality Score | Critical QS Spend | < 10% spend on QS < 5 | > 20% spend on QS < 5 <sup>4</sup> | Critical |
| G22 | Keywords | Match Type Mix | Broad Match < 20% (if Manual CPC) | Match > 50% (if Manual CPC) | High |
| G23 | Keywords | Broad Match + Smart Bidding | Broad Match used with tCPA/tROAS | Broad Match used with Manual CPC | High |
| G24 | Keywords | Ad Group Relevance | QS "Ad Relevance" component Above Avg | "Below Average" for >20% spend | Medium |
| G25 | Keywords | Landing Page Exp. | QS "LP Exp" component Above Avg | "Below Average" for >20% spend | High |

### 3.4 Ads, Assets, and Performance Max

The transition from Expanded Text Ads (ETAs) to Responsive Search Ads (RSAs) and Performance Max (PMax) campaigns requires a shift in auditing focus from "copywriting" to "asset density." PMax, in particular, acts as a black box that requires sufficient fuel (assets) to function.

**PMax Specifics:** The audit enforces a "Maximum Asset Density" standard. A PMax asset group must contain the full complement of 20 images, 5 logos, and 5 videos to access all inventory slots (Discovery, YouTube, Display). Missing videos is a common failure point that restricts PMax to standard Display slots, degrading performance.<sup>1</sup>

**Table 4: Google Ads Creative (RSA & PMax) Audit**

| Check # | Category | Check Name | Pass Criteria | Fail Criteria | Severity |
|---------|----------|------------|---------------|---------------|----------|
| G26 | Ads (RSA) | Ad Strength | > 80% "Good" or "Excellent" | < 50% "Good" or "Excellent" | Medium |
| G27 | Ads (RSA) | Asset Performance | < 10% assets rated "Low" | > 20% assets rated "Low" <sup>1</sup> | High |
| G28 | Ads (RSA) | Headline Utilization | 10--15 Headlines | < 5 Headlines | High |
| G29 | Ads (RSA) | Description Utilization | 4 Descriptions | < 2 Descriptions | High |
| G30 | Ads (RSA) | Pinning Rate | < 20% assets pinned | > 50% assets pinned (AI restriction) | Medium |
| G31 | PMax | Asset Group Density | 20 img, 5 logo, 5 vid <sup>1</sup> | < 10 img OR 0 video | Critical |
| G32 | PMax | Audience Signals | High Intent Segments attached | No Signals / Generic Interest only | High |
| G33 | PMax | Brand Exclusions | Brand List applied (if Search active) | No Brand Exclusions | Medium |
| G34 | PMax | URL Expansion | On (with exclusions) | On (without exclusions) or Off | Medium |
| G35 | PMax | Negative Keywords | Account-level negatives applied | No negatives applied | High |

### 3.5 Bidding, Budget, and Impression Share

Budget allocation efficiency is measured through "Lost Impression Share (IS)." This metric bifurcates lost volume into "Lost to Rank" (quality/bid issue) and "Lost to Budget" (financial constraint).

**Threshold Logic:** If a campaign has profitable ROAS but loses >15-25% of its Impression Share to budget, it is a mathematical failure of capital allocation.<sup>5</sup> Conversely, a campaign limited by budget should not be using "Maximize Clicks" or manual bidding without strict caps, as it will simply exhaust the budget earlier in the day at a higher CPC.

**Table 5: Google Ads Bidding & Budget Audit**

| Check # | Category | Check Name | Pass Criteria | Fail Criteria | Severity |
|---------|----------|------------|---------------|---------------|----------|
| G36 | Budget | Lost IS (Budget) | < 10% | > 15--25% <sup>5</sup> | High |
| G37 | Budget | Lost IS (Rank) | < 20% | > 50% (Quality/Bid issue) | High |
| G38 | Bidding | Strategy Alignment | tCPA/tROAS has >30 conv/mo | tCPA/tROAS with <15 conv/mo | Critical |
| G39 | Bidding | Limited by Budget | Status: Active | Status: Limited by Budget | Medium |
| G40 | Bidding | Enhanced CPC | Disabled (on Auto-bidding) | Enabled (redundant/conflicting) | Low |
| G41 | Bidding | Target Reality Check | Actual ROAS within +/- 20% of Target | Variance > 50% (Unrealistic) | High |

### 3.6 Conversion Tracking and Attribution

This is the bedrock of the account. Without accurate conversion data, Smart Bidding algorithms optimize toward noise.

**Table 6: Google Ads Conversion & Attribution Audit**

| Check # | Category | Check Name | Pass Criteria | Fail Criteria | Severity |
|---------|----------|------------|---------------|---------------|----------|
| G42 | Conversions | Primary Action Check | At least 1 Primary Action | No Primary Actions / All Secondary | Critical |
| G43 | Conversions | Tracking Status | "Recording Conversions" | "No recent conversions" (>7 days) | Critical |
| G44 | Conversions | Enhanced Conversions | Status: Active/On <sup>6</sup> | Status: Off | High |
| G45 | Conversions | Attribution Model | Data-Driven | Last Click (Legacy) | High |
| G46 | Conversions | Conversion Window | 30--90 Days | 7 Days (for high-consideration) | Medium |
| G47 | Conversions | Repeat Rate | < 1.1 (Lead Gen) | > 1.5 (Duplicate tracking error) | Critical |
| G48 | Conversions | Offline Import | Scheduled / API Connected | Manual / None | Medium |
| G49 | Conversions | View-Through Window | 1 Day | > 1 Day (Inflation risk) | Low |

### 3.7 Extensions, Audiences, and Landing Pages

**Table 7: Google Ads Assets & Landing Page Audit**

| Check # | Category | Check Name | Pass Criteria | Fail Criteria | Severity |
|---------|----------|------------|---------------|---------------|----------|
| G50 | Extensions | Sitelink Coverage | > 4 Active Sitelinks | < 2 | Medium |
| G51 | Extensions | Callout Coverage | > 4 Active Callouts | < 2 | Low |
| G52 | Extensions | Snippet Coverage | > 1 Active Snippet | 0 | Low |
| G53 | Extensions | Image Extensions | > 1 Active Image Ext | 0 | Medium |
| G54 | Extensions | Disapproval Rate | 0% | > 10% | Low |
| G55 | Audiences | RLSA List Size | > 1,000 Users | < 100 Users (Too small) | Medium |
| G56 | Audiences | Customer Match | Upload < 30 Days ago | Upload > 90 Days ago | Medium |
| G57 | Audiences | Observation Mode | > 5 Audiences Observed | 0 | Medium |
| G58 | Landing Page | Mobile Speed | Score > 70 | Score < 40 | High |
| G59 | Landing Page | Destination Errors | 0% 404/500 Errors | > 0% | Critical |
| G60 | Landing Page | Relevance | QS LP Exp "Average" | QS LP Exp "Below Average" | High |
| G61 | Maintenance | Change History | > 5 changes in 30 days | 0 changes (Dormant) | High |

---

## 4. Meta Ads Audit Checklist: The Social Signal Graph

Auditing Meta (Facebook/Instagram) Ads requires a fundamentally different approach than search. While search is deterministic (keyword = intent), social is probabilistic. The algorithm relies on "Signal Resilience" (Event Match Quality) and "Creative Velocity" to function. The "Learning Phase" is the central mechanic; ad sets that fail to exit the learning phase effectively waste budget by operating without full algorithmic optimization.

### 4.1 Technical Setup: Pixel, CAPI, and Signal Resilience

In a post-iOS14 world, the browser pixel is insufficient. The audit must verify the implementation of the Conversions API (CAPI) and the quality of the events being passed.

**Metric Analysis:** The "Event Match Quality" (EMQ) score is Meta's grading of how well it can link an event to a user. A score of "Great" (8-10) is ideal. Scores in the "Poor" (0-2) or "OK" (3-5) range <sup>7</sup> indicate that the data is too degraded for effective retargeting or lookalike modeling. Additionally, "Deduplication" is critical; checking that every event has a unique Event ID ensures that browser and server events are unified, preventing ROAS inflation.

**Table 8: Meta Ads Technical & Signal Audit**

| Check # | Category | Check Name | Pass Criteria | Fail Criteria | Severity |
|---------|----------|------------|---------------|---------------|----------|
| M01 | Technical | Pixel Activity | Active / Firing | Inactive / No Recent Events | Critical |
| M02 | Technical | CAPI Integration | Connected | Not Connected | Critical |
| M03 | Technical | EMQ Score | Score ≥ 6 (Good/Great) <sup>7</sup> | Score ≤ 5 (OK/Poor) | Critical |
| M04 | Technical | Deduplication | 100% Deduplicated | Duplicated (Double Counting) | Critical |
| M05 | Technical | Domain Verification | Verified | Not Verified | High |
| M06 | Technical | Aggregated Event Msmt | 8 Priority Events Configured | Not Configured | High |
| M07 | Technical | Advanced Matching | Auto-Matching ON | Auto-Matching OFF | High |
| M08 | Technical | Currency Match | Ad Account = Pixel Currency | Mismatch | Low |
| M09 | Technical | Parameters Passed | Email, Phone, Name, IP, Agent | Missing User Data Keys | High |
| M10 | Technical | Standard Events | Standard Events Used | Custom Conversions Only | Medium |

### 4.2 Account Structure and Learning Phase Mechanics

Meta's algorithm thrives on consolidated data. Fragmented accounts with dozens of low-budget ad sets prevent any single ad set from achieving the necessary 50 conversions per week to exit the "Learning Phase."

**Table 9: Meta Ads Structure & Learning Audit**

| Check # | Category | Check Name | Pass Criteria | Fail Criteria | Severity |
|---------|----------|------------|---------------|---------------|----------|
| M11 | Structure | Campaign Consolidation | < 5 Campaigns per Objective | > 10 (Fragmentation) | High |
| M12 | Structure | Learning Phase Status | < 20% Ad Sets "Learning Limited" | > 50% "Learning Limited" | High |
| M13 | Structure | Conversion Volume | > 50 Conversions/week <sup>8</sup> | < 10 Conversions/week | High |
| M14 | Structure | Ad Set Audience | > 100,000 <sup>9</sup> | < 100,000 (Too small) | Medium |
| M15 | Structure | Advantage+ Budget | CBO / Advantage + Budget ON | ABO (if > 3 ad sets) | Medium |
| M16 | Structure | Advantage+ Shopping | Active (if E-com) | Inactive (if E-com) | Medium |
| M17 | Structure | Objective Alignment | Sales/Leads | Traffic/Awareness (for perf.) | High |
| M18 | Structure | Naming Conventions | Consistent Taxonomy | Chaotic | Low |

### 4.3 Audience Dynamics and Overlap

"Audience Overlap" is a silent budget killer. If two ad sets target overlapping audiences (e.g., "Interest: Golf" and "Interest: Tiger Woods"), they compete against each other in the auction, raising CPMs. The audit threshold for overlap is 30%.<sup>10</sup>

**Table 10: Meta Ads Audience & Targeting Audit**

| Check # | Category | Check Name | Pass Criteria | Fail Criteria | Severity |
|---------|----------|------------|---------------|---------------|----------|
| M19 | Audience | Audience Overlap | < 20% | > 30% <sup>10</sup> | High |
| M20 | Audience | Exclusion Logic | Past Purchasers Excluded (TOF) | No Exclusions | High |
| M21 | Audience | Lookalike Recency | Dynamic / < 60 days | Static List > 90 days | Medium |
| M22 | Audience | Retargeting Window | Appropriate (e.g. 30D) | Too small (<1000 users) | Medium |
| M23 | Audience | Advantage+ Audience | Enabled (Expansion ON) | Disabled (Strict targeting) | Medium |
| M24 | Audience | Geo-Targeting | "Living in" (if local) | "Recently in" (if shipping ltd) | Low |

### 4.4 Creative Strategy, Diversity, and Fatigue

Creative is the new targeting. The audit evaluates "Creative Diversity" (mix of static and video) and "Fatigue." Creative fatigue is identified via Frequency metrics. A frequency > 3.0 for prospecting audiences correlates with diminishing returns and rising CPAs.<sup>11</sup>

**Table 11: Meta Ads Creative & Settings Audit**

| Check # | Category | Check Name | Pass Criteria | Fail Criteria | Severity |
|---------|----------|------------|---------------|---------------|----------|
| M25 | Creative | Format Diversity | Image + Video present | Single Format Only | High |
| M26 | Creative | Aspect Ratio | 1:1, 9:16, 1.91:1 all present | Missing 9:16 (Reels/Stories) | High |
| M27 | Creative | Ad Density per Ad Set | 3--6 Ads <sup>12</sup> | 1 Ad or > 10 Ads | Medium |
| M28 | Creative | Frequency (Prospecting) | < 2.5 | > 3.0 <sup>11</sup> | High |
| M29 | Creative | Creative Refresh | < 14 Days <sup>11</sup> | > 30 Days | High |
| M30 | Creative | Text Overlay | < 20% Text | Text Heavy (Delivery penalty) | Low |
| M31 | Creative | Hook Rate | > 25% (3-sec view / Imp) | < 10% | Medium |
| M32 | Creative | Hold Rate | > 15% (ThruPlay / Imp) | < 5% | Low |
| M33 | Placements | Advantage+ Placements | Enabled (Auto) | Manual (unless strict safety) | Medium |
| M34 | Placements | Audience Network | < 20% Spend | > 50% Spend (Low quality) | High |
| M35 | Settings | Attribution Setting | 7-day click / 1-day view | Varies by ad set | Medium |
| M36 | Settings | Bid Strategy | Lowest Cost / Highest Vol | Cost Cap (with 0 delivery) | High |
| M37 | Settings | Budget Pacing | Standard | Accelerated (Legacy/Manual) | Low |
| M38 | Reporting | UTM Parameters | Present & Consistent | Missing | High |
| M39 | Reporting | Cross-Channel Parity | Variance < 20% | Variance > 40% | Medium |
| M40 | Reporting | Experimentation | Active A/B Tests | No historical tests | Low |

---

## 5. LinkedIn Ads Audit Checklist: Precision B2B Targeting

LinkedIn's auction dynamics are distinct: high CPCs ($8--$15+) demand extreme precision. The "Insight Tag" and "Matched Audiences" are the linchpins of success. Unlike Meta, broad targeting is a liability on LinkedIn; "Audience Expansion" often dilutes B2B intent with irrelevant industries to fill budget.

**Audience Thresholds:** A critical failure point on LinkedIn is the "Audience Size" floor. Campaigns with <300 members in the target audience will fail to deliver entirely.<sup>13</sup> Conversely, the "Audience Expansion" setting is flagged as a "High" severity fail because it breaks the precision of the Ideal Customer Profile (ICP).

**Table 12: LinkedIn Ads Audit Checklist**

| Check # | Category | Check Name | Pass Criteria | Fail Criteria | Severity |
|---------|----------|------------|---------------|---------------|----------|
| L01 | Technical | Insight Tag Health | Active / Rec'd < 24h | Inactive / Not Installed <sup>14</sup> | Critical |
| L02 | Technical | Conversion Tracking | Leads/Purchases Active | "Page View" only / None | Critical |
| L03 | Audience | Cold Audience Size | 50k -- 400k | < 50k or > 1M | High |
| L04 | Audience | Retargeting Size | > 300 Members <sup>13</sup> | < 300 (Delivery Block) | Critical |
| L05 | Audience | Audience Expansion | Disabled (Unchecked) | Enabled (Dilutes ICP) | High |
| L06 | Audience | Audience Network | Disabled (Unchecked) | Enabled (Low Quality) | High |
| L07 | Audience | Targeting Layers | Function + Seniority | Job Title Only (Unscalable) | Medium |
| L08 | Audience | Exclusions | Competitors/Customers Excluded | No Exclusions | Medium |
| L09 | Audience | Geo-Targeting | "Permanent Location" | "Recent Location" | Medium |
| L10 | Creative | Ad Variations | 3--5 Variations <sup>14</sup> | 1 Variation | High |
| L11 | Creative | Refresh Cycle | < 45 Days <sup>14</sup> | > 60 Days | Medium |
| L12 | Creative | Intro Text | < 150 chars (Mobile) | > 150 chars (Truncated) | Low |
| L13 | Creative | Video Captions | SRT Uploaded | Missing | Low |
| L14 | Forms | Lead Gen Forms | Native Forms Used | Landing Page Traffic Only | High |
| L15 | Forms | Hidden Fields | UTM/Source Passing | Missing | Medium |
| L16 | Bidding | Bid Strategy | Manual CPC (Control) | Auto-Bid (Inefficient) | Medium |
| L17 | Bidding | Budget/Bid Ratio | Budget > 5x Bid | Budget < 2x Bid | High |
| L18 | Structure | Objective | Lead Gen / Website Visits | Brand Awareness | Low |
| L19 | Structure | Naming | Consistent | Chaotic | Low |
| L20 | Structure | Ad Rotation | Rotate Evenly | Optimize (Premature) | Low |
| L21 | Performance | CTR Benchmark | > 0.40% | < 0.20% | High |
| L22 | Performance | CPC vs Target | < Target | > Target (Increase budget 25%) | Medium |
| L23 | Performance | Frequency Cap | < 4 (30-day) | > 8 (B2B Fatigue) | Medium |
| L24 | Matching | Company Match Rate | > 50% | < 20% (Data quality issue) | Medium |
| L25 | Tracking | Demographic Report | > 80% Relevant Titles | > 20% Irrelevant | High |

---

## 6. TikTok Ads Audit Checklist: The Content Graph

TikTok's algorithm consumes creative at an unprecedented rate. The core audit metric here is the "Fatigue Index." A score >0.6 indicates that the creative has exhausted its audience potential and must be refreshed.<sup>15</sup>

**Technical Nuance:** The "Pangle" placement (TikTok's audience network) is often a source of low-quality, accidental clicks. Unless the goal is pure reach, Pangle should generally be excluded or heavily monitored. Additionally, TikTok requires a specific budget threshold to exit the learning phase: the daily budget should ideally be 50x the Target CPA <sup>15</sup> to provide the system with enough "room" to find conversions.

**Table 13: TikTok Ads Audit Checklist**

| Check # | Category | Check Name | Pass Criteria | Fail Criteria | Severity |
|---------|----------|------------|---------------|---------------|----------|
| T01 | Technical | Connection Type | Pixel + Events API <sup>15</sup> | Pixel Only | High |
| T02 | Technical | Advanced Matching | Enabled (Email/Phone) | Disabled | High |
| T03 | Structure | Ad Group Diversity | 3--5 Ad Groups <sup>15</sup> | 1 Ad Group | Medium |
| T04 | Structure | Broad Targeting | Broad (Gender/Age) | Narrow (Restrictive) | Medium |
| T05 | Creative | Fatigue Index | < 0.6 | > 0.6 <sup>15</sup> | High |
| T06 | Creative | Creative Velocity | > 3 New Ads/Week | 0 New Ads | High |
| T07 | Creative | Ad Count | 3--5 Active Ads <sup>15</sup> | 1 Active Ad | High |
| T08 | Creative | Video Duration | > 21s (Ideal: 21-34s) | < 5s | Medium |
| T09 | Creative | Sound On | Audio Enabled | Muted | High |
| T10 | Creative | Safe Zone | UI Safe Zone Clear | Elements Obscured | Medium |
| T11 | Bidding | Budget Floor | > 50x Target CPA <sup>15</sup> | < 10x Target CPA | High |
| T12 | Bidding | Dayparting | All Day | Restricted Hours | Low |
| T13 | Learning | Learning Phase | > 50 Conv/Week <sup>15</sup> | < 20 Conv/Week | High |
| T14 | Settings | Pangle Placement | Excluded / Monitored | Included (Blind) | Medium |
| T15 | Settings | Comments | Enabled (Moderated) | Disabled (Reach penalty) | Low |
| T16 | Settings | ACO | Enabled | Disabled | Low |
| T17 | Performance | CTR | > 1.0% | < 0.5% | Medium |
| T18 | Performance | CVR | Within Benchmark | < 50% Benchmark | High |
| T19 | Performance | CPA Stability | Stable | > 1.5x KPI | High |
| T20 | Structure | CBO | Enabled | Disabled | Low |
| T21 | Creative | Spark Ads | Active | None | Medium |
| T22 | Attribution | Window | 7d Click / 1d View | Default | Low |
| T23 | Technical | Parameters | Value/Currency Passed | Missing | Medium |
| T24 | Creative | Resolution | ≥ 720p <sup>15</sup> | < 720p | Low |
| T25 | Structure | Budget Util. | > 80% (Ready to scale) | < 50% (Delivery issue) | Low |

---

## 7. Microsoft Ads Audit Checklist: The Import Hygiene

Microsoft Ads (Bing) is frequently managed via "Import from Google," which introduces specific failure modes. The most critical audit check is "Syndication on Brand." Microsoft's search partners (Syndication) can generate high-volume, low-quality traffic. Unlike Google, where partners are often benign, on Microsoft, enabling partners on Brand campaigns can lead to massive budget waste on irrelevant queries.<sup>16</sup>

**Table 14: Microsoft Ads Audit Checklist**

| Check # | Category | Check Name | Pass Criteria | Fail Criteria | Severity |
|---------|----------|------------|---------------|---------------|----------|
| MS01 | Technical | UET Tag Health | Active / Verified | Inactive / Missing | Critical |
| MS02 | Technical | Import Errors | 0 Failed Items | > 0 Failed Items | High |
| MS03 | Technical | Auto-Tagging | MSCLKID Enabled | Disabled | Critical |
| MS04 | Syndication | Brand Syndication | Excluded / Off <sup>16</sup> | Included / On | Critical |
| MS05 | Syndication | Website Exclusions | List > 0 Domains | 0 Domains | High |
| MS06 | Bidding | Bid Modifiers | Reviewed post-import | Google Defaults | Medium |
| MS07 | Bidding | CPC Arbitrage | 20--30% < Google <sup>16</sup> | > Google CPC | High |
| MS08 | Structure | Import Schedule | Scheduled | Manual | Medium |
| MS09 | Structure | Spend Ratio | 10--30% of Google Spend | < 5% | Low |
| MS10 | Audience | LinkedIn Targeting | Profile Layers Applied | None | High |
| MS11 | Creative | RSA Coverage | Active | None (ETAs only) | Medium |
| MS12 | Creative | Image Extensions | Active | None | Medium |
| MS13 | Creative | Audience Ads Img | 1.91:1 & 1:1 Present | Missing one ratio | Medium |
| MS14 | Settings | Time Zone | Correct | Incorrect (Import error) | Low |
| MS15 | Settings | Location Opt | "People In" | "People Searching For" | High |
| MS16 | Performance | Quality Score | > 5 | < 3 | High |
| MS17 | Performance | Brand SOV | > 70% | < 50% | High |
| MS18 | Attribution | Conv. Window | 30 Days <sup>16</sup> | Default | Medium |
| MS19 | Extensions | Action Ext. | Active | None | Low |
| MS20 | Extensions | Sitelinks | > 4 Active | < 2 | Low |

---

## 8. Conclusion: The Unified Audit Standard

This technical standard provides a deterministic framework for evaluating ad account health. By strictly adhering to these 170+ pass/fail criteria, claude-ads moves beyond subjective advice to provide an objective measurement of algorithmic compliance. The scoring model ensures that critical signal failures (like EMQ < 3.0 or broken UET tags) effectively "fail" the audit, forcing user attention where it impacts revenue most. This is the baseline for high-performance, automated advertising management in the algorithmic era.

---

## Works Cited

1. How to Audit B2B Google Ads Accounts [+Free Template] - AdConversion, accessed February 10, 2026, [https://www.adconversion.com/blog/google-ads-audit](https://www.adconversion.com/blog/google-ads-audit)
2. The First 30 Days of Autonomous Google Ads: What Actually Happens - groas, accessed February 10, 2026, [https://groas.ai/post/the-first-30-days-of-autonomous-google-ads-what-actually-happens](https://groas.ai/post/the-first-30-days-of-autonomous-google-ads-what-actually-happens)
3. Helium 10 Ads Video: The First Thing Existing Sellers Should Do in Helium 10 Ads, accessed February 10, 2026, [https://kb.helium10.com/hc/en-us/articles/30452442370459-Helium-10-Ads-Video-The-First-Thing-Existing-Sellers-Should-Do-in-Helium-10-Ads](https://kb.helium10.com/hc/en-us/articles/30452442370459-Helium-10-Ads-Video-The-First-Thing-Existing-Sellers-Should-Do-in-Helium-10-Ads)
4. What Is Quality Score, And Why Is It Important? - Pepper PPC agency, accessed February 10, 2026, [https://pepper.agency/blog/what-is-quality-score-and-why-is-it-important/](https://pepper.agency/blog/what-is-quality-score-and-why-is-it-important/)
5. How to Estimate Google Ads Budget (with Examples) - Sheldon Payne, accessed February 10, 2026, [https://sheldonpayne.com/how-to-estimate-google-ads-budget/](https://sheldonpayne.com/how-to-estimate-google-ads-budget/)
6. Everything You Need to Know About Google Ads Measurement for 2024 & Beyond, accessed February 10, 2026, [https://kpplaybook.com/resources/google-ads-measurement/](https://kpplaybook.com/resources/google-ads-measurement/)
7. What is Event Match Quality (EMQ) in Facebook Ads and How to ..., accessed February 10, 2026, [https://www.customerlabs.com/blog/improve-your-event-match-quality-from-ok-to-great/](https://www.customerlabs.com/blog/improve-your-event-match-quality-from-ok-to-great/)
8. How to scale facebook ads: Proven Growth Tactics - Sprello, accessed February 10, 2026, [https://sprello.ai/blog/how-to-scale-facebook-ads](https://sprello.ai/blog/how-to-scale-facebook-ads)
9. Facebook Ads Audit: Free Template and Step-by-Step Account Checklist - Vaizle Insights, accessed February 10, 2026, [https://insights.vaizle.com/facebook-ads-audit/](https://insights.vaizle.com/facebook-ads-audit/)
10. 5 Tips to Prevent Interest-Based Audience Overlap - AdAmigo.ai Blog, accessed February 10, 2026, [https://www.adamigo.ai/blog/prevent-interest-based-audience-overlap](https://www.adamigo.ai/blog/prevent-interest-based-audience-overlap)
11. Facebook Creative Fatigue: What Is It and How to Avoid It? - inBeat Agency, accessed February 10, 2026, [https://inbeat.agency/blog/facebook-creative-fatigue](https://inbeat.agency/blog/facebook-creative-fatigue)
12. 5 Common Meta Ads Mistakes and How to Fix Them - AdAmigo.ai Blog, accessed February 10, 2026, [https://www.adamigo.ai/blog/5-common-meta-ads-mistakes-and-how-to-fix-them](https://www.adamigo.ai/blog/5-common-meta-ads-mistakes-and-how-to-fix-them)
13. Running ABM on LinkedIn -- The Ultimate Guide [Updated for 2026] - ZenABM, accessed February 10, 2026, [https://zenabm.com/blog/running-abm-on-linkedin-the-ultimate-guide](https://zenabm.com/blog/running-abm-on-linkedin-the-ultimate-guide)
14. Definitive LinkedIn Ads Optimisation Checklist Guide - Priority Pixels, accessed February 10, 2026, [https://prioritypixels.co.uk/blog/definitive-checklist-for-linkedin-ads-optimisation/](https://prioritypixels.co.uk/blog/definitive-checklist-for-linkedin-ads-optimisation/)
15. TikTok Web Auction Best Practices - TikTok For Business, accessed February 10, 2026, [https://ads.tiktok.com/business/library/TikTok_WebAuctionBestPractices.pdf](https://ads.tiktok.com/business/library/TikTok_WebAuctionBestPractices.pdf)
16. Ads on Bing: 2026 Microsoft Ads Guide | Gravitate - Gravitate Design, accessed February 10, 2026, [https://www.gravitatedesign.com/blog/ads-on-bing-microsoft-ads-guide/](https://www.gravitatedesign.com/blog/ads-on-bing-microsoft-ads-guide/)
