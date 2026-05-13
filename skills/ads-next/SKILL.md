---
name: ads-next
description: "Continuous coach. Reads the most recent <platform>-audit-results.json files (cwd + ~/.claude-ads/history/), ranks Quick Wins and Critical Issues by impact × ease using the user's saved spend mix, surfaces the top 3 next actions, and optionally walks the user through fixing the #1 right now. Detects regressions vs the previous audit (score drops, new failures) and flags them as Priority 0. Use when user says next, what should I do, recommend, fix, suggest, what's next, qué sigue, recomienda, próximo paso."
user-invokable: false
argument-hint: "[show | compare | walk]"
allowed-tools: Bash, Read, Write, AskUserQuestion
---

# Continuous coaching: what to fix next

`/ads next` turns audits into a stream of small, ordered, verified actions.
It's the second half of the seguimiento loop: `/ads start` connects, `/ads
audit` measures, `/ads next` coaches.

## Subcommand routing

| Arg | Behavior |
|-----|----------|
| (none) | Default — Discover → Rank → Top 3 → offer to walk through #1. |
| `show` | Discover → Rank → print top 10 → exit (no walk-through prompt — good for client reports). |
| `compare` | Print full delta between the two most-recent audits per platform via `python3 scripts/profile.py compare <p>`. |
| `walk` | Skip the prompt — go straight to walking the user through the top action. |

## Core rules

1. **Read the profile first.** `python3 scripts/profile.py get` — if exit 2,
   suggest `/ads start` and exit (a coach with no context is just guessing).
2. **One action at a time during walk-through.** Same step-by-step verified
   loop as `/ads start` Phase C.3.
3. **Never invent issues.** If no audits are found in cwd or history, print
   the exact command to generate one (`/ads audit` or platform-specific) and
   exit.

---

## Phase 1 — Discover audit JSON

Search for `*-audit-results.json` files in this order, newest first:

1. **`<cwd>`** — current working directory. Glob `*-audit-results.json`.
2. **`~/.claude-ads/history/`** — the persistent log. Read
   `~/.claude-ads/history/index.json` and resolve files for the most recent
   audit per platform.

Validate each file:

- Must parse as JSON.
- Must include `platform`, `health_score`, `checks`.
- `platform` must be one of `meta`, `google`, `tiktok`.

If a file fails validation, skip it and print a single `WARNING:
skipped <path> (<reason>)` line. Don't abort the run.

If **zero** valid audits found:

```
No audits yet. Run one first:

  /ads audit                 — full multi-platform
  /ads <meta|google|tiktok>  — single platform deep-dive
```

Then exit.

---

## Phase 2 — Persist any new audits to history

For each audit file discovered in cwd that is NEWER than the most recent
entry for that platform in `~/.claude-ads/history/index.json` (compare
`generated_at`), copy it to history via:

```bash
python3 scripts/profile.py save-audit <path>
```

This is what builds the multi-session memory — every audit run from anywhere
on disk eventually ends up in the history index.

---

## Phase 3 — Rank items by impact × ease

Pool every `quick_win`, every `critical_issue`, and every `check` with
`result` in (`FAIL`, `WARNING`) across all valid audits. Deduplicate by
(`platform`, `check_id`) — if a check appears in both `critical_issues` and
`checks`, treat as one item using the critical metadata.

For each item, compute an **impact score**:

```
severity_weight = { critical: 5.0, high: 3.0, medium: 1.5, low: 0.5 }[severity]
effort_inverse  = 1 / (fix_time_minutes + 1)            # default fix_time = 30 if null
budget_share    = platform_budget_share(platform)       # see below
impact          = severity_weight × effort_inverse × budget_share × 100
```

**`platform_budget_share`** — derive from the user's profile + audit
`account_id` presence:

- If profile lists 1 active platform, share = 1.0 for that platform.
- If profile lists 2 or 3, share = `1 / n` baseline. Then bump the platform
  that the user spends most on (use `monthly_spend_usd` ÷ platform count as
  the rough prior; if the user has set per-platform spend in the future,
  use that instead) by +0.1 (cap at 0.8).
- If profile is empty, fall back to equal weight.

Sort all items by `impact` descending.

---

## Phase 4 — Regression detection (Priority 0)

For each platform with ≥2 audits in history, run:

```bash
python3 scripts/profile.py compare <platform>
```

Inspect the JSON output:

- `score_delta < -5` → **PRIORITY 0 alert** appended at the top of the
  ranked list. Format:

  ```
  ⚠ <Platform> health dropped from <prev>/100 (<prev_grade>) → <new>/100 (<new_grade>) since your last audit.
    New issues: <comma list of new_issues>
    Resolved:   <comma list of resolved_issues>
  ```

- `score_delta > +5` → success line at the very bottom of the output:
  `🎉 <Platform> health improved <delta>+ points since last audit. Keep going.`

Regressions take precedence over normal Quick Wins. They appear ABOVE the
Top 3 list, with their own header.

---

## Phase 5 — Output the top 3

Default subcommand prints:

```
Next actions (ranked by impact × ease for your $XXX/mo across <platforms>):

  1. [<platform> · <check_id> · <severity>] <name>
     Finding:        <finding>
     Recommendation: <recommendation>
     Estimated fix:  <fix_time_minutes> min · Impact: <impact rounded>
     Reference:      <reference file if known, e.g. tracking-meta.md>

  2. [...]

  3. [...]

