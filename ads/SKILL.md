---
name: ads
description: "Free-first paid advertising audit and optimization skill, focused on the 3 platforms where 95% of advertiser spend lives: Meta, Google, TikTok. ~158 weighted checks with scoring, parallel agents, industry templates, and AI creative generation."
argument-hint: "audit | google | meta | tiktok | creative | landing | budget | plan <type> | competitor | dna <url> | create | generate | photoshoot | update <platform|all> | publish"
license: MIT
---

# Ads: Free-first Paid Advertising Audit & Optimization

Focused ad account analysis on the 3 base platforms where most ad spend
lives: **Meta, Google, TikTok**. Orchestrates 17 specialized sub-skills and
7 agents (3 audit + 4 creative).

## Quick Reference

| Command | What it does |
|---------|-------------|
| `/ads audit` | Full multi-platform audit with parallel subagent delegation (3 agents: Meta, Google, TikTok) |
| `/ads google` | Google Ads deep analysis (Search, PMax, includes YouTube video campaigns) |
| `/ads meta` | Meta Ads deep analysis (FB, IG, Advantage+) — MCP-wired to claude.ai Facebook |
| `/ads tiktok` | TikTok Ads deep analysis (Creative, Shop, Smart+, Symphony, GMV Max) |
| `/ads creative` | Cross-platform creative quality audit |
| `/ads landing` | Landing page quality assessment for ad campaigns |
| `/ads budget` | Budget allocation and bidding strategy review |
| `/ads plan <business-type>` | Strategic ad plan with industry templates |
| `/ads competitor` | Competitor ad intelligence analysis |
| `/ads math` | PPC financial calculator (CPA, ROAS, break-even, budget forecasting) |
| `/ads test` | A/B test design (hypothesis, significance, duration, sample size) |
| `/ads report` | PDF audit report generation for client deliverables |
| `/ads dna <url>` | Extract brand DNA from website, outputs `brand-profile.json` |
| `/ads create` | Generate campaign concepts + copy briefs, outputs `campaign-brief.md` |
| `/ads generate` | Generate AI ad images from brief, outputs to `ad-assets/` |
| `/ads photoshoot` | Product photography in 5 styles (Studio, Floating, Ingredient, In Use, Lifestyle) |
| `/ads update <platform\|all>` | Refresh per-platform references with last 30 days of changes (COSTLY: ~50–150k tokens/platform; gates on confirmation) |
| `/ads publish` | Publish generated creatives to 14+ social networks via Zernio (first 2 accounts free; see `skills/ads-publish/SKILL.md`) |

## Context Intake (Required: Always Do This First)

Before any audit or analysis, collect this context. Without it, benchmarks will
be generic and recommendations may be wrong for the user's situation.

Ask these questions upfront (combine into one message):

1. **Industry / Business type**: Which best describes you?
   E-commerce · Local Service · Real Estate · Healthcare · Finance · Agency · Other
   (Note: B2B-enterprise, SaaS, mobile-app, and info-products templates were removed in v2.3.0 since they depended on LinkedIn/Apple/YouTube which are no longer audited; use the `generic` template plus the platform-specific skills below.)
2. **Monthly ad spend**: Total budget and per-platform breakdown (approximate is fine)
3. **Primary goal**: Sales / Revenue · Leads / Demos · App Installs · Calls · Brand
4. **Active platforms**: Of the 3 supported (Meta, Google, TikTok), which are you advertising on?

If the user provides data upfront (e.g. "audit my Google Ads, I spend $5k/mo on SaaS"),
extract context from that and proceed without re-asking.

Use the provided context to:
- Select the correct industry benchmarks from `references/benchmarks.md`
- Apply budget-appropriate recommendations (e.g. Smart Bidding requires 15+ conv/month)
- Calibrate severity scoring (a $500/mo account has different priorities than $50k/mo)

## Orchestration Logic

When the user invokes `/ads audit`, delegate to subagents in parallel:
1. **Collect context** (see Context Intake above; do this first)
2. Collect account data (exports, screenshots, or pasted metrics)
3. Detect business type and identify active platforms
4. Spawn 3 subagents via Task tool with `context: fork` — one per active platform: `audit-google`, `audit-meta`, `audit-tiktok`
5. **Validate**: each subagent writes both `<platform>-audit-results.json` and `<platform>-audit-results.md`. Parse the JSON and validate against `references/audit-output-schema.json` before aggregating. If any subagent's JSON is missing or invalid, surface the error and stop — do not silently aggregate partial results.
6. Aggregate scores using the platform-budget-share formula in `references/scoring-system.md` and generate the unified Ads Health Score (0-100)
7. Create prioritized action plan from the `quick_wins` and `critical_issues` arrays of each JSON

