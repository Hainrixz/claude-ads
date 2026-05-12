#!/usr/bin/env python3
"""Fetch Google Ads API data via GAQL for claude-ads audits.

Capa-2 (direct API) adapter. The output JSON is consumed by the
``audit-google`` agent in place of manual exports / Change History downloads.

## Auth setup (one-time, ~1-3 business days for the developer-token approval)

1. Create or use an existing Google Ads MCC (manager) account.
2. Apply for API access:
   https://developers.google.com/google-ads/api/docs/access-levels#access-level
   You'll get a **developer token** (initial level: Test → request Basic/Standard).
3. Create an OAuth 2.0 client in Google Cloud Console for application type
   "Desktop". Note the **client_id** and **client_secret**.
4. Generate a **refresh_token** using the OAuth Playground or the
   ``google-ads-python`` ``generate_user_credentials.py`` script. Scope:
   ``https://www.googleapis.com/auth/adwords``.
5. Find your **customer_id** (the 10-digit number under the MCC, or directly
   under a child account). Strip dashes (``123-456-7890`` → ``1234567890``).
6. Export env vars (see "Env vars" below).

## Env vars

- ``GOOGLE_ADS_DEVELOPER_TOKEN`` (required) — from step 2.
- ``GOOGLE_ADS_CLIENT_ID`` (required) — OAuth client ID.
- ``GOOGLE_ADS_CLIENT_SECRET`` (required) — OAuth client secret.
- ``GOOGLE_ADS_REFRESH_TOKEN`` (required) — long-lived OAuth refresh token.
- ``GOOGLE_ADS_LOGIN_CUSTOMER_ID`` (optional) — MCC customer ID without dashes
  (only needed if your refresh-token user accesses the account through an MCC).
- ``GOOGLE_ADS_API_VERSION`` (optional) — defaults to ``v18``.

## Usage

    python3 scripts/api/google_fetch.py --account-id 1234567890 -o google-data.json

    # Just campaigns + search-terms report:
    python3 scripts/api/google_fetch.py --account-id 1234567890 \\
        --what campaigns search_terms

The script issues one GAQL query per requested section. All errors are
captured in the output JSON's ``errors`` array rather than raised, so the
audit agent always gets a parseable file.
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

DEFAULT_API_VERSION = "v18"
OAUTH_TOKEN_URL = "https://oauth2.googleapis.com/token"
ADS_API_BASE = "https://googleads.googleapis.com"

# Each entry: (section_key, GAQL query). Date filters are injected via _date_filter().
QUERIES: dict[str, str] = {
    "campaigns": """
        SELECT campaign.id, campaign.name, campaign.status, campaign.advertising_channel_type,
               campaign.advertising_channel_sub_type, campaign.bidding_strategy_type,
               campaign.serving_status, campaign.start_date, campaign.end_date,
               campaign_budget.amount_micros, campaign_budget.delivery_method
        FROM campaign
        WHERE campaign.status != 'REMOVED'
    """,
    "ad_groups": """
        SELECT ad_group.id, ad_group.name, ad_group.campaign, ad_group.status,
               ad_group.type, ad_group.cpc_bid_micros, ad_group.cpm_bid_micros,
               ad_group.target_cpa_micros, ad_group.target_roas
        FROM ad_group
        WHERE ad_group.status != 'REMOVED'
    """,
    "keywords": """
        SELECT ad_group_criterion.criterion_id, ad_group_criterion.keyword.text,
               ad_group_criterion.keyword.match_type, ad_group_criterion.ad_group,
               ad_group_criterion.status, ad_group_criterion.quality_info.quality_score,
               ad_group_criterion.quality_info.creative_quality_score,
               ad_group_criterion.quality_info.post_click_quality_score,
               ad_group_criterion.quality_info.search_predicted_ctr,
               metrics.impressions, metrics.clicks, metrics.cost_micros,
               metrics.conversions
        FROM keyword_view
        WHERE ad_group_criterion.status != 'REMOVED'
          AND segments.date BETWEEN '__SINCE__' AND '__UNTIL__'
    """,
    "search_terms": """
        SELECT search_term_view.search_term, search_term_view.status,
               campaign.id, ad_group.id,
               metrics.impressions, metrics.clicks, metrics.cost_micros,
               metrics.conversions, metrics.ctr
        FROM search_term_view
        WHERE segments.date BETWEEN '__SINCE__' AND '__UNTIL__'
        ORDER BY metrics.cost_micros DESC
        LIMIT 1000
    """,
    "conversion_actions": """
        SELECT conversion_action.id, conversion_action.name,
               conversion_action.type, conversion_action.status,
               conversion_action.category, conversion_action.primary_for_goal,
               conversion_action.click_through_lookback_window_days,
               conversion_action.view_through_lookback_window_days,
               conversion_action.attribution_model_settings.attribution_model,
               conversion_action.counting_type,
               conversion_action.value_settings.default_value
        FROM conversion_action
        WHERE conversion_action.status != 'REMOVED'
    """,
    "ads": """
        SELECT ad_group_ad.ad.id, ad_group_ad.ad.name, ad_group_ad.ad.type,
               ad_group_ad.ad.responsive_search_ad.headlines,
               ad_group_ad.ad.responsive_search_ad.descriptions,
               ad_group_ad.ad.responsive_search_ad.path1,
               ad_group_ad.ad.responsive_search_ad.path2,
               ad_group_ad.ad.final_urls, ad_group_ad.ad_strength,
               ad_group_ad.ad_group, ad_group_ad.status
        FROM ad_group_ad
        WHERE ad_group_ad.status != 'REMOVED'
    """,
    "asset_groups": """
        SELECT asset_group.id, asset_group.name, asset_group.campaign,
               asset_group.status, asset_group.ad_strength,
               asset_group.final_urls
        FROM asset_group
        WHERE asset_group.status != 'REMOVED'
    """,
    "campaign_metrics": """
        SELECT campaign.id, campaign.name,
               metrics.impressions, metrics.clicks, metrics.cost_micros,
               metrics.conversions, metrics.conversions_value, metrics.ctr,
               metrics.search_impression_share, metrics.search_top_impression_share,
               metrics.search_absolute_top_impression_share,
               metrics.search_budget_lost_impression_share
        FROM campaign
        WHERE segments.date BETWEEN '__SINCE__' AND '__UNTIL__'
          AND campaign.status != 'REMOVED'
    """,
}


def _exchange_refresh_token(client_id: str, client_secret: str, refresh_token: str) -> tuple[str, str | None]:
    """Returns (access_token, error_message). One is non-None."""
    body = urllib.parse.urlencode({
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token,
        "grant_type": "refresh_token",
    }).encode("utf-8")
    req = urllib.request.Request(
        OAUTH_TOKEN_URL,
        data=body,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
            return payload.get("access_token", ""), None
    except urllib.error.HTTPError as e:
        return "", f"OAuth refresh failed: HTTP {e.code} {e.read().decode('utf-8', 'replace')[:300]}"
    except urllib.error.URLError as e:
        return "", f"OAuth refresh failed: {e}"


def _run_query(api: str, customer_id: str, query: str, headers: dict[str, str]) -> dict:
    url = f"{ADS_API_BASE}/{api}/customers/{customer_id}/googleAds:search"
    req = urllib.request.Request(
        url,
        data=json.dumps({"query": query}).encode("utf-8"),
        headers={**headers, "Content-Type": "application/json", "Accept": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return {"_http_error": {"status": e.code, "body": e.read().decode("utf-8", "replace")[:500]}}
    except urllib.error.URLError as e:
        return {"_http_error": {"status": None, "message": str(e)}}


def _default_dates() -> tuple[str, str]:
    today = dt.date.today()
    return ((today - dt.timedelta(days=28)).isoformat(), today.isoformat())


def main() -> int:
    ap = argparse.ArgumentParser(description="Fetch Google Ads API data via GAQL (Capa 2).")
    ap.add_argument("--account-id", required=True,
                    help="10-digit customer ID without dashes (e.g. 1234567890).")
    since_default, until_default = _default_dates()
    ap.add_argument("--since", default=since_default, help="ISO date (default: 28 days ago).")
    ap.add_argument("--until", default=until_default, help="ISO date (default: today).")
    ap.add_argument("--what", nargs="+",
                    choices=["all"] + list(QUERIES.keys()),
                    default=["all"], help="Sections to fetch.")
    ap.add_argument("--output", "-o", help="Output JSON file. Defaults to stdout.")
    args = ap.parse_args()

    required_envs = ["GOOGLE_ADS_DEVELOPER_TOKEN", "GOOGLE_ADS_CLIENT_ID",
                     "GOOGLE_ADS_CLIENT_SECRET", "GOOGLE_ADS_REFRESH_TOKEN"]
    missing = [v for v in required_envs if not os.environ.get(v)]
    if missing:
        print(f"Error: missing env vars: {', '.join(missing)}", file=sys.stderr)
        print("See scripts/api/README.md → Google for OAuth setup.", file=sys.stderr)
        return 2

    api = os.environ.get("GOOGLE_ADS_API_VERSION", DEFAULT_API_VERSION)
    access_token, err = _exchange_refresh_token(
        os.environ["GOOGLE_ADS_CLIENT_ID"],
        os.environ["GOOGLE_ADS_CLIENT_SECRET"],
        os.environ["GOOGLE_ADS_REFRESH_TOKEN"],
    )
    if err:
        print(f"Error: {err}", file=sys.stderr)
        return 3

    headers = {
        "Authorization": f"Bearer {access_token}",
        "developer-token": os.environ["GOOGLE_ADS_DEVELOPER_TOKEN"],
    }
    login_cid = os.environ.get("GOOGLE_ADS_LOGIN_CUSTOMER_ID")
    if login_cid:
        headers["login-customer-id"] = login_cid

    sections = set(args.what)
    if "all" in sections:
        sections = set(QUERIES.keys())

    result: dict = {
        "platform": "google",
        "account_id": args.account_id,
        "fetched_at": dt.datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "data_source": "direct_api",
        "api_version": api,
        "date_range": {"since": args.since, "until": args.until},
        "errors": [],
    }

    for section in sections:
        query = QUERIES[section].strip()
        query = query.replace("__SINCE__", args.since).replace("__UNTIL__", args.until)
        resp = _run_query(api, args.account_id, query, headers)
        if "_http_error" in resp:
            result["errors"].append({"section": section, **resp["_http_error"]})
            result[section] = []
        else:
            result[section] = resp.get("results", [])

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
