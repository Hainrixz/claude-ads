# The definitive paid advertising reference for 2026

**Paid advertising in February 2026 is defined by AI-driven automation, privacy adaptation, and rising costs offset by improving conversion rates.** Google abandoned third-party cookie deprecation in Chrome, Privacy Sandbox is officially dead, and platforms are consolidating around AI-powered campaign types that demand less manual control and more creative quality. CPCs rose for the fifth consecutive year (now averaging **$5.26** on Google Search), [TheeDigital] yet conversion rates improved for **65% of industries**. [Swydo +2] This report provides the authoritative technical reference needed to build the [claude-ads] CLI tool -- every benchmark, threshold, API endpoint, and audit criterion current as of February 2026.

---

## SECTION 1: Google Ads -- the complete platform reference

### 1.1 Campaign types available in February 2026

Google Ads offers **11 campaign types**, with significant structural changes in 2025:

**Search** remains the core intent-capture format. [Growthmindedmarketing] **Performance Max (PMax)** is Google's AI-driven cross-channel workhorse spanning Search, YouTube, Display, Gmail, Discover, and Maps. [Google] [Lseo] **AI Max for Search** launched in 2025 as the fastest-growing AI Search product, adding AI-driven text customization and final URL expansion. [ALM Corp] [MediaPost Publications] **Demand Gen** replaced both Discovery campaigns (auto-upgraded March 2025) [NestScale] and Video Action Campaigns (auto-upgraded July 2025), now reaching [Google Support] **3 billion monthly users** across YouTube, Discover, Gmail, and GDN. **Display, Shopping, Video**, and **App** campaigns continue. [Definedigitalacademy] **Hotel** campaigns serve that vertical specifically. **Smart Campaigns** persist for simplified automation. **Call Campaigns** stop new creation in February 2026 and sunset fully in February 2027. [PPC Land]

Google introduced the **"Power Pack"** framework at Google Marketing Live (May 2025): PMax + Demand Gen + AI Max working together as a unified strategy, replacing the earlier "Power Pair" concept. [ALM Corp +2]

**Performance Max evolution in 2025-2026** brought transformative transparency: [ALM Corp] campaign-level negative keywords expanded to **10,000** [Google Support] (up from 100), search themes increased to **50 per asset group**, [Google Support] full search term reporting became available (March 2025), [Adnabu] and channel-level reporting now breaks down performance across Search, YouTube, Display, Gmail, Discover, and Maps. [PPC Land] Device targeting, demographic controls, brand exclusions by format, and asset-level reporting with impressions, clicks, and cost data are all now available. [ALM Corp]

**Demand Gen** supports single/multi-image ads, carousels, video ads, and product feeds. Bidding options include Maximize Conversions, Maximize Conversion Value, Target CPA, Target ROAS, Maximize Clicks, and **Target CPC** (new for Demand Gen). [ALM Corp] Advertisers with video+image assets see **20% more conversions** at the same CPA versus video-only. [Google Support] Demand Gen delivers **58% higher ROAS** than the Video Action Campaigns it replaced. [Google]

### 1.2 Bidding strategies and thresholds

**Smart Bidding (conversion-based, auction-time):** Target CPA, Target ROAS, Maximize Conversions, and Maximize Conversion Value. [Google Support] **Other automated strategies:** Maximize Clicks, Target Impression Share (Search only), Target CPC (Demand Gen only), CPM/tCPM/vCPM (Display/Video), CPV (Video), and Pay per Conversion (Display, eligibility required). **Manual CPC** remains available for full advertiser control.

> **Enhanced CPC (ECPC) was deprecated March 31, 2025** for Search and Display campaigns. Campaigns not migrated now use Manual CPC. [google +2] This is confirmed by official Google documentation.

**Smart Bidding Exploration** launched in 2025, allowing tROAS campaigns to temporarily ease targets to discover new traffic. [ALM Corp] Campaigns using it see **18% more unique search query categories** and **19% more conversions**. [Google Support]

**Minimum conversion thresholds for Smart Bidding: 15-30 conversions per month** minimum for effective operation. [ALM Corp] Google recommends at least **15 conversions in the last 30 days** for Target CPA. [Google Support] [WordStream] Below this threshold, use Manual CPC or Maximize Clicks. For new campaigns, start with Maximize Clicks or uncapped Maximize Conversions, then transition to Target CPA/ROAS after 30-60 days of data.

### 1.3 Quality Score mechanics

Quality Score is rated **1-10** at the keyword level [Automationlinks] [Americaneagle] with three components rated Below Average / Average / Above Average: **Expected CTR (~39% weight), Ad Relevance (~22% weight)**, and **Landing Page Experience (~39% weight)**. [Store Growers] The Ad Rank formula: **Max CPC x Quality Score x Expected Impact of Ad Assets**. [Growleads] Actual CPC equals the Ad Rank of the competitor below divided by your Quality Score plus $0.01. [Website.com] In 2025, Google increased weight on landing page user experience and mobile optimization -- a **1-second delay** in mobile load reduces conversions by up to **20%**. [Roam Digital +2] Improving RSA Ad Strength from "Poor" to "Excellent" yields **15% more conversions** on average. [Google Support]

### 1.4 Ad copy and RSA specifications

**Responsive Search Ads** are the default format since June 30, 2022. Specs: **minimum 3, maximum 15 headlines** (30 chars each); **minimum 2, maximum 4 descriptions** (90 chars each). [Appearonline] Best practice is **8-10 headlines and 2-3 descriptions**. [Search Engine Land] Pinning should be used sparingly -- only for legal/compliance messaging. [Search Engine Land] **Expanded Text Ads cannot be created or edited** since June 2022 but existing ones continue serving.

