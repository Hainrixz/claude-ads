# Image Generation Providers

<!-- Updated: 2026-04-01 -->
<!-- Used by: ads-generate, ads-photoshoot, visual-designer agent -->

## Default Provider: banana-claude

banana-claude (v1.4.1) is the default image generation provider. It acts as a Creative Director
layer on top of Google Gemini, providing 5-component prompt engineering, 9 domain modes,
brand presets, cost tracking, and post-processing.

### Prerequisites
- banana-claude installed (`/banana setup` to verify)
- nanobanana-mcp configured with GOOGLE_AI_API_KEY
- No additional pip packages needed (banana uses stdlib only)

### MCP Tools (Primary Method)

| Tool | Purpose | Key Parameters |
|------|---------|----------------|
| `set_aspect_ratio` | Configure ratio for next generation | ratio: "16:9", "1:1", "9:16", etc. |
| `set_model` | Switch Gemini model | model: "gemini-3.1-flash-image-preview" (default) |
| `gemini_generate_image` | Text-to-image generation | prompt: (string) |
| `gemini_edit_image` | Modify existing image | imagePath, prompt |
| `get_image_history` | Review session generations | (none) |

### Domain Modes for Ad Creative

| Mode | Use For | Ad Type |
|------|---------|---------|
| Product | E-commerce packshots, product ads | Shopping, PMax, Meta catalog |
| Editorial | Brand awareness, lifestyle campaigns | Meta Feed, YouTube, LinkedIn |
| Cinema | Dramatic storytelling, video thumbnails | YouTube, TikTok, Demand Gen |
| Portrait | People-centric ads, testimonials | Meta, LinkedIn, Google Display |
| UI/Web | App install ads, SaaS screenshots | Google UAC, Meta app install |
| Logo | Brand identity, favicon generation | All platforms (identity assets) |
| Landscape | Environment, travel, real estate | Google Display, YouTube |
| Infographic | Data-driven ads, comparison charts | LinkedIn, Google Display |
| Abstract | Background textures, patterns | All (supporting assets) |

### 5-Component Prompt Formula

Banana constructs optimized prompts using:
1. [SUBJECT]: Physical details, appearance, material
2. [ACTION]: What it's doing, pose, state
3. [LOCATION/CONTEXT]: Where, when, atmosphere
4. [COMPOSITION]: Camera angle, framing, perspective
5. [STYLE]: Camera/lens specs, lighting, brand voice mapped attributes

Visual-designer agent builds these components from campaign brief + brand profile.

### Pricing (Gemini via banana)

| Resolution | Cost/Image | Use Case |
|------------|-----------|----------|
| 512px | $0.020 | Quick drafts, concepts |
| 1K | $0.039 | Standard web assets |
| 2K (recommended) | $0.078 | Quality ad creatives |
| 4K | $0.156 | Print, hero images |
| Batch API | 50% off | Bulk campaign generation |

### Aspect Ratios (14 supported)

| Ratio | Dimensions | Platform Use |
|-------|-----------|-------------|
| 1:1 | 1080x1080 | Meta Feed, LinkedIn, Carousel |
| 4:5 | 1080x1350 | Meta Feed (preferred), Instagram |
| 9:16 | 1080x1920 | TikTok, Reels, Shorts, Stories |
| 16:9 | 1920x1080 | YouTube, Google Display, LinkedIn |
| 3:2 | 1200x800 | DSLR standard, photo prints |
| 2:3 | 800x1200 | Pinterest, posters |
| 21:9 | Cinematic | Ultra-wide banners |
| 4:1 | 1200x300 | Website banners |
| 1:4 | Vertical banner | Mobile banners |

Note: Gemini does not natively support 1.91:1. Use 16:9 and crop to 1200x628 for Google PMax/LinkedIn.

### Brand Presets

banana supports brand presets stored at `~/.banana/presets/NAME.json`.
The ads-generate skill auto-creates a preset from brand-profile.json before generation.

Preset schema:
- colors: array of hex values from brand DNA
- style: visual style description from brand aesthetic
- mood: mood keywords from brand voice
- default_ratio: "16:9" (or platform-specific)
- default_resolution: "2K"

### Cost Tracking

banana logs all generations to `~/.banana/costs.json`.
ads-generate reads this after generation and includes cost summary in generation-manifest.json.

---

## Fallback Providers

If banana is not installed, these providers can be used directly via generate_image.py (deprecated).

### OpenAI (gpt-image-1)
- Env: `OPENAI_API_KEY`
- Price: ~$0.040/image (1024x1024), ~$0.060 (1024x1536)
- Package: `openai>=1.75.0`

### Stability AI (stable-diffusion-3.5-large)
- Env: `STABILITY_API_KEY`
- Price: ~$0.065/image flat
- Package: `stability-sdk>=0.8.4`

### Replicate (FLUX.1 Pro)
- Env: `REPLICATE_API_TOKEN`
- Price: ~$0.055/image
- Package: `replicate>=1.0.4`

---

## Error Reference

| Error | Cause | Fix |
|-------|-------|-----|
| banana MCP not found | nanobanana-mcp not configured | Run `/banana setup` |
| IMAGE_SAFETY | Safety filter triggered | Rephrase; use abstraction or artistic framing |
| 429 Too Many Requests | Rate limit | banana auto-retries with exponential backoff |
| FAILED_PRECONDITION | Billing not enabled | Enable billing in Google AI Studio |

### Rate Limits (Gemini via banana)

| Tier | RPM | Daily Images |
|------|-----|-------------|
| Free | 5-15 | 20-500 |
| Tier 1 (<$250 spend) | 150 | 1,500 |
| Tier 2 (>$250 spend) | 1,000+ | Unlimited |