For individual commands (`/ads google`, `/ads meta`, etc.), load the relevant
sub-skill directly. Still collect context first if not already provided.

For `/ads update <platform|all>`, route to `skills/ads-update/SKILL.md`. The update
skill enforces a mandatory cost-confirmation gate before fetching — do NOT bypass
it. See `references/update-cost-warning.md` for the rationale.

## Creative Workflow

Sequential pipeline (each step is independently runnable):
1. `/ads dna <url>` → `brand-profile.json` in current directory
2. `/ads create` → reads profile + optional audit results → `campaign-brief.md`
3. `/ads generate` → reads brief + profile → `ad-assets/` directory
4. `/ads photoshoot` → standalone or reads profile for style injection

Requires `GOOGLE_API_KEY` (Gemini default) or `ADS_IMAGE_PROVIDER` + matching key.
If API key is missing, `/ads generate` and `/ads photoshoot` display setup
instructions and exit; they never fail silently.

## Industry Detection

Detect business type from ad account signals:
- **SaaS**: trial_start/demo_request events, pricing page targeting, long attribution windows
- **E-commerce**: purchase events, product catalog/feed, Shopping/PMax campaigns
- **Local Service**: call extensions, location targeting, store visits, directions events
- **B2B Enterprise**: LinkedIn Ads active, ABM lists, high CPA tolerance ($50+), long sales cycle
- **Info Products**: webinar/course funnels, lead gen forms, low-ticket offers
- **Mobile App**: app install campaigns, in-app events, deep linking
- **Real Estate**: listing feeds, property-specific landing pages, geo-heavy targeting
- **Healthcare**: HIPAA compliance flags, healthcare-specific ad policies
- **Finance**: Special Ad Categories declared, financial products compliance
- **Agency**: multiple client accounts, white-label reporting needs

## Quality Gates

Hard rules (never violate these):
- Never recommend Broad Match without Smart Bidding (Google)
- 3x Kill Rule: flag any ad group/campaign with CPA >3x target for pause
- Budget sufficiency: Meta ≥5x CPA per ad set, TikTok ≥50x CPA per ad group
- Learning phase: never recommend edits during active learning phase
- Compliance: always check Special Ad Categories for housing/employment/credit/finance
- Creative: never run silent video ads on TikTok (sound-on platform)
- Attribution: default to 7-day click / 1-day view (Meta), data-driven (Google)
- Andromeda creative diversity: Flag Meta accounts with <10 genuinely distinct creatives
- Privacy infrastructure gate: Always verify tracking stack (Consent Mode V2, CAPI, Events API, AdAttributionKit) before making optimization recommendations
- PDF report quality gate: When generating reports via `/ads report`, always use `scripts/generate_report.py` with `--check` first. Reports must have: clean layout with no overlapping elements, proper margins (0.75in), word-wrapped table cells (no clipping), all charts/images sized within page boundaries, page numbers and section dividers, captions on every visual, and zero empty sections. Run `--check` before `--output` and fix any warnings before delivering the PDF

## Reference Files

Load these on-demand as needed; do NOT load all at startup.

**Path resolution:** All references are installed at `~/.claude/skills/ads/references/`.
When sub-skills or agents reference `ads/references/*.md`, resolve to
`~/.claude/skills/ads/references/*.md`.

- `references/audit-methodology.md`: **Shared 7-step audit process** all platform skills delegate to. Single source of truth for the audit skeleton, check ID convention, MCP-first rule, and output contract reference.
- `references/audit-output-schema.json`: **Canonical JSON schema** every audit-* agent must emit. The orchestrator validates against this before aggregating cross-platform scores. New integrations conform to this contract.
- `references/scoring-system.md`: Weighted scoring algorithm and grading thresholds
- `references/benchmarks.md`: Industry benchmarks by platform (CPC, CTR, CVR, ROAS)
- `references/bidding-strategies.md`: Bidding decision trees per platform
- `references/budget-allocation.md`: Platform selection matrix, scaling rules, MER
- `references/platform-specs.md`: Creative specifications across all platforms
- `references/conversion-tracking.md`: Pixel, CAPI, EMQ, ttclid implementation
- `references/compliance.md`: Regulatory requirements, ad policies, privacy
- `references/google-audit.md`: 80-check Google Ads audit checklist (includes YouTube video campaigns)
- `references/meta-audit.md`: 50-check Meta Ads audit checklist
- `references/tiktok-audit.md`: 28-check TikTok Ads audit checklist
- `references/brand-dna-template.md`: Brand DNA schema and extraction guide
- `references/image-providers.md`: Provider config (Gemini/OpenAI/Stability/Replicate)
- `references/google-creative-specs.md`: PMax/RSA/YouTube generation-ready specs
- `references/meta-creative-specs.md`: Feed/Reels/Stories specs + safe zones
- `references/tiktok-creative-specs.md`: 9:16 only + safe zone overlay
- `references/gaql-notes.md`: GAQL field compatibility, deduplication patterns, filter scope best practices
- `references/voice-to-style.md`: Brand voice axis to visual attribute mapping for image generation
- `references/copy-frameworks.md`: 6 ad copy frameworks (AIDA, PAS, BAB, 4P, FAB, Star-Story-Solution)
- `references/mcp-integration.md`: Canonical MCP integration pattern + per-platform MCP server catalog
- `references/mcp-meta-integration.md`: Meta MCP check↔tool mapping (template for new MCP integrations)

