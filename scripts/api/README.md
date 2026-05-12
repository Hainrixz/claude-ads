# `scripts/api/` — Capa 2 (Direct API adapters)

This package is the **free, no-MCP-server-required** path for fetching
ad-account data into claude-ads. Each `<platform>_fetch.py` script reads
credentials from environment variables, calls the platform's official
Marketing API, and writes a JSON file the corresponding `audit-<platform>`
agent reads.

```
Capa 1 — MCP server          (recommended when one exists)
Capa 2 — these scripts       ◀── you are here
Capa 3 — manual exports      (always works)
```

All adapters are **pure stdlib** (Python 3.10+, no extra dependencies needed).

## Common shape

Every script accepts the same base CLI:

```
python3 scripts/api/<platform>_fetch.py \
    --account-id <ID>            # required, platform-specific format
    --since 2026-04-14           # default: 28 days ago, ISO date
    --until 2026-05-12           # default: today, ISO date
    --what all                   # or specific sections (see --help)
    --output <platform>-data.json   # default: stdout
```

The output JSON always starts with:

```json
{
  "platform": "<meta|google|tiktok>",
  "account_id": "...",
  "fetched_at": "2026-05-12T15:30:00Z",
  "data_source": "direct_api",
  "api_version": "...",
  "date_range": {"since": "...", "until": "..."},
  "errors": []
}
```

Followed by platform-specific sections. HTTP errors are appended to
`errors` rather than thrown; the script always produces a parseable file.

## Per-platform setup

### Meta (Facebook + Instagram)

**Effort:** ~5 minutes. Easiest of the seven.

1. Go to [developers.facebook.com](https://developers.facebook.com) → My Apps → create a Business app.
2. Add the **Marketing API** product.
3. In Graph API Explorer, request a User Token with `ads_read`, `ads_management`, `business_management` permissions.
4. (Recommended for unattended use) Convert to a long-lived 60-day token:
   ```
   GET https://graph.facebook.com/v22.0/oauth/access_token
       ?grant_type=fb_exchange_token
       &client_id=<APP_ID>
       &client_secret=<APP_SECRET>
       &fb_exchange_token=<SHORT_TOKEN>
   ```
5. (Even better) Create a System User in Business Settings → generate a System User token (never expires).
6. Find `ad_account_id` in Ads Manager URL (`act_<digits>`).

```bash
export META_ACCESS_TOKEN='EAA...'
export META_PIXEL_ID='<numeric, optional>'
python3 scripts/api/meta_fetch.py --account-id act_123456789 -o meta-data.json
```

### Google Ads

**Effort:** 1-3 business days (developer-token approval). Once approved, ~10 min.

1. Create or use a Google Ads MCC (manager) account.
2. Apply for API access at [developers.google.com/google-ads/api](https://developers.google.com/google-ads/api/docs/access-levels) → get a **developer token** (start at Test level; request Basic/Standard for production).
3. Create an OAuth 2.0 client in [Google Cloud Console](https://console.cloud.google.com) → Credentials → OAuth client ID → **Desktop app**. Note `client_id` and `client_secret`.
4. Generate a refresh token via OAuth Playground or the [google-ads-python](https://github.com/googleads/google-ads-python/blob/main/examples/authentication/generate_user_credentials.py) helper. Scope: `https://www.googleapis.com/auth/adwords`.
5. Find your customer ID (10-digit, strip dashes).

```bash
export GOOGLE_ADS_DEVELOPER_TOKEN='...'
export GOOGLE_ADS_CLIENT_ID='...apps.googleusercontent.com'
export GOOGLE_ADS_CLIENT_SECRET='GOCSPX-...'
export GOOGLE_ADS_REFRESH_TOKEN='1//...'
export GOOGLE_ADS_LOGIN_CUSTOMER_ID='1234567890'   # MCC ID, optional
python3 scripts/api/google_fetch.py --account-id 1234567890 -o google-data.json
```

### TikTok

**Effort:** ~30 min.

1. Apply for the [TikTok for Business API](https://business-api.tiktok.com/portal/docs?id=1738455508553729) (Business Center account required).
2. Create an app in the Developer Portal. Note the **App ID** and **App Secret**.
3. Complete the [auth-code OAuth flow](https://business-api.tiktok.com/portal/docs?id=1739965703387137) → you get a long-lived `access_token` and the list of `advertiser_ids` you can query.

```bash
export TIKTOK_ACCESS_TOKEN='...'
python3 scripts/api/tiktok_fetch.py --account-id 7000000000000000001 -o tiktok-data.json
```

## Summary table

| Platform | Setup time | Friction | Free? | Stdlib only? |
|----------|-----------|----------|-------|--------------|
| Meta | ~5 min | None | ✅ | ✅ |
| Google | 1-3 business days for dev-token approval | Dev-token gate | ✅ | ✅ |
| TikTok | ~30 min | None | ✅ | ✅ |

## What's verified vs. what to verify before production

These adapters were authored against each platform's published REST documentation. **Their `--help` and module-import behavior is covered by `pytest tests/`; their actual HTTP calls have not been exercised against live ad accounts during authoring.** Treat them as well-formed first drafts that you should validate against your account before relying on them for scheduled audits.

The riskiest moving parts to verify per platform:

| Adapter | What to confirm on your first run |
|---|---|
| `meta_fetch.py` | Long-lived token still valid (60-day default); pixel fetch needs `META_PIXEL_ID` to work. |
| `google_fetch.py` | Developer-token level grants the operations you need (test mode vs basic vs standard); GAQL field names match your account's API version. |
| `tiktok_fetch.py` | Your `advertiser_id` is one of the IDs returned by the OAuth flow; otherwise the API will refuse. |

Each adapter handles HTTP errors by appending to the output JSON's `errors` array rather than throwing. Always check `result["errors"]` before treating the payload as authoritative — a partial fetch is still a valid JSON file the agent will consume, but the audit will only score what came back.

## Exit codes

- `0` — completed successfully, no errors recorded.
- `1` — completed but `errors` array is non-empty (some sections failed; audit may be partial).
- `2` — missing required env var(s); did not call the API.
- `3` — OAuth refresh / JWT signing failed; did not call the API.

## Workflow with the audit agents

After running any of these scripts, the audit agent picks up the JSON
automatically. Example for Meta:

```bash
# Once per audit
python3 scripts/api/meta_fetch.py --account-id act_123 -o meta-data.json

# In Claude Code
/ads meta
# The agent sees meta-data.json in cwd, reads it as Capa 2,
# emits meta-audit-results.json (against audit-output-schema.json)
# plus the human-readable meta-audit-results.md.
```

If neither MCP nor the script output is available, the agent falls back
to asking for manual exports / screenshots (Capa 3) — that path is
unchanged from v2.2.0.
