---
name: ads-start
description: "Guided first-run wizard. Walks the user from cold install to a working audit pipeline: business-context capture, per-platform connection choice (MCP / direct API / manual) with step-by-step OAuth verification, optional Zernio + Meta Developers account walkthroughs, profile persistence to ~/.claude-ads/profile.json. Re-runnable to edit settings (`/ads start edit`), reset (`/ads start reset`), or check status (`/ads start status`). Use when user says start, setup, init, onboard, first time, get started, walkthrough, connect my accounts, conectar mis cuentas, empezar."
user-invokable: false
argument-hint: "[reset | edit | status]"
allowed-tools: Bash, Read, Write, AskUserQuestion
---

# Guided onboarding wizard

You are running the first-run / re-entry wizard that produces and maintains
`~/.claude-ads/profile.json`. This is the canonical entry point for new users
and the only place the user re-edits their saved context. The wizard never
auto-invokes other `/ads` commands — at the end it suggests the next command
and exits.

## Core rules

1. **One question at a time.** Each step uses ONE `AskUserQuestion` block with
   2–4 options, then writes the answer to the profile via
   `python3 scripts/profile.py set <dot.path> <value>` BEFORE asking the next
   question. Partial completion must be recoverable.
2. **Step-by-step verification.** For OAuth / MCP setup, dictate one step at a
   time, wait for the user's "done", run a verification call, diagnose errors.
   Cap retries at 3 per platform before offering "skip + come back later".
3. **Never store secrets in the profile.** Tokens, API keys, refresh tokens
   live in environment variables only. The profile records `api_key_present:
   true/false`, never the value.
4. **The wizard is inert at the end.** Suggest the next command in plain text,
   do NOT execute it.

## Subcommand routing

Read the user's argument (if any):

| Arg | Behavior |
|-----|----------|
| (none) | Phase A — detect first-run vs re-entry. |
| `status` | Run `python3 scripts/profile.py get`, print a 5-line summary, exit. |
| `edit` | Skip Phase A welcome, jump to the edit selector in Phase A.4. |
| `reset` | Confirm with AskUserQuestion → call `python3 scripts/profile.py reset --yes` → restart from Phase A. |

---

## Phase A — Detect first-run vs re-entry

**A.1** Run `python3 scripts/profile.py get` and capture exit code.

- Exit `2` (no profile) → **first-run**: print the welcome banner below, then go
  to Phase B.
- Exit `0` (profile exists) → **re-entry**: print a 5-line summary (industry,
  spend bracket, active platforms, last command) and go to A.4.

