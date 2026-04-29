# Microsoft Creative Specs: Generation Guide

<!-- Updated: 2026-03-12 -->
<!-- Source: platform-specs.md + Microsoft Advertising requirements -->
<!-- Used by: ads-generate, visual-designer agent -->

## Purpose

Generation-ready specifications for Microsoft (Bing) Ads creative. Microsoft creative
is largely a subset of Google creative; most Google assets can be reused directly.
The unique format is the Multimedia Ad.

---

## Multimedia Ads (Microsoft-Unique)

The primary image-based format unique to Microsoft Ads.

| Component | Spec |
|-----------|------|
| Image | 1200×628 (1.91:1) |
| Short Headline | 30 chars |
| Long Headline | 90 chars |
| Description | 90 chars |
| Business Name | 25 chars |

**Generation target: 1200×628 (1.91:1)**
This is the only unique image dimension for Microsoft. Everything else mirrors Google.

---

## Responsive Search Ads (RSA)

Identical to Google RSA character limits:

| Component | Min | Max | Character Limit |
|-----------|-----|-----|-----------------|
| Headlines | 3 | 15 | 30 chars each |
| Descriptions | 2 | 4 | 90 chars each |
| Display Paths | N/A | 2 | 15 chars each |

**Asset reuse:** RSA copy written for Google can be used directly in Microsoft
with no changes. Use the same headlines and descriptions.

---

## Audience Ads (Display Network)

| Size | Dimensions |
|------|-----------|
| Landscape | 1200×628 (1.91:1) |
| Square | 1200×1200 (1:1) |
| Small square | 628×628 (1:1) |

These display on the Microsoft Audience Network (MSN, Outlook, Edge).
**Asset reuse:** Generate the same 3 Google Display assets (1200×628, 1200×1200, and
960×1200 scaled to 628×628). No unique generation needed.

---

## Microsoft-Unique Extensions

These require copy but no image generation:

| Extension | Description |
|-----------|-------------|
| Action Extension | Pre-defined action buttons (Book Now, Download, etc.) |
| Filter Link Extension | Category-based deep links (e.g., product categories) |
| Review Extension | Third-party review quotes with source attribution |

---

## Copilot Ad Integration (2025-2026)

Microsoft Ads now surface in Bing/Copilot AI responses. This affects:
- **Ad copy relevance**: Copilot reads headline + description for context matching
- **Sitelinks**: More likely to be shown in AI responses than on traditional SERPs
- **Image assets**: Multimedia Ad images may appear in Copilot responses

**Generation implication:** Use clear, descriptive product language in image alt context.
Generate images that visually communicate the product/service without requiring copy.

---

## Google Import Strategy

Most advertisers import Google campaigns to Microsoft. After import:
- Bid adjustment: Microsoft CPCs are typically 20-35% lower than Google
- Image assets: All Google PMax images (1200×628, 1200×1200, 960×1200) import directly
- No additional image generation needed for Microsoft-only

**When to generate Microsoft-specific assets:**
- Multimedia Ads (1200×628) if not using Google import
- Custom copy for Copilot-optimized RSA headlines

---

## Image Generation Prompt Modifiers

**For Multimedia Ads (1200×628):**
- `"horizontal composition, 1.91:1 aspect ratio"`
- `"clean professional background"`
- `"Microsoft Bing search audience; professional, trustworthy aesthetic"`
- `"product or service clearly visible"`

**Tone guidance:** Microsoft's audience skews slightly older (35+) and more professional
than Google Search. Apply a slightly more conservative, trust-signaling visual style.
Avoid TikTok-style dramatic edits or Meta-style casual lifestyle photography.

---

## Asset Reuse Summary

| Source | Reusable for Microsoft? |
|--------|------------------------|
| Google PMax 1200×628 | ✅ Direct reuse for Multimedia Ads |
| Google PMax 1200×1200 | ✅ Direct reuse for Audience Ads |
| Google RSA copy | ✅ Use as-is |
| Meta 4:5 (1080×1350) | ❌ Wrong ratio |
| TikTok 9:16 (1080×1920) | ❌ Wrong ratio |

**When using Google import:** No new image generation needed for Microsoft.
Generate Microsoft-specific assets only if running Microsoft-native campaigns.
