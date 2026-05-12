#!/usr/bin/env python3
"""Fetch Meta (Facebook + Instagram) Marketing API data for claude-ads audits.

Capa-2 (direct API) adapter. The output JSON is consumed by the ``audit-meta``
agent in place of manual Ads Manager exports.

## Auth setup (one-time, ~5 minutes)

1. Open https://developers.facebook.com → My Apps → create a Business app.
2. Add the **Marketing API** product to the app.
3. In Graph API Explorer, request a User Token with these permissions:
   ``ads_read``, ``ads_management`` (read-only is fine), ``business_management``.
4. (Recommended) Convert to a long-lived (60-day) token:
   ``GET https://graph.facebook.com/v22.0/oauth/access_token?grant_type=fb_exchange_token&client_id=<APP_ID>&client_secret=<APP_SECRET>&fb_exchange_token=<SHORT_TOKEN>``
5. For unattended use, create a System User in Business Settings and
   generate a System User token (no expiry).
6. Export the token:
   ``export META_ACCESS_TOKEN='EAA...'``

Find your ``ad_account_id`` in Ads Manager URL: ``act_<numeric>`` (use the
full ``act_...`` prefix when invoking this script).

## Env vars

- ``META_ACCESS_TOKEN`` (required) — user, app, or system-user token.
- ``META_API_VERSION`` (optional) — defaults to ``v22.0``.
- ``META_PIXEL_ID`` (optional) — if set, the script fetches pixel diagnostics
  alongside ad-account data.

## Usage

    python3 scripts/api/meta_fetch.py --account-id act_123 -o meta-data.json

    # Last 14 days only:
    python3 scripts/api/meta_fetch.py --account-id act_123 \\
        --since 2026-04-28 --until 2026-05-12

    # Just fetch campaigns + ad sets:
    python3 scripts/api/meta_fetch.py --account-id act_123 --what campaigns adsets

The output JSON validates ad-hoc (no formal schema yet); top-level keys are
stable: ``platform``, ``account_id``, ``fetched_at``, ``data_source``,
``date_range``, plus the requested sections.
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

DEFAULT_API_VERSION = "v22.0"
GRAPH_BASE = "https://graph.facebook.com"

CAMPAIGN_FIELDS = (
    "id,name,objective,status,bid_strategy,daily_budget,lifetime_budget,"
    "buying_type,special_ad_categories,start_time,stop_time,created_time,updated_time"
)
ADSET_FIELDS = (
    "id,name,campaign_id,status,daily_budget,lifetime_budget,bid_strategy,"
    "billing_event,optimization_goal,attribution_spec,targeting,"
    "learning_stage_info,start_time,end_time,created_time"
)
AD_FIELDS = "id,name,adset_id,campaign_id,status,creative{id,name,object_type,thumbnail_url},created_time"
INSIGHTS_FIELDS = (
    "campaign_id,campaign_name,adset_id,adset_name,ad_id,ad_name,"
    "spend,impressions,clicks,ctr,cpc,cpm,reach,frequency,"
    "actions,action_values,quality_ranking,engagement_rate_ranking,"
    "conversion_rate_ranking"
)


def _http_get(path: str, params: dict[str, str], token: str) -> dict:
    params = {**params, "access_token": token}
    url = f"{GRAPH_BASE}/{path.lstrip('/')}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        try:
            err = json.loads(body)
        except ValueError:
            err = {"raw": body}
        return {"_http_error": {"status": e.code, "message": str(e), "body": err}}
    except urllib.error.URLError as e:
        return {"_http_error": {"status": None, "message": str(e)}}


def _paginate(path: str, params: dict[str, str], token: str, max_pages: int = 20) -> list[dict]:
    """Walk Graph API cursor pagination. Returns a flat ``data`` list."""
    items: list[dict] = []
    next_url: str | None = None
    page = 0
    while page < max_pages:
        if next_url is None:
            resp = _http_get(path, params, token)
        else:
            # next_url already contains query string + access_token.
            req = urllib.request.Request(next_url, headers={"Accept": "application/json"})
            try:
                with urllib.request.urlopen(req, timeout=30) as r:
                    resp = json.loads(r.read().decode("utf-8"))
            except (urllib.error.HTTPError, urllib.error.URLError) as e:
                return items + [{"_http_error": str(e)}]
        if "_http_error" in resp:
            items.append(resp)
            break
        items.extend(resp.get("data", []) or [])
        next_url = (resp.get("paging") or {}).get("next")
        if not next_url:
            break
        page += 1
    return items


def fetch_account(api: str, account_id: str, token: str) -> dict:
    fields = (
        "id,name,account_id,account_status,currency,timezone_name,"
        "amount_spent,balance,business_country_code,disable_reason,owner"
    )
    return _http_get(f"{api}/{account_id}", {"fields": fields}, token)


def fetch_campaigns(api: str, account_id: str, token: str) -> list[dict]:
    return _paginate(f"{api}/{account_id}/campaigns", {"fields": CAMPAIGN_FIELDS, "limit": "100"}, token)


def fetch_adsets(api: str, account_id: str, token: str) -> list[dict]:
    return _paginate(f"{api}/{account_id}/adsets", {"fields": ADSET_FIELDS, "limit": "100"}, token)


def fetch_ads(api: str, account_id: str, token: str) -> list[dict]:
    return _paginate(f"{api}/{account_id}/ads", {"fields": AD_FIELDS, "limit": "100"}, token)


def fetch_custom_audiences(api: str, account_id: str, token: str) -> list[dict]:
    fields = "id,name,subtype,approximate_count_lower_bound,approximate_count_upper_bound,delivery_status"
    return _paginate(f"{api}/{account_id}/customaudiences", {"fields": fields, "limit": "100"}, token)


def fetch_insights(api: str, account_id: str, token: str, since: str, until: str, level: str = "ad") -> list[dict]:
    params = {
        "level": level,
        "fields": INSIGHTS_FIELDS,
        "time_range": json.dumps({"since": since, "until": until}),
        "limit": "100",
    }
    return _paginate(f"{api}/{account_id}/insights", params, token)


def fetch_pixel(api: str, pixel_id: str, token: str) -> dict:
    fields = "id,name,last_fired_time,creation_time,is_unavailable,code"
    return _http_get(f"{api}/{pixel_id}", {"fields": fields}, token)


def _default_dates() -> tuple[str, str]:
    today = dt.date.today()
    return ((today - dt.timedelta(days=28)).isoformat(), today.isoformat())


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Fetch Meta Marketing API data for claude-ads audits (Capa 2)."
    )
    ap.add_argument("--account-id", required=True, help="Ad account ID in ``act_<digits>`` form.")
    since_default, until_default = _default_dates()
    ap.add_argument("--since", default=since_default, help="ISO date inclusive (default: 28 days ago).")
    ap.add_argument("--until", default=until_default, help="ISO date inclusive (default: today).")
    ap.add_argument("--what", nargs="+",
                    choices=["all", "account", "campaigns", "adsets", "ads",
                             "audiences", "insights", "pixel"],
                    default=["all"],
                    help="Which sections to fetch. Default ``all``.")
    ap.add_argument("--output", "-o", help="Output JSON file. Defaults to stdout.")
    args = ap.parse_args()

    token = os.environ.get("META_ACCESS_TOKEN")
    if not token:
        print("Error: META_ACCESS_TOKEN env var is not set.", file=sys.stderr)
        print("See scripts/api/README.md → Meta for OAuth setup.", file=sys.stderr)
        return 2

    api = os.environ.get("META_API_VERSION", DEFAULT_API_VERSION)
    pixel_id = os.environ.get("META_PIXEL_ID")

    if not args.account_id.startswith("act_"):
        print(f"Warning: account-id {args.account_id!r} does not start with 'act_'; "
              "the Marketing API typically requires the act_ prefix.", file=sys.stderr)

    sections = set(args.what)
    if "all" in sections:
        sections = {"account", "campaigns", "adsets", "ads", "audiences", "insights", "pixel"}

    result: dict = {
        "platform": "meta",
        "account_id": args.account_id,
        "fetched_at": dt.datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "data_source": "direct_api",
        "api_version": api,
        "date_range": {"since": args.since, "until": args.until},
        "errors": [],
    }

    def _record(key: str, payload):
        if isinstance(payload, dict) and "_http_error" in payload:
            result["errors"].append({"section": key, **payload["_http_error"]})
        elif isinstance(payload, list):
            errs = [p for p in payload if isinstance(p, dict) and "_http_error" in p]
            if errs:
                for e in errs:
                    result["errors"].append({"section": key, **(e.get("_http_error") or e)})
                payload = [p for p in payload if not (isinstance(p, dict) and "_http_error" in p)]
        result[key] = payload

    if "account" in sections:
        _record("account", fetch_account(api, args.account_id, token))
    if "campaigns" in sections:
        _record("campaigns", fetch_campaigns(api, args.account_id, token))
    if "adsets" in sections:
        _record("adsets", fetch_adsets(api, args.account_id, token))
    if "ads" in sections:
        _record("ads", fetch_ads(api, args.account_id, token))
    if "audiences" in sections:
        _record("customaudiences", fetch_custom_audiences(api, args.account_id, token))
    if "insights" in sections:
        _record("insights", fetch_insights(api, args.account_id, token, args.since, args.until))
    if "pixel" in sections and pixel_id:
        _record("pixel", fetch_pixel(api, pixel_id, token))
    elif "pixel" in sections:
        result["pixel"] = None
        result["errors"].append({"section": "pixel", "message": "META_PIXEL_ID env var not set; skipped pixel fetch."})

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
