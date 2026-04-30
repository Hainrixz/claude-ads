# Changelog

All notable changes to claude-ads are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.1.2] - 2026-04-29

Visual identity rewrite — replaced all five raster JPGs (generated with AI image models in v2.1.0–v2.1.1) with hand-authored, hand-coded SVG infographics in the [tododeia.com](https://tododeia.com) house style: light dot-pattern background (`#FAFAFA` + `#E5E5E5`), bold black wordmarks (`#0A0A0A`), pill-shaped buttons (`rx=full`), and a flat brand palette of orange (`#F47B30`) and blue (`#2563EB`). Total weight dropped from ~1.77 MB to ~29 KB (60× lighter), text is now perfectly crisp at any zoom, and there is zero risk of AI typos in rendered text.

### Changed

- **All 5 README images rewritten as hand-authored SVG**, replacing the v2.1.1 Nano Banana PRO raster renders:
  - `assets/hero.svg` (3.4 KB) — `claude-ads.` wordmark in 200pt black, gold-shimmer "VERSION 2.1.2 · 250+ checks · 7 platforms · MCP-ready" pill, two rows of clickable-style command pills (`/ads audit`, `/ads google`, `/ads meta`, `/ads tiktok`, `Connect MCP`, `/ads update`, `/ads report`).
  - `assets/how-it-works.svg` (4.9 KB) — three-stage flow with section labels (1 · INPUT, 2 · ORCHESTRATE, 3 · OUTPUT). Dashed orchestrator container holds the `/ads orchestrator` black pill with six agent pills below (Google · 80, Meta · 50, Creative, Tracking, Budget, Compliance). Output: orange `HEALTH SCORE 78 / 100 · B` pill.
  - `assets/platforms.svg` (7.1 KB) — 4×2 tile grid. Each tile is a white card with a colored top accent bar, platform name in 26pt black, check count in 56pt color (Google 80 orange, Meta 50 blue, YouTube multi black, LinkedIn 27 blue, TikTok 28 black, Microsoft 24 orange, Apple 35+ black) and area tags. Cross-platform tile is dashed/dimmed.
  - `assets/connect.svg` (5.3 KB) — radial network: black `claude-code · /ads` hub at center, five outlined pills around it labeled with platform name + monospace MCP server identifier (`cohnen/mcp-google-ads`, `brijr/meta-mcp`, `Synter · Adzviser`, `AdsMCP/tiktok-ads-mcp`, `CData · Synter`). Below: white "Manual mode" pill vs orange "Live mode" pill.
  - `assets/showcase.svg` (8.4 KB) — three-column dashboard. Left card: 78/100 semicircle gauge with cyan→orange gradient stroke and B grade badge. Center card: full A–F grade scale with B row highlighted ("← you are here"). Right card: three findings cards (CRITICAL/WARNING/QUICK WIN with proper red/yellow/green vertical accent bars) plus three platform breakdown bars (Google 82, Meta 71, LinkedIn 88).
- All SVGs use the same design tokens: `Inter` system font with fallbacks, dot-pattern background `<pattern id="dots">`, pill `rx=full` corner radius, `viewBox="0 0 1600 900"` (16:9), `role="img"` + `aria-label` for screen-reader accessibility.
- README image alt text reused from v2.1.1 (already accurate descriptions of rendered content), only the file extension swapped `.jpg` → `.svg` in both EN and ES.
- Version bumped `2.1.1` → `2.1.2` across `README.md` badge, `README.es.md` badge, `.claude-plugin/plugin.json`, and `.claude-plugin/marketplace.json`.

### Removed

- `assets/{hero,how-it-works,platforms,connect,showcase}.jpg` (v2.1.1 Nano Banana PRO renders, ~1.77 MB total). The visual identity changed enough that keeping both formats wasn't worth the binary churn.

### Why this rewrite

- **Brand consistency.** v2.1.1's dark-navy/cyan/magenta cinematic mood was inherited from prompt experimentation with Higgsfield, not from the maintainer's actual brand. The new SVGs match [tododeia.com](https://tododeia.com)'s light-bg dot-pattern aesthetic, so the README, the website, and the brand wordmark all read as one product.
- **Sharper text.** AI-rendered text occasionally has subtle artifacts (kerning, partial letterforms) that are visible at GitHub's raw image scale. SVG text is rasterized by the browser and is pixel-perfect at every zoom level.
- **60× smaller.** ~29 KB total vs 1.77 MB. README loads on slow connections, and the repo's `assets/` no longer dominates clone size.
- **Editable.** Future content updates (new platform, new command, score change) are 5-minute SVG text edits — no MCP server needed, no credit cost, no AI prompt re-rolls.

### Notes

- Pure docs / assets / version-string change. Zero behavior change in any sub-skill, agent, script, or routing logic.
- All 5 SVGs validated with `xmllint --noout` (well-formed XML).
- GitHub renders `<img src="*.svg">` natively in markdown — no additional setup needed.

## [2.1.1] - 2026-04-29

Visual identity upgrade — replaced the v2.1.0 atmospheric mood images with didactic infographics that actually teach what Claude Ads does. Same 5-image footprint (~1.8 MB total), but each image now contains rendered text, labeled diagrams, and concrete data instead of abstract visual mood.

### Changed

- **Re-rendered 5 README images using Nano Banana PRO** (Google's `nano_banana_2`, "Ultimate quality, text and diagrams"), replacing the v2.1.0 Higgsfield Cinema Studio renders. The new images include readable text, flow arrows, labeled tiles, and dashboard mockups so the README is informative even before reading the prose:
  - `assets/hero.jpg` — terminal showing `$ /ads audit → Dispatching 6 parallel agents...`, brand wordmark, sample 78/100 dashboard with six platform bars (Google, Meta, LinkedIn, TikTok, YouTube, Apple).
  - `assets/how-it-works.jpg` — left-to-right flow diagram: `Your ad data → /ads orchestrator → 6 agent panels (Google · 80 checks, Meta · 50 checks, Creative quality, Tracking + privacy, Budget + bidding, Compliance) → Ads Health Score 0–100`.
  - `assets/platforms.jpg` *(renamed from `agents.jpg`)* — 4×2 grid of 7 platform tiles + 1 cross-platform tile, each showing platform name, check count (80, 50, 27, 28, 24, 35+, multi, 3), and key area tags. Moved from "Industry templates" section to "Platforms covered" section in both READMEs (visual TOC for the table that follows).
  - `assets/connect.jpg` — radial network diagram: `Claude Code · /ads` central hexagon → 5 platform nodes labeled with their MCP server identifiers (`cohnen/mcp-google-ads`, `brijr/meta-mcp`, `Synter · Adzviser`, `AdsMCP`, `CData · Synter`); MANUAL MODE vs LIVE MODE lanes at the bottom.
  - `assets/showcase.jpg` — sample report mockup: 78/100 gauge with B grade, A–F grade-scale legend with B highlighted, three findings cards (CRITICAL · WARNING · QUICK WIN), platform breakdown bars (Google 82 / Meta 71 / LinkedIn 88).
- **README image alt text** rewritten in both EN and ES to describe the actual rendered content (e.g. "Flow diagram — your ad data → /ads orchestrator → 6 parallel audit agents → Ads Health Score 0–100") instead of generic mood descriptions. Improves screen-reader and SEO clarity.
- Industry templates section in both READMEs now relies on the table alone (image moved to Platforms section, where it's more useful as a visual TOC).
- Version bumped `2.1.0` → `2.1.1` across `README.md` badge, `README.es.md` badge, `.claude-plugin/plugin.json`, and `.claude-plugin/marketplace.json` (both metadata and per-plugin entries).

### Notes

- File renames: `assets/agents.jpg` → `assets/platforms.jpg` (matches the new content). All four other JPGs keep their existing filenames; only the underlying pixels changed.
- Compressed sizes: hero 276 KB · how-it-works 337 KB · platforms 438 KB · connect 377 KB · showcase 345 KB (total ~1.77 MB, comparable to v2.1.0).
- Pure docs / assets / version-string change. Zero behavior change in any sub-skill, agent, script, or routing logic.

## [2.1.0] - 2026-04-29

Documentation and visual identity release. No behavior change in any sub-skill, agent, script, or routing logic — pure docs / assets / version-string update so users (and clients) get a clear, distinctive face for the fork instead of an upstream lookalike.

### Added

- **Spanish README** (`README.es.md`) — full localized version for LatAm / Spanish-speaking practitioners, with bilingual switcher (`EN · ES`) at the top of both files. Voice is natural LatAm Spanish, not a literal translation; commands, code blocks, and product names stay untranslated.
- **"Connect to your real ad accounts" section** — new top-level section in both READMEs with a per-platform MCP server table (Google Ads → `cohnen/mcp-google-ads`, Meta → `brijr/meta-mcp` or Adspirer, LinkedIn → Synter / Adzviser, TikTok → `AdsMCP/tiktok-ads-mcp-server`, Microsoft → CData / Synter), including install commands, auth requirements, and a read-vs-write safety caveat. Gives users a documented path from "paste-based analyzer" to "live ads agent." Points to existing `ads/references/mcp-integration.md` for the full per-platform setup walkthrough.
- **5 new cinematic dark/neon brand images** at `assets/{hero,how-it-works,agents,connect,showcase}.jpg`, generated via Higgsfield Cinema Studio 2.5 (16:9, JPEG q90, ~1.7 MB total). All images feature dark navy backgrounds with subtle cyan/magenta accents and contain no real brand logos or readable text (trademark hygiene).
- **Inline mermaid orchestration diagram** in both READMEs replacing the most important upstream SVG flow (`/ads audit` → 6 parallel agents → scored report). Renders natively on GitHub, no asset to maintain, easy to keep in sync with code changes.
- **LICENSE: tododeia.com copyright line** added below the upstream `agricidaniel` line. Original upstream copyright preserved verbatim per MIT §2.

### Changed

- **`README.md` fully rewritten** (395 → 292 lines). New ELI5 intro in plain English ("you know how you can ask Claude to review your code? Claude Ads is the same idea, but for paid advertising") explains what the skill is and isn't (analysis tool by default, real ads agent when paired with MCP). Restructured into 16 sections: What is this? · Quick start · How it works · What you can run · Platforms covered · Connect to your real ad accounts · Industry templates · Showcase · `/ads update` · What's different in this fork · Privacy · FAQ · Requirements · Uninstall · Credits · License.
- **Honest "What's different in this fork" section** — 3-bullet summary distinguishing what tododeia actually added (`/ads update`, refreshed 2026 references, rebrand) from what came from upstream (250+ checks, 19 sub-skills, 10 agents, 12 templates, audit pipeline). Replaces scattered attribution.
- Version bumped `2.0.3` → `2.1.0` across `README.md` badge, `README.es.md` badge, `.claude-plugin/plugin.json` (`version`), and `.claude-plugin/marketplace.json` (both `metadata.version` and the per-plugin entry).

### Removed

- All 18 upstream-derived SVG diagrams in `assets/diagrams/` (`01-architecture.svg` through `20-install-methods.svg`, ~970 lines of vector markup). The fork now has its own visual identity instead of carrying upstream visuals.
- `assets/demo.gif` (628 KB) — to be replaced with a freshly recorded terminal cast in a follow-up commit (asciinema → `agg`).

### Notes

- Doc-level verification passed: 5/5 image references resolve, 6/6 internal relative links resolve (`ads/references/mcp-integration.md`, `scripts/lib/THIRD_PARTY_NOTICES.md`, `skills/ads-update/SKILL.md`, `scripts/url_utils.py`, `CHANGELOG.md`, `LICENSE`), zero leftover references to deleted `assets/diagrams/` or `demo.gif`, EN↔ES section parity (16 sections / 292 lines each), plugin manifest version strings match the README install command (`claude-ads@tododeia-claude-ads`).
- The "LICENSE preserved verbatim" stance from v2.0.0 is updated here — adding the fork maintainer's copyright is allowed under MIT and standard practice for actively maintained forks. The upstream `agricidaniel` line remains untouched immediately above.

## [2.0.3] - 2026-04-29

### Fixed

- **PDF report header/footer version strings** — `scripts/generate_report.py` had two stale `claude-ads v1.5` strings (page-footer canvas string at line 481 and title-page subtitle at line 502) that were missed in the v2.0.0 brand-strip pass. PDFs generated by `/ads report` now show `v2.0` consistently across all three locations.
- **Phantom file reference removed** — `README.md` and `ads/references/mcp-integration.md` both referenced `scripts/fetch_meta_ads.py`, which has never existed in the repository (this was an upstream documentation bug inherited at fork time). Replaced the README mention with the Adspirer MCP recommendation alone, and rewrote the mcp-integration.md note to point at the Meta Marketing API directly without referencing a non-existent script.

## [2.0.2] - 2026-04-29

### Fixed

- **Uninstall script coverage** — `uninstall.sh` and `uninstall.ps1` now also remove `ads-math`, `ads-test`, and `ads-update` sub-skills. Without this fix, those three directories would have been left behind in `~/.claude/skills/` after running uninstall (`ads-math` and `ads-test` were already missing from the upstream uninstall list — `ads-update` is new in this fork).

## [2.0.1] - 2026-04-29

### Fixed

- **Install path coverage** — `install.sh` and `install.ps1` now recursively copy `scripts/` so the vendored `scripts/lib/` (dates, signals, dedupe, story) actually deploys. Previously, only top-level `*.py` files were copied, which would have caused `from lib import ...` to fail at runtime on installed environments.
- **Reference file location** — moved the 8 new reference files (7 platform changelogs + `update-cost-warning.md`) from top-level `references/` to `ads/references/`, matching the existing convention and the install scripts' source path. Updated all path references in `README.md`, `CHANGELOG.md`, `skills/ads-update/SKILL.md`, and `scripts/run_update.py` accordingly.

These were structural bugs in v2.0.0 that would have made `/ads update` fail for any user installing via the install scripts. Pure filesystem-layout fix; no behavior changes.

## [2.0.0] - 2026-04-28

This release is a community fork. Maintained by [tododeia.com](https://tododeia.com).

### Added

- **`/ads update <platform|all>`** — new self-refreshing knowledge layer. Pulls the last 30 days of platform changes (features, deprecations, policy updates) for any of: `meta`, `google`, `tiktok`, `linkedin`, `microsoft`, `apple`, `youtube`, or `all`. Sources include Reddit, Hacker News, official vendor changelogs, and the open web (via WebSearch fallback).
- New sub-skill `skills/ads-update/SKILL.md` with mandatory cost-confirmation gate before any fetch.
- Vendored time-bounded research pipeline at `scripts/lib/` (dates, signals, dedupe + `Story` dataclass) — adapted from [last30days-skill](https://github.com/mvanhorn/last30days-skill) (MIT, by Matt Van Horn). Full attribution at `scripts/lib/THIRD_PARTY_NOTICES.md`.
- Per-platform source configuration at `scripts/ads_sources.py` (7 platforms, 23 subreddits, 17 official changelog URLs).
- CLI helper `scripts/run_update.py` with `--dry-run` and `--prep` modes.
- Canonical credit-cost warning at `ads/references/update-cost-warning.md`, surfaced in README, `ads/SKILL.md`, and the new ads-update skill.
- README now leads with a "Cost & Credits" section explaining the per-platform vs `all` cost tradeoff and recommending Sonnet over Opus for `/ads update` runs.

### Changed

- Forked from upstream `claude-ads` v1.5.1 (MIT). Skill name and command prefix preserved (`/ads`) so existing muscle memory and docs still work.
- Replaced upstream branding (community footer, author links, banner image) with a minimal "Maintained by tododeia.com" footer at the end of `ads/SKILL.md`.
- README hero is text-only (no banner asset shipped in v2.0.0).
- Repository moved to https://github.com/Hainrixz/claude-ads.

### Removed

- Per-deliverable upstream community footer block from `ads/SKILL.md` (~35 lines).
- "Author" section and "Related Projects" link from README.
- Branded URL references in install scripts, scripts/, .github templates, support docs.

### Notes

- `LICENSE` preserved verbatim (MIT §2 requires the original copyright line to remain in all copies). The original copyright on the upstream codebase remains attributed to the original author.
- No changes to existing `/ads audit`, `/ads google`, `/ads meta`, or any other v1.x command — backward compatible aside from the new `/ads update` addition.

## [1.5.1] - 2026-04-14

### Security

- Added shared SSRF validation module (`scripts/url_utils.py`) used by all URL-handling scripts
- Blocked IPv4 private ranges (127/8, 10/8, 172.16/12, 192.168/16, 169.254/16, 0/8, 100.64/10) and IPv6 (::1, fc00::/7, fe80::/10, ::ffff:0:0/96)
- DNS resolution failures now reject the URL instead of silently passing through
- Added `_sanitize_error()` to strip API keys, tokens, and passwords from error messages
- Added reference image extension allowlist to prevent arbitrary file reads
- Added batch size limit (50 jobs max) and dimension bounds (8192px max)
- Validated Replicate API response URLs are HTTPS before fetching
- Truncated Stability API error responses to prevent info leakage

### Changed

- GitHub Actions pinned to full SHA hashes instead of mutable version tags
- Dependabot auto-merge restricted to patch updates only (was all versions)
- CI workflow scoped to `permissions: contents: read` (least privilege)
- `pip-audit` added to CI for dependency vulnerability scanning
- `install.sh` tries standard pip first, falls back to `--break-system-packages` with warning
- `install.sh` trap variable quoting fixed for safer cleanup
- `.gitignore` now excludes `*.pem`, `*.key`, `*.p12`, `*.pfx`, `credentials.json`, `service-account.json`

## [1.4.0] - 2026-04-01

### Added
- **banana-claude integration**: Replaced generate_image.py with banana-claude (v1.4.1) as the default image generation provider. Uses MCP tools (`gemini_generate_image`, `set_aspect_ratio`), 5-component prompt formula, 9 domain modes, and brand presets.
- **Voice-to-style mapping** (`voice-to-style.md`): Maps 6 brand voice axes to visual attributes for banana's [STYLE] prompt component. Used by creative-strategist and visual-designer agents.
- **Ad copy frameworks** (`copy-frameworks.md`): 6 proven frameworks (AIDA, PAS, BAB, 4P, FAB, Star-Story-Solution) with platform-specific templates, character counts, and e-commerce/SaaS examples.
- **E-commerce creative playbook** (`ecommerce-creative.md`): 5 campaign types (Product Launch, Sale/Promotion, Seasonal, Retargeting, Brand Awareness) with banana domain modes, aspect ratios, copy frameworks, and budget allocation.
- **Visual consistency anchoring**: visual-designer generates a "hero" image first and passes it as a style reference to all subsequent campaign assets.
- **3-variant A/B strategy**: visual-designer now generates 3 variants per brief (base, alternative angle, lighting/mood variation) instead of 2.
- **Copy zone validation**: format-adapter uses Claude vision to check if generated images have clear space in platform-specific copy zones.
- **Framework-driven copy**: copy-writer applies selected framework structure and generates 2 variants per platform (primary + A/B alternative).
- **Multi-screenshot brand DNA**: ads-dna captures 3 screenshots (homepage, product page, about page) for richer brand anchoring.
- **Brand preset auto-creation**: ads-generate creates a banana preset from brand-profile.json before generation.
- **Campaign cost tracking**: reads banana's `~/.banana/costs.json` and aggregates per-campaign creative spend.
- **Quality gate**: ads-generate scores each image 1-10 via Claude vision; auto-regenerates if score below 6.

### Changed
- **ads-generate**: banana MCP is primary; generate_image.py is deprecated fallback
- **ads-photoshoot**: Uses banana Product mode (Studio, Floating, Ingredient) and Editorial mode (In Use, Lifestyle) at 2K resolution
- **visual-designer agent**: 5-component banana formula replaces 7 preprocessing rules
- **creative-strategist agent**: Reads voice-to-style.md, copy-frameworks.md, and ecommerce-creative.md; generates 2 visual direction variants per concept (photography + illustration)
- **copy-writer agent**: Framework-based copy with hook word validation and action verb CTAs
- **format-adapter agent**: Added copy zone validation and cost tracking
- **requirements.txt**: google-genai moved to optional (banana handles image generation)
- **install.sh / install.ps1**: Removed Playwright chromium install; added banana-claude dependency check
- Reference file count: 21 to 23 (added voice-to-style.md, copy-frameworks.md)

### Deprecated
- `scripts/generate_image.py`: Kept as fallback for environments without banana-claude. Use banana MCP tools instead.

## [1.3.0] - 2026-04-01

### Added
- **marketplace.json** for plugin system discoverability and update mechanism (Issue #14)
- **Validation gates** in 6 skills; cherry-picked from PR #12 (Tessl):
  - `ads/SKILL.md`: Task tool orchestration clarity + subagent JSON score verification
  - `ads-audit`: Platform data availability check + subagent score field verification
  - `ads-budget`: 14-day minimum for kill/scale decisions + 20-click/$100 data sufficiency
  - `ads-creative`: Data existence check + assumption prevention gate
  - `ads-google`: 30-day data minimum + 74-check completeness verification
  - `ads-youtube`: Active campaign check + campaign type completeness gate
- **GAQL compatibility reference** (`gaql-notes.md`): known field incompatibilities, deduplication patterns, filter scope best practices, legacy BMM detection heuristic
- **Google Ads MCP integration** in ads-google: optional automated data collection via [google-ads-mcp](https://github.com/googleads/google-ads-mcp) with fallback to manual export
- **Shared negative keyword list support** (G14/G15): campaigns covered by shared lists no longer flagged as "missing negatives"
- **Keyword-level brand detection** (G05/G07/G-PM3): derives brand tokens from account name, classifies by keyword composition instead of campaign naming conventions
- **G-SYS1 diagnostic**: guidance for reporting API fetch failures instead of silently skipping checks
- **`dependencies` label** created for Dependabot PR automation

### Fixed
- **G03**: False positives from zero-impression keywords, paused ad groups, match type duplication, and stopword-only keywords diluting coherence scores (~18% false positive reduction)
- **G04**: False positives from multi-location campaign structures; now strips geographic identifiers before counting objectives
- **G12**: Inverted Search Partners logic; flag OFF as missed opportunity (was incorrectly flagging ON)
- **G16/G-WS1**: Wasted spend threshold raised to >$10 spend + 0 conversions (was flagging all non-converting terms including long-tail exploration)
- **G17/FL04**: Legacy BMM false positives; BROAD + Manual CPC is legacy BMM (not intentional broad). Only flags BROAD in Smart Bidding campaigns
- **G19**: Search term visibility calculated from ALL fetched terms before truncation (was computing from truncated subset)
- **G48/CT-FL5**: False flags on Smart Campaign system-managed conversions excluded from DDA and counting-type checks
- **G-CT1**: False duplicate detection on HIDDEN/REMOVED conversion actions; now only checks ENABLED actions
- **Conversion tracking**: Added duplicate detection accuracy rules (exclude HIDDEN/REMOVED, exclude Smart Campaign system conversions)

### Changed
- Dependabot: actions/checkout v4 → v6, actions/setup-python v5 → v6, Pillow `<12.0.0` → `<13.0.0`
- Version aligned to 1.3.0 (plugin.json was incorrectly at 2.0.0)
- Reference file count: 20 → 21 (added gaql-notes.md)

### Community
- Closed PRs #4, #5, #13 (out of scope: white-label rebrand, campaign system, FastAPI web app)
- Cherry-picked validation improvements from PR #12 (Tessl); 6 of 18 files
- Replied to Discussion #11 ("Does this really work?")
- Closed Issue #14 (marketplace.json shipped)
- GAQL accuracy fixes sourced from akarls-web fork (44 commits of audit engine improvements)
- MCP integration sourced from double-agency fork

## [1.2.0] - 2026-03-12

### Added
- **Apple Search Ads sub-skill** (`/ads apple`): 35 checks across campaign structure (BOFU/MOFU/Search Match), bid health (CPT vs install rate, CPA Goals), Creative Sets (Custom Product Pages), MMP attribution (AppsFlyer/Adjust/SKAdNetwork), budget pacing, TAP placement coverage (Today/Search/Product Pages), and goal CPA benchmarks by app category and country tier
- **Context Intake** step in orchestrator: Claude now asks for industry, monthly ad spend, primary goal, and active platforms before any audit; ensures benchmarks and recommendations match the user's actual situation instead of defaulting to generic industry averages
- **Google Ads MCP reference** in README: links to [google-ads-mcp](https://github.com/googleads/google-ads-mcp) for users who want live API-connected audits
- **FAQ section** in README: addresses top community questions (API login, benchmark accuracy, manual ad posting, budget context, platform support)
- **"How It Analyzes Your Ads"** section in README: clearly explains manual data input model and data export workflow

### Fixed
- `install.ps1`: PowerShell 5.1 crash on git clone: git progress writes to stderr which PS 5.1 treated as a terminating error under `$ErrorActionPreference = "Stop"`. Fixed by temporarily setting `Continue` around clone call and using `2>&1 | Out-Null`
- `uninstall.ps1`: Parse failure on non-UTF-8-BOM systems; Unicode `→` and `✓` characters in double-quoted strings caused `TerminatorExpectedAtEndOfString`. Replaced with ASCII equivalents
- `ads-google/SKILL.md`: Negative keyword guidance now enforces Exact Match `[kw]` and Phrase Match `"kw"` types by default; never Broad Match negatives. Negatives must be sourced from Search Terms Report data and grouped into themed Shared Lists. Includes over-blocking review step
- `ads/SKILL.md`: Removed unsupported `allowed-tools` frontmatter field per Anthropic skill spec
- `ads/SKILL.md`: Added `apple` to `argument-hint` subcommand list
- Install scripts: Updated sub-skill count from 12 → 13 to reflect new ads-apple addition

## [1.1.1] - 2026-02-11

### Fixed
- M-CR2 vs M37 frequency threshold ambiguity: clarified M-CR2 is ad set level (<3.0) and M37 is campaign level (<4.0)
- Ecommerce template PMax image count aligned to G31 audit check (15 → 20 images per asset group)
- Real estate template budget percentages widened to bracket 100% (was 90-105%, now 80-110%)
- Info products template TikTok allocation note: added minimum $50/day campaign budget caveat
- Duplicate step numbering in ads-tiktok (two step 7s) and ads-creative (two step 6s)

### Added
- `argument-hint` field on orchestrator skill for CLI subcommand hints

## [1.1.0] - 2026-02-11

### Fixed
- Audit check count corrected from 186 to 190 (actual total: Google 74 + Meta 46 + LinkedIn 25 + TikTok 25 + Microsoft 20)
- TikTok budget sufficiency threshold aligned to authoritative checklist (Pass ≥50x CPA, Warning 20-49x, Fail <20x)
- Benchmarks typo: Local Services CPC `$7.85-$15-$30` → `$7.85-$15.00`
- Call Campaigns context note: clarified creation vs serving deadlines (Feb 2026 / Feb 2027)
- Flexible Ads context note: corrected launch date from 2025 to 2024
- Scoring system weighting rationale: corrected "20-25%" to "25-30%" to match actual platform weights
- G59 mobile speed: LCP now measured on mobile viewport (375x812) instead of desktop
- G61 schema check: validates Product/FAQ/Service types per audit reference (not any schema)
- Removed unused beautifulsoup4 and lxml from requirements.txt

### Added
- `uninstall.ps1` for Windows parity (Unix already had `uninstall.sh`)
- `.gitattributes` to fix GitHub language detection (Markdown, not PowerShell)
- Research context notes in google-audit.md (ECPC deprecation, Call Campaigns sunset, Power Pack, AI Max)
- Research context notes in meta-audit.md (detailed targeting removal, Flexible Ads, Financial Products SAC)
- Research context notes in linkedin-audit.md (Connected TV, BrandLink, Live Event Ads, Accelerate campaigns)
- Weighting rationale section in scoring-system.md explaining grading band design
- Scoring system reference added to ads-tiktok and ads-creative process steps
- Missing `.gitignore` patterns for creative, landing, budget, and competitor reports

### Changed
- Removed non-spec `color` field from all 6 agent frontmatter files
- Agent frontmatter now uses only official Claude Code spec fields (name, description, model, maxTurns, tools)

## [1.0.0] - 2026-02-11

### Added
- Main orchestrator skill (`/ads`) with industry detection and quality gates
- 12 sub-skills: audit, google, meta, youtube, linkedin, tiktok, microsoft, creative, landing, budget, plan, competitor
- 6 parallel audit agents: audit-google, audit-meta, audit-creative, audit-tracking, audit-budget, audit-compliance
- 12 reference files with 2026 benchmarks, bidding decision trees, platform specs, compliance requirements
- 11 industry templates: saas, ecommerce, local-service, b2b-enterprise, info-products, mobile-app, real-estate, healthcare, finance, agency, generic
- 190 audit checks across all platforms (Google 74, Meta 46, LinkedIn 25, TikTok 25, Microsoft 20)
- Ads Health Score (0-100) with weighted severity scoring
- install.sh and uninstall.sh for Unix/macOS/Linux
- install.ps1 for Windows PowerShell
- Agent frontmatter uses model sonnet, maxTurns 20, with example blocks
- Sub-skills set user-invocable false to avoid menu clutter
- Reference files follow RAG pattern (loaded on-demand per analysis)
- Quality gates: Broad Match safety, 3x Kill Rule, budget sufficiency, learning phase protection
