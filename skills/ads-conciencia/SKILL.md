---
name: ads-conciencia
description: "Campaign awareness (conciencia de campaña). Tracks what Claude knows and does NOT know about the real business outcome of lead / WhatsApp / form / call campaigns — results the pixel can't see. Registers campaigns, runs dated check-ins asking the user how many real conversations, qualified leads, closed customers, revenue and junk contacts arrived, cross-references them with platform clicks/messages/spend, and computes the real close rate, cost per closed customer and junk rate. Writes conciencia-de-campana.md. Use when user says conciencia, did it work, closed customers, lead quality, junk leads, ¿me funcionó?, ¿me trajo clientes?, cerré clientes, llegaron mensajes, calidad de leads, leads basura, cuántos cerré."
user-invokable: false
argument-hint: "[registrar | checkin | ver | lista]"
allowed-tools: Bash, Read, Write, AskUserQuestion
---
<!-- Portions Copyright (c) 2026 Enrique Rocha (@soyenriquerocha) - see LICENSE for original authors · tododeia.com · id er-fd4fa55b -->

# Campaign awareness: what the platform can't see

Platforms count clicks and messages. Whether those messages turned into
customers — or were garbage — only the user knows. `/ads conciencia` makes
Claude **explicitly aware of that gap**: it stores the user's dated answers,
asks again on a schedule, and cross-references them with platform metrics to
compute the campaign's real success rate.

Storage (handled entirely by `scripts/conciencia.py`, never hand-edited):

- Source of truth: `~/.claude-ads/conciencia/<platform>-<campaign_id>.json`
  (validates against `ads/references/conciencia-schema.json`).
- Human view: `conciencia-de-campana.md` in the working folder (or
  `conciencia-<platform>-<campaign_id>.md` when the folder tracks more than
  one campaign).

Formulas, thresholds and how to read the cross-reference live in
`ads/references/conciencia.md`. Load it before presenting results.

## Core rules

1. **Profile first.** `python3 scripts/profile.py get`. Exit 2 → one-line tip
   to run `/ads start`, then continue inline.
2. **Never assume a business outcome.** Anything the user did not report is
   `null` and shows as `N/A` with what is missing. Never write 0 for "didn't
   say". A ratio is only computed from check-ins where both sides were
   reported — the script already enforces this; don't recompute by hand.
3. **Ask once, all together.** Each check-in is ONE message with every
   question. Whatever the user skips stays `null`; say so in one line.
4. **Cite the numbers.** Every verdict names the figure that triggered it and
   how many check-ins it rests on: *"tasa de cierre 11.8 % (10 cerrados / 85
   conversaciones, 2 check-ins)"*.
5. **E-commerce with purchase pixel doesn't need this.** The platform already
   sees the sale.

## Subcommand routing

| Arg | Behavior |
|-----|----------|
| (none) | If `conciencia.py due` lists overdue campaigns → Check-in. Else if no campaigns → Register. Else → `ver` for the most recently updated. |
| `registrar` | Phase 2 — register one or more campaigns. |
| `checkin` | Phase 3 — check-in (all overdue, or the one the user names). |
| `ver [<key>]` | Phase 4 — cross-reference + render, no questions. |
| `lista` | `python3 scripts/conciencia.py list` → short table: name, status, check-ins, close rate, next check-in. |

---

## Phase 1 — Does awareness apply?

Read `context.industry` and `context.primary_goal` from the profile (or the
campaign the user names).

- `industry = ecommerce` **and** conversion is a pixel purchase → tell the user
  in one line that the pixel already tracks the sale, so this isn't needed.
  Proceed only if they insist (register with `--channel pixel_purchase`; such
  campaigns are never flagged as due).
- Objective is leads / messages / calls / forms, or the close happens on
  WhatsApp, Messenger, IG DM, a form or a phone call → it applies. Continue.

## Phase 2 — Register

1. Look for campaigns to offer: latest `*-audit-results.json` in cwd, then
   `~/.claude-ads/history/index.json`. Audit JSON has `account_id`; campaign
   names / IDs come from the audit's `evidence` or the platform data pulled
   in the audit (MCP / `scripts/api/<platform>_fetch.py` / export). If none
   found, ask the user.
