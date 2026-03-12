---
description: Sales Velocity System workflow to create a Growth Strategy presentation for a client. Generates a premium HTML data-driven strategy document with current situation analysis, numerical objectives, prioritized action plan, and key decisions. This is the STRATEGIC layer — tactical deliverables (ads, VSL, reels) build on top of this.
---

# /create-growth-strategy — Growth Strategy Presentation

## Overview
This workflow creates a **premium, data-driven growth strategy presentation** (HTML) for a client. It consolidates all available data (GHL pipeline, dashboard metrics, Meta Ads tracker, CSVs) into a clear, visual document with:
1. **Panorama Actual** — Where we are (data-backed diagnostic)
2. **Objetivos** — Where we want to go (numerical targets)
3. **Plan de Acción** — How we get there (phased, prioritized by impact)
4. **Decisiones** — What the client needs to decide

This is the **strategic base layer**. Tactical deliverables (Ads, VSL, content scripts) are built after this is approved.

---

## Prerequisites
Before running this workflow, ensure you have:
- [ ] Client's **Brand Manual** — `01_marca/BRAND_MANUAL.html` (or the deployed GitHub Pages version). Extract: primary/secondary/accent colors, fonts, logo, tone.
- [ ] Client's **Base de Conocimiento** (knowledge base) — `06_docs/base_de_conocimiento_[client].md`
- [ ] **GHL + Meta Ads connected** — Client must be in `clients_config.json` with valid API credentials (see Step 0)
- [ ] Any **call notes** or strategic context from recent meetings

---

## Steps

### STEP 0: Connect Data Sources (GHL + Meta Ads)
// turbo

> **⚠️ THIS STEP IS MANDATORY.** Never skip it. Every growth strategy must be backed by real, verified data from GHL and Meta Ads. If the client is not connected, guide the user through setup BEFORE doing anything else.

#### 0.1 — Check if client exists in config
```bash
python3 -c "import json; data=json.load(open('$HOME/Desktop/Clientes/LuchoBranding/config/clients_config.json')); [print(f'{k}: {v[\"name\"]} -> {v[\"folder\"]}') for k,v in data['clients'].items() if v.get('enabled')]"
```

#### 0.2 — IF CLIENT NOT FOUND → Guided Setup

Ask the user for credentials **one at a time** in this order. For each one, explain exactly where to find it:

**Step A — GHL API Key (fastest to get):**
> "Necesito la API Key de GoHighLevel. Ve a GHL → Settings → Business Profile → API Key. Empieza con `pit-`."

**Step B — GHL Location ID:**
You can try to auto-discover it from the API. If the pipelines endpoint works, you already have access:
```python
import requests
r = requests.get("https://services.leadconnectorhq.com/opportunities/pipelines",
    headers={"Authorization": f"Bearer {API_KEY}", "Version": "2021-07-28"},
    params={"locationId": "TEST"})
```
If 403 → ask user: "Necesito el Location ID. Ve a GHL → Settings → Business Profile → Location ID (string alfanumérico tipo `ZB1TGjQaChjyGKO0Af0M`)."

**Step C — Auto-discover Pipeline IDs:**
Once you have the API key + Location ID, **auto-discover all pipelines** instead of asking the user:
```python
import requests
r = requests.get("https://services.leadconnectorhq.com/opportunities/pipelines",
    headers={"Authorization": f"Bearer {API_KEY}", "Version": "2021-07-28", "Accept": "application/json"},
    params={"locationId": LOCATION_ID})
pipelines = r.json().get("pipelines", [])
for p in pipelines:
    print(f"  {p['name']}: {p['id']} ({len(p.get('stages',[]))} stages)")
```
Save **ALL pipeline IDs** in the config (not just "leads"/"clientes"). Many clients have custom pipelines (B2B, B2C, Webinar, etc.).

**Step D — Meta Ad Account ID:**
> "Necesito el Meta Ad Account ID. Ve a Meta Business Suite → Settings → Ad Account. Empieza con `act_`. Si Diego todavía no tiene pauta activa, déjame saber y arrancamos solo con GHL."

**Step E — Save to clients_config.json:**
```json
"client_key": {
  "name": "Client Name",
  "folder": "Exact Folder Name",
  "meta_ad_account_id": "act_XXXXXXX",
  "ghl_api_key": "pit-XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX",
  "ghl_location_id": "XXXXXXXXXXXXX",
  "pipeline_ids": {
    "pipeline_name_1": "ID_1",
    "pipeline_name_2": "ID_2"
  },
  "enabled": true
}
```

> **💡 LEARNING:** Pipeline IDs can be auto-discovered from the API. Never ask the user to dig through URLs for these.

#### 0.3 — IF CLIENT FOUND → Run extraction
```bash
cd ~/Desktop/Clientes/LuchoBranding && python3 scripts/extract_client_data.py --client [CLIENT_KEY]
```

