# Setup: TikTok Ads

Loaded by `/ads start` Phase C when the user picks TikTok. Three sections —
**A** for the MCP path (community-built), **B** for Direct API, **C** for
Manual exports.

---

## Section A — AdsMCP/tiktok-ads-mcp-server (Capa 1)

Effort: ~15 min. Like Google, it reuses Capa 2 credentials; if the user
hasn't done OAuth yet they'll need to run Section B Steps B1–B5 first.

### STEP A1 — Prerequisite check
- **Goal**: confirm Python 3.10+.
- **Do this**: `python3 --version`.
- **Expect to see**: 3.10 or later.

### STEP A2 — Install
- **Do this**:
  ```bash
  pip3 install tiktok-ads-mcp-server
  ```
- **Expect to see**: install confirmation.
- **On error**: package not found → some forks live on GitHub only. Clone
  AdsMCP/tiktok-ads-mcp-server and `pip3 install -e .` inside the repo.

### STEP A3 — Reuse direct-API creds
- **Goal**: have a TikTok access token ready.
- **Do this**: ensure `TIKTOK_ACCESS_TOKEN` is exported. If not, run Section
  B steps B1–B5.
- **Expect to see**: `echo $TIKTOK_ACCESS_TOKEN` non-empty.

### STEP A4 — Wire to MCP config
- **Do this**: edit `~/.claude/mcp_servers.json`:
  ```json
  { "tiktok-ads": { "command": "python3", "args": ["-m", "tiktok_ads_mcp"] } }
  ```
  Restart Claude Code.
- **Expect to see**: `/mcp` lists `mcp__tiktok_ads__*` tools.
- **On error**: check `~/.claude/logs/` for stderr.

### STEP A5 — Verify
- **Do this**: call the MCP's `list_advertisers` (or equivalent) tool.
- **Expect to see**: array with ≥1 advertiser_id.
- **On error**: empty → token's auth scope didn't include the advertiser
  account. Redo Step B4 with full scope selection.

Save: `tier = mcp_adsmcp`, `ad_account_id = <advertiser_id>`,
`connected_at`, `last_verified_at`.

---

## Section B — Direct API (Capa 2)

Effort: ~30 min.

### STEP B1 — Sign up for TikTok for Business
- **Goal**: have a Business Center account.
- **Do this**: https://business.tiktok.com → sign up → create a Business
  Center (BC).
- **Expect to see**: BC dashboard.
- **On error**: country not supported → use a VPN to a supported region for
  signup; subsequent API access works globally.

### STEP B2 — Create a developer app
- **Do this**: https://business-api.tiktok.com → **My Apps** → Create. Fill
  app name, callback URL (use `http://localhost:8080` for testing), advertiser
  scope = at least `ad.management:read`.
- **Expect to see**: app dashboard with **App ID** and **Secret**.
- **On error**: must register as developer first → click the prompt and pass
  the (auto-approved) review.

### STEP B3 — Authorize advertisers
- **Goal**: pick which advertiser accounts the app can query.
- **Do this**: in the app dashboard → **Authorization URL** → click it
  (acts as OAuth start) → sign in with the BC owner → grant access to one or
  more advertiser_ids → callback returns `auth_code` in the URL.
- **Expect to see**: a URL like
  `http://localhost:8080/?auth_code=xxx&state=...`. Copy `auth_code`.
- **On error**: `app under review` → some scopes need TikTok approval; start
  with read-only.

### STEP B4 — Exchange auth_code for access_token
- **Do this**:
  ```bash
  curl -X POST 'https://business-api.tiktok.com/open_api/v1.3/oauth2/access_token/' \
    -H 'Content-Type: application/json' \
    -d '{"app_id":"<APP_ID>","secret":"<SECRET>","auth_code":"<AUTH_CODE>"}'
  ```
- **Expect to see**: JSON `{"data": {"access_token":"...","advertiser_ids":[...]}}`.
  Long-lived (no automatic expiry; revoke manually).
- **On error**: `auth_code expired` → it's single-use and short-lived;
  re-do Step B3.

### STEP B5 — Pick an advertiser_id
- **Do this**: from the JSON in B4, pick one `advertiser_id` to audit.
- **Expect to see**: a 17–19 digit number.

### STEP B6 — Export + verify
- **Do this**:
  ```bash
  export TIKTOK_ACCESS_TOKEN='<token>'
  python3 scripts/api/tiktok_fetch.py --account-id <advertiser_id> --what account
  ```
- **Expect to see**: JSON with `platform: "tiktok"`, `errors: []`.
- **On error**: `40001 Authentication failed` → token revoked or wrong
  advertiser_id; redo Step B4.

Save: `tier = direct_api`, `ad_account_id = <advertiser_id>`,
`connected_at`, `last_verified_at`.

---

## Section C — Manual exports (Capa 3)

### STEP C1 — Export campaign data
- **Do this**: Ads Manager → **Reporting** → custom report → dimensions
  Campaign + Ad Group + Ad, metrics CPM, CTR, CVR, CPA, ROAS → date range 28
  days → Export CSV.

### STEP C2 — Capture Events API state
- **Do this**: Assets → **Events** → click the pixel → screenshot
  Overview tab (shows event match score, server-side share).

### STEP C3 — Note advertiser_id
- **Do this**: top-left of Ads Manager.

Save: `tier = manual`, `ad_account_id = <advertiser_id>`, `connected_at`.

---

## Troubleshooting summary

| Symptom | Cause | Fix |
|---------|-------|-----|
| `40001 Authentication failed` | Token revoked / wrong advertiser | Redo Step B4 |
| `40105 No permission` | Scope didn't include `ad.management:read` | Re-do Step B2 with right scopes |
| Region block on signup | Country-restricted onboarding | VPN to supported country for signup only |
| `auth_code expired` | Single-use code timed out | Click authorization URL again |