For platforms where MCP is not the preferred path, the audit agent reads
`<platform>-data.json` produced by `scripts/api/<platform>_fetch.py`.
These are pure-stdlib API adapters covering Meta, Google, and TikTok.
See `scripts/api/README.md` for the per-platform OAuth setup walkthrough.

## Scoring Methodology

### Ads Health Score (0-100)

Per-platform score using weighted algorithm from `references/scoring-system.md`.
Cross-platform aggregate weighted by budget share:

```
Aggregate = Sum(Platform_Score x Platform_Budget_Share)
```

### Grading

| Grade | Score | Action Required |
|-------|-------|-----------------|
| A | 90-100 | Minor optimizations only |
| B | 75-89 | Some improvement opportunities |
| C | 60-74 | Notable issues need attention |
| D | 40-59 | Significant problems present |
| F | <40 | Urgent intervention required |

### Priority Levels

- **Critical**: Revenue/data loss risk (fix immediately)
- **High**: Significant performance drag (fix within 7 days)
- **Medium**: Optimization opportunity (fix within 30 days)
- **Low**: Best practice, minor impact (backlog)

## Sub-Skills

This skill orchestrates 17 specialized sub-skills:

1. **ads-audit**: Full multi-platform audit with parallel delegation across Meta / Google / TikTok
2. **ads-google**: Google Ads deep analysis (Search, PMax, YouTube video campaigns — they share the Google Ads API)
3. **ads-meta**: Meta Ads deep analysis (FB, IG, Advantage+) — MCP-wired to claude.ai Facebook
4. **ads-tiktok**: TikTok Ads deep analysis (Creative, Shop, Smart+, Symphony, GMV Max)
5. **ads-creative**: Cross-platform creative quality audit
6. **ads-landing**: Landing page quality for ad campaigns
7. **ads-budget**: Budget allocation and bidding strategy
8. **ads-plan**: Strategic ad planning with industry templates (8 templates after v2.3.0 scope-down)
9. **ads-competitor**: Competitor ad intelligence
10. **ads-dna**: Brand DNA extraction from website URL
11. **ads-create**: Campaign concepts, copy decks, creative briefs
12. **ads-generate**: AI image generation with pluggable providers
13. **ads-photoshoot**: Product photography in 5 professional styles
14. **ads-update**: Refresh per-platform references with last 30 days of changes
15. **ads-math**: PPC financial calculator (CPA, ROAS, break-even, LTV:CAC, MER)
16. **ads-test**: A/B test design (hypothesis, sample size, statistical significance)
17. **ads-publish**: Publish creatives to 14+ social networks via Zernio (first 2 accounts free)

Plus `/ads report` for PDF deliverable generation (implemented in `scripts/generate_report.py`, no SKILL.md).

## Subagents

For parallel analysis during full audits — one deep specialist per platform:
- `audit-google`: Google Ads 80-check audit (G01-G74, G-PM*, G-AI*, G-DG*, G-CTV*, G-WS*, G-KW*, G-CT*, G-AD*)
- `audit-meta`: Meta Ads 50-check audit (M01-M40, M-AN*, M-AT*, M-CR*, M-ST*, M-IA*, M-TH*) — MCP-wired
- `audit-tiktok`: TikTok Ads 28-check audit (T01-T25, T-SR*) — consolidates the former audit-creative/tracking/budget/compliance for TikTok into one deep-specialist agent

Creative pipeline agents (unchanged):
- `creative-strategist`: Campaign concepts from brand profile + audit results (Opus, maxTurns: 25)
- `visual-designer`: Image generation with brand injection via generate_image.py (Sonnet, maxTurns: 30)
- `copy-writer`: Headlines, CTAs, primary text within platform limits (Sonnet, maxTurns: 20)
- `format-adapter`: Asset dimension validation and spec compliance reporting (Haiku, maxTurns: 15)

---

Maintained by [tododeia.com](https://tododeia.com) — Instagram [@soyenriquerocha](https://instagram.com/soyenriquerocha)
