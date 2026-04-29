# Brand Voice to Visual Style Mapping

> Updated: 2026-04-01
> Source: Used by creative-strategist and visual-designer agents

## Purpose

Brand voice scores (1 to 10 scale) from `brand-profile.json` translate directly
into visual style descriptors for image generation prompts. Each axis maps to
specific aesthetic attributes that become the [STYLE] component in banana prompts.
When multiple axes combine, their descriptors merge into a cohesive style string.

## Axis Mappings

### 1. formal_casual

| Range     | Score | Visual Descriptors                                      |
|-----------|-------|---------------------------------------------------------|
| Low       | 1-3   | Clean lines, symmetrical, muted palette, serif type     |
| Mid       | 4-6   | Balanced layout, neutral tones, modern sans-serif       |
| High      | 7-10  | Organic shapes, warm palette, hand-drawn elements       |

### 2. rational_emotional

| Range     | Score | Visual Descriptors                                      |
|-----------|-------|---------------------------------------------------------|
| Low       | 1-3   | Data overlays, charts, structured grids, cool tones     |
| Mid       | 4-6   | Infographic style, balanced data and imagery            |
| High      | 7-10  | Expressive color, human faces, dynamic motion blur      |

### 3. bold_subtle

| Range     | Score | Visual Descriptors                                      |
|-----------|-------|---------------------------------------------------------|
| Low       | 1-3   | Soft focus, pastel tones, whitespace, thin strokes      |
| Mid       | 4-6   | Medium contrast, standard weight type, clear hierarchy  |
| High      | 7-10  | High contrast, saturated color, heavy type, full bleed  |

### 4. traditional_innovative

| Range     | Score | Visual Descriptors                                      |
|-----------|-------|---------------------------------------------------------|
| Low       | 1-3   | Classic compositions, heritage textures, earth tones    |
| Mid       | 4-6   | Contemporary layouts, balanced modern and classic cues  |
| High      | 7-10  | Futuristic gradients, 3D renders, neon accents, glass   |

### 5. friendly_authoritative

| Range     | Score | Visual Descriptors                                      |
|-----------|-------|---------------------------------------------------------|
| Low       | 1-3   | Rounded shapes, illustration style, bright accents      |
| Mid       | 4-6   | Mixed photography and illustration, approachable layout |
| High      | 7-10  | Editorial photography, dark backgrounds, gold accents   |

### 6. playful_serious

| Range     | Score | Visual Descriptors                                      |
|-----------|-------|---------------------------------------------------------|
| Low       | 1-3   | Whimsical patterns, cartoon elements, candy colors      |
| Mid       | 4-6   | Lifestyle photography, natural color grading            |
| High      | 7-10  | Cinematic lighting, desaturated palette, minimal decor  |

## How to Apply

1. Read `brand-profile.json` and extract the six voice axis scores.
2. For each axis, look up the matching range (Low, Mid, High) in the table above.
3. Collect one or two descriptors per axis that best fit the brand context.
4. Combine all selected descriptors into a single [STYLE] string, separated by commas.
5. Append the [STYLE] string to the banana prompt template before generation.

## Example

Given a brand with these scores:

- formal_casual: 7 (High; organic shapes, warm palette)
- bold_subtle: 8 (High; high contrast, saturated color)
- playful_serious: 3 (Low; whimsical patterns, candy colors)

The resulting [STYLE] component:

```
[STYLE]: organic shapes, warm palette, high contrast, saturated color,
whimsical patterns, candy colors
```

This creates a vibrant, approachable visual identity that feels energetic
and playful while maintaining strong visual impact.