Google offers **15+ asset types** (formerly extensions): [Bind Media] sitelinks, callouts, structured snippets, call, location, affiliate location, price, promotion, lead form, app, image, business logo, business name, and seller ratings. [WordStream] Advertisers with **6 sitelinks per campaign see 3.5% more conversions**. [Google Support] Ad Strength is diagnostic, not a direct performance factor -- ads rated lower can still outperform. [Pattern]

### 1.5 Keyword strategy in 2026

Match types function as thematic signals rather than strict rules. [Downey Marketing] **Broad match** relates to the keyword including synonyms and related concepts. **Phrase match** includes the meaning. **Exact match** captures same meaning or intent including close variants. [Jyll] When Smart Bidding is active, campaigns now default to treating all keywords as broad match. [McIvor Marketing LLC] Close variants include misspellings, synonyms, paraphrases, and same-intent queries. **15% of daily Google searches are brand new**. [Jyll]

> **2025 change:** Negative keywords now expand to cover misspellings. [WordStream] PMax supports up to **10,000 negative keywords** applying to Search and Shopping inventory only. [Google Support] [ALM Corp]

**SKAGs are largely outdated.** The consensus has shifted to **STAGs (Single Theme Ad Groups)** with 3-20 keywords per group sharing common intent. [SiteCentre] Google's AI requires data volume that single keywords cannot provide. [Greenlane Marketing] The modern recommendation is themed ad groups with **10-20 related keywords** per ad group, [RedTrack Blog] with **7-10 ad groups per campaign**.

### 1.6 Audience targeting and privacy landscape

Audience types include in-market, affinity, detailed demographics, life events, custom segments, remarketing, Customer Match, combined segments, and optimized targeting. **Observation mode** collects performance data without restricting reach; **targeting mode** restricts to selected audiences only. [Adnabu]

**Customer Match** requires 90 days of history and **$50,000+ lifetime spend** for full access. [Google Support] Maximum membership duration is **540 days** [Google] (changed April 7, 2025 -- infinite duration removed). Minimum list size is **100 members**. [PPC Land]

> **Google abandoned third-party cookie deprecation in July 2024.** [CookieYes] Chrome does NOT block third-party cookies by default. [Cookie-Script] In April 2025, Google confirmed no separate consent prompt. [Jentis] [Usercentrics] **Privacy Sandbox was officially retired in October 2025.** [Adweek] Third-party cookies remain functional in Chrome (~67% global browser share), [CookieYes] though Safari and Firefox already block them.

**Consent Mode v2 is mandatory since March 2024 for EEA/UK.** [Termly] Enforcement tightened in July 2025 [Groas] -- sites without proper implementation reported **90-95% metric drops**. Advanced Consent Mode can recover **30-50%** of lost conversions through modeling. Only **~31% of users accept tracking cookies** globally. [Dataslayer]

### 1.7 Conversion tracking essentials

Use Google Ads native conversion tracking as primary for bidding optimization (real-time data), and import GA4 conversions for observation only. Never count both to avoid double-counting. **Enhanced conversions** send hashed first-party data (email, phone, name, address) via SHA-256 [Conversios] [Google] and deliver approximately **10% more measured conversions**. Server-side tagging is now considered essential -- it recovers **10-30% accuracy improvement** and bypasses ad blockers.

> **Data-driven attribution (DDA) is now the mandatory default** (September 2025). Only two models remain: DDA and Last Click. All rule-based models (first-click, linear, time decay, position-based) are deprecated. No minimum data threshold is required for DDA.

Conversion windows: click-through **1, 3, 7, 30 (default), 60, or 90 days**; engaged-view default **3 days**; view-through default **1 day**. [MeasureMinds]

### 1.8 Automation, scripts, and the Recommendations tab

The **Google Ads API v23** (released January 27, 2026) provides granular channel-level PMax reporting. [PPC Land] Google Ads Scripts use V8 JavaScript with scheduling down to hourly frequency. Key use cases: bid management, budget monitoring, broken URL detection, [KlientBoost] quality score analysis, negative keyword management, anomaly detection, and N-gram analysis.

**Recommendations tab guidance:** Optimization Score increases equally whether you accept or dismiss recommendations. **Never auto-apply recommendations.** Safe to accept: optimized ad rotation, relevant extensions, fix disapproved ads. **Usually reject:** "Raise your budget," "Add broad match keywords," "Add new keywords," auto-created RSAs, and bidding strategy switches.

### 1.9 Account structure philosophy

The 2025-2026 shift moves from hyper-granular to **consolidated, AI-friendly structures**. Google's AI thrives on data volume -- consolidation provides more conversion data for machine learning. [Rebid] Separate campaigns by business objective, budget needs, geography, branded vs. non-branded, and campaign type. Critical settings: turn auto-apply recommendations **OFF**, [IMPACTABLE] search partners **OFF** [IMPACTABLE] initially, and **never combine Display and Search** in the same campaign.

### 1.10 Industry benchmarks for 2025-2026

**WordStream/LocaliQ 2025 benchmarks (16,000+ campaigns):** [WordStream]

| Metric | All Industries Average |
|---|---|
| Search CTR | **6.66%** [RentVision] (up 3.74% YoY) |
| Search CPC | **$5.26** (up for 87% of industries) |
| Search CVR | **7.52%** [LocaliQ] (up for 65% of industries) |
| Search CPL | **~$70** [LocaliQ] (up ~5% YoY) |

**By industry (Search):**

