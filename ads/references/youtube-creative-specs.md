# YouTube Creative Specs: Generation Guide

<!-- Updated: 2026-03-12 -->
<!-- Source: platform-specs.md + Google Ads YouTube requirements -->
<!-- Used by: ads-generate, visual-designer agent -->

## Purpose

Generation-ready specifications for YouTube ad creative. Note: full video generation
requires a video production workflow. This reference covers thumbnail generation,
storyboard frame generation, and static companion assets.

---

## Ad Format Overview

| Format | Ratio | Resolution | Duration | Skip |
|--------|-------|-----------|----------|------|
| Skippable In-Stream | 16:9 | 1920×1080 | 12s-3min (rec 15-30s) | After 5s |
| Non-Skippable | 16:9 | 1920×1080 | 15-60s (expanded 2025) | No |
| Bumper | 16:9 | 1920×1080 | ≤6s | No |
| In-Feed Video | 16:9 | 1920×1080 | Any | N/A |
| YouTube Shorts | 9:16 | 1080×1920 | ≤60s | Swipe |

---

## Thumbnail Generation

Thumbnails are the primary generation output for YouTube campaigns.

### Standard Thumbnail

| Property | Value |
|----------|-------|
| Dimensions | 1280×720 (16:9) |
| Format | JPG or PNG |
| Max size | 2MB |
| Min resolution | 640×360 |

**Thumbnail generation guidelines:**
- High contrast between subject and background
- Face or product in center-left (text overlays typically placed right side)
- Bright, saturated colors outperform muted palettes for CTR
- Include human faces when relevant (psychological click-trigger)
- Avoid cluttered backgrounds; viewer evaluates at 246×138px in search
- Shock or curiosity gap increases CTR more than informational thumbnails

### Shorts Thumbnail

| Property | Value |
|----------|-------|
| Dimensions | 1080×1080 (1:1) |
| Safe zone | Center 1080×1080 (full frame) |

---

## Shorts Safe Zone (1080×1920)

```
┌─────────────────────────────────┐ ← Top (Y:0)
│                                 │
│   ██████████████████████████   │ ← SAFE START Y:250
│   █                        █   │
│   █   SAFE CONTENT ZONE    █   │
│   █     1080×1420px        █   │
│   █   (full width, center) █   │
│   █                        █   │
│   ██████████████████████████   │ ← SAFE END Y:1670
│                                 │
│  SUBSCRIBE / LIKE / COMMENT UI  │ ← Y:1670-1920 (avoid)
└─────────────────────────────────┘ ← Bottom (Y:1920)
```

**Safe zone:** Full width, Y:250-1670. Bottom 250px is UI overlay (subscribe, like).

---

## Storyboard Frame Generation

For agencies creating video assets, use image generation for storyboard frames:

### Pre-Skip Hook (Skippable In-Stream)
First 5 seconds must capture attention before the skip button appears.

**Generate as:** Single 1920×1080 frame capturing the hook visual.
Prompt modifier: `"dramatic opening frame, immediate visual interest, skip-proof hook"`

### Bumper Ad Frame (≤6s)
Single message, no time for story arc.

**Generate as:** One 1920×1080 frame = the entire bumper concept.
Prompt modifier: `"single clear message, product/brand front and center, high recall"`

---

## Copy Limits (YouTube Companion)

| Component | Limit |
|-----------|-------|
| Headline | 15 chars |
| CTA button | Predefined |
| Description (in-feed) | 2 lines, 35 chars each |

---

## Image Generation Prompt Modifiers

**For Standard Thumbnail (1280×720):**
- `"horizontal composition, 16:9 aspect ratio"`
- `"subject in center-left third of frame"`
- `"high contrast, bold colors"`
- `"dramatic lighting"` (thumbnails need visual pop)
- `"designed to be legible at thumbnail size"`

**For Shorts (1080×1920 vertical):**
- `"vertical composition, subject centered in upper portion"`
- `"bottom 250px is clear background only"`
- `"bold, full-bleed vertical visual"`
- `"designed for mobile fullscreen viewing"`

**For Storyboard Frames (1920×1080):**
- `"cinematic composition, widescreen"`
- `"broadcast quality, professional production"`
- `"clear storytelling in single frame"`

---

## Generation Scope Limitation

Full video ads (MP4) cannot be generated with still image models. Use:
- `generate_image.py` → thumbnail, companion banner, storyboard frames
- `/ads generate` → static assets only
- For video generation → use `/ads generate` with the `ads-youtube` video generation workflow
  (requires separate video generation API, not covered by `generate_image.py`)