**A.2** First-run welcome (print verbatim, adapt to user's language):

```
Welcome to claude-ads. I'll walk you through 4 quick steps:

  1. Tell me about your business (~1 min)
  2. Connect Meta / Google / TikTok — one at a time, step by step (~2-10 min each)
  3. Optional: Zernio for publishing creatives, Meta for Developers
  4. Pick your first action

Nothing leaves your machine. Tokens go to env vars, not the profile.
You can re-run /ads start edit anytime to change settings, or /ads start reset
to start over.
```

**A.3** First-run: run `python3 scripts/profile.py init` and continue to
Phase B.

**A.4** Re-entry edit selector — `AskUserQuestion`:

> *"What do you want to change?"*

- `Business context` — re-run Phase B.
- `Meta connection` — re-run Phase C for Meta only.
- `Google connection` — re-run Phase C for Google only.
- `TikTok connection` — re-run Phase C for TikTok only.
- `Zernio publishing` — re-run Phase D Zernio block.

(`AskUserQuestion` will add "Other" — treat it as cancel.)

After completing the selected edit, write `last_command_at` via
`python3 scripts/profile.py set last_command_at $(date -u +%FT%TZ)` and exit
with a one-line "Saved." confirmation.

---

## Phase B — Business context (first-run or `edit context`)

Four sequential AskUserQuestion blocks. Save EACH answer immediately.

### B.1 Industry — `AskUserQuestion` (single-select)

Options: `Ecommerce` · `Local service` · `Real estate` · `Healthcare` ·
`Finance` · `Agency / multiple clients` · `Other`.

Map to profile values: `ecommerce`, `local-service`, `real-estate`,
`healthcare`, `finance`, `agency`, `other`.

Then: `python3 scripts/profile.py set context.industry <value>`.

### B.2 Monthly ad spend — `AskUserQuestion` (single-select)

Options: `Under $500/mo` · `$500–$2,000/mo` · `$2,000–$10,000/mo` ·
`$10,000+/mo`. (User can pick "Other" and type an exact figure — coerce to a
number.)

Map bracket → midpoint USD: 250, 1250, 6000, 25000. If user gave an exact
number, use it.

Then: `python3 scripts/profile.py set context.monthly_spend_usd <number>`.

### B.3 Primary goal — `AskUserQuestion` (single-select)

Options: `Sales / revenue` · `Leads / signups` · `App installs` ·
`Phone calls` · `Brand awareness`.

Map → `sales`, `leads`, `app-installs`, `calls`, `brand`.

Then: `python3 scripts/profile.py set context.primary_goal <value>`.

### B.4 Active platforms — `AskUserQuestion` (multiSelect: true)

> *"Which platforms do you actively run (or plan to run) ads on?"*

Options: `Meta (Facebook + Instagram)` · `Google Ads (incl. YouTube)` ·
`TikTok Ads`.

Require ≥1. Map to `["meta","google","tiktok"]` subset.

Then: `python3 scripts/profile.py set context.active_platforms '<json>'`.

---

## Phase C — Per-platform connection wizard

For each platform in `context.active_platforms` (in order Meta → Google →
TikTok, only those selected in B.4), run the loop below.

### C.1 Tier selection — `AskUserQuestion` (single-select)

> *"How do you want to connect `<PLATFORM>`?"*

| Option | Save as `connections.<p>.tier` | Notes |
|--------|---------------------------------|-------|
| `MCP server (recommended)` | `mcp_claude_ai` for Meta · `mcp_cohnen` for Google · `mcp_adsmcp` for TikTok | Capa 1. Quickest. |
| `Direct API (free, OAuth once)` | `direct_api` | Capa 2. Full control. |
| `Manual exports for now` | `manual` | Capa 3. Always works, no setup. |
| `Skip — set this up later` | `skipped` | Leave unconfigured. |

If `manual` or `skipped`: write the tier, write `connected_at` to now, **skip
C.2-C.4**, continue to the next platform.

### C.2 Load the platform setup walkthrough

Read the relevant reference file:

| Platform | Reference |
|----------|-----------|
| Meta | `ads/references/setup-meta.md` |
| Google | `ads/references/setup-google.md` |
| TikTok | `ads/references/setup-tiktok.md` |

Each file has Sections A (MCP), B (Direct API), C (Manual). Jump to the
section that matches the user's tier choice. Within that section, walk the
steps in order.

### C.3 Step-by-step verified walkthrough

For each STEP in the chosen section:

1. **Print the step verbatim**: its Goal, the exact URL/action under "Do
   this", and what they should "Expect to see".
2. `AskUserQuestion` → *"Done with step N?"* with options:
   - `Done — next step`
   - `Hit an error`
   - `Cancel and skip this platform`
3. On `Done`: continue to the next step.
4. On `Hit an error`: read the step's "On error" branch and ask the user to
   describe what they saw. Suggest the most likely fix from the reference.
   Retry the step. Cap at 3 attempts → offer to skip.
5. On `Cancel`: set `connections.<p>.tier = "skipped"` and continue to next
   platform.

After the LAST step, run the verification call:

| Platform | Tier A (MCP) verification | Tier B (Direct API) verification |
|----------|---------------------------|----------------------------------|
| Meta   | Call `mcp__claude_ai_Facebook__ads_get_ad_accounts` | `python3 scripts/api/meta_fetch.py --account-id <id> --what account` |
| Google | Call `mcp__cohnen_google_ads__list_customers` (if available) — else ask user to paste `customer_id` | `python3 scripts/api/google_fetch.py --customer-id <id> --what account` |
| TikTok | List advertiser via MCP tool — else ask user to paste `advertiser_id` | `python3 scripts/api/tiktok_fetch.py --advertiser-id <id> --what account` |

(If the MCP tool isn't present in this session — e.g., the user hasn't enabled
it on claude.ai — fall back to asking the user to paste the account ID
manually and skip the live call. Record `last_verified_at: null` so /ads next
knows to re-verify next time.)

### C.4 Save the connection

On verification success:

```bash
python3 scripts/profile.py set connections.<platform>.ad_account_id "<id>"
python3 scripts/profile.py set connections.<platform>.connected_at "$(date -u +%FT%TZ)"
python3 scripts/profile.py set connections.<platform>.last_verified_at "$(date -u +%FT%TZ)"
```

Print ✓ confirmation with the account ID. Continue to next platform.

---

## Phase D — Optional account-creation walkthroughs

### D.1 Meta for Developers (only if Meta tier == `direct_api`)

`AskUserQuestion`:

> *"Do you already have a Meta for Developers account? (Required for the
> direct Meta API path.)"*