| Industry | CPC | CTR | CVR |
|---|---|---|---|
| Legal | $8.58- [Engage Coders] $9.21 | 5.97% [TheeDigital] | 5.09% [TheeDigital] |
| Home Improvement | $7.85 | 6.37% [TheeDigital] | 7.33% |
| Education | $6.23 | -- | -- |
| Dental | $7.85 | 5.44% [Engage Coders] | -- |
| Arts & Entertainment | $1.60 [LocaliQ] | 13.10% [Engage Coders] | -- |
| Travel | $2.12 [LocaliQ] | -- | -- |
| Restaurants | $2.05 [LocaliQ] | -- | -- |

**E-commerce benchmarks (Triple Whale 2025):** Median CPA **$23.74** (up 12.35% YoY), median CPM **$12.79** (up 10.01%), [Triple Whale] median ROAS **3.68** (down 10.03%). [Growth-onomics] CTR improved across all 14 tracked industries while CVR declined in 13 of 14. [Triple Whale]

---

## SECTION 2: Meta Ads -- the AI-first advertising platform

### 2.1 Campaign structure and Advantage+ dominance

Meta consolidated to **6 ODAX objectives**: Awareness, Traffic, Engagement, Leads, App Promotion, and Sales. [Veuno] [veuno] **Advantage+ is now the default** for Sales, Leads, and App Promotion campaigns, [Jon Loomer] with CBO, Advantage+ Placements, and Advantage+ Audience all auto-enabled. [Code Inc Solutions]

> **Advantage+ Shopping was renamed to Advantage+ Sales** in 2025, [Social Media Today] now supporting sales, lead generation, AND app installs. [Birch] Performance data: **$4.52 ROAS** (22% higher than manual), CPA reduced up to **32%**, CTR improved **11-15%**. **35% of US retail ad spend** now uses Advantage+, reaching a **$60B annualized revenue run rate** by end of 2025. [FinancialContent]

**Advantage+ Audience** uses interests/demographics as suggestions (not hard rules) [Adnabu] while location and minimum age remain hard controls. [TrueFuture Media] [CIM] It delivers **13% lower cost per catalog sale** and **28% lower average CPC**. Manual targeting remains available for retargeting and niche control. [Strike Social]

**CBO vs ABO:** CBO (now Advantage+ Campaign Budget) auto-distributes budget across ad sets and is the default in Advantage+. ABO provides manual budget control per ad set for testing and controlled experiments.

> **Major 2025 targeting changes:** Detailed targeting exclusions were removed [Zaginteractive] from new ad sets (March 31, 2025), from boosted posts (June 10, 2025), [Faniq] and existing campaigns with old exclusions stopped delivering January 15, 2026. Meta cited **22.6% lower median cost per conversion** without exclusions.

### 2.2 Creative specifications and fatigue management

All current formats: single image (**1080x1350, 4:5**), [The Brief AI] video (MP4/MOV, 4GB max), [Buffer] carousel (2-10 cards, 1:1), collection, Stories (9:16), Reels (9:16, 1080x1920), [Ads Uploader] slideshow, Messenger ads, playable (HTML5), Instant Experience, and **Flexible Ads** (new in 2025 -- auto-tests up to 10 images/videos). [Metricool] Text limits: primary **125 chars**, headline **27-40 chars**, [veuno] Reels primary **72 chars**.

**Creative fatigue thresholds:** Replace when frequency exceeds **4.0** OR CTR declines >**20%** over two weeks. At 4 repeated exposures, conversion drops **~45%**. Top-of-funnel fatigues in **3-4 weeks**; bottom-of-funnel in **6-7 weeks**. Meta introduced new Creative Fatigue and Creative Similarity scores in 2025.

The **Andromeda algorithm** now processes **10,000x more ad variants in parallel**, [Anchour] making creative diversity more important than creative volume. [Flighted] Meta's Advantage+ Creative offers **14+ enhancement options** [Coinis] [Jon Loomer] including AI-generated backgrounds, text variations, music overlays, and CTA stickers.

### 2.3 Conversions API and Event Match Quality

CAPI is now essential -- it provides **15-20% performance increase** and bypasses ad blockers and iOS ATT limitations. [Madgicx] The Offline Conversions API was deprecated in May 2025; CAPI is the replacement.

**Event Match Quality (EMQ)** scoring: **8+** for optimal performance, **6.0 minimum acceptable** (below = poor ad delivery). Key customer information parameters by impact: email (+4.0 pts), phone (+3.0 pts), external ID, fbp, fbc. Target **90%+ deduplication rate** using event_id in both Pixel and CAPI. **87% of advertisers have poor EMQ** -- fixing it can improve performance **20-40%**.

### 2.4 Meta benchmarks for 2025-2026

**WordStream 2025 benchmarks (1,000+ campaigns):**

| Objective | CTR | CPC | CVR | CPL |
|---|---|---|---|---|
| Traffic (all) | 1.71% [wordstream] | $0.70 [WordStream] | -- | -- |
| Leads (all) | 2.59% [wordstream] | $1.92 [WordStream] | 7.72% [wordstream] | $27.66 |

**ROAS benchmarks:** Median all-industries **2.19:1**, [Enrichlabs +2] retargeting **3.61:1**, [Billo] Advantage+ **4.52:1**. [Madgicx] CPM benchmarks: Arts & Entertainment **$5.82** (lowest), most industries **$6-$8**. [Lebesgue: AI CMO] Global CPC trend: Jan 2026 at **$0.85** (24% below prior January; Nov 2025 peaked at $1.32 during Q4). [Superads]

---

## SECTION 3: YouTube Ads -- video at scale

### Campaign types and creative framework