(Run `/ads next show` to see the top 10. `/ads next compare` for full audit delta.)
```

If `show` subcommand: print top 10 instead, no prompt, exit.

---

## Phase 6 — Walk-through (default and `walk` subcommands)

`AskUserQuestion`:

> *"Want me to walk you through fixing #1 right now?"*

Options: `Yes — step by step` · `Show me #2 instead` · `Exit, I'll handle it`.

On `Yes`:

1. **Determine the reference file** for this check_id based on its platform
   and category. Lookup table:

   | Platform | Category prefix | Reference file |
   |----------|----------------|----------------|
   | meta | Tracking / Pixel / CAPI | `tracking-meta.md` |
   | meta | Creative | `creative-fatigue.md` |
   | meta | Structure / Budget | `meta-audit.md` |
   | google | Tracking / Conversion | `tracking-google.md` |
   | google | Bidding / Structure | `google-audit.md` |
   | google | Quality Score / Keywords | `google-audit.md` |
   | tiktok | Tracking / Events API | `tracking-tiktok.md` |
   | tiktok | Creative / Spark | `tiktok-audit.md` |
   | tiktok | Structure | `tiktok-audit.md` |

   If no reference matches, use the check's own `recommendation` field as
   the only source.

2. **Step-by-step loop** (same pattern as `/ads start` Phase C.3):

   - Print step 1: Goal · Do this · Expect to see · How I'll verify.
   - `AskUserQuestion`: `Done — verify now` · `Hit an error` · `Pause`.
   - On `Done`: run the verification (re-call the relevant MCP tool / API
     script) and confirm the check now passes. If it does → ✓, move to
     step 2. If not → diagnose, retry.
   - Cap at 3 attempts per step.

3. After the action, ask if the user wants to proceed to action #2.

On `Show me #2 instead`: re-enter Phase 6 with index 2.

On `Exit`: print:

> *Run `/ads audit` after you've fixed this to update your score, then `/ads
> next` again for the new top 3.*

---

## Phase 7 — Save state

At the end:

```bash
python3 scripts/profile.py set last_command "/ads next"
python3 scripts/profile.py set last_command_at "$(date -u +%FT%TZ)"
```

The history index updates itself when `/ads audit` runs next — `/ads next`
itself doesn't add to history (it only reads + acts).

---

## Compare mode (`/ads next compare`)

For each platform with ≥2 history entries:

```bash
python3 scripts/profile.py compare <platform>
```

Print the full diff for each: score delta, grade change, new issues, resolved
issues, file timestamps. No ranking, no walk-through prompt — this is the
audit changelog view.

---

## Error handling

- Profile missing → print one-liner suggesting `/ads start`, exit.
- No audits anywhere → print one-liner suggesting `/ads audit`, exit.
- All audits failed validation → print the warnings collected and exit.
- During walk-through: if 3 retries fail, log to console "Skipped
  <check_id> — come back to this with `/ads next walk` later" and ask whether
  to try #2.

## Output contract

`/ads next` produces NO files. It is purely interactive coaching plus
side-effects on `~/.claude-ads/history/` (via `save-audit`) and the profile's
`last_command*` fields.
