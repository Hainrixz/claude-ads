# Setup: Google Ads (Search, PMax, YouTube)

Loaded by `/ads start` Phase C when the user picks Google. Three sections —
**A** for the MCP path, **B** for Direct API, **C** for Manual exports.
Section B has a 1–3 business-day waiting period for developer-token approval;
warn the user upfront so they can pick A or C first if they need same-day.

---

## Section A — cohnen/mcp-google-ads (Capa 1)

Effort: ~10 min for first-time install (still needs OAuth client + refresh
token; same env vars as Capa 2). Worth it because the MCP exposes natural-
language GAQL.

### STEP A1 — Confirm Python + pip available
- **Goal**: prerequisite check.
- **Do this**: `python3 --version` (need 3.10+) and `pip3 --version`.
- **Expect to see**: Python ≥3.10.
- **On error**: install Python via `brew install python` (mac) or the
  python.org installer.

### STEP A2 — Install the MCP server
- **Goal**: have the server binary on disk.
- **Do this**:
  ```bash
  pip3 install mcp-google-ads
  ```
- **Expect to see**: `Successfully installed mcp-google-ads-...`.
- **On error**: permission denied → `pip3 install --user mcp-google-ads`.

### STEP A3 — Reuse Direct API credentials
- **Goal**: the MCP needs the same env vars as Section B. Either set them now
  or come back after Section B.
- **Do this**: ensure these are exported:
  `GOOGLE_ADS_DEVELOPER_TOKEN`, `GOOGLE_ADS_CLIENT_ID`,
  `GOOGLE_ADS_CLIENT_SECRET`, `GOOGLE_ADS_REFRESH_TOKEN`,
  (optional) `GOOGLE_ADS_LOGIN_CUSTOMER_ID`.
- **Expect to see**: `echo $GOOGLE_ADS_DEVELOPER_TOKEN` prints non-empty.
- **On error**: missing → go run Section B steps B1–B5 first, then return.

