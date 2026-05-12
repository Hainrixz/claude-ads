# MCP Integration Guide

> **Purpose:** how to pair claude-ads with live ad-platform MCP servers, and the canonical pattern any new integration must follow.

## Overview

claude-ads works with manually provided data by default (exports, screenshots, pasted metrics). For live API access, pair it with MCP servers that connect Claude Code directly to ad platform APIs.

## Canonical MCP Pattern (for new integrations)

Every audit that supports an MCP must follow the same three-layer pattern. **When adding a new platform (Pinterest, Reddit, X, etc.) duplicate this pattern verbatim** — don't invent a new one.

1. **Detection** — the sub-skill's `Process` step 1 declares: *"if user supplies `<platform>_account_id`, use MCP; otherwise fall back to exports/screenshots"*. Never require MCP — always degrade gracefully.
2. **Tool whitelist** — the corresponding `agents/audit-<platform>.md` frontmatter lists the exact `mcp__<server>__<tool>` names in its `tools:` field. Adding tools requires editing the agent, not run-time discovery.
3. **Output contract** — the audit emits `<platform>-audit-results.json` against `ads/references/audit-output-schema.json` with `data_source` set to `"mcp"` (or `"export"` / `"mixed"`). See `mcp-meta-integration.md` for a worked example.

Each platform that has an MCP gets its own `mcp-<platform>-integration.md` file mapping individual checks (Gxx, Mxx, etc.) to specific MCP tools. That file is the source of truth for the audit agent's behavior.

## Available MCP Servers

### Google Ads: cohnen/mcp-google-ads

**Repo:** https://github.com/cohnen/mcp-google-ads
**Stars:** ~395 | **Tools:** 29 GAQL-based tools

**Setup:**
1. Install: `pip install mcp-google-ads` (or clone repo)
2. Configure Google Ads API credentials (OAuth2 or service account)
3. Add to `.mcp.json`:
```json
{
  "mcpServers": {
    "google-ads": {
      "command": "python",
      "args": ["-m", "mcp_google_ads"],
      "env": {
        "GOOGLE_ADS_DEVELOPER_TOKEN": "your-token",
        "GOOGLE_ADS_CLIENT_ID": "your-client-id",
        "GOOGLE_ADS_CLIENT_SECRET": "your-client-secret",
        "GOOGLE_ADS_REFRESH_TOKEN": "your-refresh-token",
        "GOOGLE_ADS_LOGIN_CUSTOMER_ID": "your-mcc-id"
      }
    }
  }
}
```

**What becomes automated:**
- Search term data for G13, G16, G17, G18, G19 (wasted spend checks)
- Quality Score data for G20-G25
- Campaign structure for G01-G12
- Conversion tracking status for G42-G49
- PMax asset group data for G31-G34, G-PM1 through G-PM6
- Budget and bidding data for G36-G41

**What stays manual:**
- Landing page analysis (G59-G61): use `analyze_landing.py`
- Creative quality assessment (subjective)
- Consent Mode V2 verification (requires GTM/tag audit)

### Meta Ads: claude.ai Facebook MCP (**canonical — wire this first**)

The official **claude.ai Facebook** MCP server is the recommended Meta integration. It exposes `mcp__claude_ai_Facebook__*` tools directly inside Claude Code with no extra setup beyond connecting your Meta Business account from claude.ai's MCP catalog.

**Setup:** in claude.ai → MCP servers → connect "Facebook". The tools become available automatically.

**Tools used by claude-ads** (full mapping in `mcp-meta-integration.md`):

| Tool | Covers checks |
|------|---------------|
| `mcp__claude_ai_Facebook__ads_get_dataset_quality` | M02 (CAPI), M03 (dedup), M04 (EMQ) |
| `mcp__claude_ai_Facebook__ads_get_ad_entities` | M11-M18 (structure), M19 (overlap), M13 (learning phase) |
| `mcp__claude_ai_Facebook__ads_catalog_get_diagnostics` | M15 (Advantage+ Shopping), M-CR* (catalog) |
| `mcp__claude_ai_Facebook__ads_insights_performance_trend` | M28 (creative fatigue), M25 (creative diversity over time) |
| `mcp__claude_ai_Facebook__ads_insights_industry_benchmark` | Live benchmarks (overrides static `benchmarks.md` when available) |
| `mcp__claude_ai_Facebook__ads_get_ad_account_pages` | Page-level diagnostics |
| `mcp__claude_ai_Facebook__ads_get_opportunity_score` | Meta's own "opportunity score" — cross-reference with our health score |

**What stays manual:** subjective creative quality, organic Threads activity, off-platform attribution.

### Meta Ads: alternative — Adspirer MCP

**Docs:** https://www.adspirer.com/blog/connect-claude-meta-ads
**Type:** Commercial MCP server. Use only if you cannot connect the claude.ai Facebook MCP (e.g., need write access or features the official MCP does not expose).

### Meta Ads: alternative — direct Marketing API

Roll your own integration with the Meta Marketing API. Free, self-hosted, but requires significant setup. Only worth it for advanced cases the official MCP does not cover.

### TikTok Ads

**Community MCP:** [`AdsMCP/tiktok-ads-mcp-server`](https://github.com/AdsMCP/tiktok-ads-mcp-server) provides campaign / adgroup / ad / report data access (free, open-source).

**Free fallback:** `scripts/api/tiktok_fetch.py` (Capa 2 — direct API adapter, pure stdlib).

## Hybrid Workflow

The recommended approach combines MCP live data with claude-ads' direct-API
adapters and manual exports — the 3-tier free-first strategy:

```
1. Capa 1 — Connect MCP server(s) for available platforms (Meta, Google, TikTok)
2. Capa 2 — Or run scripts/api/<platform>_fetch.py to produce <platform>-data.json
3. Capa 3 — Or paste exports manually
4. Run /ads audit (claude-ads auto-detects whatever data source is present)
5. Health Score calculated across all 3 platforms regardless of data source
```

## Security Notes

- MCP servers run locally; no data leaves your machine (except API calls to ad platforms)
- Credentials stored in `.mcp.json` or environment variables
- Read-only access recommended for audit purposes
- For write operations (campaign changes), see the CEP safety protocol discussion in the itallstartedwithaidea/google-ads-skills repo
