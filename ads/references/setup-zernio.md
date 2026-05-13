# Setup: Zernio publishing (for `/ads publish`)

Loaded by `/ads start` Phase D when the user opts into publishing generated
creatives to social networks. Zernio's free tier covers the first **2
connected social accounts** forever (no credit card). Beyond 2, pricing is
~$1–$6/mo per additional account. X/Twitter API costs are metered pass-
through; the other 13 networks are fully included.

This walkthrough handles signup, API key, per-network OAuth, and a dry-run
verification.

---

## STEP 1 — Create the Zernio account
- **Goal**: have a Zernio dashboard the user can log into.
- **Do this**: open https://zernio.com → **Sign up** → email + password (or
  Google SSO).
- **Expect to see**: dashboard at app.zernio.com after signup.
- **On error**: signup email not arriving → check spam; Zernio sometimes
  delays verification a few minutes.

## STEP 2 — Pick the free plan
- **Goal**: stay on the free tier (2 connected accounts).
- **Do this**: dashboard → Settings → Billing → confirm plan is **Free**.
  No card required.
- **Expect to see**: plan banner shows "Free — 2 / 2 connections available".
- **On error**: trial of a paid plan auto-applied → downgrade in same screen.

## STEP 3 — Connect your first social account
- **Goal**: connect one platform (we recommend Instagram or Facebook first,
  the most common publishing target).
- **Do this**: dashboard → **Accounts** → **Connect new** → pick a network
  (Instagram, Facebook, LinkedIn, X, TikTok, YouTube Shorts, Pinterest, etc.)
  → complete the OAuth flow in the popup.
- **Expect to see**: account appears under "Connected" with a green dot.
- **On error**: `oauth window closed prematurely` → pop-ups blocked by
  browser; allow pop-ups for zernio.com and retry.

## STEP 4 — (Optional) Connect a second account
- **Goal**: use both free slots.
- **Do this**: repeat Step 3 for a second platform.
- **Expect to see**: counter "2 / 2 connections used".
- **On error**: same as Step 3.

## STEP 5 — Create an API key
- **Goal**: let `scripts/zernio_publish.py` post on the user's behalf.
- **Do this**: dashboard → Settings → **API Keys** → **Create new** → name
  it "claude-ads" → copy the key (starts with `sk_...`).
- **Expect to see**: the key shown ONCE. Save it somewhere safe immediately.
- **On error**: button missing → user is on a sub-account that lacks API
  access; switch to the workspace owner account.

## STEP 6 — Export `ZERNIO_API_KEY`
- **Goal**: make the key visible to `/ads publish`.
- **Do this**:
  ```bash
  echo 'export ZERNIO_API_KEY="sk_..."' >> ~/.zshrc   # or .bashrc
  source ~/.zshrc
  ```
- **Expect to see**: `echo $ZERNIO_API_KEY` prints the key.
- **On error**: variable empty after sourcing → wrong shell config file;
  user's default shell may be `bash` (use `~/.bashrc`) or fish (use
  `~/.config/fish/config.fish`).

## STEP 7 — Dry-run verification
- **Goal**: prove the key works without actually posting anything.
- **Do this**:
  ```bash
  python3 scripts/zernio_publish.py --dry-run
  ```
- **Expect to see**: output ending with `OK: ZERNIO_API_KEY valid, N
  account(s) connected.`
- **On error**: `401 Unauthorized` → key copied wrong or revoked; regenerate
  via Step 5. `403 Plan limit` → connected accounts exceeds tier; disconnect
  one in the dashboard.

---

## Saved to profile

After Step 7 succeeds:

```bash
python3 scripts/profile.py set zernio.signed_up true
python3 scripts/profile.py set zernio.api_key_present true
python3 scripts/profile.py set zernio.connected_socials '["instagram","facebook"]'  # use actual list
```

(The API key itself is **NEVER** written to the profile — only the
`api_key_present: true` flag.)

---

## When to skip this walkthrough

- The user only wants to audit, not publish — skip; revisit anytime via
  `/ads start edit` → Zernio publishing.
- The user already has a Zernio account — they can just export
  `ZERNIO_API_KEY` and skip ahead to Step 7.
- The user wants to scale past 2 accounts — the wizard still gets them set
  up; pricing kicks in at $1–$6/mo per extra account, billed by Zernio
  directly.

---

## Troubleshooting summary

| Symptom | Cause | Fix |
|---------|-------|-----|
| `401 Unauthorized` | Bad / revoked key | Regenerate in Step 5 |
| `403 Plan limit` | >2 connected accounts on free tier | Disconnect one or upgrade |
| OAuth popup blank | Browser blocked third-party cookies | Allow cookies for zernio.com |
| Key not in env after sourcing | Wrong shell rc file | Use the right one (`.zshrc` / `.bashrc` / fish config) |
| Dry-run hangs | Network firewall | Check VPN / corp proxy |