Six primary ad formats: **Skippable In-Stream** (skip after 5s, most flexible), **Non-Skippable** [Google Support] (now up to 60s -- expanded from 30s in 2025), **Bumper** (<=6s), [Teamology] **In-Feed** [EssenceMediacom] (click to watch), **YouTube Shorts** (vertical 9:16), and **Masthead** (reserved buy). Campaign types include Video Reach, Video View, Demand Gen (replaced Video Action Campaigns in Q2 2025), [Strike Social] and Performance Max. [PPC Land]

**ABCD creative framework: Attract** with a hook in the first 5 seconds using tight framing and 2+ shots. **Brand** within the first 5 seconds via logo, audio, or product. **Connect** through education, humor, or emotion. **Direct** with a clear CTA. [Think with Google] [Wow-How] Campaigns following ABCD deliver **30% lift in short-term sales** and **17% lift in long-term brand contribution**. [Google Support] [PPC Land]

**YouTube benchmarks 2025-2026:** Average CTR **~0.65%**, [Store Growers] average view rate **~31.9%**, average CPV **$0.02-$0.03**, [Marketing LTB] [Store Growers] average CPM **$4-$10**. [inBeat] Brand Lift Study minimums: **$5,000 per question** (BLS 2.0), recommended **$15,000** for reliable detection. [Metric Theory]

---

## SECTION 4: LinkedIn Ads -- B2B's precision targeting leader

### Targeting capabilities and new formats

LinkedIn offers professional targeting unmatched by other platforms: [LinkedFusion] [Microsoft Learn] job title, company (up to 300,000 via upload), industry, seniority [LinkedIn] (Entry through CXO/Owner), company size, growth rate, revenue, skills, education, years of experience, [LinkedIn] and member interests. Minimum audience: **500 members** for delivery; recommended **50,000-300,000**. [Factors.ai]

> **Lookalike audiences were discontinued February 29, 2024**, [LinkedIn] replaced by **Predictive Audiences** [Social Media Today] (AI-powered, [Microsoft Learn] requires 300+ members as seed). [LinkedIn] New formats in 2024-2025: **Connected TV Ads** (US/Canada, 60M+ households), [Neil Patel] **Thought Leader Ads** (sponsor individual profile posts), **BrandLink** (video alongside publisher content), [AdExchanger] and Live Event Ads. Campaign hierarchy was renamed October 2025: "Campaign Groups" -> "Campaigns"; "Campaigns" -> "Ad Sets." [ALM Corp]

### LinkedIn benchmarks

| Metric | Benchmark |
|---|---|
| Average CPC | $5-$7 globally; [Viewmetrics] [NAV43] median $3.94 [Closely] |
| Average CPM | $31-$38 [Closely] |
| Average CTR | 0.44%-0.65% (sponsored content) [NAV43] |
| Average CPL | $60-$150+ [Adbacklog] [NAV43] |
| Lead Gen Form CVR | **13%** (3.25x higher than landing pages) |
| Message Ads CTR | 3% with ~30% open rate |
| Conversation Ads | ~50% open rate, 10-12% CTR [ZenABM] |
| B2B ROAS | 113% ($1.13 per $1 spent) [ZenABM] |
| Min daily budget | $10/day [Fibbler] |

**CPL by industry:** Software & IT **$125**, Finance **$100**, Healthcare **$125**, Education **$64**, Media **$65**, Manufacturing **$100**, Retail **$80**. [Tamarind +2]

Senior decision-makers (VP/Director/C-suite) cost **$6.40+** per click. [NAV43] [SEO Design Chicago] North America carries a **40-50% premium** over global averages. [ZenABM] CPC is up **8% YoY** in 2025. [NAV43]

---

## SECTION 5: TikTok Ads -- automation and commerce converge

### Smart+ and TikTok Shop transformation

TikTok restructured objectives with "Website Conversions" and "Product Sales" merging into a unified **"Sales" objective** supporting TikTok Shop, Website, and App destinations. **GMV Max** became the default and only campaign type for TikTok Shop Ads in July 2025. [TikTok]

> **Smart+ campaigns** (major October 2025 upgrade) now offer modular automation -- advertisers customize automation level per module (targeting, budget, creative, placement) rather than accepting a black box. [Social Media Today] [Segwise] Adoption surged from **9% to 42%** of US TikTok performance campaigns in 2025. [eMarketer] Smart+ supports up to **30 ad groups per campaign, 50 creatives per asset group**. [TikTok] Symphony AI integration auto-generates video variations, hooks, music, and scripts.

**TikTok Shop conversion rates exceed 10%** (versus 0.46-2.4% for standard campaigns), with **22% higher conversion** than sending users off-platform. [Creatify] Available in 11 countries including US, UK, and key Asian/European markets. [TikTok]

**Search Ads** launched on TikTok in 2025, targeting intent-driven users [Creatify] with keywords for Web Conversion and Traffic objectives. [TikTok]

### TikTok benchmarks 2025-2026

| Metric | Average |
|---|---|
| CPM | $3.21-$10 (median ~$4.26) |
| CPC | $0.20-$2.00 (avg ~$1.00) |
| CTR | 0.5%-1.5% (avg ~0.84%) |
| CVR | 0.3%-1.0% (avg ~0.46%) |
| Engagement Rate | **5-16%** (far exceeds FB 0.09%, IG 1.22%) |

TikTok is **40-60% cheaper than Meta on CPMs**. [Creatify] Spark Ads deliver ~3% CTR versus ~2% for standard In-Feed, with ~$60 CPA versus ~$100. [adbacklog] Minimum budgets: **$50/day** campaign level, **$20/day** ad group level. [Printify] The algorithm needs **~50 conversions** in 7 days to pass the learning phase. [XMP Blog]

---

