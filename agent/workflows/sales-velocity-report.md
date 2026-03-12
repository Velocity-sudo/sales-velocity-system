---
description: "Sales Velocity Report — Weekly unified report correlating Meta Ads campaigns with GoHighLevel pipeline data. Extracts campaign/ad-level performance, GHL lead stages, and generates a premium branded HTML report with week-over-week comparisons and detailed action items with responsibles."
---

# /sales-velocity-report — Weekly Ads-to-Pipeline Performance Report

## Overview
This workflow generates a **weekly Sales Velocity Report** for a client. It unifies Meta Ads campaign data with GHL pipeline stages to provide a complete view of the acquisition funnel.

**Replaces:** `/meta-ads-review` (which still works as alias)

**Key features:**
- Always includes **GHL pipeline correlation** (mandatory, not optional)
- **Week-over-week comparisons** with deltas, trend arrows, and narrative
- **Campaign + Ad-level breakdown** with active/paused ads and reasons for pausing
- **Lead-by-lead detail** linking each Meta lead to their GHL pipeline stage
- **Lead quality scoring** (qualified, pending, disqualified, lost)
- **Detailed action items** with responsible person, steps, expected impact, effort, and deadline
- **Previous report JSON** is parsed automatically for comparison

**Principles:**
- Each report is **immutable** — once created, never modified
- Each new report **compares against the previous** (week-over-week deltas)
- Reports are **branded** per client (colors, fonts, logo from Brand Manual)
- Self-contained HTML deployed to GitHub Pages
- Naming: `sv_report_[YYYY-MM-DD].html`

**NotebookLM Notebook ID:** `6aab2459-81ea-406f-b46d-59ac8ecc4fc0`

---

## Prerequisites
- [ ] Client in `clients_config.json` with valid GHL + Meta credentials
- [ ] Client has Brand Manual in `01_marca/`
- [ ] Client has Base de Conocimiento in `06_docs/`
- [ ] Meta Ads token is VALID (not expired)
- [ ] GHL API Key is VALID

---

## Steps

### STEP 0: Load Client Context & Previous Report
// turbo

1. **Read Base de Conocimiento** from `06_docs/base_de_conocimiento_[client].md`
2. **Read Brand Manual** from `01_marca/`
3. **Check for previous reports** in `07_meta_reviews/`:
   ```bash
   ls -t ~/Desktop/Clientes/[CLIENT]/07_meta_reviews/sv_report_*.html 2>/dev/null | head -1
   ls -t ~/Desktop/Clientes/[CLIENT]/07_meta_reviews/meta_review_*.html 2>/dev/null | head -1
   ```
   - If previous exists: parse `<script id="review-data">` JSON for delta calculations
   - If none: this is BASELINE (no deltas, show "BASELINE" badges)
4. Create `07_meta_reviews/` if needed

---

### 🚨 STEP 0.5: META ADS ACCESS GATE (MANDATORY — NEVER SKIP)

> [!CAUTION]
> **HARD GATE — DO NOT PROCEED PAST THIS STEP** unless BOTH validations pass OR the user explicitly says `--force` or "avanza sin Meta Ads".
> Running this workflow without Meta Ads data produces an incomplete report. It's a waste of time.

**Validation 1 — Token validity:**
```bash
TOKEN=$(python3 -c "import json; print(json.load(open('$HOME/Desktop/Clientes/LuchoBranding/config/clients_config.json'))['meta_app_token'])")
curl -s "https://graph.facebook.com/v22.0/debug_token?input_token=${TOKEN}&access_token=${TOKEN}" | python3 -m json.tool
```
- ✅ `is_valid: true` → pass
- ❌ `is_valid: false` or error → **HARD STOP** → tell user token expired, follow renewal procedure

**Validation 2 — Client ad account access:**
```bash
AD_ACCOUNT_ID="act_[CLIENT_AD_ACCOUNT]"
curl -s "https://graph.facebook.com/v22.0/${AD_ACCOUNT_ID}?fields=name,account_status&access_token=${TOKEN}" | python3 -m json.tool
```
- ✅ Returns `name` + `account_status` → pass
- ❌ Returns error 190/100/273 → **HARD STOP** → tell user: "El cliente no ha otorgado permiso ads_read. No puedo generar un Sales Velocity Report sin datos de Meta Ads. Pídele que otorgue acceso."

**Gate result:**
- **BOTH pass** → proceed to STEP 1
- **ANY fails** → STOP immediately. Report to user what failed and what action is needed. Do NOT proceed to pipeline extraction, NotebookLM, or HTML generation.
- **User says `--force` or explicitly overrides** → proceed but add a visible ⚠️ banner in the report: "REPORTE SIN DATOS DE META ADS — Generado con --force. Datos de ads NO disponibles."

---

### STEP 1: Extract Fresh Meta Ads Data (Campaign + Ad Level)
// turbo

1. **Campaign-level data** (7 days): name, status, spend, impressions, clicks, reach, frequency, leads, CPR, CTR
2. **Ad-level data** (7 days): name, status (ACTIVE/PAUSED), ad set, spend, clicks, reach, actions (complete_registration)
3. **Calculate per ad:** registrations, CPR, status
4. **For paused ads, determine reason:**
   - "$X spent with 0 registrations"
   - "Good CTR but 0 conversions — hook doesn't close"
   - "Meta didn't distribute (<50 impressions)"
   - "High CPR vs sibling ads"

