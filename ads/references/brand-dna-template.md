# Brand DNA Template

<!-- Updated: 2026-03-12 -->
<!-- Used by: ads-dna (extraction), ads-create (consumption), ads-generate (style injection) -->

## Purpose

Defines the canonical schema for `brand-profile.json`. All agents that produce or
consume brand data must use these exact field names and value types.

---

## JSON Schema

```json
{
  "schema_version": "1.0",
  "brand_name": "string",
  "website_url": "string (full URL including https://)",
  "extracted_at": "ISO-8601 timestamp (e.g. 2026-03-12T14:30:00Z)",

  "voice": {
    "formal_casual":          7,
    "rational_emotional":     4,
    "playful_serious":        5,
    "bold_subtle":            8,
    "traditional_innovative": 6,
    "expert_accessible":      5,
    "descriptors": ["authoritative", "warm", "direct"]
  },

  "colors": {
    "primary":    "#1A2E4A",
    "secondary":  ["#F4A623", "#FFFFFF"],
    "forbidden":  ["#FF0000"],
    "background": "#F9F9F9",
    "text":       "#1A1A1A"
  },

  "typography": {
    "heading_font":       "Inter",
    "body_font":          "Source Sans Pro",
    "pairing_descriptor": "modern sans-serif, clean and readable"
  },

  "imagery": {
    "style":       "professional photography",
    "subjects":    ["people using product", "clean product shots", "diverse workforce"],
    "composition": "clean backgrounds, good negative space",
    "forbidden":   ["stock photo clichés", "corporate handshakes", "cheesy smiles"]
  },

  "aesthetic": {
    "mood_keywords": ["trustworthy", "modern", "approachable"],
    "texture":        "minimal, flat",
    "negative_space": "generous"
  },

  "brand_values":   ["transparency", "innovation", "customer-first"],

  "target_audience": {
    "age_range":   "28-45",
    "profession":  "marketing managers and small business owners",
    "pain_points": ["time-consuming reporting", "unclear ROI"],
    "aspirations": ["grow efficiently", "look professional"]
  },

  "screenshots": {
    "homepage":  "./brand-screenshots/example_com_desktop.png",
    "secondary": ["./brand-screenshots/example_com_pricing_desktop.png"]
  }
}
```

---

## Field Reference

### Voice Axes (1-10 scale)

Score interpretation: 1 = extreme left pole, 10 = extreme right pole, 5 = neutral.

| Field | 1 (Left) | 10 (Right) | Ad Implication |
|-------|----------|------------|----------------|
| `formal_casual` | Very formal, corporate | Very casual, conversational | Headlines tone |
| `rational_emotional` | Data-driven, logical | Emotionally evocative | Story vs stats |
| `playful_serious` | Fun, humorous | Serious, no-nonsense | CTA phrasing |
| `bold_subtle` | Big claims, loud | Understated, nuanced | Visual hierarchy |
| `traditional_innovative` | Classic, established | Cutting-edge, disruptive | Imagery style |
| `expert_accessible` | Deep expertise, jargon | Everyone can understand | Copy complexity |

`descriptors` (array of 3-5 strings): Free-form adjectives capturing tone not covered by axes.

### Colors

- `primary`: Main brand color. **Always inject into image generation prompts.**
- `secondary`: Supporting palette. Use for accents in generation prompts.
- `forbidden`: Colors to explicitly exclude from prompts (e.g., competitor brand colors).
- `background` / `text`: Digital UI colors (less relevant for ad image generation).

**Null handling:** If extraction fails for a color, set to `null`. Agents must skip null
color injection rather than defaulting to arbitrary colors.

### Typography

Used by `copy-writer` agent for tone calibration. Not injected into image prompts
(typography is handled by ad platform copy fields, not image generation).

### Imagery

- `style`: Main descriptor passed to image generation (e.g., "professional photography",
  "illustration", "flat design").
- `subjects`: Array injected as subject guidance in prompts.
- `composition`: Passed verbatim as a composition constraint.
- `forbidden`: Converted to negative prompt modifiers (e.g., "no corporate handshakes").

### Aesthetic

- `mood_keywords`: Injected directly into generation prompts as atmosphere descriptors.
- `texture`: Passed as texture preference.
- `negative_space`: "generous" → "plenty of white space, uncluttered composition".

### Screenshots (optional, populated by `/ads dna`)

- `homepage`: Desktop screenshot of homepage. **Primary visual style reference** for
  `visual-designer` agent. When present, generation auto-uses `gemini-3.1-flash-image-preview`
  (Nano Banana 2) for better brand style-transfer.
- `secondary`: Additional pages (pricing, about, product). Supplemental context.
- **If field absent**: `visual-designer` falls back to text-only generation (`gemini-2.5-flash-image`).
- **If field present but file missing on disk**: `visual-designer` logs a warning and falls back gracefully.
- Set by `ads-dna` Step 2b. Omitted entirely if screenshot capture failed or `--quick` was used.

---

## Extraction Guide

### Pages to scan (in order)

1. **Homepage**: Primary brand impression, dominant colors, hero headline tone
2. **About / Our Story**: Brand values, voice descriptors, team photography style
3. **Product / Service page**: Imagery style, composition, subject matter
4. **Existing ads** (if accessible via Meta Ad Library or Google Ads Transparency): Override

### CSS extraction targets

```
background-color, color         → colors.primary / secondary
font-family                     → typography.heading_font / body_font
@import url (Google Fonts)      → typography (font name from URL path)
og:image meta tag               → imagery.style (analyze dominant visual)
```

### Voice scoring heuristics

| Signal | Scoring |
|--------|---------|
| Uses "you" and "your" frequently | formal_casual +2 (casual) |
| Industry jargon in hero text | expert_accessible -2 (expert) |
| Short sentences (≤10 words) | bold_subtle +1 (bold) |
| Testimonials lead with emotion | rational_emotional +2 (emotional) |
| "Trusted by 10,000+ companies" | traditional_innovative -1 (traditional) |

### Fallback heuristics

- **No Google Fonts detected**: Set `typography.heading_font` to "system-ui"
- **Sparse content (< 200 words)**: Mark `extracted_at` note: "low confidence extraction"
- **Dark mode site**: If background is dark (#333 or darker), swap `background` and `text`
- **Cannot extract primary color**: Use most prominent color from og:image analysis

---

## Usage in Generation Prompts

When building image generation prompts, inject brand DNA as:

```
"[subject], [imagery.style], [imagery.composition],
brand colors [colors.primary] and [colors.secondary[0]],
[aesthetic.mood_keywords joined by comma] atmosphere,
[aesthetic.texture] texture, [aesthetic.negative_space] composition,
no [imagery.forbidden joined by comma]"
```

Example output:
```
"person using laptop, professional photography, clean backgrounds good negative space,
brand colors #1A2E4A and #F4A623, trustworthy modern approachable atmosphere,
minimal flat texture, generous white space composition,
no stock photo clichés, no corporate handshakes"
```
