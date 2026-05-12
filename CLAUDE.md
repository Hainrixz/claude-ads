# Claude Ads: Free-first Paid Advertising Audit & Optimization Skill

## Project Overview

This repository contains **Claude Ads**, a Tier 4 Claude Code skill focused on the
3 base advertising platforms where 95% of ad spend lives: **Meta, Google, TikTok**.
It follows the Agent Skills open standard and the 3-layer architecture (directive,
orchestration, execution). After the v2.3.0 scope refocus, the skill has 17 sub-skills,
7 agents (3 audit + 4 creative), 8 industry templates, and ~158 weighted audit checks
+ 3 cross-platform checks.

## Architecture

```
claude-ads/
  CLAUDE.md                          # Project instructions (this file)
  ads/                               # Main orchestrator skill
    SKILL.md                         # Entry point, routing table, core rules
    references/                      # On-demand knowledge files
  skills/                            # 17 specialized sub-skills (v2.3.0)
    ads-audit/SKILL.md              # Full multi-platform audit
    ads-google/SKILL.md            # Google Ads deep analysis (includes YouTube)
    ads-meta/SKILL.md              # Meta/Facebook Ads analysis — MCP-wired
    ads-tiktok/SKILL.md           # TikTok Ads analysis
    ads-creative/SKILL.md         # Cross-platform creative quality
    ads-landing/SKILL.md          # Landing page analysis
    ads-budget/SKILL.md           # Budget allocation optimization
    ads-plan/SKILL.md             # Strategic ad planning by industry
    ads-competitor/SKILL.md       # Competitor ad research
    ads-dna/SKILL.md              # Brand DNA extraction
    ads-create/SKILL.md           # Campaign briefs / copy decks
    ads-generate/SKILL.md         # AI image generation
    ads-photoshoot/SKILL.md       # Product photography (5 styles)
    ads-math/SKILL.md             # PPC calculator
    ads-test/SKILL.md             # A/B test design
    ads-update/SKILL.md           # Self-refresh platform references
    ads-publish/SKILL.md          # Zernio publishing (first 2 accounts free)
  agents/                            # 7 agents (3 audit + 4 creative)
    audit-google.md                # Google Ads audit (80 checks, includes YouTube)
    audit-meta.md                  # Meta Ads audit (50 checks, MCP-wired)
    audit-tiktok.md                # TikTok Ads audit (28 checks, NEW in v2.3.0)
    creative-strategist.md         # Campaign concept agent
    visual-designer.md             # Image generation agent
    copy-writer.md                 # Copy generation agent
    format-adapter.md              # Asset dimension validation
  scripts/api/                       # Capa-2 direct-API adapters (NEW in v2.3.0)
    meta_fetch.py · google_fetch.py · tiktok_fetch.py · README.md
  install.sh / install.ps1          # Cross-platform installers
  uninstall.sh / uninstall.ps1      # Cross-platform uninstallers
```

## Commands

| Command | Purpose |
|---------|---------|
| `/ads audit` | Full multi-platform audit with 3 parallel agents (Meta, Google, TikTok) |
| `/ads google` | Google Ads deep analysis (includes YouTube video campaigns) |
| `/ads meta` | Meta/Facebook Ads analysis (MCP-wired to claude.ai Facebook) |
| `/ads tiktok` | TikTok Ads analysis (Smart+, Shop, Symphony, GMV Max) |
| `/ads creative` | Creative quality and fatigue assessment |
| `/ads landing` | Landing page conversion analysis |
| `/ads budget` | Budget allocation optimization |
| `/ads plan <type>` | Strategic ad planning by industry |
| `/ads competitor` | Competitor ad research |
| `/ads math` | PPC financial calculator (CPA, ROAS, break-even, LTV:CAC) |
| `/ads test` | A/B test design (hypothesis, significance, sample size) |
| `/ads report` | PDF audit report generation for client deliverables |
| `/ads update <plat\|all>` | Refresh per-platform references with last 30 days of changes |
| `/ads publish` | Publish generated creatives to 14+ social networks via Zernio (first 2 accounts free) |

## Removed in v2.3.0

The fork upstream covered 7 platforms; v2.3.0 refocuses on the 3 base. **Removed:**

- `ads-apple/` — no MCP exists for Apple Ads; partner-API setup high-friction.
- `ads-linkedin/` — LinkedIn Marketing Developer Platform partner approval is a barrier; paid MCPs only.
- `ads-microsoft/` — lower advertiser usage; effort not justified.
- `ads-youtube/` — YouTube video campaigns live inside Google Ads; covered via `/ads google` and `audit-google` checks G-DG*, G-CTV*.

Also removed: cross-platform audit agents (`audit-creative`, `audit-tracking`, `audit-budget`, `audit-compliance`) — merged into `audit-tiktok.md`. Industry templates `saas`, `b2b-enterprise`, `info-products`, `mobile-app` deleted (depended on removed platforms).

## Development Rules

- Keep SKILL.md files under 500 lines / 5000 tokens
- Reference files should be focused and under 200 lines (enforced by `tests/test_references.py`)
- Scripts must have docstrings, CLI interface, and JSON output
- Follow kebab-case naming for all skill directories
- Agents invoked via Task tool with `context: fork`, never via Bash
- No hardcoded credentials; use MCP servers for external API access
- Every `audit-*` agent must emit **both** `<platform>-audit-results.md` (human-readable) and `<platform>-audit-results.json` (validates against `ads/references/audit-output-schema.json`). The orchestrator parses the JSON to aggregate scores; markdown is for human consumption only.
- Platform sub-skills (`ads-google`, `ads-meta`, `ads-tiktok`) declare only their platform-specific data-collection step, then delegate the 7-step audit process to `ads/references/audit-methodology.md`. Do not restate the generic process.
- Sub-skill frontmatter is canonically: `name` (matches directory), `description`, `user-invokable: false`. Skills with command arguments add `argument-hint`. Skills that need extra permissions add `allowed-tools`.
- New MCP integrations follow the **canonical pattern** documented in `ads/references/mcp-integration.md` and templated in `ads/references/mcp-meta-integration.md`: tools declared in the agent's `tools:` frontmatter, a `mcp-<platform>-integration.md` mapping checks↔tools, SKILL.md step 1 is MCP-first with manual fallback.
- Every platform audit must offer **three free-first data tiers** in this order:
  1. **Capa 1 — MCP** (server-based, recommended when one exists).
  2. **Capa 2 — Direct API** (script in `scripts/api/<platform>_fetch.py`, free, OAuth setup once).
  3. **Capa 3 — Manual exports** (always works, no setup).
  All adapters in `scripts/api/` are pure-stdlib (Python 3.10+, no external dependencies). See `scripts/api/README.md` for per-platform OAuth setup.
- Paid integrations (Adspirer for Meta MCP; Zernio for `/ads publish`) are documented as **optional Tier 3**. Never make a paid SaaS a required dependency.

## Quality Gates

Before merging a change that touches skills, agents, references, or scripts, run:

```bash
pytest tests/                                              # all must pass
find ads/references -name "*.md" -exec wc -l {} \; | awk '$1 > 200'   # must be empty
python3 -c "import json; json.load(open('ads/references/audit-output-schema.json'))"
bash -n install.sh && bash -n uninstall.sh
```

CI runs all of the above on every push and PR (`.github/workflows/ci.yml`).

## Releases

Cut releases via `git tag vX.Y.Z` and `gh release create vX.Y.Z`. Update `CHANGELOG.md` first. Bump version in `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `CITATION.cff`, and the README version badges (both EN and ES). Install scripts compute the asset counts dynamically — no manual bump needed there.
