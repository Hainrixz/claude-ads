<!-- Portions Copyright (c) 2026 Enrique Rocha (@soyenriquerocha) - see LICENSE for original authors · tododeia.com · id er-fd4fa55b -->
# Campaign Awareness (Conciencia de campaña) — Formulas & Reading Guide

Loaded by `/ads conciencia`, `/ads audit` (when awareness files exist) and
`/ads next`. Data lives in `~/.claude-ads/conciencia/*.json`
(`conciencia-schema.json`), computed by `scripts/conciencia.py show`.

## Why it exists

For lead / message / call / form campaigns, the platform's "result" is a
contact, not a sale. A low CPL can hide a campaign that closes nothing, and a
"expensive" CPL can hide the best campaign in the account. The only source for
the close is the user — so Claude asks, stores it with a date, and never
assumes it.

Not needed when a purchase pixel tracks the sale (e-commerce): the platform
already sees revenue. Those campaigns use `tracking_mode: pixel` and are never
flagged as due.

## The funnel

```
clicks ─▶ platform messages/leads ─▶ real conversations ─▶ qualified ─▶ closed ─▶ revenue
 (platform)        (platform)              (user)            (user)      (user)    (user)
```

## Formulas

All ratios are summed **only over check-ins where both sides were reported**.
Each metric carries `checkins` = how many check-ins it rests on. Cite it.

| Metric | Formula | Answers |
|---|---|---|
| `click_to_message_rate` | messages / clicks | Does the ad + landing convert to a contact? |
| `platform_vs_real` | conversations / messages | Are the platform's "messages" real people? |
| `qualification_rate` | qualified / conversations | Is targeting bringing the right people? |
| `close_rate` | closed / conversations | **Real success rate of the campaign.** |
| `close_rate_qualified` | closed / qualified | Is the sales process closing good leads? |
| `junk_rate` | junk / conversations | Share of garbage contacts. |
| `cost_per_conversation` | spend / conversations | True cost per contact. |
| `cost_per_close` | spend / closed | True customer acquisition cost. |
| `real_roas` | revenue / spend | Reported return. |
| `estimated_roas` | closed × ticket_value / spend | Return when revenue isn't reported. Label it "estimated". |

`trend` compares the latest check-in with the previous one for `close_rate`,
`junk_rate` and `cost_per_close` (null if either side is missing).

## Reading the cross-reference

Combine the platform verdict (from the latest audit or platform CPL) with the
business verdict (from check-ins):

| Platform says | Business says | Reading | First move |
|---|---|---|---|
| Good (cheap CPL) | Bad (low close, high junk) | **Cheap junk.** The algorithm is optimizing for the easiest contact, not a buyer. | Tighten the qualifier: optimize for a deeper event (qualified lead via CAPI / offline conversions), add friction (form questions, price in copy). |
| Bad (expensive CPL) | Good (healthy close, cost_per_close fits margin) | **Expensive but profitable.** Don't kill it on CPL. | Protect it. Judge by cost_per_close vs ticket, not CPL. |
| Good | Good | Working. | Scale gradually (+20 % budget steps), keep check-ins. |
| Bad | Bad | Not working end to end. | Fix tracking first, then offer / audience. |
| Any | Unknown | **Blind.** | Get the first check-in before any optimization verdict. |

Gaps worth naming explicitly:

- `platform_vs_real` well below 1 → the platform counts conversations that
  never became real (bots, accidental taps, "hola" with no reply). Check
  message-start optimization vs. replies.
- `qualification_rate` low but `close_rate_qualified` healthy → audience
  problem, not sales problem.
- `qualification_rate` healthy but `close_rate_qualified` low → sales / follow-up
  problem (response time, price, offer), not an ads problem. Say so: the
  campaign can't fix it.

## Thresholds

There is **no universal benchmark** for close rate — it depends on ticket,
industry and the user's sales process. Rules:

1. The primary benchmark is the user's own history: compare against the
   previous check-ins of this campaign and their other campaigns.
2. The hard economic test is `cost_per_close` vs. what one customer is worth
   (`ticket_value`, or margin if the user gives it). If `cost_per_close` >
   ticket value → flag as losing money, citing both numbers.
3. Working heuristics (not industry data — say so when using them):
   `junk_rate` > 50 % → lead-quality problem worth prioritizing;
   `platform_vs_real` < 0.6 → platform over-counting contacts;
   a `close_rate` drop of more than half vs the previous check-in → regression.
4. With only 1 check-in, present numbers as a first reading, not a verdict.

## How other commands use it

- **`/ads` (any command):** runs `conciencia.py due` after the profile check;
  overdue campaigns → ask the check-in first (now / later → snooze 1 day).
- **`/ads audit`:** for audited lead / message campaigns with an awareness
  file, include `close_rate`, `cost_per_close`, `junk_rate` (with check-in
  counts) in the summary next to platform CPL. Without one, the business
  outcome is `N/A` and the audit offers `/ads conciencia registrar`.
- **`/ads next`:** turns `junk_rate` > 50 %, `cost_per_close` > ticket and
  close-rate regressions into ranked items; campaigns with no check-in yet
  produce a low-effort "register business results" item.