## SECTION 6: Microsoft Ads -- the underestimated competitor

### Unique capabilities and Copilot integration

Microsoft simplified Google Import with three options (Quick Import, Smart Import, Advanced Import) in February 2025. [Microsoft Advertising] Key unique features include **LinkedIn Profile Targeting** (exclusive to Microsoft -- company, industry, job function targeting), [Microsoft Advertising] [WebFX] now expanded to Performance Max campaigns. [Conversios] [Conversios] Copilot integration delivers **73% higher CTR** and **16% stronger conversion rates** versus traditional search, with customer journeys **33% shorter**. [Dataslayer]

> **Copilot Checkout** launched [Microsoft Advertising] January 2026: users discover, compare, and purchase within Copilot conversations. Launch partners include Urban Outfitters, Etsy, and Ashley Furniture. Users are **194% more likely to purchase** when shopping intent is present.

**Cost advantages:** Microsoft Ads average CPC is **$1.20-$1.55** [Marketing LTB] versus Google's **$2.00-$2.50** -- a **20-35% discount**. CTR averages **2.83-3.1%** [Jitendra Vaswani] (higher than Google's ~2.0%). Bing users click paid ads **25% more often** than Google users. **37% of advertisers report higher ROAS** on Microsoft than Google. [Marketing LTB]

**Market share (2025-2026):** [Invoca] US all-devices hit record **8.78%**; [Resourcera] [Aureate Labs] US desktop **16.75-17.58%**; [Resourcera] including Yahoo/AOL partners reaches **~25% of US desktop searches**. [Marketing LTB] Bing users skew affluent (**~50% in top 25%** of household incomes), [Nerdynav] educated (**34% hold degrees**), [Electro IQ] and older (**45-64 perform 38%** of searches). [Marketing LTB]

---

## SECTION 7: Cross-platform strategy frameworks

### Budget allocation and attribution

The **70/20/10 rule** dominates: 70% to proven performers, 20% to promising growth, 10% to experiments. [ALM Corp] Platform selection by business type:

- **E-commerce:** 50% Google (Shopping), 35% Meta, 15% TikTok
- **B2B SaaS:** 40% LinkedIn, 35% Google, 25% Meta/YouTube
- **B2C/DTC:** 50% Meta, 20% Google, 30% TikTok [Go Digital Alpha]
- **Local Business:** 60% Meta, 30% Google, 10% testing

**Minimum viable budgets:** Google $1,000+/mo, Meta $600-800/mo, LinkedIn $3,000+/mo, [Swydo] TikTok $300+/mo. [Madgicx]

**Attribution in 2026** requires a triangulation approach: platform attribution data + incrementality testing + Media Mix Modeling. [Measured] **49% of marketers** now use MMM. [Dataslayer] Open-source tools: Meta's **Robyn** (R-based, [Facebookexperimental] best for ~80% of organizations), [Search Engine Land] Google's **Meridian** (Python, Bayesian, geo-level), [Eliya] **PyMC-Marketing** (fully customizable). [Sellforte] Post-purchase surveys fill **~30%** of the attribution gap that digital tracking misses. [Fairing]

### Landing page optimization

**82.9% of landing page traffic is mobile.** [Backlinko] Pages loading in 1 second have **3x higher conversion rates** than pages taking 5 seconds. A 1-second delay causes a **7% drop in conversions**. [Roam Digital +2] Quality Score's landing page experience component can mean a **50% CPC discount** at high scores versus **400% extra CPC** at low scores. [Crystallize] [Optmyzr] Median landing page CVR across industries is **6.6%**; [InterTeam Marketing] top 10% achieve **20%+**.

---

## SECTION 8: Ad account audit framework with scoring

### Google Ads audit checklist (70 items)

The complete audit covers 11 categories. Here are the critical thresholds for each:

**Conversion Tracking (Critical foundation -- 20% weight):**

- Active conversion actions exist (no active = CRITICAL FAIL)
- Primary conversions set for bidding
- No duplicate conversion counting
- GA4 linked and data flowing
- Enhanced conversions enabled [Sharpinnovations]
- Google Tag firing correctly on all pages

**Keywords & Search Terms (20% weight):**

- Impression-weighted average QS: >=7 PASS, 5-6 WARNING, <=4 FAIL
- Low QS keywords: >**25% with QS <=4 = FAIL**
- Zero-conversion keywords with >100 clicks = FAIL
- Search term relevance: >**20% irrelevant by spend = FAIL**
- Negative keyword lists exist (none = CRITICAL FAIL)
- Wasted spend on irrelevant terms: >**15% = FAIL**

**Ads & RSAs (15% weight):**

- At least 1 active RSA per ad group (none = CRITICAL FAIL)
- Ad Strength: **"Poor" = FAIL, "Average" = WARNING**
- Headline utilization: **<8 headlines = WARNING**
- CTR below **50% of industry average = FAIL**
- No new ads in >90 days = WARNING

**Campaign Settings (10% weight):**

- Location targeting method: "Presence or interest" for local business = CRITICAL FAIL
- Unintended Display opt-in on Search = FAIL
- 20% spend during zero-conversion hours = WARNING
- 30% spend on device with <50% avg CVR = WARNING

**Bidding & Budgets (10% weight):**

- Smart Bidding with <30 conversions/month = WARNING
- Lost Impression Share (budget) >**20% = WARNING, >40% = FAIL**
- Lost Impression Share (rank) >**40% = WARNING, >60% = FAIL**
- Target CPA <50% of actual CPA = FAIL (unrealistic)

**Extensions/Assets (5% weight):**

- No sitelinks = FAIL
- No callouts or structured snippets = WARNING
- Use 4+ asset types per campaign [Google Support]

