---
name: ads-publish
description: "Publish generated ad creatives to 14+ social networks via the Zernio API. Optional paid layer that closes the loop after /ads generate or /ads photoshoot. Use when user says publish, schedule, post, ship, Zernio, distribute, send to socials, push to Instagram/Facebook/LinkedIn/TikTok/Twitter, or auto-publish."
user-invokable: false
argument-hint: "[<platforms>] [--schedule <ISO-8601>] [--dry-run]"
allowed-tools: Bash, Read, Write, AskUserQuestion
---

# `/ads publish` — Push creatives to socials via Zernio

> **Pricing:** Zernio is **free for the first 2 connected social accounts** (no
> credit card). Solo users posting to Instagram + Facebook = $0/mo forever.
> Agencies pay $1–$6/mo per additional account (see "Pricing tiers" below).
> X/Twitter API costs are metered pass-through even on the free tier; all
> other 13 networks are fully included up to your account quota.

## When to use this

After `/ads generate` (image ad creatives) or `/ads photoshoot` (product
photography) produces an `ad-assets/` directory, `/ads publish` takes those
files and schedules them as posts on every social network you've connected
in Zernio. Supported: Twitter/X · Instagram · Facebook · LinkedIn · TikTok ·
YouTube · Pinterest · Reddit · Bluesky · Threads · Google Business ·
Telegram · Snapchat · WhatsApp · Discord.

## Process

1. **Verify prerequisites.** Confirm:
   - `ZERNIO_API_KEY` is set (see "Auth setup" below).
   - `ad-assets/` exists or the user passed `--assets <dir>`.
   - Optionally, `campaign-brief.md` exists (the script will extract per-platform captions from it).
2. **Discover assets.** List images and videos in the assets directory. For each, infer compatible platforms from the filename aspect-ratio hint (`9x16`, `1x1`, `16x9`, `1.91x1`).
3. **Plan the publication.** Show the user a table: per asset, which platforms it would go to, the caption length, and the scheduling time. Ask the user to confirm before calling Zernio (unless `--dry-run`). **If `twitter` or `x` is in the target platforms list, surface the X/Twitter pass-through cost note before posting** — those posts incur metered Twitter API charges on top of any Zernio tier; the other 13 networks are free up to the account quota.
4. **Call `scripts/zernio_publish.py`.** Use Bash with the user's selected platforms and the optional `--schedule` flag.
5. **Report results.** Read the JSON output, show what was published vs. errored, and surface any rate-limit or auth issues clearly. If anything was scheduled (vs. posted immediately), remind the user of when posts will go live.

## Auth setup

1. Sign up at https://zernio.com — **first 2 accounts are always free, no credit card**. Confirm at https://zernio.com/pricing.
2. Dashboard → API Keys → create a key (`sk_<64-hex-chars>`). Keys are shown once.
3. For each social network you want to publish to, complete the OAuth flow in Zernio's dashboard at `/connect/<platform>`. Zernio handles the per-network OAuth — you don't need to manage Twitter/Meta/LinkedIn tokens yourself. Each social network you connect counts as one of your "accounts" toward the free quota.
4. Export:
   ```bash
   export ZERNIO_API_KEY='sk_...'
   ```

## Pricing tiers

| Accounts connected | Price per account / month |
|---|---|
| **First 2** | **$0 (free forever)** |
| 3–10 | $6 |
| 11–100 | $3 |
| 101–2,000 | $1 |
| 2,001+ | Custom |

**Important caveat:** X/Twitter API costs are metered pass-through at
X's published rates regardless of your Zernio tier. All other 13
platforms (Instagram, Facebook, LinkedIn, TikTok, YouTube, Pinterest,
Reddit, Bluesky, Threads, Google Business, Telegram, Snapchat,
WhatsApp, Discord) are fully included.

## Without Zernio (alternative for 3+ accounts)

The free 2-account quota covers the typical solo user. If you manage
3+ social accounts (an agency setup) and don't want to pay Zernio's
per-account fee, run `/ads publish --dry-run` to get the **plan**
(which asset goes to which network with which caption) and then
publish manually using each platform's native scheduler:

- Meta Business Suite: free, supports Facebook + Instagram scheduling.
- LinkedIn Page Posts → schedule from the composer.
- TikTok Business Suite: free scheduling for organic posts.
- Buffer / Hootsuite free tiers: limited but functional.

Same plan, zero recurring cost — just more clicks per post.

## Asset-to-platform matching

| Aspect | Platforms |
|--------|-----------|
| 9:16 (vertical) | Instagram Stories/Reels, TikTok, YouTube Shorts, Snapchat, Facebook Stories |
| 1:1 (square) | Instagram Feed, Facebook Feed, LinkedIn, Pinterest, X/Twitter |
| 16:9 (horizontal) | YouTube, X/Twitter, LinkedIn, Facebook |
| 1.91:1 (landscape) | LinkedIn Single Image, Facebook link previews |

The script reads the filename's aspect token (e.g. `hero_9x16.png`,
`product_1x1.jpg`) to decide. Override with `--platforms <list>`.

## Caption extraction from brief

If `campaign-brief.md` exists, the script parses sections like
`## Instagram caption`, `## TikTok caption`, etc. and uses each as the
caption for that platform. A `## Default caption` section is used as
fallback for any platform without a specific one.

## Output

`/ads publish` writes a JSON report (`publish-results.json`) with:

```json
{
  "tool": "zernio_publish",
  "dry_run": false,
  "assets_found": 5,
  "captions_parsed": ["instagram", "facebook", "linkedin", "default"],
  "planned": [
    {"asset": "ad-assets/hero_9x16.png", "platform": "instagram", "scheduled_at": "..."}
  ],
  "published": [
    {"asset": "...", "platform": "instagram", "post_id": "...", "status": "scheduled"}
  ],
  "errors": []
}
```

Use it to verify what landed and what didn't.

## Quality gates

- Never publish without explicit user confirmation unless `--yes` was passed.
- If `--schedule` is in the past, refuse and prompt for a future timestamp.
- If the caption exceeds the platform's limit (X: 280, LinkedIn: 3000, etc.),
  show a warning before posting.
- Per asset: cap to ≤5 platforms per `/ads publish` invocation by default
  (avoids burning Zernio quota on large directories accidentally).