### STEP A4 — Wire to Claude Code MCP config
- **Goal**: tell Claude Code to launch the server.
- **Do this**: edit `~/.claude/mcp_servers.json` (or your team's MCP config)
  to add:
  ```json
  { "google-ads": { "command": "python3", "args": ["-m", "mcp_google_ads"] } }
  ```
  Restart Claude Code.
- **Expect to see**: in this chat, `/mcp` lists `mcp__google_ads__*` tools.
- **On error**: tools missing → check `~/.claude/logs/mcp-*.log` for the
  server's stderr. Most often: refresh-token expired (redo Step B4).

### STEP A5 — Verify
- **Goal**: live call returns customer list.
- **Do this**: agent calls `mcp__google_ads__list_customers` (or similar
  per the server's tool catalog).
- **Expect to see**: array with ≥1 customer ID.
- **On error**: empty → user's OAuth grant didn't include the right
  customer; redo refresh-token generation with the correct Google account.

Save: `tier = mcp_cohnen`, `ad_account_id = <customer_id>`,
`connected_at`, `last_verified_at`.

---

## Section B — Direct API (Capa 2)

Effort: 1–3 business days for dev-token approval, then ~10 min OAuth.

### STEP B1 — Apply for developer-token
- **Goal**: get an API key that can talk to Google Ads.
- **Do this**: sign in to your MCC (manager) account → top-right tools icon
  → **API Center** → fill the application. Start at **Test access level**
  (instant; only works against test accounts). Apply for **Basic** for real
  data. URL: https://ads.google.com/aw/apicenter
- **Expect to see**: developer token displayed (string like `aBcD-1234...`).
- **On error**: "You must be on an MCC" → create an MCC at
  https://ads.google.com/home/tools/manager-accounts/ and link the operating
  account to it.

### STEP B2 — Create OAuth 2.0 client
- **Goal**: a client_id + client_secret to exchange for tokens.
- **Do this**: https://console.cloud.google.com → **APIs & Services** →
  **Credentials** → Create Credentials → OAuth client ID → application type
  **Desktop app** → name "claude-ads" → Create.
- **Expect to see**: a dialog with `client_id` and `client_secret`. Save
  both. Also click **Download JSON** if you prefer file-based config.
- **On error**: "Configure OAuth consent screen first" → do that (External,
  test users = your own Google account).

### STEP B3 — Enable the Google Ads API
- **Goal**: turn the API on in the GCP project.
- **Do this**: APIs & Services → **Enabled APIs & Services** → + ENABLE APIS
  → search "Google Ads API" → Enable.
- **Expect to see**: status "Enabled".

### STEP B4 — Generate a refresh token
- **Goal**: long-lived token that the script can refresh automatically.
- **Do this**: easiest path is the [OAuth 2.0 Playground](https://developers.google.com/oauthplayground/):
  gear icon → tick **Use your own OAuth credentials** → paste client_id/
  secret → scope `https://www.googleapis.com/auth/adwords` → Authorize APIs
  → Sign in → **Exchange authorization code for tokens** → copy
  `refresh_token`.
- **Expect to see**: a string starting with `1//...`.
- **On error**: `redirect_uri_mismatch` → in GCP Credentials, add
  `https://developers.google.com/oauthplayground` as an authorized redirect
  URI.

### STEP B5 — Find customer_id + login_customer_id
- **Goal**: pick which account to query.
- **Do this**: in Google Ads UI, the 10-digit ID is top-right next to the
  account name (format `123-456-7890` — strip dashes for env vars).
  `login_customer_id` is the MCC ID if the operating account sits under one.
- **Expect to see**: a 10-digit number.

### STEP B6 — Export env vars + verify
- **Goal**: prove `google_fetch.py` works.
- **Do this**:
  ```bash
  export GOOGLE_ADS_DEVELOPER_TOKEN='...'
  export GOOGLE_ADS_CLIENT_ID='....apps.googleusercontent.com'
  export GOOGLE_ADS_CLIENT_SECRET='GOCSPX-...'
  export GOOGLE_ADS_REFRESH_TOKEN='1//...'
  export GOOGLE_ADS_LOGIN_CUSTOMER_ID='1234567890'   # MCC, if applicable
  python3 scripts/api/google_fetch.py --account-id 1234567890 --what account
  ```
- **Expect to see**: JSON with `platform: "google"`, `errors: []`.
- **On error**: `DEVELOPER_TOKEN_NOT_APPROVED` → still on Test level; either
  use a test account or wait for Basic approval. `USER_PERMISSION_DENIED` →
  the Google account that authorized OAuth doesn't have access to the
  customer.

Save: `tier = direct_api`, `ad_account_id = <customer_id>`,
`connected_at`, `last_verified_at`.

---

## Section C — Manual exports (Capa 3)

### STEP C1 — Export Search Terms Report
- **Do this**: Reports → Predefined reports → **Search terms** → date range
  last 28 days → Download CSV.

### STEP C2 — Export Campaigns report
- **Do this**: Campaigns tab → Download → CSV. Columns: Campaign, Status,
  Bid strategy, Budget, Cost, Impressions, Clicks, Conversions, Conv. value.

### STEP C3 — Capture Change History
- **Do this**: Tools → **Change History** → last 30 days → screenshot or CSV.

Save: `tier = manual`, `ad_account_id = <customer_id>` (10-digit, no dashes),
`connected_at`. Leave `last_verified_at = null`.

---

## Troubleshooting summary

| Symptom | Cause | Fix |
|---------|-------|-----|
| `DEVELOPER_TOKEN_NOT_APPROVED` | Test-level token vs production account | Wait for Basic, or use a test account |
| `redirect_uri_mismatch` | Playground URL not in GCP credentials | Add it in Step B2 |
| `USER_PERMISSION_DENIED` | OAuth'd Google user can't see customer | Re-auth with the right Google account |
| MCC errors | Operating account not under MCC | Add `GOOGLE_ADS_LOGIN_CUSTOMER_ID` |