Options: `Yes — I have one` · `No — walk me through it` · `Skip`.

On `No`: load `ads/references/setup-meta-developers.md` and run the
step-by-step loop (same pattern as C.3). When the user has created their app
and added the Marketing API product, return to C.3 step 1 of the Direct API
section in `setup-meta.md`.

### D.2 Zernio publishing (asked once at the end of Phase C, regardless of tier)

`AskUserQuestion`:

> *"Do you want to enable `/ads publish` for posting generated creatives to 14+
> social networks? Zernio's free tier covers 2 connected accounts forever (no
> credit card)."*

Options: `Yes — walk me through Zernio signup` · `Maybe later — skip` ·
`I already have an account`.

- `Yes`: load `ads/references/setup-zernio.md`, run step loop. On success
  write `zernio.signed_up = true`. If user reports they saved the API key to
  `ZERNIO_API_KEY`, also write `zernio.api_key_present = true`.
- `I already have an account`: just ask if `ZERNIO_API_KEY` is exported.
  Write `zernio.signed_up = true` and `zernio.api_key_present` accordingly.
- `Skip`: leave defaults (`false`).

---

## Phase E — First-action recommendation

Print a one-screen summary:

```
✓ Profile saved to ~/.claude-ads/profile.json
✓ Connected:  <platform list with tier>
✓ Zernio:     <on / off>
```

Then `AskUserQuestion`:

> *"You're set up. What would you like to run first?"*

Options (filter to what the user actually configured):

- `/ads audit — full multi-platform audit` (recommended if ≥2 platforms
  connected with tier ≠ skipped).
- `/ads <single-platform> — deep-dive on one platform` (single-select the
  platforms they connected).
- `/ads plan <industry> — strategic plan from your industry template`
  (use their `context.industry`, falling back to `generic`).
- `Just exit — I'll explore on my own`.

Print the EXACT next command to type (do not invoke it). Example:

> *Great — next, type: `/ads audit`*

Finalize: `python3 scripts/profile.py set last_command "/ads start" && python3
scripts/profile.py set last_command_at "$(date -u +%FT%TZ)"`.

---

## Status mode (`/ads start status`)

Run `python3 scripts/profile.py get` and print:

```
claude-ads profile
  Industry:           <context.industry or "—">
  Monthly spend:      ~$<context.monthly_spend_usd>/mo
  Goal:               <context.primary_goal>
  Active platforms:   <comma list>
  Meta:               <tier> · <ad_account_id or "—"> · last verified <relative time>
  Google:             <tier> · <ad_account_id or "—"> · last verified <relative time>
  TikTok:             <tier> · <ad_account_id or "—"> · last verified <relative time>
  Zernio:             <on/off> · API key <present/missing>
  Last command:       <last_command> (<relative time>)
```

Exit without further prompts.

---

## Error handling

- If `python3 scripts/profile.py` is not executable, run it as `python3
  scripts/profile.py …` (already the default).
- If `~/.claude-ads/` is read-only, print the path and ask the user to fix
  permissions before retrying.
- If `AskUserQuestion` returns "Other" without useful text, treat as cancel
  for that step.

## Output contract

The wizard does NOT produce a report file. It only writes
`~/.claude-ads/profile.json` and emits user-facing prose. Other /ads commands
read the profile via `python3 scripts/profile.py get`.
