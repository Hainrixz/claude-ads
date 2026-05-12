# Bidding Strategy Decision Trees — Index

Bidding decision trees are split per-platform to keep each file under the 200-line reference budget. Load only what you need:

| Platform | File |
|----------|------|
| Google Ads (strategy flow, Smart Bidding Exploration, AI Max, attribution, portfolios) | [`bidding-google.md`](bidding-google.md) |
| Meta Ads (auction, Lowest Cost/Cost Cap/Bid Cap, Andromeda, CBO/ABO, learning phase) | [`bidding-meta.md`](bidding-meta.md) |
| TikTok Ads (Smart+, GMV Max, learning phase, cross-platform red flags) | [`bidding-tiktok.md`](bidding-tiktok.md) |

## Quick decision

If you only have time to read one thing per platform:

- **Google**: do you have 15+ conversions/30d? Yes → Smart Bidding. No → Maximize Clicks or Manual CPC.
- **Meta**: Lowest Cost is right 90% of the time. Cost Cap if margins matter. Daily budget must be ≥5× target CPA.
- **TikTok**: Lowest Cost default. Budget ≥50× CPA per ad group. GMV Max for Shop campaigns.
