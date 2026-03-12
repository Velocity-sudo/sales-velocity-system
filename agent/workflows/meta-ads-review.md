---
description: Sales Velocity System workflow to run a weekly Meta Ads performance review for a client. Extracts fresh data, consults the NotebookLM expert notebook for benchmarks and recommendations, generates a premium branded HTML review, and deploys to GitHub Pages. Reviews are immutable — each week creates a new dated file that compares against the previous review.
---

# /meta-ads-review — Weekly Meta Ads Performance Review

## Overview
This workflow generates a **weekly Meta Ads performance review** for a client. It combines real data (Meta Ads API + GHL pipeline) with expert analysis from the **Meta Ads Mastery 2026 NotebookLM notebook** (51 sources, benchmarks, Andromeda strategy, Sales Velocity frameworks).

**Key principles:**
- Each review is **immutable** — once created, it is never modified
- Each new review **compares against the previous** review (week-over-week deltas)
- Reviews are **branded** per client (colors, fonts, logo from Brand Manual)
- Output is a **self-contained HTML** deployed to GitHub Pages
- Maximum **2-3 Notion tasks** created per review

**NotebookLM Notebook ID:** `6aab2459-81ea-406f-b46d-59ac8ecc4fc0`

---

## Prerequisites
- [ ] Client exists in `~/Desktop/Clientes/LuchoBranding/config/clients_config.json` with valid GHL + Meta credentials
- [ ] Client has a **Brand Manual** in `01_marca/`
- [ ] Client has a **Base de Conocimiento** in `06_docs/`
- [ ] Fresh data extracted (auto-runs Thursdays 7AM, or run manually with Step 1)
- [ ] **⚠️ MANDATORY: Meta Ads token is VALID** (not expired) — verified in Step 1
- [ ] **⚠️ MANDATORY: Data validated in Step 1.5** — NEVER proceed without both Meta Ads + GHL data

---

## Steps

### STEP 0: Load Client Context
// turbo

1. **Read the client's Base de Conocimiento** from `06_docs/base_de_conocimiento_[client].md`
   - Extract: industry, offer, average ticket, monthly budget, campaign objectives, target audience
   - Identify client mode: **High Ticket** (VSL → call) or **Volume** (Webinar/Lead Magnet)

2. **Read the client's Brand Manual** from `01_marca/` (HTML file or GitHub Pages URL)
   - Extract: primary color, secondary color, accent color, font families, logo path/URL, dark mode variant
   - These will be used for the HTML review styling

3. **Check for previous reviews** in `07_meta_reviews/`:
   ```bash
   ls -t ~/Desktop/Clientes/[CLIENT_FOLDER]/07_meta_reviews/meta_review_*.html 2>/dev/null | head -3
   ```
   - If a previous review exists, **read it** to extract last week's metrics for comparison
   - Parse the data attributes or summary section from the previous HTML to get: CPL, CTR, CPC, CPM, spend, leads, ROAS, creative count, active campaigns
   - If no previous review exists, this is the baseline — no deltas shown

4. **Create the reviews folder** if it doesn't exist:
   ```bash
   mkdir -p ~/Desktop/Clientes/[CLIENT_FOLDER]/07_meta_reviews
   ```

---

### STEP 1: Extract Fresh Data
// turbo

**⚠️ CRITICAL: Before anything else, validate the Meta Ads token is alive.**

0. **Validate Meta Ads token FIRST** (NON-NEGOTIABLE):
   ```bash
   TOKEN=$(python3 -c "import json; print(json.load(open('$HOME/Desktop/Clientes/LuchoBranding/config/clients_config.json'))['meta_app_token'])")
   curl -s "https://graph.facebook.com/v22.0/debug_token?input_token=${TOKEN}&access_token=${TOKEN}" | python3 -m json.tool
   ```
   - ✅ If response contains `"is_valid": true` → proceed
   - 🛑 If response contains `"error"` or `"is_valid": false` → **STOP IMMEDIATELY**
     - Do NOT proceed to Step 2 or beyond
     - Notify user: "Meta Ads token expired. Go to Meta Business Suite → Settings → System Users to generate a new 60-day token. Then tell me the new token so I can update clients_config.json."
     - **This is a HARD STOP — no review can be generated without Meta Ads data.**

