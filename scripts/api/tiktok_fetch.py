#!/usr/bin/env python3
"""Fetch TikTok Business API data for claude-ads audits.

Capa-2 (direct API) adapter. The output JSON is consumed by the
``audit-tiktok`` agent in place of Ads Manager exports.

## Auth setup (one-time, ~30 min)

1. Apply for TikTok for Business API access at
   https://business-api.tiktok.com/portal/docs?id=1738455508553729
   (you'll need a Business Center account).
2. Create an app in the TikTok Developer Portal. Note the **App ID** and
   **App Secret**.
3. Generate a long-lived access token via the OAuth flow:
   https://business-api.tiktok.com/portal/docs?id=1739965703387137
   The OAuth response gives you ``access_token`` and ``advertiser_ids``
   the user has authorized you to query.
4. Pick the ``advertiser_id`` you want to audit and use it as
   ``--account-id`` to this script.

## Env vars

- ``TIKTOK_ACCESS_TOKEN`` (required) — long-lived TikTok Business API token.
- ``TIKTOK_API_VERSION`` (optional) — defaults to ``v1.3``.

## Usage

    python3 scripts/api/tiktok_fetch.py --account-id 7000000000000000001 -o tiktok-data.json
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

DEFAULT_API_VERSION = "v1.3"
API_BASE = "https://business-api.tiktok.com/open_api"


def _http_get(path: str, params: dict, token: str, version: str) -> dict:
    url = f"{API_BASE}/{version}/{path.lstrip('/')}"
    # TikTok wants JSON-encoded filter/page params as URL params.
    if params:
        encoded = {}
        for k, v in params.items():
            encoded[k] = json.dumps(v) if isinstance(v, (dict, list)) else str(v)
        url += "?" + urllib.parse.urlencode(encoded)
    req = urllib.request.Request(url, headers={
        "Access-Token": token,
        "Content-Type": "application/json",
    })
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
            # TikTok wraps all responses in {"code": 0, "message": "OK", "data": {...}}.
            if payload.get("code") != 0:
                return {"_http_error": {"status": payload.get("code"),
                                        "message": payload.get("message", "")}}
            return payload.get("data", {})
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")[:500]
        return {"_http_error": {"status": e.code, "body": body}}
    except urllib.error.URLError as e:
        return {"_http_error": {"status": None, "message": str(e)}}


def fetch_advertiser_info(advertiser_id: str, token: str, version: str) -> dict:
    return _http_get("advertiser/info/", {"advertiser_ids": [advertiser_id]}, token, version)


def fetch_campaigns(advertiser_id: str, token: str, version: str) -> dict:
    return _http_get("campaign/get/",
                     {"advertiser_id": advertiser_id,
                      "filtering": {"primary_status": "STATUS_ALL"},
                      "page_size": 100}, token, version)


def fetch_adgroups(advertiser_id: str, token: str, version: str) -> dict:
    return _http_get("adgroup/get/",
                     {"advertiser_id": advertiser_id,
                      "filtering": {"primary_status": "STATUS_ALL"},
                      "page_size": 100}, token, version)


def fetch_ads(advertiser_id: str, token: str, version: str) -> dict:
    return _http_get("ad/get/",
                     {"advertiser_id": advertiser_id,
                      "filtering": {"primary_status": "STATUS_ALL"},
                      "page_size": 100}, token, version)


def fetch_pixels(advertiser_id: str, token: str, version: str) -> dict:
    return _http_get("pixel/list/", {"advertiser_id": advertiser_id, "page_size": 100}, token, version)


def fetch_reports(advertiser_id: str, token: str, version: str, since: str, until: str) -> dict:
    return _http_get("report/integrated/get/", {
        "advertiser_id": advertiser_id,
        "service_type": "AUCTION",
        "report_type": "BASIC",
        "data_level": "AUCTION_AD",
        "dimensions": ["ad_id", "stat_time_day"],
        "metrics": ["spend", "impressions", "clicks", "ctr", "cpc", "cpm",
                    "conversion", "cost_per_conversion", "video_play_actions",
                    "video_views_p25", "video_views_p50", "video_views_p75",
                    "video_views_p100", "frequency"],
        "start_date": since,
        "end_date": until,
        "page_size": 100,
    }, token, version)


def _default_dates() -> tuple[str, str]:
    today = dt.date.today()
    return ((today - dt.timedelta(days=28)).isoformat(), today.isoformat())


def main() -> int:
    ap = argparse.ArgumentParser(description="Fetch TikTok Business API data (Capa 2).")
    ap.add_argument("--account-id", required=True, help="TikTok advertiser_id (numeric).")
    since_default, until_default = _default_dates()
    ap.add_argument("--since", default=since_default)
    ap.add_argument("--until", default=until_default)
    ap.add_argument("--what", nargs="+",
                    choices=["all", "advertiser", "campaigns", "adgroups", "ads",
                             "pixels", "reports"],
                    default=["all"])
    ap.add_argument("--output", "-o")
    args = ap.parse_args()

    token = os.environ.get("TIKTOK_ACCESS_TOKEN")
    if not token:
        print("Error: TIKTOK_ACCESS_TOKEN env var is not set.", file=sys.stderr)
        print("See scripts/api/README.md → TikTok for OAuth setup.", file=sys.stderr)
        return 2

    version = os.environ.get("TIKTOK_API_VERSION", DEFAULT_API_VERSION)

    sections = set(args.what)
    if "all" in sections:
        sections = {"advertiser", "campaigns", "adgroups", "ads", "pixels", "reports"}

    result: dict = {
        "platform": "tiktok",
        "account_id": args.account_id,
        "fetched_at": dt.datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "data_source": "direct_api",
        "api_version": version,
        "date_range": {"since": args.since, "until": args.until},
        "errors": [],
    }

    fetchers = {
        "advertiser": lambda: fetch_advertiser_info(args.account_id, token, version),
        "campaigns": lambda: fetch_campaigns(args.account_id, token, version),
        "adgroups": lambda: fetch_adgroups(args.account_id, token, version),
        "ads": lambda: fetch_ads(args.account_id, token, version),
        "pixels": lambda: fetch_pixels(args.account_id, token, version),
        "reports": lambda: fetch_reports(args.account_id, token, version, args.since, args.until),
    }
    for section in sections:
        resp = fetchers[section]()
        if "_http_error" in resp:
            result["errors"].append({"section": section, **resp["_http_error"]})
            result[section] = None
        else:
            # TikTok responses are usually {"list": [...], "page_info": {...}}.
            result[section] = resp.get("list", resp)

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
