# Setup: Meta for Developers account (prerequisite for Meta direct API)

Loaded by `/ads start` Phase D.1 when the user picks Meta direct-API tier
but doesn't yet have a Meta for Developers account.

After completing this walkthrough, return to **`setup-meta.md` Section B** to
finish creating the User Token + System User Token + verifying with
`meta_fetch.py`.

Effort: ~5–10 min including phone verification.

---

## STEP 1 — Go to the developer portal
- **Goal**: open the right onboarding page.
- **Do this**: https://developers.facebook.com → **Get Started** (top right)
  → **Continue as <Facebook user>** (uses the user's existing Facebook
  account; no separate dev account needed).
- **Expect to see**: a "Welcome, developer" landing page.
- **On error**: blank page → log out of Facebook, log back in, then retry.

## STEP 2 — Accept developer policies
- **Goal**: agree to platform terms.
- **Do this**: read + check both boxes (Platform Policy, Developer Policies)
  → **Continue**.
- **Expect to see**: redirect to phone/email verification.

## STEP 3 — Verify phone number
- **Goal**: Meta requires a verified phone for app creation.
- **Do this**: enter mobile number → receive SMS code → enter it.
- **Expect to see**: ✓ phone verified.
- **On error**: SMS doesn't arrive → use a different number; some VOIP
  numbers are blocked. WhatsApp Business numbers work.

## STEP 4 — Pick the "Developer" role (not "Marketer")
- **Goal**: select the right account type.
- **Do this**: when prompted "How will you use Meta for Developers?", pick
  **Developer** (or "Other" → "Developer"). NOT "Marketer" — that's a
  different track without API access.
- **Expect to see**: developer dashboard at developers.facebook.com/apps.

## STEP 5 — Create the first app
- **Goal**: an app shell to add the Marketing API to.
- **Do this**: **My Apps** → **Create App** → use case **Other** → app type
  **Business** → app name "claude-ads" (or any name) → **Create app** →
  enter Facebook password to confirm.
- **Expect to see**: app dashboard with empty product list.
- **On error**:
  - "Consumer" auto-selected and won't let you switch → start over with a
    fresh app; some accounts default oddly.
  - "Business app type unavailable" → user's Facebook account is too new
    (<60 days). Add a Business Manager first at business.facebook.com,
    then retry.

## STEP 6 — Add Marketing API product
- **Goal**: enable the API endpoints `meta_fetch.py` calls.
- **Do this**: in app dashboard → left nav **Add Product** → find
  **Marketing API** → **Set Up**.
- **Expect to see**: Marketing API now in left nav.
- **On error**: "App must be associated with a Business" → in app Settings →
  Basic → assign a Business in the Business Account dropdown.

## STEP 7 — Note App ID + App Secret
- **Goal**: save credentials needed in `setup-meta.md` Step B3.
- **Do this**: app dashboard → Settings → Basic → copy **App ID** (numeric)
  + **App Secret** (click "Show", paste password, copy).
- **Expect to see**: both values saved to a vault / password manager.
- **On error**: "Show" button greyed → user isn't an app admin (only Tester);
  switch roles or use a different Facebook account.

## STEP 8 — Confirm Business Manager link
- **Goal**: ensure the app can act on a real ad account.
- **Do this**: business.facebook.com → Business Settings → Accounts → **Ad
  Accounts**. The ad account the user wants to audit MUST be listed here.
  If not, **Add** → Add an Ad Account → enter the `act_<id>`.
- **Expect to see**: the ad account in the list, status Connected.
- **On error**: "You don't own this ad account" → ad account owner must
  share it via Business Manager → People → Add Partner.

---

## What's next

Back to **`setup-meta.md` Section B Step B2** — generate the User Token in
Graph API Explorer, then proceed through B3–B5 to verify.

The numbers / strings to keep from this walkthrough:

| Field | Where used later |
|-------|------------------|
| App ID | `setup-meta.md` Step B3 (token exchange) |
| App Secret | `setup-meta.md` Step B3 (token exchange) |
| Business name | confirmation only |
| Ad account `act_<id>` | every `meta_fetch.py` call |

---

## Troubleshooting summary

| Symptom | Cause | Fix |
|---------|-------|-----|
| Phone verification fails | VOIP number blocked | Use a real mobile / WhatsApp Business number |
| Can't select "Business" app type | New Facebook account (<60 days) | Add a Business Manager first |
| App Secret "Show" greyed out | Logged-in user is Tester, not Admin | Switch to admin user |
| Marketing API not appearing in product list | App not associated with a Business | Set Business in Settings → Basic |