1. **Check if fresh data exists** (from Thursday auto-extraction):
   ```bash
   ls -t ~/Desktop/Clientes/[CLIENT_FOLDER]/06_docs/metricas_semanales_*.json | head -1
   ```
   - If the latest file is from this week → use it
   - If stale (>7 days old) → run extraction:
   ```bash
   cd ~/Desktop/Clientes/LuchoBranding && python3 scripts/extract_client_data.py --client [CLIENT_KEY]
   ```

2. **Read the metrics JSON** — it contains:
   - `meta_ads.7d` — Last 7 days: spend, impressions, reach, clicks, leads, CPL, CTR, CPC, CPM, active_ads
   - `meta_ads.30d` — Last 30 days: same metrics aggregated
   - `pipeline.[name]` — Opportunities by stage, total value
   - `kpis` — lead_to_client_conversion_pct, meta_cpl_7d, meta_spend_30d
   - `deltas` — Week-over-week changes from extraction script

3. **Read Meta Ads campaign-level data** if CSVs exist:
   ```bash
   ls -t ~/Desktop/Clientes/[CLIENT_FOLDER]/03_ads/meta_insights_7d_*.csv | head -1
   ```
   Parse to identify: best/worst campaigns, creative fatigue signals, spend distribution

---

### STEP 1.5: Data Validation Gate (MANDATORY — HARD STOP)

**⚠️ NON-NEGOTIABLE: This gate MUST pass before proceeding to Step 2.**

After extraction, validate that ALL required data sources returned real data:

```python
import json

# Load the metrics JSON
with open('~/Desktop/Clientes/[CLIENT_FOLDER]/06_docs/metricas_semanales_[DATE].json') as f:
    data = json.load(f)

# === VALIDATION CHECKS ===
validation = {
    'meta_ads_data': False,
    'ghl_pipeline_data': False,
    'can_proceed': False
}

# Check 1: Meta Ads data exists and has real numbers
meta = data.get('meta_ads', {}).get('7d', {})
if meta.get('spend') and float(meta['spend']) > 0:
    validation['meta_ads_data'] = True
else:
    print('🛑 FAIL: No Meta Ads data (spend is 0 or missing)')
    print('   → Token may be expired or account access revoked')
    print('   → Run token debug check from Step 1.0')

# Check 2: GHL pipeline data exists
pipeline = data.get('pipeline', {})
if any(v.get('total', 0) > 0 for v in pipeline.values() if isinstance(v, dict)):
    validation['ghl_pipeline_data'] = True
else:
    print('🛑 FAIL: No GHL pipeline data')
    print('   → GHL API key may be invalid or pipeline IDs incorrect')

# FINAL GATE
validation['can_proceed'] = validation['meta_ads_data'] and validation['ghl_pipeline_data']

if validation['can_proceed']:
    print('✅ ALL CHECKS PASSED — Proceed to Step 2')
else:
    print('🛑 HARD STOP — Cannot generate review without complete data')
    print('   Missing:', [k for k, v in validation.items() if not v and k != 'can_proceed'])
```

**Decision matrix:**

| Meta Ads | GHL Pipeline | Action |
|----------|-------------|--------|
| ✅ Valid | ✅ Valid | ✅ Proceed to Step 2 |
| ❌ Missing | ✅ Valid | 🛑 **STOP** — Fix token, do NOT generate review |
| ✅ Valid | ❌ Missing | 🛑 **STOP** — Fix GHL API key |
| ❌ Missing | ❌ Missing | 🛑 **STOP** — Fix both before retrying |

**If validation fails:**
1. Notify user immediately with the specific failure reason
2. Provide exact instructions to fix (token renewal URL, API key location, etc.)
3. **DO NOT** generate a partial review — a "Meta Ads Review" without Meta Ads data is worthless
4. Create a Notion task for the fix if one doesn't exist already
5. Exit the workflow

---

### STEP 2: Consult NotebookLM for Expert Analysis