#### 0.4 — Verify data quality
After extraction, **always cross-verify critical numbers**:
1. Check GHL UI filters to confirm lead counts match API results
2. For contacts/leads: always use **pipeline opportunity counts** (from `/opportunities/search`), NOT total contact counts (from `/contacts/`)
3. If numbers look suspiciously high, verify with a UI screenshot

> **⚠️ CRITICAL BUG FIX (March 2026):**
> GHL's `/contacts/` endpoint pagination does NOT support numeric offset via `startAfter`. Using `startAfter=100, 200, 300...` returns the **same first page repeatedly**, inflating counts by 30-40x. 
>
> **Correct approaches for contact data:**
> - Use **pipeline searches** (`/opportunities/search` with `pipeline_id`) — these paginate correctly with `page=1,2,3...`
> - If you must count total contacts, use only `meta.total` from the first page — do NOT paginate
> - For tag-based counts, use the GHL UI filter as source of truth
>
> **Rule:** Pipeline opportunity counts = reliable. Raw contact counts = use `meta.total` only, never paginate.

> **NOTE:** Extraction also runs automatically every Thursday at 7AM via launchd.

---

### STEP 1: Gather & Analyze Data
// turbo
1. Read the client's **Brand Manual** from `01_marca/` (HTML file or GitHub Pages URL). Extract:
   - Primary color, secondary color, accent color
   - Font family (headings + body)
   - Logo URL or path
   - Brand tone/voice keywords
2. Read the client's Base de Conocimiento from `06_docs/`
3. **Read the freshly extracted JSON** (just generated in Step 0):
   ```bash
   ls -t ~/Desktop/Clientes/[CLIENT_FOLDER]/06_docs/metricas_semanales_*.json | head -1
   ```
   The JSON contains ALL the data needed:
   - `meta_ads.7d` — Last 7 days: spend, impressions, reach, clicks, leads, purchases, CPL, CTR, active ads
   - `meta_ads.30d` — Last 30 days: same metrics aggregated
   - `pipeline.[name]` — Opportunities by stage, total value per pipeline
   - `kpis` — lead_to_client_conversion_pct, meta_cpl_7d, meta_spend_30d
   - `deltas` — Week-over-week changes (previous vs current with delta_pct)
   - `week_1_ago` — Full snapshot from previous week (if available)
   - `week_2_ago` — Full snapshot from 2 weeks ago (if available)
   Use this data directly — no need for manual CSV imports or screenshots.
4. **FALLBACK — Manual data (only if extraction failed):**
   If the script failed or the client is not in `clients_config.json`:
   - Read CSV files: leads.csv, Clientes.csv (at client folder root)
   - Read Meta Ads data from GHL dashboard or manual tracker
5. If there are **meeting notes** or **seguimiento** docs in `06_docs/`, read them for strategic context.

### STEP 2: Identify Critical Findings
From the data, identify and rank the top findings by urgency:
- **Revenue gaps** (uncollected payments, low ticket, pricing issues)
- **Conversion gaps** (LP conversion drops, lead-to-client rates)
- **Traffic issues** (high CPL, creative fatigue, channel dependency)
- **Operational gaps** (pipeline not optimized, no follow-up system)
- **Growth opportunities** (untapped organic traffic, reactivation potential)

### STEP 3: Build the HTML Presentation
// turbo
Create the strategy file at: `06_docs/estrategia_crecimiento_q[N]_[year]_final.html`

**Design specs — BRANDED per client (use Brand Manual):**
- **Color palette from Brand Manual:** Use client's primary color for accents/highlights, secondary for cards/borders, dark background adapted from brand palette. If brand has no dark variant, use #0a0e1a as base with brand accent colors.
- **Typography from Brand Manual:** Import and use the client's brand fonts (headings + body). Fallback to Inter if brand manual font is unavailable.
- **Logo:** Include client's logo in the hero section and footer.
- Glassmorphism cards (backdrop-filter: blur) with brand-colored borders
- Responsive design (mobile-friendly)
- Sections separated by subtle gradient dividers using brand colors
- The "SALES VELOCITY × [CLIENT BRAND]" header should use the brand's accent color

**Required sections:**

#### Hero
- "SALES VELOCITY × [CLIENT BRAND]"
- "Estrategia Q[N] [YEAR]"
- Date + "Presentación para [Client Name]"

#### 01 — Panorama Actual
- Pipeline overview cards (Total Leads, Active Clients, Pipeline Value, Critical Metric)
- Lead pipeline distribution table (by stage, with %, value, and status indicators)
- Client pipeline distribution table
- **Critical findings** highlighted in callout boxes:
  - Red for urgent (payment, conversion drops)
  - Yellow for opportunities (organic capture, reactivation)
