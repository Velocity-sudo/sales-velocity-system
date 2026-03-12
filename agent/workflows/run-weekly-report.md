---
description: Sales Velocity System workflow to run the weekly data extraction and report generation. Can be triggered manually or runs automatically via N8N every Thursday at 7AM.
---

# /run-weekly-report — Weekly Report Generation

## Overview
This workflow extracts fresh data from Meta Ads + GHL for each configured client, generates an AI-powered weekly performance report, saves it locally, and emails it to the team.

**Automatic mode:** N8N runs this every Thursday at 7AM.
**Manual mode:** Use the steps below to trigger a report on-demand.

---

## Prerequisites
- [ ] Python 3 + `requests` installed
- [ ] `clients_config.json` configured with API keys for each client
- [ ] N8N running with the `Sales Velocity — Weekly Report` workflow imported
- [ ] OpenAI API key configured in N8N

---

## Steps (Manual Trigger)

### STEP 1: Extract Data
// turbo
Run the extraction script for a specific client or all clients:

```bash
# Single client
cd ~/Desktop/Clientes/LuchoBranding
python3 scripts/extract_client_data.py --client walter_pagano

# All enabled clients
python3 scripts/extract_client_data.py --all

# With JSON output (for debugging N8N integration)
python3 scripts/extract_client_data.py --client walter_pagano --json-output
```

### STEP 2: Trigger N8N Report
If N8N is running, trigger the workflow manually via:
1. Open N8N dashboard → `Sales Velocity — Weekly Report` workflow
2. Click "Execute Workflow" (manual run)
3. The workflow will extract data, generate AI analysis, build HTML report, and send email

### STEP 3: Verify Output
// turbo
Check the generated files:
```bash
# Check KPI JSON
cat ~/Desktop/Clientes/[Client Folder]/06_docs/metricas_semanales_*.json | python3 -m json.tool

# Check HTML report
ls -la ~/Desktop/Clientes/[Client Folder]/06_docs/informe_semanal_*.html
```

---

## Output Files
| File | Location |
|------|----------|
| KPI JSON | `06_docs/metricas_semanales_YYYY-MM-DD.json` |
| HTML Report | `06_docs/informe_semanal_YYYY-MM-DD.html` |
| Leads CSV | `leads.csv` (root of client folder) |
| Clients CSV | `Clientes.csv` (root of client folder) |
| Meta CSV (7d) | `03_ads/meta_insights_7d_YYYY-MM-DD.csv` |
| Meta CSV (30d) | `03_ads/meta_insights_30d_YYYY-MM-DD.csv` |
| Backup CSVs | `_archivados/` |

---

## N8N Setup Instructions
1. Open N8N → Import Workflow → select `scripts/n8n_weekly_report.json`
2. Configure credentials:
   - **OpenAI**: Add your API key in N8N credentials
   - **SMTP**: Add your email SMTP credentials (Gmail, SendGrid, etc.)
3. Update the email node with your actual FROM/TO addresses
4. Activate the workflow → it runs every Thursday at 7AM

---

## Adding New Clients
1. Add the client to `config/clients_config.json` with Meta + GHL credentials
2. Set `"enabled": true`
3. The workflow automatically picks up all enabled clients

---

## Token Renewal
- Meta Ads long-lived token expires every 60 days
- Re-run the OAuth flow to generate a new token
- Update `clients_config.json` with the new token