**Performance Max (added category):**

- Asset groups without audience signals = WARNING [Adalysis]
- "Poor" ad strength = FAIL
- 30% conversions from brand terms = WARNING (brand cannibalization)

### Meta Ads audit checklist (42 items)

**Pixel/CAPI Health (25% weight):**

- Pixel not firing = CRITICAL FAIL
- No CAPI = CRITICAL FAIL (30-40% data loss post-iOS 14.5)
- EMQ **<6/10 = FAIL, 6-7 = WARNING, 8+ = PASS**
- Missing key conversion events = CRITICAL FAIL
- Deduplication not configured = WARNING
- Domain not verified = FAIL

**Creative Performance (20% weight):**

- Only 1 format used = WARNING (need image, video, carousel minimum)
- Frequency >**3 prospecting = WARNING, >5 = FAIL**
- Frequency >**8 retargeting = WARNING, >12 = FAIL**
- CTR **<0.5% = FAIL, 0.5-1.0% = WARNING**
- No new creative in >**30 days = WARNING, >60 days = FAIL**
- CTR declined >20% from peak + frequency >3 = WARNING (fatigue)

**Learning Phase & Delivery (15% weight):**

- 50% ad sets "Learning Limited" = FAIL
- Ad sets with <50 optimization events/week = WARNING
- Daily budget <5x CPA = WARNING; <2x = FAIL
- Budget utilization <80% = WARNING

**Audience Targeting (15% weight):**

- Audience overlap >20% between any two audiences = WARNING; >40% = FAIL
- No purchaser exclusions from prospecting = WARNING
- Custom audiences <1,000 or >180 days old = WARNING

### Universal health score formula

```
Account Health Score = (Points Earned / Total Possible Points) x 100

Severity weights:
  Critical items: 5 points each
  High items: 3 points each
  Medium items: 1 point each

Scoring per item:
  PASS = full points
  WARNING = 50% of points
  FAIL = 0 points
  N/A = excluded from total
```

| Score | Grade | Action Required |
|---|---|---|
| 90-100 | A | Minor optimizations only |
| 80-89 | B | Some improvement opportunities |
| 70-79 | C | Notable issues need attention |
| 60-69 | D | Significant problems present |
| <60 | F | Urgent intervention required |

---

## SECTION 9: AI and automation across platforms

### Platform AI features in 2026

**Google** launched **Asset Studio with Nano Banana Pro** (November 2025, built on Gemini 3): generates professional-grade images in <10 seconds, [MediaPost Publications] now including people/faces (adults only), all tagged with **SynthID** for transparency. [Google] AI Max for Search provides text guidelines allowing natural language instructions to steer AI content. [Groas] Conversational campaign creation makes advertisers using it **63% more likely** to publish campaigns with "Good" or "Excellent" Ad Strength. [Google]

> Google VP Dan Taylor publicly denied plans for ads in the Gemini app (December 2025). However, ads ARE running in **AI Mode** (75M+ daily active users) and **AI Overviews** (2B+ monthly users), expanded to 11 countries in December 2025.

**Meta's** Advantage+ reached **$60B annualized revenue run rate** by end of 2025. The **GEM AI model** (November 2025) boosted Instagram conversions by **5%** and Facebook Feed by **3%**. Meta's 2026 vision: businesses input a product image + budget goal -> AI generates the entire campaign including imagery, video, text, targeting, and budget allocation.

**TikTok's** Smart+ with Symphony AI integration auto-generates video variations. **42%** of US TikTok performance campaigns now use Smart+, achieving median ROAS of **1.41-1.67**.

**LinkedIn's** Accelerate campaigns (AI-powered end-to-end creation) deliver **42% lower cost per action** in A/B testing and **21% reduction in cost-per-lead** via Predictive Audiences.

**Microsoft's** Copilot in Advertising generates **73% higher CTR**. The **Image Animation** feature (November 2025) converts static images to video assets. Copilot Checkout enables in-conversation commerce.

### What to automate versus keep manual

| Automate | Keep Manual |
|---|---|
| Bidding (Smart Bidding, tROAS, tCPA) | Strategy and goal setting |
| Creative variation testing | Brand messaging and positioning |
| Audience expansion (Predictive/Advantage+) | Budget allocation across platforms |
| Reporting and performance snapshots | Policy compliance review |
| Ad scheduling and pacing | Creative concepting |
| Placement optimization | Sensitive category targeting |

**Guardrails:** Set daily/lifetime budget caps, use Cost Cap or tCPA as safety nets, pause rules if CPA exceeds target by a set percentage, allow 7-10 day learning phases before judging, and start small with AI campaigns before scaling.

---

## SECTION 10: Compliance and privacy regulations

### Critical policy requirements

**Google Ads** enforces a three-strike system: Strike 1 = 90-day probation; Strike 2 = 90-day restriction; Strike 3 = permanent suspension. Prohibited content includes counterfeit goods, dangerous products, dishonest behavior enablement, and inappropriate content. Restricted categories requiring certification: online pharmacies, telemedicine, health insurance, gambling, political ads, and cryptocurrency.

**Meta Ads** rejected or removed **over 1.3 billion ads** in 2024. Special Ad Categories (Housing, Employment, Credit) restrict targeting -- no ZIP code targeting, age must be 18-65+, no lookalike audiences. **Financial Products & Services** became a new Special Ad Category enforced January 2025.

### Privacy landscape in February 2026

> **Privacy Sandbox is officially dead.** Google confirmed retirement of the entire project in October 2025. Third-party cookies remain enabled by default in Chrome. Safari and Firefox already block them.