- Q-1 vs Current Q comparison table with arrows (↑/↓)
- Insight box summarizing: "Lo bueno / Lo malo / La oportunidad"

#### 02 — Objetivos Q[N]
- Side-by-side comparison: "Hoy (Q[N-1])" vs "Meta Q[N]"
- Metrics: Clients/Q, Conversion rate, Collection rate, CPL, Ad spend, Revenue
- Funnel projection math: Budget → Leads → Registrations → Clients → Revenue
- Show the exact math behind the revenue target

#### 03 — Plan de Acción
- Structured in **4 phases**, prioritized by speed of impact:
  - 🔴 **Fase 1 (Semana 1): ACCIÓN INMEDIATA** — Highest ROI, zero investment needed (e.g., collections, quick fixes)
  - 🟡 **Fase 2 (Semana 1-2): FUNDACIÓN** — Fix the funnel, capture organic (landing page, reactivation)
  - 🔵 **Fase 3 (Semana 2-4): ACELERACIÓN** — Scale paid (new creatives, retargeting)
  - 🟢 **Fase 4 (Semana 4-8): ESCALA** — Systemize (pipeline automation, YouTube, scale revenue)
- Each phase includes: action items, specific metrics to hit, and timeline badge

#### 04 — Decisiones y Siguientes Pasos
- Numbered list of specific decisions the client needs to make
- Each with context and recommendation
- Examples: budget allocation, landing page strategy, payment policy, content plan

#### 05 — Resumen Ejecutivo
- Visual roadmap with 4 boxes (Semana 1 → Semana 1-2 → Semana 2-4 → Semana 4-8)
- "La Idea Central" callout with the core thesis
- Footer with Sales Velocity branding

### STEP 4: Deploy & Distribute
1. **Local folder:** Copy the final HTML to `02_funnel_ghl/estrategia_crecimiento_q[N]_[year]_final.html`
2. **GitHub Pages:** Copy to `05_deploy/index.html`, commit, and push to `Velocity-sudo/[client-slug]`
3. **Notion:** Create a child page under the client's project page with:
   - Links to GitHub Pages live URL
   - Strategy summary (findings, objectives, phases)
   - Decision checklist (to-do items)
4. **DELIVERABLES.md:** Add the strategy entry with local, live, Notion, and repo links

### STEP 5: Verify
// turbo
1. Open the GitHub Pages URL in browser to verify it renders correctly
2. Verify Notion page has all content
3. Confirm DELIVERABLES.md is updated

---

## Output Files
| File | Location |
|------|----------|
| Strategy HTML (source) | `06_docs/estrategia_crecimiento_q[N]_[year]_final.html` |
| Strategy HTML (funnel copy) | `02_funnel_ghl/estrategia_crecimiento_q[N]_[year]_final.html` |
| GitHub Pages | `05_deploy/index.html` → `https://velocity-sudo.github.io/[client-slug]/` |
| Notion | Child page of client project page |
| DELIVERABLES.md | Updated with all links |

---

## Lessons Learned & Gotchas

### GHL API Pagination (CRITICAL)
- **Pipelines endpoint** (`/opportunities/pipelines`): Works with `locationId` param. Reliable.
- **Opportunities search** (`/opportunities/search`): Use `page=1,2,3...` for pagination. Reliable.
- **Contacts endpoint** (`/contacts/`): `meta.total` is accurate, but pagination via `startAfter` does NOT work as numeric offset. **Never paginate contacts** — use `meta.total` from first request only.
- The `requests` Python library must be used (not `urllib.request`) — GHL returns 403 with urllib due to header handling differences.

### GHL API Key Types
- A `pit-` key is a **Sub-Account** (Location) API key
- It requires `locationId` as a separate parameter — the key alone is NOT enough
- Test with `/opportunities/pipelines?locationId=XXX` first — if it returns 200, the key works

### Pipeline Discovery
- Always auto-discover pipeline IDs from the API instead of asking the user
- Clients often have multiple pipelines beyond "leads"/"clientes" (B2B, B2C, Webinar, Lanzamiento, etc.)
- Save ALL pipelines in config, not just the two defaults

### Data Cross-Verification
- Always verify GHL API numbers against the GHL UI
- If a number looks too high, filter by tag in GHL UI to confirm
- Pipeline opportunity counts are the reliable source of truth for lead counts

---

## Notes
- This workflow produces the **strategic layer only**. Tactical deliverables are created using other workflows:
  - `/create-ad-creatives` — Meta Ads creatives
  - `/create-vsl-ht` — VSL scripts and pages
  - `/copy-viral` / `/guiones-virales` — Content scripts
  - `/create-ghl-communications` — Pipeline communications
- Always prioritize phases by **speed of ROI**: what generates cash fastest goes first.
- The presentation must be self-contained (single HTML file, no external dependencies except Google Fonts).
- All data should be real and sourced — never use placeholder numbers.