> [!CAUTION]
> **🚨 THIS STEP IS MANDATORY — NEVER SKIP IT UNDER ANY CIRCUMSTANCES 🚨**
> The NotebookLM expert analysis is the core differentiator of this workflow. A review without it is just raw numbers — useless to the client.
> 
> **If NotebookLM authentication fails:**
> 1. Run `nlm login` in the terminal (automated browser auth)
> 2. If that fails, run `nlm login switch <profile>` to try a different profile
> 3. If the CLI is not installed, guide the user to install it (`pip install notebooklm-cli`)
> 4. As a last resort, use `refresh_auth` MCP tool
> 5. **NEVER proceed to Step 3 or 4 without completing this step. HARD STOP.**

This is the core differentiator. Use the NotebookLM notebook to get **contextual, benchmark-backed recommendations**.

1. **Query 1 — Benchmark Comparison:**
   ```
   Notebook ID: 6aab2459-81ea-406f-b46d-59ac8ecc4fc0

   Query: "Tengo un cliente de [INDUSTRY] en [COUNTRY] con un budget de $[X]/mes en Meta Ads.
   Sus métricas de los últimos 7 días son:
   - CPL: $[Y]
   - CTR: [Z]%
   - CPC: $[W]
   - CPM: $[V]
   - Spend: $[S]
   - Leads: [N]
   - Active ads: [A]

   ¿Cómo se compara vs los benchmarks 2026 para su industria?
   ¿Está por encima o por debajo del promedio?
   Dame números exactos de referencia y un diagnóstico claro."
   ```
   Save the response — it gives benchmark-backed context.

2. **Query 2 — Actionable Recommendations:**
   ```
   Query (same conversation_id): "Basándote en estos datos y en las mejores prácticas de Andromeda 2026:
   - ¿Cuántos creativos debería tener activos? (tiene [A])
   - ¿Su estructura de campaña es óptima o debería consolidar?
   - ¿Qué 3 acciones específicas darían el mayor impacto en las próximas 2 semanas?
   - ¿Hay señales de fatiga creativa?
   - ¿Su bidding strategy es correcta para su objetivo ([MODE])?
   Prioriza las acciones por impacto inmediato."
   ```
   Save the response — these become the prioritized action items.

3. **Query 3 — Landing Page & Funnel Assessment (if applicable):**
   ```
   Query (same conversation_id): "El funnel de este cliente es: Meta Ad → [VSL/Landing Page] → [Calendar/Form] → [Call/Purchase].
   Su tasa de conversión del pipeline es [X]%. El show rate es [Y]%.
   ¿Qué aspectos de la landing page y el funnel debería optimizar según las mejores prácticas 2026?
   ¿Cuál debería ser su tasa de conversión objetivo?"
   ```

> **💡 TIP:** Use the `conversation_id` from Query 1's response for Queries 2 and 3 to maintain context.

---

### STEP 3: Run 46-Check Audit (Key Checks)
// turbo

Don't run all 46 checks every week — focus on the **high-impact subset**:

#### Creative Health (weekly)
- [ ] Active creative count (target: ≥5 per ad set)
- [ ] Format diversity (target: ≥3 formats — image, video, carousel)
- [ ] CTR trend (ALERT if declining >20% over 14 days)
- [ ] Creative age (ALERT if any creative >4 weeks without refresh)

#### Budget & Efficiency (weekly)
- [ ] Budget per ad set vs target CPA (target: ≥5x CPA)
- [ ] Any ad sets in "Learning Limited"? (FAIL if >30%)
- [ ] Kill list check: any campaign with CPA >3x target?
- [ ] Frequency check: prospecting <3.0, retargeting <8.0

#### Structure (monthly — flag only)
- [ ] Campaign consolidation status
- [ ] Advantage+ adoption status
- [ ] Audience overlap check

---

### STEP 4: Build the HTML Review
// turbo

Create the review file at: `07_meta_reviews/meta_review_[YYYY-MM-DD].html`

**Date is TODAY's date** (the day the review runs).

**⚠️ IMMUTABILITY RULE:** NEVER overwrite an existing review file. Always create a NEW file with today's date. If a file for today already exists, append `_v2`.

**Design specs — BRANDED per client (from Brand Manual):**
- Color palette from Brand Manual (primary, secondary, accent)
- Typography from Brand Manual (headings + body fonts)
- Logo in header
- Glassmorphism cards with brand-colored borders
- Dark background adapted from brand palette (fallback: `#0a0e1a`)
- Responsive design (mobile-friendly)
- Self-contained HTML (no external deps except Google Fonts)