**iOS ATT opt-in rates:** Industry average **~35%** (Q2 2025, up from 29% in 2022). Gaming highest at 37-50%; education lowest at 7-14%. Apps with <30% opt-in lose **58% of ad revenue** on average.

**US state privacy laws: 20 state consumer privacy laws in effect by January 2026** -- up from ~5 in 2023. New laws effective January 1, 2026: Indiana, Kentucky, and Rhode Island. California's CPPA finalized sweeping new regulations requiring **mandatory cybersecurity audits** and **data processing risk assessments** before targeted advertising. Texas AG obtained a **$1.4 billion settlement** for tracking violations. Server-side tracking is now architecturally necessary for compliance.

---

## SECTION 11: Industry-specific playbooks

### SaaS/Software

**Budget split:** Google Search 45%, LinkedIn 30%, Meta 15%, YouTube/Display 10%. **Key benchmarks:** Google CPC $5-8+, LinkedIn CPC $8.04, CVR 2-5%, CPA $100-200 (Google) / $150-400 (LinkedIn), target ROAS 3-4x on LTV basis. **Critical mistakes:** Measuring immediate ROAS instead of LTV/CAC payback, broad keywords without negative lists, running same creative 30+ days. **Scale path:** High-intent branded/competitor keywords -> category terms -> LinkedIn ABM for enterprise -> retargeting waterfall -> CRM data feedback via CAPI.

### E-commerce/D2C

**Budget split:** Meta 60-68%, Google 23-25%, TikTok 5-10%, Pinterest 2-5%. **Key benchmarks:** Google Shopping CPC $0.66, median ROAS 3.68 (Google) / 2.19 (Meta) / 3.61 (Meta retargeting), Advantage+ ROAS $4.52, CPA $23.74 (up 12.35% YoY). **Critical mistakes:** Over-investing in BOF only (allocate 60% to TOF/MOF), ignoring rising CPAs (CVR dropped 9.28%), pixel-only tracking (missing 18-22% of touchpoints). **Scale path:** Prove unit economics at $50-100/day -> scale winners 20% every 3 days -> diversify Meta to Google Shopping + PMax -> TikTok for CPM arbitrage -> track POAS not just ROAS.

### Local Services

**Budget split:** Google LSA 60%, Google Search PPC 30%, Meta 10%. **Key benchmarks:** LSA CPL ranges from $34 (locksmith) to $249 (personal injury lawyer); home services CPC $7.85, CVR 7.33%, CPL $90.92. 90%+ of LSA leads are phone calls; 50-70% convert to customers. **Critical rule:** Target **4.8+ star rating with 150+ reviews** -- this is the #1 LSA ranking factor. Respond to leads within 5 minutes (21x more effective than 30-minute response).

### B2B/Enterprise

**Budget split:** LinkedIn 39%, Google Search 35%, Meta/Display 15%, programmatic 11%. **Key benchmarks:** LinkedIn CPC $5.58-$10 (Q3 highest at $15.72), CPM $33-$55, CTR 0.52%, LinkedIn ROAS 113%. Average B2B sales cycle is **211 days** with **76 touches** before purchase. LinkedIn cost per company influenced is **EUR154** -- 25% cheaper than Google, 70% cheaper than Meta for B2B. **Critical insight:** Lead Gen Forms convert at **13%** (3.25x higher than landing pages) but produce lower SQL rates -- use 60-70% TOFU budget for LGF, flip for BOFU.

### Healthcare

**Budget split:** Google Search 55%, Meta 20%, Microsoft 10%, YouTube/Display 10%, programmatic 5%. Healthcare has the **highest CPM of any industry at $36.82**. Google certification required for online pharmacies, telemedicine, and prescription drugs. **LegitScript certification** required for pharmacies and telemedicine. **Cannot use remarketing/retargeting** for health services -- this violates Google's personalized advertising policy and risks account suspension. Cannot target by health conditions. Use contextual targeting instead of audience targeting.

### Finance/Fintech

**Budget split:** Google Search 40%, LinkedIn 30%, Meta 15%, YouTube/Display 10%, TikTok 5%. Google CPC $3.46-$3.77 (consumer), CTR 8.33%, CVR 2.55% (among lowest). Financial ads require clear disclosures (APR, fees, terms). Google certification required for lending and crypto products. A $100 CPL on a $10K LTV customer represents excellent economics -- optimize for downstream revenue, not surface-level CPA.

### Additional playbooks

**Agency:** Standardize onboarding per vertical, build templatized campaign structures, invest in cross-account reporting (Swydo, Supermetrics), minimum viable client spend $1,500-3,000/month, target 85%+ client retention. **Info Products/Coaching:** 70-80% Meta, webinar registration $5-15/registrant, show-up rate 25-40% (live), conversion 5-10% of attendees, 60% budget to TOF/MOF. **Mobile App:** Average CPI $2.65-3.50 (Google), $3.75 (Meta), $2.88 (TikTok); iOS ~$3.60 vs Android ~$1.20; optimize for post-install quality not just CPI. **Real Estate:** Google CPC $1.55-2.53, CTR 8.43%, CVR 3.28%; 96.72% don't convert on first visit -- retargeting is essential.

---

## SECTION 12: Tools, APIs, and building the CLI tool

### Essential tools landscape

