# LinkedIn Creative Specs: Generation Guide

<!-- Updated: 2026-03-12 -->
<!-- Source: platform-specs.md + LinkedIn Campaign Manager requirements -->
<!-- Used by: ads-generate, visual-designer agent -->

## Purpose

Generation-ready specifications for LinkedIn ad creative. LinkedIn is a professional
platform; tone, imagery style, and composition constraints differ significantly from
Meta and TikTok.

---

## Single Image Ad Specs

| Ratio | Dimensions | Priority | Notes |
|-------|-----------|----------|-------|
| 1:1 (square) | 1080×1080 | **Primary target** | Better engagement than landscape |
| 1.91:1 (landscape) | 1200×628 | Secondary | Legacy placements, desktop sidebar |

**File requirements:** PNG or JPG, max 5MB.

**Primary generation target: 1080×1080 (1:1)**
Square performs better in the LinkedIn feed because it takes up more vertical space
on mobile, increasing scroll-stop rate.

---

## Copy Limits

| Component | Recommended | Max |
|-----------|------------|-----|
| Intro text | 150 chars | 600 chars |
| Headline | 70 chars | 200 chars |
| Description | 100 chars |: (desktop only) |
| CTA button | Predefined list | N/A |

**Copy generation rule:** Write intro text ≤150 chars (truncated on mobile beyond this).
Headline ≤70 chars. The description only shows on desktop; treat as supplementary.

---

## Video Ad Specs

| Component | Requirement |
|-----------|------------|
| Format | MP4 (required) |
| File size | 75KB - 500MB |
| Duration | 3s - 30min (rec 15-30s) |
| Resolution | 360p min; 720p+ recommended |
| Aspect ratios | 16:9 (landscape), 1:1 (square), 9:16 (mobile only) |

For video thumbnail generation: use 1:1 (1080×1080) as the primary thumbnail size.

---

## Document Ad Specs

- Formats: PDF, DOC, DOCX, PPT, PPTX
- Max: 100MB, 300 pages (10-20 pages recommended)
- Cover image: 1200×628 (1.91:1); generate this as the document cover visual

---

## Audience Network / Programmatic

When LinkedIn Audience Network is enabled, ads run on partner sites.
Supported sizes for network: 300×250, 728×90, 160×600, 300×600.
These are not generation targets; LinkedIn resizes from your primary assets.

---

## B2B Tone Constraints

LinkedIn is a professional context. Apply these constraints to every generation prompt:

**Always include:**
- `"professional photography"` or `"B2B professional context"`
- `"clean, uncluttered background"`
- `"business-appropriate attire if people present"`
- `"high quality, corporate-grade visual"`

**Avoid in prompts:**
- `"casual"`, `"fun"`, `"playful"` (unless brand voice explicitly requires it)
- Lifestyle photography in non-work contexts
- Overly saturated or high-contrast styles (looks out of place in LinkedIn feed)
- Celebrity or influencer aesthetic

**Target audience contexts (use one per generation):**
- Person in office setting, focused on screen/work
- Abstract product/service visualization (SaaS dashboards, data viz)
- Clean product shot on neutral background
- Team collaboration scene (diverse, professional)

---

## Lead Gen Form Integration

LinkedIn Lead Gen Forms auto-populate from member profiles. When generating creative
that promotes lead gen forms:
- Image should visually represent the offer (e.g., whitepaper cover, webinar slide)
- For document/guide offers: generate a stylized cover image at 1200×628
- Avoid "download now" styled images (LinkedIn discourages heavy promotional aesthetics)

---

## Aspect Ratio Priority

When generating a single image for LinkedIn (time-constrained):
1. `1080×1080` (1:1); covers Feed (best engagement)
2. `1200×628` (1.91:1); covers legacy + desktop placements

Always generate both for full coverage.

---

## Image Generation Prompt Modifiers

**For Feed (1:1):**
- `"square composition, subject centered"`
- `"professional B2B photography style"`
- `"clean neutral background"`
- `"no lifestyle elements, business context"`

**For Landscape (1.91:1):**
- `"horizontal composition"`
- `"wide framing with subject left or center"`
- `"ample negative space on right for text overlay area"`
