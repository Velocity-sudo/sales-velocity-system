---
description: Sales Velocity System workflow to extract weekly metrics from Meta Ads API and GoHighLevel API for a client. Saves standardized CSVs and a KPI summary JSON to the client's local folder. Run before /create-growth-strategy to have fresh data.
---

# /extract-client-data — Weekly Metrics Extraction

## Overview
Extracts **Meta Ads** and **GoHighLevel pipeline** data for a client and saves it locally. This is the **data layer** — run this first, then use `/create-growth-strategy` to build the strategy on top.

## Prerequisites
- [ ] Python 3 with `requests` installed (`pip3 install requests`)
- [ ] Config file has client credentials: `~/Desktop/Clientes/LuchoBranding/config/clients_config.json`
- [ ] For Meta Ads: System User Token + Ad Account ID
- [ ] For GHL: API Key + Location ID

---

## Steps

### STEP 1: Run extraction for a specific client
// turbo
```bash
python3 ~/Desktop/Clientes/LuchoBranding/scripts/extract_client_data.py --client walter_pagano
```

Or for ALL enabled clients:
```bash
python3 ~/Desktop/Clientes/LuchoBranding/scripts/extract_client_data.py --all
```

Options:
- `--dry-run` → Use mock data (test without API calls)
- `--days 14` → Change Meta Ads lookback period (default: 7)

### STEP 2: Verify output files
// turbo
Check that these files exist in the client folder:
- `leads.csv` — GHL LEADS pipeline opportunities
- `Clientes.csv` — GHL CLIENTES pipeline opportunities 
- `03_ads/meta_insights_7d_YYYY-MM-DD.csv` — Meta Ads metrics (7 days)
- `03_ads/meta_insights_30d_YYYY-MM-DD.csv` — Meta Ads metrics (30 days)
- `06_docs/metricas_semanales_YYYY-MM-DD.json` — KPI summary with deltas

### STEP 3: Run Growth Strategy (manual)
Now that data is fresh, run:
```
/create-growth-strategy
```
for the same client. The workflow will automatically pick up the updated CSVs and JSON.

---

## Adding a New Client

### Guided flow (ask user for credentials one at a time):

**1. GHL API Key** — Ask: "Necesito la API Key de GHL. Ve a Settings → Business Profile → API Key. Empieza con `pit-`."

**2. GHL Location ID** — Ask: "Necesito el Location ID. Ve a Settings → Business Profile → Location ID."

**3. Auto-discover Pipeline IDs** — Once you have the API key + Location ID, discover pipelines automatically:
```python
import requests
r = requests.get("https://services.leadconnectorhq.com/opportunities/pipelines",
    headers={"Authorization": f"Bearer {API_KEY}", "Version": "2021-07-28"},
    params={"locationId": LOCATION_ID})
for p in r.json().get("pipelines", []):
    print(f"  {p['name']}: {p['id']}")
```
> **💡 Never ask the user for pipeline IDs manually.** The API returns all of them.

**4. Meta Ad Account ID** — Ask: "Necesito el Meta Ad Account ID (`act_XXXXXXX`). Si no tiene pauta activa, me dices."

**5. Save config:**
```json
"nuevo_cliente": {
  "name": "Nombre del Cliente",
  "folder": "Nombre del Cliente",
  "meta_ad_account_id": "act_XXXXXXXXXX",
  "ghl_api_key": "pit-XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX",
  "ghl_location_id": "YOUR_LOCATION_ID",
  "pipeline_ids": {
    "pipeline_name_1": "AUTO_DISCOVERED_ID_1",
    "pipeline_name_2": "AUTO_DISCOVERED_ID_2"
  },
  "enabled": true
}
```

**6. Test:** `python3 scripts/extract_client_data.py --client nuevo_cliente --dry-run`

---

## ⚠️ GHL API Gotchas

| Issue | Fix |
|---|---|
| **Contacts pagination returns duplicates** | NEVER paginate `/contacts/` with numeric offsets. Use `meta.total` from first page only. For lead counts, use pipeline opportunities instead. |
| **urllib returns 403** | Always use Python `requests` library, not `urllib.request`. GHL rejects urllib's header handling. |
| **Pipeline IDs** | Auto-discover from API — don't ask users to find them in URLs. |
| **`pit-` API keys need locationId** | The key alone is not enough — always pass `locationId` as a separate param. |

---

## Scheduling (Optional)
To run automatically every Monday at 7AM:
```bash
crontab -e
# Add this line:
0 7 * * 1 /usr/bin/python3 ~/Desktop/Clientes/LuchoBranding/scripts/extract_client_data.py --all >> ~/Desktop/Clientes/LuchoBranding/logs/extraction.log 2>&1
```

---

## Output Files
| File | Location | Description |
|------|----------|-------------|
| `leads.csv` | Client root | GHL LEADS pipeline (overwritten each run) |
| `Clientes.csv` | Client root | GHL CLIENTES pipeline (overwritten each run) |
| `meta_insights_7d_*.csv` | `03_ads/` | Meta Ads last 7 days (accumulated) |
| `meta_insights_30d_*.csv` | `03_ads/` | Meta Ads last 30 days (accumulated) |
| `metricas_semanales_*.json` | `06_docs/` | KPI summary with deltas (accumulated) |
