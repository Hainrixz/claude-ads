<div align="right">
<sub><a href="README.md">EN</a> · <strong>Español</strong></sub>
</div>

<p align="center">
  <img src="assets/hero.svg" alt="Claude Ads — terminal corriendo /ads audit, wordmark de la marca y dashboard de muestra con health score 78/100" width="100%">
</p>

# Claude Ads

> Un skill gratuito para Claude Code que convierte a Claude en tu equipo interno de ads pagados — audita, planea, califica y reporta.

[![Sitio](https://img.shields.io/badge/web-tododeia.com-1f6feb)](https://tododeia.com)
[![Instagram](https://img.shields.io/badge/IG-%40soyenriquerocha-E4405F?logo=instagram)](https://instagram.com/soyenriquerocha)
[![Licencia: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Versión](https://img.shields.io/badge/version-2.1.2-blue)](https://github.com/Hainrixz/claude-ads/releases)
[![Claude Code Skill](https://img.shields.io/badge/Claude%20Code-Skill-blue)](https://claude.ai/claude-code)

---

## ¿Qué es esto? (en español sencillo)

¿Sabes que le puedes pedir a Claude que revise tu código? **Claude Ads es la misma idea, pero para publicidad pagada.** Lo instalas una vez y a Claude le hacen un trasplante de cerebro: ahora sabe Google Ads, Meta, YouTube, LinkedIn, TikTok, Microsoft Ads y Apple Search Ads a nivel estratega senior — más de 250 verificaciones específicas, 12 plantillas por industria, y la capacidad de entregarte un reporte de auditoría real al final.

Le pasas tus datos de ads (un export, un screenshot, o pegas tus números directo en el chat), escribes un comando como `/ads audit`, y Claude despacha seis analistas en paralelo — uno por cada parte de tu cuenta. Te regresa un health score de 0–100, una lista priorizada de qué arreglar, y (si quieres) un reporte PDF pulido que le puedes pasar a un cliente.

No es un botón mágico que te corre las campañas. Es un revisor senior que vive dentro de tu terminal, sabe qué está roto antes que tú, y nunca olvida revisar las cosas aburridas (Consent Mode V2, CAPI, reglas de learning phase, kill thresholds). Y desde la v2.0+ se actualiza solo mes con mes para no quedarse desactualizado.

---

## Inicio rápido (en menos de 2 minutos)

**Instalación como plugin (recomendado)** — se registra como plugin nativo de Claude Code con auto-updates:

```shell
/plugin marketplace add Hainrixz/claude-ads
/plugin install claude-ads@tododeia-claude-ads
```

**O en una línea (Unix / macOS / Linux):**

```bash
curl -fsSL https://raw.githubusercontent.com/Hainrixz/claude-ads/main/install.sh | bash
```

**O en una línea (Windows PowerShell):**

```powershell
irm https://raw.githubusercontent.com/Hainrixz/claude-ads/main/install.ps1 | iex
```

Después abre Claude Code y corre tu primera auditoría:

```shell
claude
> /ads audit
```

Claude te va a preguntar tu industria, gasto mensual y qué plataformas incluir. Le contestas. Él hace el resto.

---

## Cómo funciona

<p align="center">
  <img src="assets/how-it-works.svg" alt="Diagrama de flujo — tus datos de ads → /ads orchestrator → 6 agentes en paralelo (Google 80, Meta 50, Creative, Tracking, Budget, Compliance) → Ads Health Score 0–100" width="100%">
</p>

```mermaid
flowchart LR
  U([Tú]) -->|/ads audit| O[Orquestador]
  O -.despacha en paralelo.-> G[Auditoría Google]
  O -.-> M[Auditoría Meta]
  O -.-> C[Auditoría Creative]
  O -.-> T[Auditoría Tracking]
  O -.-> B[Auditoría Budget]
  O -.-> X[Auditoría Compliance]
  G & M & C & T & B & X -->|hallazgos| S[Reporte calificado]
  S --> R([health score 0–100 · fixes priorizados · PDF opcional])
```

El orquestador (`/ads`) no intenta hacer todo solo. Despacha seis agentes especializados en paralelo — cada uno con su checklist, sus referencias cargadas on-demand (estilo RAG), y sus pesos de severidad. Sus hallazgos se fusionan en un único reporte calificado.

---

## Qué puedes correr

| Grupo | Comando | Qué hace |
|---|---|---|
| **Auditoría** | `/ads audit` | Auditoría completa multi-plataforma — 6 agentes en paralelo, reporte calificado |
| **Por plataforma** | `/ads google` | Google Ads (Search, PMax, Demand Gen, CTV, YouTube) — 80 checks |
| | `/ads meta` | Meta Ads (FB / IG / Advantage+) — 50 checks |
| | `/ads youtube` | YouTube Ads (Skippable, Shorts, Demand Gen) |
| | `/ads linkedin` | LinkedIn Ads (B2B, Lead Gen, TLA) — 27 checks |
| | `/ads tiktok` | TikTok Ads (Smart+, Shop, Search) — 28 checks |
| | `/ads microsoft` | Microsoft / Bing Ads (Copilot, import safety) — 24 checks |
| | `/ads apple` | Apple Search Ads (CPPs, AdAttributionKit, TAP) — 35+ checks |
| **Creative** | `/ads creative` | Auditoría de calidad creativa + detección de fatiga |
| | `/ads landing` | Revisión de landing pages para conversión |
| **Estrategia** | `/ads plan <tipo>` | Plan estratégico desde 12 plantillas por industria |
| | `/ads budget` | Revisión de asignación de presupuesto + estrategia de bidding |
| | `/ads competitor` | Inteligencia de competencia entre todas las plataformas |
| **Números** | `/ads math` | Calculadora PPC: CPA, ROAS, break-even, LTV:CAC, MER |
| | `/ads test` | Diseño de A/B test (hipótesis, sample size, duración) |
| **Output** | `/ads report` | Reporte PDF de auditoría para entregar a clientes |
| **Mantenimiento** | `/ads update <plataforma\|all>` | Refrescar referencias con cambios de los últimos 30 días (NUEVO en v2.0) |

---

## Plataformas cubiertas

<p align="center">
  <img src="assets/platforms.svg" alt="Grid de cobertura por plataforma — Google 80, Meta 50, YouTube multi, LinkedIn 27, TikTok 28, Microsoft 24, Apple 35+, más 3 checks multi-plataforma" width="100%">
</p>

| Plataforma | Checks | Áreas clave |
|---|---|---|
| Google Ads | **80** | Match types · PMax · AI Max · Demand Gen · CTV · YouTube |
| Meta Ads | **50** | Pixel + CAPI · diversidad creativa Andromeda · Advantage+ Shopping · estructura de audiencias |
| LinkedIn Ads | **27** | Targeting B2B · TLA · Lead Gen · integración CRM |
| TikTok Ads | **28** | Creative-first · Smart+ · GMV Max · Search Ads · Events API |
| Microsoft Ads | **24** | Seguridad de import desde Google · Copilot · CTV · LinkedIn targeting |
| Apple Search Ads | **35+** | Estructura de campaña · CPPs · Maximize Conversions · AdAttributionKit |
| Multi-plataforma | **3** | Infra de privacidad · diversidad creativa · cadencia de refresh |
| **Total** | **250+** | con peso por severidad → Ads Health Score 0–100 |

---

## Conecta tus cuentas reales de ads

<p align="center">
  <img src="assets/connect.svg" alt="Arquitectura MCP — Claude Code como hub central conectado a Google Ads (cohnen/mcp-google-ads), Meta (brijr/meta-mcp), LinkedIn (Synter · Adzviser), TikTok (AdsMCP), Microsoft (CData · Synter); modo manual vs modo en vivo" width="100%">
</p>

Por default, Claude Ads corre en **modo manual** — pegas exports, screenshots o números, y Claude los analiza. Es el camino más fácil y funciona en cualquier plan.

Si quieres que Claude lea tus cuentas directo — convirtiendo el skill en un agente real de ads que jala datos en vivo cuando los necesita — conecta un **servidor MCP** para la plataforma. MCP es el protocolo de plugins de Claude Code para fuentes de datos en vivo. Lo instalas una sola vez, pegas tus credenciales en `~/.claude/.mcp.json`, y de ahí en adelante Claude puede llamar a tu plataforma de ads por su cuenta.

| Plataforma | Servidor MCP | Instalación | Auth necesaria |
|---|---|---|---|
| **Google Ads** | [`cohnen/mcp-google-ads`](https://github.com/cohnen/mcp-google-ads) | `pip install -r requirements.txt` | Proyecto Google Cloud · Developer Token · OAuth refresh token · login customer ID |
| **Meta Ads** | [`brijr/meta-mcp`](https://github.com/brijr/meta-mcp) (open-source) o [Adspirer](https://www.adspirer.com) (comercial) | clone + `pip install -r requirements.txt` | Meta Business Manager · Marketing API access token |
| **LinkedIn Ads** | [Synter](https://syntermedia.ai/blog/mcp-server-linkedin-ads) o [Adzviser](https://adzviser.com) | Signup SaaS y agregar entrada MCP | OAuth de LinkedIn Marketing API (suele manejarlo el servicio) |
| **TikTok Ads** | [`AdsMCP/tiktok-ads-mcp-server`](https://github.com/AdsMCP/tiktok-ads-mcp-server) | `uv sync` o `pip install -e .` | App ID + secret del TikTok Developer Portal · OAuth del advertiser |
| **Microsoft Ads** | [CData Bing Ads MCP](https://github.com/CDataSoftware/bing-ads-mcp-server-by-cdata) (solo lectura) o [Synter](https://syntermedia.ai) (lectura/escritura) | `mvn clean install` o signup SaaS | OAuth de Microsoft Advertising |

> **Ojo.** El modo en vivo significa que Claude puede leer — y con algunos servidores MCP, **escribir** — sobre tus cuentas reales de ads. Empieza en modo solo lectura, apúntalo a un sandbox o a una cuenta de bajo gasto primero, y solo activa write-access cuando ya lo hayas visto correr varias veces. El walkthrough completo de setup por plataforma vive en [`ads/references/mcp-integration.md`](ads/references/mcp-integration.md).

---

## Plantillas por industria

`/ads plan <tipo>` arma un plan estratégico completo desde una plantilla afinada para tu modelo de negocio — mix de plataformas, arquitectura de campañas, ángulos creativos, targeting, distribución de presupuesto y KPIs. Vienen 12 incluidas:

| Plantilla | Para qué sirve |
|---|---|
| `saas` | SaaS / software B2B · enfoque trial + demo · Google + LinkedIn |
| `ecommerce` | DTC / ecom · Shopping / PMax · ROAS-driven · estacional |
| `b2b-enterprise` | B2B enterprise · ABM en LinkedIn · ciclos de venta largos |
| `local-service` | Plomeros, dentistas, agencias · Google Search + LSA · call tracking |
| `info-products` | Coaches / cursos · Meta + YouTube · funnels webinar / VSL |
| `mobile-app` | Apps móviles · Meta + Google UAC · MMP requerido |
| `real-estate` | Inmobiliarias · Special Ad Category (housing) · campañas comprador/vendedor |
| `healthcare` | Clínicas / salud · HIPAA · LegitScript · targeting restringido |
| `finance` | Fintech / créditos · Special Ad Category · disclosures requeridos |
| `agency` | Manejo multi-cliente · framework de reporting |
| `ecommerce-creative` | Ecom con testing creativo agresivo |
| `generic` | Cuestionario universal cuando ninguna otra encaja |

---

## Showcase: cómo se ve un reporte de `/ads audit`

<p align="center">
  <img src="assets/showcase.svg" alt="Dashboard de reporte de muestra — gauge 78/100 grade B, escala A–F, tres tarjetas de hallazgos (CRITICAL · WARNING · QUICK WIN) y barras de breakdown por plataforma (Google 82, Meta 71, LinkedIn 88)" width="100%">
</p>

Toda auditoría produce la misma estructura de salida, así tú (o tu cliente) siempre saben dónde buscar:

| Sección | Qué incluye |
|---|---|
| **Ads Health Score** | Un único número 0–100 (y letra A–F) que resume la cuenta |
| **Breakdown por plataforma** | Sub-scores por plataforma para ver dónde está sangrando la cuenta |
| **Issues críticos** | Violaciones duras (regla 3× kill, broad match sin smart bidding, falta CAPI) — estos van primero |
| **Quick wins** | Cosas que arreglas en menos de una hora con lift medible |
| **Recomendaciones estratégicas** | Movimientos a más largo plazo (cadencia de refresh creativo, restructura de cuenta) |
| **Flags de compliance** | Special Ad Categories, privacidad de Apple, status de Consent Mode V2 en EU |

| Letra | Score | Qué significa |
|---|---|---|
| **A** | 90–100 | Solo optimizaciones menores |
| **B** | 75–89 | Hay oportunidades de mejora |
| **C** | 60–74 | Issues notables que requieren atención |
| **D** | 40–59 | Problemas significativos presentes |
| **F** | <40 | Intervención urgente |

Corre `/ads report` después de cualquier auditoría para empacar los hallazgos en un PDF listo para cliente (gauge del health score, gráficas por plataforma, tablas formateadas, layout sin overlap).

---

## `/ads update` — manteniendo el skill al día

Las plataformas de ads sacan cambios en su API, features nuevas y deprecations casi cada semana. Tu auditoría es tan buena como sus datos de referencia. **`/ads update <plataforma|all>` regenera los archivos de referencia por plataforma** con los últimos 30 días de cambios desde changelogs oficiales (Google, Meta, TikTok, LinkedIn, Microsoft, Apple), discusión de practitioners (r/PPC, r/GoogleAds, r/FacebookAds, r/adops, Hacker News) y prensa de la industria (Search Engine Land, AdWeek, MarTech) vía WebSearch como fallback.

El pipeline está adaptado de [last30days-skill](https://github.com/mvanhorn/last30days-skill) (MIT, por Matt Van Horn — ver [`scripts/lib/THIRD_PARTY_NOTICES.md`](scripts/lib/THIRD_PARTY_NOTICES.md)).

| Modo | Costo aprox. | Cadencia recomendada |
|---|---|---|
| `/ads update <una plataforma>` | 50–150k tokens | Mensual por plataforma |
| `/ads update all` | 500k+ tokens | Mensual, en horario de bajo tráfico |

`/ads update` siempre pide confirmación y muestra el costo estimado antes de correr — puedes cancelar o caer al modo `--depth quick`. Si tu plan de créditos es ajustado, prefiere modo por-plataforma, corre mensual (no diario) y elige Sonnet sobre Opus para esta corrida. Los datos de referencia siguen válidos ~30 días; correrlo diario quema créditos sin output diferente.

Detalles completos: [`skills/ads-update/SKILL.md`](skills/ads-update/SKILL.md).

---

## Qué cambia este fork

Este es un fork comunitario de [tododeia.com](https://tododeia.com) basado en el proyecto open-source `claude-ads` (MIT). Resumen honesto de 30 segundos sobre qué es realmente diferente:

- **`/ads update` (NUEVO en v2.0)** — conocimiento de plataforma auto-refrescante con un pipeline vendoreado de research time-bounded. El skill upstream no se actualizaba solo; este fork sí.
- **Referencias de plataforma actualizadas a 2026** — expansión de Apple Search Ads, AdAttributionKit, diversidad creativa Andromeda, Consent Mode V2 + ganchos de policy EU.
- **Mantenimiento, identidad y rebrand visual** — bug fixes (cobertura de install paths, version strings, refs a archivos fantasma), branding tododeia, este README.

Las 250+ checks originales, los 19 sub-skills, los 10 agentes, las 12 plantillas, la guía de integración MCP y todo el pipeline de auditoría/scoring/reporting vienen del proyecto upstream — el crédito va al maintainer original. Ver [`CHANGELOG.md`](CHANGELOG.md) para la historia completa.

---

## Privacidad y manejo de datos

- **Ejecución local.** Claude Ads corre completamente dentro de tu sesión local de Claude Code. No se manda data de cuentas de ads a tododeia, al autor original ni a ningún servidor de terceros.
- **Sin credenciales en el repo.** Las credenciales de MCP viven en tu propio `~/.claude/.mcp.json`, nunca en el skill.
- **Fetches de URL validados contra SSRF.** El análisis de landing pages bloquea IPs privadas y valida URLs antes de fetch ([`scripts/url_utils.py`](scripts/url_utils.py)).
- **Llamadas de salida de `/ads update`.** Este comando hace llamadas HTTP a internet público (Reddit JSON, Hacker News Algolia, páginas de changelog oficiales, WebSearch) para juntar cambios — nada de tu data de ads sale en esas llamadas.

---

## Preguntas frecuentes

**¿Claude Ads se mete a mi ad manager solito?**
No por default — analiza la data que tú le pases. Si quieres acceso en vivo, instala el servidor MCP que corresponda (ver [Conecta tus cuentas reales de ads](#conecta-tus-cuentas-reales-de-ads)).

**¿Puede crear o editar ads por mí?**
Aún con un servidor MCP con permisos de escritura conectado, Claude Ads se posiciona como herramienta de auditoría + estrategia: encuentra issues, recomienda fixes, arma planes de campaña. Si quieres que efectivamente escriba cambios a tu cuenta es decisión tuya y se activa por MCP — no viene prendido por default.

**¿Qué tan frescos son los benchmarks y reglas de plataforma?**
Las referencias built-in las cura el maintainer. `/ads update` refresca los changelogs por plataforma mensualmente con los últimos 30 días de cambios. Córrelo mensual para mantenerte al día.

**Mi cuenta es chica — ¿siguen aplicando estos benchmarks?**
Dile a Claude tu gasto mensual desde el principio. *"Gasto $2k/mes en Google Ads para un negocio local de plomería"* da resultados mucho mejores que correr `/ads google` en frío. Los benchmarks cambian un montón entre cuentas de $500/mes y $50k/mes.

**¿`/ads update all` me va a tronar los créditos?**
Puede — ver la [tabla de costos de `/ads update`](#ads-update--manteniendo-el-skill-al-día). Usa modo por-plataforma si andas justo de presupuesto, corre mensual no diario, elige Sonnet sobre Opus para la corrida.

**¿Qué plataformas no están cubiertas?**
First-class: Google · Meta · YouTube · LinkedIn · TikTok · Microsoft · Apple. Reddit, CTV/OTT, Pinterest y Snapchat están cubiertas para planeación estratégica pero no para auditoría completa.

---

## Requisitos

- Claude Code CLI
- Python 3.10+
- Playwright (opcional, para análisis de landing pages en vivo)
- reportlab (opcional, para generación de PDF en `/ads report`)

---

## Desinstalar

```bash
# Unix / macOS / Linux
curl -fsSL https://raw.githubusercontent.com/Hainrixz/claude-ads/main/uninstall.sh | bash
```

```powershell
# Windows PowerShell
irm https://raw.githubusercontent.com/Hainrixz/claude-ads/main/uninstall.ps1 | iex
```

---

## Créditos

Mantenido por [**tododeia.com**](https://tododeia.com) · Enrique Henry · [@soyenriquerocha](https://instagram.com/soyenriquerocha).

Originalmente basado en el proyecto open-source `claude-ads` (MIT). El pipeline de research time-bounded vendoreado que potencia `/ads update` está adaptado de [last30days-skill](https://github.com/mvanhorn/last30days-skill) (MIT, por Matt Van Horn) — ver [`scripts/lib/THIRD_PARTY_NOTICES.md`](scripts/lib/THIRD_PARTY_NOTICES.md).

## Licencia

MIT — ver [LICENSE](LICENSE).