**Required sections:**

#### Header
- "META ADS REVIEW — [CLIENT NAME]"
- "Semana del [DATE]"
- Sales Velocity × [Client Brand] badge
- Review number badge (e.g., "Review #4" based on file count in folder)

#### 01 — Resumen Ejecutivo (The Verdict)
Traffic-light system for instant read:
- 🟢 **En camino** — Metrics at or better than benchmarks
- 🟡 **Atención** — 1-2 metrics below benchmark, actionable
- 🔴 **Acción urgente** — Critical issues detected (CPA >3x, creative fatigue, learning limited)

One-paragraph AI-generated summary: "Esta semana el CPL bajó 12% a $18.50, acercándose al benchmark de $16.61 para real estate. Sin embargo, el CTR cayó 15% lo que sugiere inicio de fatiga creativa. Recomendación: rotar creativos esta semana."

#### 02 — Métricas Clave (7 días)
KPI cards in a grid:

| Metric | Current | Previous | Delta | Benchmark | Status |
|--------|---------|----------|-------|-----------|--------|
| CPL | $18.50 | $21.00 | -12% ↓ | $16.61 | 🟡 |
| CTR | 1.1% | 1.3% | -15% ↓ | 1.2% | 🟡 |
| CPC | $1.20 | $1.35 | -11% ↓ | $1.72 | 🟢 |
| CPM | $12.50 | $11.80 | +6% ↑ | $14.08 | 🟢 |
| Spend | $850 | $900 | -6% | — | — |
| Leads | 46 | 43 | +7% ↑ | — | 🟢 |
| ROAS | 3.2x | 2.8x | +14% ↑ | 2.5x | 🟢 |

- "Previous" = last week's review data (or extraction delta)
- "Benchmark" = from NotebookLM response for this industry
- Status = traffic light based on benchmark comparison

#### 03 — Tendencia (30 días)
- Line chart visualization (CSS-only or inline SVG) showing 4-week trend
- Or at minimum: a 4-row table showing week-over-week progression
- Highlight: "El CPL ha bajado 3 semanas consecutivas" or "El CTR lleva 2 semanas cayendo — señal de fatiga"

#### 04 — Diagnóstico del Notebook (AI Analysis)
- Paste the NotebookLM benchmark comparison response (Query 1)
- Format as a branded callout card
- Highlight specific numbers from the analysis

#### 05 — Acciones Prioritarias
From NotebookLM Query 2 + audit checks, create a prioritized table:

| # | Prioridad | Acción | Impacto Esperado | Esfuerzo | Status |
|---|-----------|--------|------------------|----------|--------|
| 1 | 🔴 URGENTE | Pausar campaña X (CPA $180 vs target $50) | Ahorrar $130/semana | 5 min | Pendiente |
| 2 | 🟡 ALTO | Agregar 5 creativos nuevos UGC | Bajar CPL ~20-30% | 2-3 días | Pendiente |
| 3 | 🟡 ALTO | Migrar a Advantage+ | Mejorar distribución | 1 hora | Pendiente |
| 4 | 🟢 MEDIO | Refresh hook de video principal | Recuperar CTR | 1 día | Pendiente |

Maximum 5-7 actions, ordered by impact.

#### 06 — Comparación vs Review Anterior (if exists)
If a previous review exists, show:
- "La semana pasada recomendamos [X] → [Se implementó / Pendiente]"
- Side-by-side metrics comparison table
- Progress narrative: "De las 5 acciones recomendadas, 3 se implementaron. El CPL bajó 12% como resultado."

#### Footer
- "Generado por Sales Velocity × Antigravity"
- "NotebookLM Notebook: Meta Ads Mastery 2026 (51 fuentes)"
- Date and review number
- Link to previous review (if exists)

