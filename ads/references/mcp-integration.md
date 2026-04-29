# MCP Integration Guide

<!-- Created: 2026-04-13 | v1.5 -->
<!-- Purpose: How to pair claude-ads with live ad platform MCP servers -->

## Overview

claude-ads works with manually provided data by default (exports, screenshots, pasted metrics). For live API access, pair it with MCP servers that connect Claude Code directly to ad platform APIs.

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

### Meta Ads: Adspirer MCP

**Docs:** https://www.adspirer.com/blog/connect-claude-meta-ads
**Type:** Commercial MCP server

**Setup:**
1. Sign up at adspirer.com
2. Connect Meta Business Manager account
3. Add MCP server config per their docs

**What becomes automated:**
- Campaign performance data for M11-M18 (structure)
- Creative metrics for M25-M32 (fatigue detection)
- Audience overlap for M19 (overlap check)
- EMQ scores for M04 (requires Events Manager access)

**Alternative: Direct Meta API:**
Use the included `scripts/fetch_meta_ads.py` with Meta Marketing API credentials for a free, self-hosted option.

### LinkedIn Ads: Multiple Options

**GrowthSpree MCP:** https://www.growthspreeofficial.com/blogs/connect-linkedin-ads-to-claude-mcp
**Adzviser MCP:** https://adzviser.com/mcp/linkedin-ads

Both provide campaign data access for LinkedIn Ads analysis. Setup follows standard MCP patterns.

### TikTok Ads

No dedicated MCP server available as of April 2026. Use:
- TikTok Ads Manager exports (CSV)
- TikTok Business API (custom integration via scripts)

### Microsoft Ads

No dedicated MCP server available as of April 2026. Use:
- Microsoft Ads Editor exports
- Google Ads import data (if mirrored)
- Microsoft Advertising API (custom integration)

### Apple Ads

No dedicated MCP server available as of April 2026. Use:
- Apple Ads dashboard exports
- Apple Ads API (custom integration)

## Hybrid Workflow

The recommended approach combines MCP live data with claude-ads structured analysis:

```
1. Connect MCP server(s) for available platforms
2. Run /ads audit (claude-ads auto-detects MCP data sources)
3. For platforms without MCP, provide exports manually
4. claude-ads merges all data into unified audit
5. Health Score calculated across all platforms regardless of data source
```

## Security Notes

- MCP servers run locally; no data leaves your machine (except API calls to ad platforms)
- Credentials stored in `.mcp.json` or environment variables
- Read-only access recommended for audit purposes
- For write operations (campaign changes), see the CEP safety protocol discussion in the itallstartedwithaidea/google-ads-skills repo
