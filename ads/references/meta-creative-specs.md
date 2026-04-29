# Meta Creative Specs: Generation Guide

<!-- Updated: 2026-03-12 -->
<!-- Source: platform-specs.md + Meta Ads Manager requirements -->
<!-- Used by: ads-generate, visual-designer agent -->

## Purpose

Generation-ready specifications for Meta (Facebook + Instagram) ad creative. Includes
safe zone diagrams, copy limits, and prompt modifiers for each placement type.

---

## Image Specs by Placement

| Placement | Ratio | Dimensions | Priority |
|-----------|-------|-----------|----------|
| Feed (preferred) | 4:5 | 1080×1350 | **Primary target** |
| Feed (square) | 1:1 | 1080×1080 | High |
| Stories | 9:16 | 1080×1920 | High |
| Reels | 9:16 | 1080×1920 | High |
| Right Column | 1:1 | 1080×1080 | Low |
| Max file size: 30MB. Min width: 600px (1080px recommended).

**Primary generation target: 1080×1350 (4:5)**
This ratio performs best in Feed and covers Instagram Feed.
Always generate this first. Generate 9:16 for Stories/Reels campaigns.

---

## Safe Zones: Reels and Stories (1080×1920)

```
┌─────────────────────────────────┐ ← Top (Y:0)
│         STATUS BAR              │ ← Y:0-120 (avoid)
│                                 │
│      ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓   │ ← SAFE START Y:120
│      ▓                     ▓   │
│      ▓   SAFE CONTENT ZONE  ▓   │
│      ▓      1080×1300px     ▓   │
│      ▓  (center of frame)   ▓   │
│      ▓                     ▓   │
│      ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓   │ ← SAFE END Y:1420
│                                 │
│   CTA BUTTON / CAPTION AREA     │ ← Y:1420-1920 (avoid)
│   REACTIONS / PROFILE INFO      │
└─────────────────────────────────┘ ← Bottom (Y:1920)
```

**Bottom 35% (~670px) is UI overlay.** Keep all critical text, faces, and product
in the center 1080×1300px zone.

**Generation instruction for 9:16 prompts:**
- Subject and key visual elements in top 60% of frame
- Bottom 450px should be background only (solid color or soft gradient)
- Vertical composition only; horizontal crops are rejected at upload

---

## Safe Zone: Feed (1080×1350, 4:5)

No hard safe zone required. The full frame is visible. However:
- Bottom 120px may be covered by the like/comment bar on mobile
- Keep primary subject in upper 80% of frame

---

## Copy Limits

| Component | Recommended | Platform Max |
|-----------|------------|-------------|
| Primary Text | 40-125 chars | 2,200 |
| Headline | 27-40 chars | N/A |
| Description | 20 chars (carousel) | N/A |
| Reels Primary Text | 72 chars max visible | N/A |
| CTA Button | Predefined list | N/A |

**Copy generation rule:** Write primary text ≤125 chars. Anything over 125 chars
gets truncated with "See More" on mobile; the critical message must land in 125.

---

## Carousel Specs

- 2-10 cards per carousel
- All cards: 1:1 (1080×1080)
- Per card: Headline ≤40 chars, Description ≤20 chars
- Generate each card as a separate image prompt
- Maintain consistent visual style across all cards (same background, same lighting)

---

## Advantage+ Creative

When Advantage+ Creative enhancements are enabled, Meta may:
- Crop the image to different aspect ratios
- Adjust brightness/contrast
- Add music to static images
- Generate text variations from your primary text

**Implication for generation:** Generate a "base" image that looks good at both
1:1 and 4:5 ratios. Avoid placing critical elements near edges.

---

## Video Specs (for storyboard reference)

| Placement | Ratio | Resolution | Duration |
|-----------|-------|-----------|----------|
| Feed | 4:5 | 1080×1350 | Up to 241 min |
| Reels | 9:16 | 1080×1920 | ≤90s (rec 15-30s) |
| Stories | 9:16 | 1080×1920 | ≤120s |
| In-Stream | 16:9 | 1920×1080 | ≤15 min |

---

## Image Generation Prompt Modifiers

**For Feed (4:5 and 1:1):**
- `"vertical composition"` or `"square composition"`
- `"subject fills upper portion of frame"`
- `"clean, scroll-stopping visual"`
- `"no text overlay"` (text added via ad copy fields)

**For Stories/Reels (9:16):**
- `"vertical composition, subject in top 60% of frame"`
- `"bottom third is clear background or soft gradient"`
- `"bold, high-contrast visual"`
- `"mobile-first, designed for small screen viewing"`

**Always avoid:**
- Cluttered backgrounds (compete with feed content)
- Low contrast (thumb-stop requires visual pop)
- Faces cropped at edges (Instagram crops aggressively on some placements)
