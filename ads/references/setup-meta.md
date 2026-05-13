# Setup: Meta Ads (Facebook + Instagram)

Loaded by `/ads start` Phase C when the user picks Meta. Three sections —
**A** for the recommended MCP path, **B** for Direct API, **C** for Manual
exports. Pick the section matching the user's tier choice and walk its steps
in order using the C.3 verified loop.

Each step has 4 lines: **Goal**, **Do this**, **Expect to see**, **On error**.

---

## Section A — claude.ai Facebook MCP (Capa 1, recommended)

Effort: ~30 seconds. The user only needs a Facebook account that owns or has
access to an ad account.

### STEP A1 — Enable the Facebook connector on claude.ai
- **Goal**: turn on the official Meta MCP in the user's Claude session.
- **Do this**: open https://claude.ai → top-right avatar → **Connectors** →
  find **Facebook (Meta Ads)** → click **Connect** → log in with Facebook →
  grant `ads_read`, `business_management`. Then in Claude Code (this chat),
  type `/mcp` to confirm `mcp__claude_ai_Facebook__*` tools are listed.
- **Expect to see**: in `/mcp` output, ≥1 tool name starting with
  `mcp__claude_ai_Facebook__`.
- **On error**: if no tools appear, ask the user to fully close and reopen
  Claude Code; if still missing, the connector wasn't enabled on their
  claude.ai plan — fall back to Section B or Section C.

### STEP A2 — Pick the ad account
- **Goal**: find the `ad_account_id` we'll audit.
- **Do this**: in this chat the agent calls
  `mcp__claude_ai_Facebook__ads_get_ad_accounts` and prints the list. The user
  picks one (format `act_<digits>`).
- **Expect to see**: at least one entry with `id: "act_..."` and a name.
- **On error**: empty list → the Facebook user has no ad-account access. Ask
  them to be added as Advertiser in Business Manager (Settings → People →
  Add → role Advertiser) and re-try.

### STEP A3 — Verify with a live call
- **Goal**: prove the connection actually works.
- **Do this**: call
  `mcp__claude_ai_Facebook__ads_get_dataset_quality` for the chosen account
  (or `ads_get_ad_entities` if dataset-quality is restricted).
- **Expect to see**: a JSON response, even if some fields are null.
- **On error**: `permission denied` → token scope incomplete; redo Step A1
  granting all requested permissions. `invalid account_id` → user pasted the
  wrong ID; redo Step A2.

Save: `tier = mcp_claude_ai`, `ad_account_id`, `connected_at`,
`last_verified_at`.

---

## Section B — Direct API via Marketing API (Capa 2)

Effort: ~5 min, assumes the user already has a Meta for Developers account.
If they don't, run `setup-meta-developers.md` first.

### STEP B1 — Pick the app + add Marketing API product
- **Goal**: have an app that's allowed to call Marketing API.
- **Do this**: developers.facebook.com → My Apps → click the user's Business
  app → **Add Product** → **Marketing API** → Set Up.
- **Expect to see**: Marketing API now in the left nav of the app dashboard.
- **On error**: button greyed out → app type is "Consumer", not "Business".
  Create a new Business-type app instead.

### STEP B2 — Generate a User Token
- **Goal**: get a short-lived token to test, then upgrade it.
- **Do this**: Tools → **Graph API Explorer** → select the app → **Generate
  Access Token** → grant `ads_read`, `ads_management`, `business_management`
  → copy the token.
- **Expect to see**: a string starting with `EAA...`, ~200 chars.
- **On error**: "User does not have permission" → user isn't an admin of the
  Business that owns the ad account; ask Business owner to add them.

### STEP B3 — Exchange for a long-lived (60-day) token
- **Goal**: avoid token expiry every 2 hours.
- **Do this**:
  ```
  curl "https://graph.facebook.com/v22.0/oauth/access_token?\
  grant_type=fb_exchange_token&client_id=<APP_ID>&\
  client_secret=<APP_SECRET>&fb_exchange_token=<SHORT_TOKEN>"
  ```
  The `app_id` and `app_secret` are in App Dashboard → Settings → Basic.
- **Expect to see**: JSON `{"access_token":"EAA...","expires_in":5183944,...}`.
- **On error**: `Invalid OAuth access token` → typo in `fb_exchange_token` or
  it already expired (regen Step B2).

### STEP B4 — (Optional but recommended) System User token
- **Goal**: never-expires token for unattended audits.
- **Do this**: business.facebook.com → Business Settings → Users → **System
  Users** → Add → Admin → click the system user → **Generate New Token** →
  pick the app → tick `ads_read` + `business_management` → 60 days, **Never
  Expire** option. Assign the ad account to this system user in Business
  Settings → Accounts → Ad Accounts → Add People.
- **Expect to see**: token string saved to a vault. This is the value to
  export as `META_ACCESS_TOKEN`.
- **On error**: "Never Expire" missing → user lacks Business admin role.

### STEP B5 — Export env var + verify
- **Goal**: prove `meta_fetch.py` can hit the API for the user's account.
- **Do this** (replace placeholders):
  ```bash
  export META_ACCESS_TOKEN='<token>'
  python3 scripts/api/meta_fetch.py --account-id act_<id> --what account
  ```
- **Expect to see**: JSON output with `platform: "meta"`, `account` section
  populated, `errors: []`.
- **On error**: `(#200) Permissions error` → re-check Step B2 scopes;
  `(#100) Tried accessing nonexisting field` → account ID typo.

Save: `tier = direct_api`, `ad_account_id`, `connected_at`,
`last_verified_at`.

---

## Section C — Manual exports (Capa 3, always works)

Effort: ~5 min per export. Zero credentials. Some checks become N/A.

### STEP C1 — Export campaigns CSV
- **Goal**: get a CSV of campaign-level performance.
- **Do this**: Ads Manager → Campaigns tab → top-right **Reports** → **Export
  Table Data** → CSV. Columns: name, budget, spend, impressions, clicks,
  results, CPA, ROAS over last 28 days.
- **Expect to see**: a CSV file downloaded to disk.
- **On error**: empty export → user filtered to date range with no spend;
  expand range.

### STEP C2 — Capture Events Manager screenshots
- **Goal**: snapshot pixel + CAPI + EMQ state for tracking checks.
- **Do this**: business.facebook.com → Events Manager → click the data source
  → Overview tab → screenshot. Also Settings tab → screenshot.
- **Expect to see**: screenshots showing EMQ scores and CAPI status.

### STEP C3 — Note `ad_account_id`
- **Goal**: record which account the manual data is from.
- **Do this**: copy `act_<digits>` from the Ads Manager URL.

Save: `tier = manual`, `ad_account_id`, `connected_at`. Leave
`last_verified_at = null` (no live call to verify against).

---

## Troubleshooting summary

| Symptom | Most likely cause | Fix |
|---------|-------------------|-----|
| No MCP tools | Connector not enabled or stale Claude Code | Reopen Claude Code |
| `(#10) Application does not have permission` | App missing Marketing API product | Step B1 |
| `(#190) Access token has expired` | Short-lived 2h token used | Step B3 or B4 |
| Empty ad accounts list | User not added to Business Manager | Add as Advertiser |
| `Invalid parameter` on account_id | Missing `act_` prefix | Add prefix |
