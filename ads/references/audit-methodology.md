# Audit Methodology — Shared Process Across Platforms

> Every platform-specific audit (ads-google, ads-meta, ads-tiktok) follows the
> same skeleton. This file is the source of truth for that skeleton. Platform
> SKILL.md files declare only what is *different* — data collection method,
> check list, unique thresholds, output sections.

## The 7-Step Audit Process

1. **Collect data.** Platform-specific. Prefer the MCP-first pattern when available (see `mcp-integration.md`); fall back to exports/screenshots/manual input otherwise. Record the actual source in the JSON output's `data_source` field (`"mcp" | "export" | "screenshot" | "manual" | "mixed"`).
2. **Read the platform audit checklist** (`<platform>-audit.md` in this directory).
3. **Read the benchmarks** (`benchmarks.md`). If the platform supports live MCP benchmarks (e.g. Meta `ads_insights_industry_benchmark`), prefer those for the current vertical and record `evidence.benchmark_source` accordingly.
4. **Evaluate every applicable check** as `PASS`, `WARNING`, `FAIL`, or `N/A`. Use `N/A` only when the relevant data was not obtainable (not as a way to hide failures).
5. **Calculate category scores** using the per-platform weights documented in `scoring-system.md`. Severity multipliers and WARNING-half-credit rules are also defined there.
6. **Identify Quick Wins.** Any check with severity `critical` or `high` AND `fix_time_minutes ≤ 15` qualifies. Sort by impact.
7. **Emit dual output** — both required:
   - `<platform>-audit-results.json` validating against `audit-output-schema.json` (machine-readable; consumed by the `/ads audit` orchestrator).
   - `<platform>-audit-results.md` human-readable, with health score, category breakdown, per-check table, Quick Wins, and platform-specific deliverables.

The orchestrator (`ads/SKILL.md`) parses the JSON files in step 5 of its own pipeline. If a JSON is missing or fails schema validation, aggregation halts — do not silently combine partial markdown.

## Check ID Convention

All check identifiers are stable strings that encode the platform/family in the first letter(s):

| Prefix | Domain |
|--------|--------|
| `G` | Google Ads (includes YouTube video campaigns) |
| `M` | Meta Ads |
| `T` | TikTok Ads |
| `X` | Cross-platform |

Two formats are valid:

- **Sequential** (`G01`, `M14`, `T05`) — original v1.0 numbering.
- **Hyphenated** (`G-AI1`, `M-AN1`, `X-PI1`) — categorical additions where the suffix encodes a sub-theme.

Both match the JSON-schema regex `^[A-Z]+(-[A-Z]+)?-?[A-Z0-9]+$`.

## Scoring

See `scoring-system.md` for:

- The full weighted scoring formula.
- Severity multipliers (`critical: 5.0`, `high: 3.0`, `medium: 1.5`, `low: 0.5`).
- Result point values (`PASS: full`, `WARNING: 50%`, `FAIL: 0`, `N/A: excluded`).
- Per-platform category weights.
- Grading thresholds (A 90+, B 75+, C 60+, D 40+, F <40).
- Cross-platform aggregation by budget share.

Platform SKILL.md files MUST NOT redefine these formulas. They MAY restate weight percentages alongside category names for readability — but those are presentation duplicates, not the source of truth.

## MCP-First Rule

If the platform has a documented MCP integration (currently Meta via the
`mcp__claude_ai_Facebook__*` server; see `mcp-integration.md`), the audit agent
must check for an `<platform>_account_id` first and use MCP tools when present.
This is not optional — it is the canonical pattern that future platform
integrations (Pinterest, Reddit, X, etc.) will inherit.

The agent's frontmatter must list each `mcp__server__tool` it intends to call.
Adding a new MCP tool requires editing the agent file, not run-time discovery.

## Output Schema

Reference: `audit-output-schema.json`. Required fields: `platform`, `version`, `health_score`, `grade`, `category_scores`, `checks`. Recommended fields: `data_source`, `account_id`, `quick_wins`, `critical_issues`, `evidence` (per-check structured evidence including MCP responses).

When a check is `N/A`, include it in the `checks` array with a `finding` explaining *why* it could not be evaluated. This preserves audit completeness and helps diagnose data-collection gaps.
