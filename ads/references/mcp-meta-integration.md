# Meta MCP Integration — Check ↔ Tool Mapping

> **Source of truth** for `agents/audit-meta.md`. When an `ad_account_id` is supplied,
> the agent calls the MCP tools listed below instead of asking for exports.
> This file is also the **canonical template** for any future MCP integration
> (Pinterest, Reddit, X, …): duplicate its structure, swap the tool names.

## Activation

The Meta MCP path activates when **all** of these are true:

1. `mcp__claude_ai_Facebook__*` tools are listed in the agent's `tools:` frontmatter.
2. The user (or upstream `/ads audit`) supplies a Meta `ad_account_id` (format `act_<numeric>`).
3. A date range is specified or defaults to the last 28 days.

If any condition fails, fall back to manual exports and set `"data_source": "export"` in the JSON output.

## Check → MCP Tool Mapping

### Pixel / CAPI Health (30% weight)

| Check | MCP Tool | What to extract |
|-------|----------|-----------------|
| M01 — Pixel installed and firing | `ads_get_dataset_details` | `is_created_by_business`, last event timestamp |
| M02 — CAPI active | `ads_get_dataset_quality` | `capi_status`, % of events with `server` source |
| M03 — Event dedup ≥90% | `ads_get_dataset_quality` | `deduplication_rate` per event |
| M04 — EMQ ≥8.0 for Purchase | `ads_get_dataset_quality` | `event_match_quality` per event |
| M05 — All standard events configured | `ads_get_dataset_stats` | event coverage list |
| M-AT1 — Offline Conversions API not in use | `ads_get_dataset_details` | flag if any offline-only dataset present |

### Creative — Diversity & Fatigue (30% weight)

| Check | MCP Tool | What to extract |
|-------|----------|-----------------|
| M25 — ≥3 creative formats active | `ads_get_ad_entities` | distinct `creative.object_type` count per ad set |
| M26 — ≥5 creatives per ad set | `ads_get_ad_entities` | ad count per ad set |
| M28 — Creative fatigue (CTR drop >20% / 14d) | `ads_insights_performance_trend` | 14-day CTR slope per ad |
| M-AN1 — Andromeda diversity (≥10 distinct concepts) | `ads_get_ad_entities` + manual concept tagging | total ads, then similarity inspection |

### Account Structure (20% weight)

| Check | MCP Tool | What to extract |
|-------|----------|-----------------|
| M11 — CBO vs ABO intentional | `ads_get_ad_entities` | `bid_strategy`, `budget_remaining` at campaign vs ad set |
| M13 — Learning phase health (<30% Limited) | `ads_get_ad_entities` | `learning_stage` per ad set |
| M14 — Budget per ad set ≥5x target CPA | `ads_get_ad_entities` + user-supplied CPA target | daily_budget / target_cpa |
| M15 — Advantage+ Sales active for e-commerce | `ads_catalog_get_catalogs` + `ads_get_ad_entities` | catalog connected + ASC enabled |
| M19 — Ad set overlap <30% | `ads_get_ad_entities` (audience definitions) | Jaccard-like overlap on audience specs |

### Audience & Targeting (20% weight)

| Check | MCP Tool | What to extract |
|-------|----------|-----------------|
| M21 — Prospecting frequency 7d <3.0 | `ads_insights_performance_trend` | `frequency` filtered to prospecting ad sets |
| M22 — Advantage+ Audience tested | `ads_get_ad_entities` | `targeting.targeting_automation` enabled |
| M-TH1 — Threads placement enabled | `ads_get_ad_entities` | `placements` contains `threads` |

### Advantage+ Shopping & Catalog

| Check | MCP Tool | What to extract |
|-------|----------|-----------------|
| M32 — Advantage+ Creative enhancements | `ads_get_ad_entities` | `degrees_of_freedom_spec` populated |
| M33 — Advantage+ Placements | `ads_get_ad_entities` | `targeting.publisher_platforms` = all |
| Catalog feed quality | `ads_catalog_get_diagnostics` | error counts per catalog |
| Product feed rules | `ads_catalog_get_feed_rules` | rule count and validity |

### Live Benchmarks Override

When `ads_insights_industry_benchmark` returns data for the relevant industry vertical,
prefer its numbers over the static `benchmarks.md` thresholds for that audit run.
Record the source in the JSON output: `evidence: { "benchmark_source": "mcp_live" | "static" }`.

## Output Wiring

The agent must populate the JSON schema (`audit-output-schema.json`) with:

```json
{
  "platform": "meta",
  "data_source": "mcp",
  "account_id": "act_123456789",
  "evidence": {
    "mcp_tools_called": [
      "ads_get_dataset_quality",
      "ads_get_ad_entities",
      "ads_catalog_get_diagnostics"
    ],
    "date_range": { "since": "2026-04-14", "until": "2026-05-11" }
  }
}
```

Per-check evidence should include the relevant MCP response slice (truncated to ≤200 chars per check).

## Failure & Fallback Rules

1. **Auth error** (account not accessible): emit `data_source: "manual"`, ask user for export, mark unevaluable checks `"result": "N/A"`.
2. **Partial data** (some tools return empty): emit `data_source: "mixed"`. Checks that depended on the missing tool become `"N/A"` with `"finding": "MCP returned no data; provide manual export to evaluate"`.
3. **Rate limit / quota**: retry once with exponential backoff (the MCP server already retries internally). On second failure, fall back to manual.
4. **Stale data warning**: if `ads_get_dataset_quality` indicates >24 h since last event, surface a `WARNING` regardless of metric values.

## Pattern Reuse for New Platforms

When adding a Pinterest / Reddit / X integration:

1. Copy this file → `mcp-<platform>-integration.md`.
2. Replace tool prefix `mcp__claude_ai_Facebook__` with the new server's prefix.
3. Rebuild the "Check → MCP Tool" tables against the new platform's check IDs (`Pxx`, `Rxx`, `Xxx`).
4. Update the corresponding `audit-<platform>.md` agent: add tools to frontmatter, add a step "0. If `<platform>_account_id` provided, fetch via MCP".
5. Update `mcp-integration.md` to list the new server under "Available MCP Servers".
6. No other changes should be necessary — the orchestrator (`ads/SKILL.md`) and JSON contract are platform-agnostic.