**DATA ATTRIBUTES (mandatory):**
Include a hidden `<script type="application/json" id="review-data">` block in the HTML with the raw metrics in JSON format. This allows future reviews to parse previous data programmatically:
```json
{
  "review_date": "2026-03-13",
  "review_number": 1,
  "client": "Client Name",
  "industry": "Real Estate",
  "metrics_7d": {
    "cpl": 18.50, "ctr": 1.1, "cpc": 1.20, "cpm": 12.50,
    "spend": 850, "leads": 46, "roas": 3.2, "active_ads": 7
  },
  "benchmarks": {
    "cpl": 16.61, "ctr": 1.2, "cpc": 1.72, "cpm": 14.08, "roas": 2.5
  },
  "actions": [
    {"priority": "urgent", "action": "Pause campaign X", "status": "pending"}
  ]
}
```

---

### STEP 5: Deploy & Distribute

1. **Save locally** (already done in Step 4):
   ```
   ~/Desktop/Clientes/[CLIENT_FOLDER]/07_meta_reviews/meta_review_[YYYY-MM-DD].html
   ```

2. **Deploy to GitHub Pages:**
   ```bash
   cd ~/Desktop/Clientes/[CLIENT_FOLDER]/05_deploy
   mkdir -p meta-reviews
   cp ~/Desktop/Clientes/[CLIENT_FOLDER]/07_meta_reviews/meta_review_[YYYY-MM-DD].html meta-reviews/
   # Also copy as latest.html for easy access
   cp meta-reviews/meta_review_[YYYY-MM-DD].html meta-reviews/latest.html
   git add -A && git commit -m "Meta Ads Review [YYYY-MM-DD]" && git push
   ```
   Live URL: `https://velocity-sudo.github.io/[client-slug]/meta-reviews/meta_review_[YYYY-MM-DD].html`
   Latest: `https://velocity-sudo.github.io/[client-slug]/meta-reviews/latest.html`

3. **Create Notion task** (max 2-3):
   - 📊 **"Meta Ads Review [Date] — [Client]"** → Assigned to Esteban + Lucho, Priority ALTA, Due: this week
     - Callout inside with: live URL, 3 most urgent actions, key metrics summary
   - 🎨 **"Crear [N] creativos nuevos — [Client]"** (only if creative refresh was flagged as urgent)

4. **Update DELIVERABLES.md:**
   Add entry with local path + live GitHub Pages URL for the review

---

### STEP 6: Verify
// turbo

1. Open the GitHub Pages URL in browser to verify rendering
2. Confirm the HTML data JSON block is parseable
3. Verify Notion task was created correctly
4. Confirm DELIVERABLES.md is updated

---

## Output Files
| File | Location |
|------|----------|
| Review HTML | `07_meta_reviews/meta_review_[YYYY-MM-DD].html` |
| GitHub Pages (dated) | `https://velocity-sudo.github.io/[client-slug]/meta-reviews/meta_review_[YYYY-MM-DD].html` |
| GitHub Pages (latest) | `https://velocity-sudo.github.io/[client-slug]/meta-reviews/latest.html` |
| Notion Task | Inside Tasks DB, assigned to Esteban + Lucho |
| DELIVERABLES.md | Updated with review links |

---

## Cadence & Triggers
- **Primary:** Run every **Thursday-Friday** after the 7AM auto-extraction deposits fresh data
- **On-demand:** Before any client meeting
- **Alert trigger (future):** If CPL increases >30% vs previous week in extraction data → auto-flag for immediate review

---

## Immutability Rules (NON-NEGOTIABLE)
1. **NEVER** overwrite or edit a `meta_review_[DATE].html` file that already exists
2. Each review is a **permanent historical record**
3. New reviews always **create a new dated file**
4. The `latest.html` on GitHub Pages is the **only file** that gets overwritten (it's a copy of the newest review)
5. When comparing with the previous review, **read** the previous file's JSON data block — never modify it

---

## Notes
- The NotebookLM notebook (`6aab2459-81ea-406f-b46d-59ac8ecc4fc0`) contains 51 sources: benchmarks, Andromeda strategy, Meta official docs, YouTube expert videos (Ben Heath, Nick Theriot, Charley T), and Sales Velocity frameworks.
- All HTML reviews must be **self-contained** (single file, no external deps except Google Fonts).
- Brand Manual is **mandatory** — every review must match the client's visual identity.
- The review is an **optimization briefing**, not a report. It must answer: "What's happening, what to do about it, in what order."
- This workflow complements `/create-growth-strategy` (strategic layer) by providing **tactical, weekly execution insights**.
