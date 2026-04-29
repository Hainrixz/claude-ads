# TikTok Creative Specs: Generation Guide

<!-- Updated: 2026-03-12 -->
<!-- Source: platform-specs.md + TikTok Ads Manager requirements -->
<!-- Used by: ads-generate, visual-designer agent -->

## Purpose

Generation-ready specifications for TikTok ad creative. TikTok is vertical-only and
sound-on. Horizontal or square creatives are **rejected at upload**. Safe zone
compliance is critical; UI elements cover significant portions of the frame.

---

## Required Format

| Ratio | Dimensions | Notes |
|-------|-----------|-------|
| **9:16 (ONLY)** | **1080×1920** | **Only accepted format for In-Feed and TopView** |

**There is no alternative.** Horizontal (16:9) or square (1:1) compositions are
rejected by TikTok Ads Manager. Always generate vertically.

**File requirements:** MP4 or MOV, H.264, AAC audio required, max 500MB.
**For image-based static ads:** PNG or JPG at 1080×1920.

---

## TikTok Safe Zone Diagram

```
┌─────────────────────────────────┐ ← Top (Y:0)
│  STATUS BAR + ACCOUNT INFO      │ ← Y:0-150 (AVOID)
├─────────────────────────────────┤
│                      │LIKE      │ ← RIGHT EDGE: X:940-1080
│                      │COMMENT   │    (AVOID; UI icons)
│   ██████████████████ │SHARE     │
│   █                █ │PROFILE   │
│   █  SAFE CONTENT  █ │          │
│   █     ZONE       █ │          │
│   █  X:40 to X:940 █ │          │
│   █  Y:150 to Y:1470█ │         │
│   █  (900×1320px)  █ │          │
│   ██████████████████ │          │
│                                 │
│  CAPTION + MUSIC + CTA + NAV    │ ← Y:1470-1920 (AVOID)
└─────────────────────────────────┘ ← Bottom (Y:1920)
```

**Safe Box: X:40-940, Y:150-1470 (900×1320px)**

All critical text, logos, faces, CTAs, and key product elements MUST be within
the safe box. Anything outside this zone will be hidden behind UI overlays.

---

## Content Area Guidelines

| Zone | Y Range | X Range | Action |
|------|---------|---------|--------|
| Status bar | 0-150 | full | Keep clear |
| Right side icons | 150-1470 | 940-1080 | Keep clear |
| Caption/CTA bar | 1470-1920 | full | Keep clear |
| **Safe content zone** | **150-1470** | **40-940** | **Place all key content here** |

**Subject placement rule:** Main subject (person, product) should be centered in the
upper 60% of the safe zone (Y:150-900). This ensures visibility even on smaller screens.

---

## Copy Limits

| Component | Max | Notes |
|-----------|-----|-------|
| Ad text | 100 chars | Appears below video |
| Display name | 25 chars | Brand name shown |
| CTA button | Predefined list | Auto-placed in safe zone |

---

## Ad Format Types

### In-Feed Ads (Non-Spark)
- Appears in For You Page (FYP) between organic videos
- Duration: 5-60 seconds (rec 9-15s for highest completion)
- Must have audio; silent video severely underperforms
- Generate: static thumbnail at 1080×1920 within safe zone

### Spark Ads
- Promotes existing organic TikTok posts
- Use organic video content; generate only the **thumbnail frame**
- Thumbnail: 1080×1920, subject centered in safe zone

### TopView
- First ad seen when app opens (premium placement)
- Specs: 720×1280 minimum (1080×1920 recommended), 5-60s
- Higher production quality expected

---

## Generation Constraints

**Always include in prompts:**
- `"vertical composition, 9:16 aspect ratio"`
- `"subject centered in upper portion of frame"`
- `"bottom third is clear or minimal background"` (caption overlay area)
- `"bold, eye-catching visual designed for mobile fullscreen"`

**Forbidden in prompts:**
- `"horizontal"`, `"landscape"`, `"widescreen"`; will generate wrong orientation
- `"text in bottom third"`: will be covered by caption UI
- `"logo in bottom corner"`: will be covered by TikTok navigation

**Text in safe zone only:** If asking for text rendered into the image (not ad copy),
specify `"text in upper center of frame, within 900px wide safe zone"`.

---

## Sound-On Platform Rule

**Never run silent video on TikTok.** Audio is expected.
- All video assets must have audio track
- For static image ads: no audio required, but platform may add music
- For generation: this constraint applies to video, not static image generation

---

## Aspect Ratio Priority

TikTok has one option: **1080×1920 (9:16)**. No alternatives.

---

## Smart+ Specs

Smart+ campaigns auto-generate creative variations:
- Up to 50 creatives per asset group
- Symphony AI generates variations from your base asset
- Generate 1 high-quality base image; Smart+ handles variations