---

### STEP 2: Extract GHL Pipeline Data & Correlate
// turbo

1. **Get all contacts created since last report** (or campaign start)
2. **Filter by date range** using `createdAt`
3. **Identify Meta leads** via source field or UTM attributions
4. **For each Meta lead:** name, pipeline stage, date, campaign (UTM), qualification:
   - **Qualified:** CALIENTE SETTER, AGENDA CLOSER, CALIENTE CLOSER, VENTA
   - **Pending:** LEAD, REDES
   - **Disqualified:** NO EMPRESA, MAL CREDITO
   - **Lost:** NO INTERESADOS, NO RESPONDE
5. **Calculate:** total Meta leads, qualification rate, booking rate, pipeline value

---

### STEP 3: Consult NotebookLM
// turbo

> [!CAUTION]
> MANDATORY — NEVER SKIP. HARD STOP if auth fails.

1. **Query 1 — Benchmarks + Comparison** (include previous week data if available)
2. **Query 2 — Actions with pipeline context** (include qualification rates, booking rate)

---

### STEP 4: Build HTML Report
// turbo

File: `07_meta_reviews/sv_report_[YYYY-MM-DD].html`

**7 Required Sections:**

#### Header
- "SALES VELOCITY REPORT — [CLIENT]"
- Report # badge, date, "Sales Velocity x [Brand]"

#### 01 — Veredicto Ejecutivo
Traffic light (green/yellow/red) + 1-paragraph summary

#### 02 — KPIs Consolidados (WITH DELTAS)
Each KPI card shows: Current | Previous | Delta (arrow + color) | Benchmark | Status
- Cost metrics (CPR, CPC, CPM): decrease = green, increase = red
- Performance metrics (CTR, leads, qualified%): increase = green, decrease = red
- If no previous: show "BASELINE" tag

#### 03 — Desglose por Campana
Per campaign: header with totals, ad table (active + paused with reasons)
Winner callout (green), paused explanation (red)
If previous: delta column per campaign

#### 04 — Correlacion Meta → Pipeline GHL
Quality cards (qualified/pending/disqualified/lost) with deltas vs previous
Funnel bar chart by stage
If previous: show quality delta percentages

#### 05 — Detalle de Leads
Table: name, GHL stage, date, campaign (UTM), status emoji
Color-coded. If previous: badge "NEW" for leads not in last report

#### 06 — Comparacion vs Reporte Anterior
**If baseline:** "Este es el primer Sales Velocity Report" badge
**If previous exists:**
- Metric comparison table (previous vs current vs change vs trend)
- Actions follow-up: which were implemented, results, pending
- Narrative: "La semana pasada se recomendo X. Se implemento Y. Resultado: Z."

#### 07 — Acciones Prioritarias (Detailed)
Each action (max 5-7) includes:
- Priority: P1 URGENTE / P2 ALTO / P3 MEDIO
- Title
- Responsible: name + role
- Deadline: specific date
- Success metric: measurable KPI
- Effort: time estimate
- Expected impact
- Steps: 3-5 numbered instructions

#### Footer + JSON Data Block
- `<script type="application/json" id="review-data">` with all metrics for future parsing

---

### STEP 5: Deploy & Distribute

1. Save locally in `07_meta_reviews/`
2. Deploy to GitHub Pages (`05_deploy/`)
3. Create Notion task with actions and responsibles
4. Update DELIVERABLES.md

---

### STEP 6: Verify
// turbo

1. Open GitHub Pages URL — verify all 7 sections render
2. Confirm JSON data block parseable
3. Verify Notion task created
4. Confirm DELIVERABLES.md updated

---

## Delta Calculation Reference

```python
def calc_delta(current, previous, metric_type="cost"):
    if previous == 0 or previous is None:
        return (None, "", "neutral")
    delta_pct = ((current - previous) / previous) * 100
    if metric_type == "cost":
        color = "green" if delta_pct < 0 else "red"
        arrow = "down" if delta_pct < 0 else "up"
    else:
        color = "green" if delta_pct > 0 else "red"
        arrow = "up" if delta_pct > 0 else "down"
    return (delta_pct, arrow, color)
```

| Cost Metrics (lower=better) | Performance Metrics (higher=better) |
|---|---|
| CPR, CPC, CPM | CTR, Leads, ROAS, Qualified%, Booking Rate |

---

## Cadence
- **Primary:** Thursday-Friday after 7AM auto-extraction
- **On-demand:** Before client meetings
- **Alert (future):** CPR increase >30% → auto-flag

## Immutability Rules
1. NEVER overwrite existing `sv_report_[DATE].html`
2. Each report is permanent
3. `latest.html` is the only overwritten file
4. Previous JSON data: read only

## Notes
- NotebookLM notebook has 51 sources (benchmarks, Andromeda, best practices)
- Old `/meta-ads-review` files recognized for comparison during migration
- Report answers: "What happened, how does it compare, what to do, who does it, by when"