2. Ask ONCE for everything missing: which campaigns, conversion channel
   (WhatsApp / Messenger / IG DM / form / call / landing), average ticket value
   and currency (optional — unlocks estimated ROAS), how often to check in
   (default 7 days).
3. For each campaign:

```bash
python3 scripts/conciencia.py register --platform meta --campaign-id 120210000000001 \
  --name "WhatsApp Clínica" --objective messages --channel whatsapp \
  --ticket-value 2400 --currency MXN --every 7
```

4. Record what the audit already established as known facts, with source:

```bash
python3 scripts/conciencia.py know meta-120210000000001 \
  --fact "CPL de plataforma 52 MXN (auditoría 2026-10-20)" --source audit
```

5. Go straight into a first check-in (Phase 3) if the campaign has been
   running ≥7 days; otherwise tell the user when Claude will ask.

## Phase 3 — Check-in

1. **Platform side** — pull spend, clicks and messages/leads for the period
   since the last check-in, using the saved tier in
   `connections.<platform>.tier`: MCP → `scripts/api/<platform>_fetch.py` →
   ask for an export / screenshot. Record which one in
   `source_of_platform_metrics`. If nothing is available, leave the block
   null and say so — never estimate.
2. **Business side** — one message, all questions:

> Sobre **<campaign name>**, del <from> al <to> (la plataforma contó
> <messages> mensajes):
> 1. ¿Cuántas conversaciones reales te llegaron?
> 2. ¿Cuántas eran gente con intención real (calificados)?
> 3. ¿Cuántos clientes cerraste?
> 4. ¿Cuánto ingreso generaron? (opcional)
> 5. ¿Cuántos fueron basura — spam, fuera de zona, no contestan?
> 6. ¿Algo que notaste? (p. ej. "preguntan precio y desaparecen")
>
> Lo que no sepas, sáltalo: queda como N/A, no como cero.

3. Save:

```bash
python3 scripts/conciencia.py checkin meta-120210000000001 --json '{
  "period_from": "2026-10-20", "period_to": "2026-10-27",
  "source_of_platform_metrics": "mcp",
  "platform_metrics": {"spend": 2800, "clicks": 850, "messages": 55},
  "user_reported": {"conversations": 40, "qualified": 14, "closed": 6,
                    "revenue": null, "junk": 12, "notes": "preguntan precio y desaparecen"}
}'
```

4. If the user says "later": `python3 scripts/conciencia.py snooze <key> --days 1`.
5. Continue to Phase 4.

## Phase 4 — Cross-reference and verdict

1. `python3 scripts/conciencia.py show <key>` → read `metrics.cumulative`,
   `metrics.latest`, `metrics.trend`.
2. Read `ads/references/conciencia.md` and classify the campaign using its
   reading table (platform says good / business says bad, etc.).
3. Render: `python3 scripts/conciencia.py render <key> --out conciencia-de-campana.md`.
4. Chat summary — short, human, money first:

```
<campaign> — conciencia al <date> (<n> check-ins)

Lo que sé:
  · Tasa de cierre 11.8 % (10 cerrados / 85 conversaciones reales)
  · Costo por cliente cerrado 580 MXN · ROAS real 8.6x (1 check-in con ingreso)
  · 37.6 % de los contactos fueron basura (32 / 85)
Lo que no sé:
  · Ingreso del primer periodo
Lectura: <one line from the reading table>
Siguiente paso: <one concrete action, ranked by money>
Próximo check-in: <date>
```

5. If the verdict points at lead quality (junk rate high, platform vs real
   gap), suggest the matching fix from `conciencia.md` and point at
   `/ads next`, which now ranks these items.

## Phase 5 — Save state

```bash
python3 scripts/profile.py set last_command "/ads conciencia"
python3 scripts/profile.py set last_command_at "$(date -u +%FT%TZ)"
```

## Error handling

- Script exit 2 (campaign not found) → offer `registrar`.
- Exit 3 (bad value, e.g. negative or decimal count) → explain in one line
  which answer didn't fit and re-ask only that one.
- Exit 4 (IO) → explain, suggest checking `~/.claude-ads/` permissions.

## Output contract

- `~/.claude-ads/conciencia/<platform>-<campaign_id>.json` (via script only).
- `conciencia-de-campana.md` (or per-campaign name) in cwd.
- No changes to ad accounts. This command only reads platforms and asks.
