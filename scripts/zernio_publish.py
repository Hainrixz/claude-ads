#!/usr/bin/env python3
"""Publish generated creatives to 14+ social networks via Zernio.

This is the runtime for `/ads publish`. It takes the output of `/ads generate`
or `/ads photoshoot` (assets in `ad-assets/`) plus optionally a campaign brief
(captions, scheduling hints), and posts them to the platforms supported by
Zernio: Twitter/X, Instagram, Facebook, LinkedIn, TikTok, YouTube, Pinterest,
Reddit, Bluesky, Threads, Google Business, Telegram, Snapchat, WhatsApp,
Discord.

## Pricing

Zernio has a **free tier for the first 2 connected social accounts** (no
credit card required), then charges per-account/month for additional
accounts:

  Accounts       Price per account / month
  ───────────    ─────────────────────────
  First 2        $0 (free forever)
  3–10           $6
  11–100         $3
  101–2,000      $1
  2,001+         custom

Per Zernio's pricing page: "X/Twitter API costs passed through at exact
X rates. All other platforms fully included." So Twitter/X carries
metered pass-through cost even on the free tier; the other 13 networks
are fully included up to your account quota.

For the typical solo user / single-brand case (Instagram + Facebook =
2 accounts), `/ads publish` is **$0/mo forever**. Agencies managing 3+
client social accounts hit the paid tiers. See https://zernio.com/pricing
for the live calculator.

## Auth setup

1. Sign up at https://zernio.com and pick a plan.
2. Generate an API key in dashboard → API Keys.
3. Connect each social account you want to post to (Zernio handles per-network
   OAuth for you — Twitter/X, Meta, LinkedIn, etc.) via `/connect/{platform}`.
4. Export:

       export ZERNIO_API_KEY='sk_<64-hex-chars>'

## Usage

    # Publish all assets in ad-assets/ to the default platforms
    python3 scripts/zernio_publish.py --assets ad-assets/

    # Specific platforms, scheduled
    python3 scripts/zernio_publish.py \\
        --assets ad-assets/ \\
        --brief campaign-brief.md \\
        --platforms instagram facebook linkedin tiktok \\
        --schedule 2026-05-13T09:00:00Z

    # Dry-run: show what WOULD be posted without calling Zernio
    python3 scripts/zernio_publish.py --assets ad-assets/ --dry-run

## Asset-to-platform matching

The script infers compatible platforms per asset based on the filename's
aspect-ratio hint (e.g. ``hero_9x16.png`` → vertical surfaces):

  9x16 / vertical → Instagram Stories/Reels, TikTok, YouTube Shorts, Snapchat
  1x1  / square   → Instagram Feed, Facebook Feed, LinkedIn, Pinterest
  16x9 / horizontal → Twitter/X, YouTube, LinkedIn, Facebook
  1.91x1 / landscape → LinkedIn Single Image, Facebook link preview

Override with ``--platforms`` to force a specific list.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

ZERNIO_API_BASE = "https://api.zernio.com/v1"

SUPPORTED_PLATFORMS = {
    "twitter", "x", "instagram", "facebook", "linkedin", "tiktok",
    "youtube", "pinterest", "reddit", "bluesky", "threads",
    "google_business", "telegram", "snapchat", "whatsapp", "discord",
}

ASPECT_TO_PLATFORMS = {
    "9x16": {"instagram", "tiktok", "youtube", "snapchat", "facebook"},
    "1x1": {"instagram", "facebook", "linkedin", "pinterest", "x", "twitter"},
    "16x9": {"twitter", "x", "youtube", "linkedin", "facebook"},
    "1.91x1": {"linkedin", "facebook", "x", "twitter"},
}


def _aspect_from_filename(name: str) -> str | None:
    # Common patterns: hero_9x16.png, asset-1x1-v2.jpg, story_1920x1080.mp4
    m = re.search(r"(\d+x\d+|\d+\.\d+x\d+)", name)
    if m:
        token = m.group(1)
        if token in ASPECT_TO_PLATFORMS:
            return token
        # Heuristic for full pixel sizes
        if re.fullmatch(r"\d+x\d+", token):
            w, h = map(int, token.split("x"))
            if h > w * 1.5:
                return "9x16"
            if abs(w - h) < min(w, h) * 0.05:
                return "1x1"
            if w > h * 1.5:
                return "16x9"
    return None


def _parse_brief_captions(brief_path: Path) -> dict[str, str]:
    """Heuristic parser: looks for headers like ``## Instagram caption`` and
    captures the paragraph below. Returns a dict ``{platform: caption}``."""
    if not brief_path.exists():
        return {}
    text = brief_path.read_text(encoding="utf-8")
    captions: dict[str, str] = {}
    current: str | None = None
    buf: list[str] = []
    for line in text.splitlines():
        m = re.match(r"^#{1,4}\s+(\w+).*?caption", line, re.IGNORECASE)
        if m:
            if current and buf:
                captions[current] = "\n".join(buf).strip()
                buf = []
            current = m.group(1).lower()
            continue
        if line.startswith("#"):
            if current and buf:
                captions[current] = "\n".join(buf).strip()
                buf = []
            current = None
            continue
        if current:
            buf.append(line)
    if current and buf:
        captions[current] = "\n".join(buf).strip()
    return captions


def _http_post_json(path: str, body: dict, token: str) -> dict:
    url = f"{ZERNIO_API_BASE}/{path.lstrip('/')}"
    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return {"_http_error": {"status": e.code,
                                "body": e.read().decode("utf-8", "replace")[:500]}}
    except urllib.error.URLError as e:
        return {"_http_error": {"status": None, "message": str(e)}}


def _discover_assets(assets_dir: Path) -> list[Path]:
    if not assets_dir.exists():
        return []
    return sorted(
        p for p in assets_dir.rglob("*")
        if p.is_file() and p.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp", ".mp4", ".mov"}
    )


def main() -> int:
    ap = argparse.ArgumentParser(description="Publish creatives via Zernio (paid).")
    ap.add_argument("--assets", required=True, type=Path,
                    help="Directory with creatives to publish (output of /ads generate or /ads photoshoot).")
    ap.add_argument("--brief", type=Path, default=Path("campaign-brief.md"),
                    help="Markdown brief to extract per-platform captions from.")
    ap.add_argument("--platforms", nargs="+",
                    help="Force a specific platform list. Otherwise inferred from asset aspect ratios.")
    ap.add_argument("--schedule", help="ISO-8601 timestamp to schedule posts (default: post now).")
    ap.add_argument("--dry-run", action="store_true",
                    help="Print what WOULD be posted, don't call Zernio.")
    ap.add_argument("--output", "-o", help="Where to write the JSON result (defaults to stdout).")
    args = ap.parse_args()

    token = os.environ.get("ZERNIO_API_KEY")
    if not token and not args.dry_run:
        print("Error: ZERNIO_API_KEY env var is not set.", file=sys.stderr)
        print("See skills/ads-publish/SKILL.md for auth setup or pass --dry-run.", file=sys.stderr)
        return 2

    if args.platforms:
        unknown = set(args.platforms) - SUPPORTED_PLATFORMS
        if unknown:
            print(f"Warning: unknown Zernio platforms ignored: {sorted(unknown)}", file=sys.stderr)

    assets = _discover_assets(args.assets)
    captions = _parse_brief_captions(args.brief)

    result: dict = {
        "tool": "zernio_publish",
        "ran_at": dt.datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "dry_run": args.dry_run,
        "assets_found": len(assets),
        "captions_parsed": list(captions.keys()),
        "schedule": args.schedule,
        "planned": [],
        "published": [],
        "errors": [],
    }

    for asset in assets:
        aspect = _aspect_from_filename(asset.name)
        inferred = ASPECT_TO_PLATFORMS.get(aspect or "", set())
        targets = set(args.platforms) if args.platforms else inferred
        targets = targets & SUPPORTED_PLATFORMS
        if not targets:
            result["errors"].append({"asset": str(asset), "reason": "no compatible platforms found",
                                     "aspect_hint": aspect})
            continue

        for platform in sorted(targets):
            caption = captions.get(platform) or captions.get("default") or ""
            plan = {
                "asset": str(asset),
                "platform": platform,
                "caption_chars": len(caption),
                "scheduled_at": args.schedule,
            }
            result["planned"].append(plan)

            if args.dry_run:
                continue

            body = {
                "platform": platform,
                "media_path": str(asset.resolve()),
                "caption": caption,
                **({"scheduled_at": args.schedule} if args.schedule else {}),
            }
            resp = _http_post_json("posts", body, token)
            if "_http_error" in resp:
                result["errors"].append({"asset": str(asset), "platform": platform,
                                         **resp["_http_error"]})
            else:
                result["published"].append({
                    "asset": str(asset),
                    "platform": platform,
                    "post_id": resp.get("id"),
                    "status": resp.get("status"),
                    "scheduled_at": resp.get("scheduled_at") or args.schedule,
                })

    payload = json.dumps(result, indent=2, default=str)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(payload)
        print(f"Wrote {args.output}", file=sys.stderr)
    else:
        print(payload)

    return 0 if not result["errors"] else 1


if __name__ == "__main__":
    sys.exit(main())