| Category | Top Tools | Key Notes |
|---|---|---|
| Competitor research | SEMrush ($140/mo), SpyFu ($39/mo), Google Auction Insights (free), Meta Ad Library (free) | SEMrush most comprehensive; SpyFu best for historical data |
| PPC automation | Optmyzr ($249+/mo), Adalysis ($149+/mo), Revealbot/Birch ($49+/mo), Madgicx ($44+/mo) | Adalysis runs 100+ automated daily checks |
| Attribution | Triple Whale ($149+/mo), GA4 (free) | Triple Whale dominant for Shopify ecommerce |
| Landing pages | Unbounce ($99/mo), Instapage ($79/mo), Leadpages ($37/mo) | Unbounce Smart Traffic delivers 30% more conversions |
| Feed management | DataFeedWatch ($64/mo), Feedonomics (enterprise), GoDataFeed ($39/mo) | DataFeedWatch best self-serve; Feedonomics best managed |
| Reporting | Looker Studio (free), Supermetrics (EUR29/mo), AgencyAnalytics | Supermetrics connects 150+ platforms |

### API reference for building claude-ads

**Google Ads API (v23, released January 27, 2026):**

- Authentication: OAuth 2.0 + Developer Token
- Access levels: Test (15K ops/day), Basic (15K ops/day), Standard (unlimited)
- Query language: GAQL (SQL-like) -- `SELECT ... FROM ... WHERE ... ORDER BY ... LIMIT`
- Client libraries: Python (`google-ads`), Java, PHP, Ruby, .NET, Perl
- **Key audit queries via GAQL:**
  - Campaign performance: `SELECT campaign.name, metrics.cost_micros, metrics.conversions FROM campaign WHERE segments.date DURING LAST_30_DAYS`
  - Quality scores: `SELECT ad_group_criterion.keyword.text, ad_group_criterion.quality_info.quality_score FROM keyword_view`
  - Search terms: `SELECT search_term_view.search_term, metrics.impressions, metrics.clicks FROM search_term_view`
  - Recommendations: `SELECT recommendation.type, recommendation.impact FROM recommendation`
  - Change history: `SELECT change_event.change_date_time, change_event.changed_fields FROM change_event`
- v23 new: Granular channel-level PMax reporting, asset A/B testing
- Cost: **FREE** with Google Ads account

**Meta Marketing API (v22.0 / Marketing API v24.0):**

- Authentication: OAuth 2.0 via Facebook Login; permissions `ads_read`, `ads_management`
- Key endpoints: `/{ad-account-id}/campaigns`, `/{object-id}/insights`, `/{ad-account-id}/customaudiences`
- Insights metrics: impressions, clicks, cpc, cpm, ctr, spend, reach, frequency, conversions, actions, cost_per_action_type, roas, video views
- Breakdowns: age, gender, country, placement, device_platform
- Rate limits: Rolling 1-hour window, Business Use Case rate limiting
- Client libraries: Python (`facebook-business`), PHP, Node.js, Ruby
- v25.0 (Q1 2026): Full deprecation of legacy ASC/AAC APIs
- Cost: **FREE**

**Other platform APIs:**

- **LinkedIn Marketing API:** Versioned monthly (e.g., 202601); OAuth 2.0; full Campaign Manager functionality; Conversions API for server-side tracking; Development access read-only for unlimited accounts
- **TikTok Marketing API:** Base URL `business-api.tiktok.com/open_api/v1.2/`; OAuth 2.0; 600 requests/minute default; SDKs in Java, Python, JavaScript
- **Microsoft Advertising API:** v13 (stable); OAuth 2.0 via Azure AD; SOAP-based with REST emerging; SDKs in .NET, Java, Python, PHP

**What can be automated via API for audits:** Quality Score analysis, search terms analysis, recommendations review, change history audit, budget pacing, ad performance metrics, keyword analysis, auction insights, landing page scores, creative performance, audience overlap detection, frequency analysis, and placement breakdowns. **What cannot be accessed:** Competitor bids, other advertisers' Quality Scores, Google's internal ML signals, Smart Bidding internals, or real-time auction data. All major ad platform APIs are **free** with active advertising accounts.

### Recommended architecture for claude-ads

**Language:** Python (best client library support across all five platforms). **Key libraries:** `google-ads` (Google), `facebook-business` (Meta), `tiktok-business-api` (TikTok), `bingads` (Microsoft). **Auth strategy:** OAuth 2.0 with refresh token storage in encrypted local JSON. **Reference project:** `gaql-cli` by GetYourGuide on GitHub provides a Python CLI pattern for GAQL queries. Priority: start with Google Ads API (richest audit data) + Meta Marketing API (largest social platform), then extend to LinkedIn, TikTok, and Microsoft.

---

## Conclusion: what the data reveals for building claude-ads

Three structural forces define the paid advertising landscape the CLI tool must navigate. First, **AI automation is no longer optional** -- Advantage+, Smart+, AI Max, and Copilot now run the majority of high-performing campaigns, meaning the tool should audit AI configuration quality rather than manual bid management. Second, **creative quality has become the primary performance lever**, accounting for up to 70% of Meta campaign results; the tool should prioritize creative diversity, fatigue detection, and format coverage in its scoring. Third, **measurement fragmentation** across 20+ state privacy laws, ATT, and deprecated attribution models means server-side tracking health (CAPI, Enhanced Conversions, Consent Mode v2) deserves Critical severity in every audit.

The audit scoring system should weight conversion tracking infrastructure heaviest (20-25% of score) because every other optimization depends on accurate measurement. The 70-item Google checklist and 42-item Meta checklist provide complete pass/fail criteria with specific numeric thresholds derived from 2025 benchmark data. The GAQL queries and API endpoints documented above enable programmatic access to approximately 70% of these audit items, with the remainder requiring heuristic analysis of the retrieved data.

The most actionable finding for the tool's users: **CPCs rose for the fifth consecutive year, but conversion rates improved for 65% of industries** -- the accounts losing money are not victims of platform economics but of poor fundamentals that systematic auditing can catch and fix.
