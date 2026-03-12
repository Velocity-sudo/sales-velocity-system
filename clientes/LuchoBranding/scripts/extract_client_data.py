#!/usr/bin/env python3
"""
Sales Velocity — Weekly Client Data Extraction
Pulls metrics from Meta Ads API + GoHighLevel API and saves to client folders.

Usage:
    python3 extract_client_data.py --client walter_pagano
    python3 extract_client_data.py --all
    python3 extract_client_data.py --client walter_pagano --dry-run
    python3 extract_client_data.py --client walter_pagano --days 14
"""

import argparse
import csv
import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from urllib.parse import urlencode

try:
    import requests
except ImportError:
    print("❌ 'requests' not found. Install with: pip3 install requests")
    sys.exit(1)

# ─────────────────────────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────────────────────────

SCRIPT_DIR = Path(__file__).parent
CONFIG_PATH = SCRIPT_DIR.parent / "config" / "clients_config.json"

META_API_VERSION = "v21.0"
META_BASE_URL = f"https://graph.facebook.com/{META_API_VERSION}"

GHL_BASE_URL = "https://services.leadconnectorhq.com"

# Meta Ads fields to extract
META_INSIGHTS_FIELDS = [
    "campaign_name", "adset_name", "ad_name",
    "spend", "impressions", "reach", "clicks",
    "cpc", "cpm", "ctr", "frequency",
    "actions", "cost_per_action_type",
    "purchase_roas"
]

# GHL opportunity fields (columns matching existing CSV format)
GHL_OPPORTUNITY_COLUMNS = [
    "Opportunity Name", "Contact Name", "phone", "email",
    "pipeline", "stage", "Lead Value", "source", "assigned",
    "Created on", "Updated on", "lost reason ID", "lost reason name",
    "Followers", "Notes", "tags", "Engagement Score", "status",
    "Opportunity ID", "Contact ID", "Pipeline Stage ID", "Pipeline ID",
    "Days Since Last Stage Change Date",
    "Days Since Last Status Change Date",
    "Days Since Last Updated"
]


def load_config():
    """Load client configuration from JSON file."""
    if not CONFIG_PATH.exists():
        print(f"❌ Config file not found at: {CONFIG_PATH}")
        print("   Create it with your API credentials first.")
        sys.exit(1)
    with open(CONFIG_PATH) as f:
        return json.load(f)


# ─────────────────────────────────────────────────────────────
# META ADS API
# ─────────────────────────────────────────────────────────────

def extract_meta_ads(config, client_config, days=7, dry_run=False):
    """
    Extract Meta Ads insights for the given client.
    Returns a list of dicts with campaign/adset/ad level metrics.
    """
    token = config["meta_app_token"]
    ad_account_id = client_config["meta_ad_account_id"]

    if dry_run:
        print("  🔸 [DRY RUN] Would call Meta Ads API for:", ad_account_id)
        return _generate_mock_meta_data()

    if token.startswith("YOUR_") or ad_account_id.startswith("act_XXXX"):
        print("  ⚠️  Meta Ads: Credentials not configured — skipping.")
        return None

    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date_7d = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    start_date_30d = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")

    results = {}
    for label, start in [("7d", start_date_7d), ("30d", start_date_30d)]:
        params = {
            "access_token": token,
            "fields": ",".join(META_INSIGHTS_FIELDS),
            "time_range": json.dumps({"since": start, "until": end_date}),
            "level": "ad",
            "limit": 500,
        }
        safe_chars = ',{}:"'
        query_string = urlencode(params, safe=safe_chars)
        url = f"{META_BASE_URL}/{ad_account_id}/insights?{query_string}"

        print(f"  📡 Fetching Meta Ads insights ({label})...")
        try:
            resp = requests.get(url, timeout=30)
            resp.raise_for_status()
            data = resp.json().get("data", [])
            results[label] = data
            print(f"  ✅ Got {len(data)} ad-level records ({label})")

            # Paginate if needed
            paging = resp.json().get("paging", {})
            while "next" in paging:
                resp = requests.get(paging["next"], timeout=30)
                resp.raise_for_status()
                page_data = resp.json().get("data", [])
                results[label].extend(page_data)
                paging = resp.json().get("paging", {})

        except requests.exceptions.HTTPError as e:
            print(f"  ❌ Meta Ads API error ({label}): {e}")
            error_body = e.response.json() if e.response else {}
            if "error" in error_body:
                err = error_body["error"]
                print(f"     Code: {err.get('code')}, Message: {err.get('message')}")
            results[label] = []
        except Exception as e:
            print(f"  ❌ Meta Ads request failed ({label}): {e}")
            results[label] = []

    return results


def _parse_meta_actions(actions_list, target_type):
    """Extract a specific action value from Meta's actions array."""
    if not actions_list:
        return 0
    for action in actions_list:
        if action.get("action_type") == target_type:
            return float(action.get("value", 0))
    return 0


def _parse_meta_cost_per_action(cost_list, target_type):
    """Extract cost per specific action from Meta's cost_per_action_type array."""
    if not cost_list:
        return 0
    for item in cost_list:
        if item.get("action_type") == target_type:
            return float(item.get("value", 0))
    return 0


def save_meta_csv(meta_data, client_folder, date_str):
    """Save Meta Ads data as CSVs in the client's 03_ads/ folder."""
    ads_folder = client_folder / "03_ads"
    ads_folder.mkdir(exist_ok=True)

    saved_files = []
    for period, records in meta_data.items():
        if not records:
            continue

        filename = f"meta_insights_{period}_{date_str}.csv"
        filepath = ads_folder / filename

        # Build clean rows
        rows = []
        for r in records:
            leads = _parse_meta_actions(r.get("actions"), "offsite_conversion.fb_pixel_complete_registration")
            cpl = _parse_meta_cost_per_action(r.get("cost_per_action_type"), "offsite_conversion.fb_pixel_complete_registration")
            purchases = _parse_meta_actions(r.get("actions"), "offsite_conversion.fb_pixel_purchase")
            roas_list = r.get("purchase_roas", [])
            roas = float(roas_list[0]["value"]) if roas_list else 0

            rows.append({
                "Campaña": r.get("campaign_name", ""),
                "Conjunto de Anuncios": r.get("adset_name", ""),
                "Anuncio": r.get("ad_name", ""),
                "Gasto (USD)": float(r.get("spend", 0)),
                "Impresiones": int(r.get("impressions", 0)),
                "Alcance": int(r.get("reach", 0)),
                "Clics": int(r.get("clicks", 0)),
                "CPC (USD)": float(r.get("cpc", 0)),
                "CPM (USD)": float(r.get("cpm", 0)),
                "CTR (%)": float(r.get("ctr", 0)),
                "Frecuencia": float(r.get("frequency", 0)),
                "Registros (Leads)": int(leads),
                "CPL (USD)": round(cpl, 2),
                "Compras": int(purchases),
                "ROAS": round(roas, 2),
            })

        with open(filepath, "w", newline="", encoding="utf-8") as f:
            if rows:
                writer = csv.DictWriter(f, fieldnames=rows[0].keys())
                writer.writeheader()
                writer.writerows(rows)

        saved_files.append(str(filepath))
        print(f"  💾 Saved: {filepath.name} ({len(rows)} rows)")

    return saved_files


def _generate_mock_meta_data():
    """Generate mock Meta data for dry-run testing."""
    return {
        "7d": [
            {
                "campaign_name": "MOCK - Campaign 1",
                "adset_name": "AdSet A",
                "ad_name": "Ad Creative 1",
                "spend": "150.00",
                "impressions": "5000",
                "reach": "3200",
                "clicks": "120",
                "cpc": "1.25",
                "cpm": "30.00",
                "ctr": "2.4",
                "frequency": "1.56",
                "actions": [
                    {"action_type": "offsite_conversion.fb_pixel_complete_registration", "value": "22"},
                    {"action_type": "offsite_conversion.fb_pixel_purchase", "value": "1"}
                ],
                "cost_per_action_type": [
                    {"action_type": "offsite_conversion.fb_pixel_complete_registration", "value": "6.82"}
                ],
                "purchase_roas": [{"value": "5.5"}]
            }
        ],
        "30d": [
            {
                "campaign_name": "MOCK - Campaign 1",
                "adset_name": "AdSet A",
                "ad_name": "Ad Creative 1",
                "spend": "600.00",
                "impressions": "19000",
                "reach": "10500",
                "clicks": "480",
                "cpc": "1.25",
                "cpm": "31.58",
                "ctr": "2.53",
                "frequency": "1.81",
                "actions": [
                    {"action_type": "offsite_conversion.fb_pixel_complete_registration", "value": "88"},
                    {"action_type": "offsite_conversion.fb_pixel_purchase", "value": "3"}
                ],
                "cost_per_action_type": [
                    {"action_type": "offsite_conversion.fb_pixel_complete_registration", "value": "6.82"}
                ],
                "purchase_roas": [{"value": "7.5"}]
            }
        ]
    }


# ─────────────────────────────────────────────────────────────
# GOHIGHLEVEL API
# ─────────────────────────────────────────────────────────────

def extract_ghl_opportunities(client_config, pipeline_key, dry_run=False):
    """
    Extract all opportunities from a GHL pipeline.
    Returns list of opportunity dicts.
    """
    api_key = client_config.get("ghl_api_key", "")
    location_id = client_config.get("ghl_location_id", "")
    pipeline_id = client_config.get("pipeline_ids", {}).get(pipeline_key, "")

    if dry_run:
        print(f"  🔸 [DRY RUN] Would call GHL API for pipeline: {pipeline_key}")
        return _generate_mock_ghl_data(pipeline_key)

    if api_key.startswith("YOUR_") or not pipeline_id:
        print(f"  ⚠️  GHL ({pipeline_key}): Credentials not configured — skipping.")
        return None

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Version": "2021-07-28",
        "Accept": "application/json",
    }

    # First: get pipeline stage names
    stages_map = {}
    try:
        print(f"  📡 Fetching GHL pipeline stages ({pipeline_key})...")
        resp = requests.get(
            f"{GHL_BASE_URL}/opportunities/pipelines",
            headers=headers,
            params={"locationId": location_id},
            timeout=20
        )
        resp.raise_for_status()
        pipelines = resp.json().get("pipelines", [])
        for p in pipelines:
            if p.get("id") == pipeline_id:
                for stage in p.get("stages", []):
                    stages_map[stage["id"]] = stage.get("name", stage["id"])
                break
    except Exception as e:
        print(f"  ⚠️  Could not fetch pipeline stages: {e}")

    # Second: get all opportunities with pagination
    all_opportunities = []
    page = 1
    while True:
        try:
            params = {
                "location_id": location_id,
                "pipeline_id": pipeline_id,
                "limit": 100,
                "page": page,
            }
            print(f"  📡 Fetching GHL opportunities ({pipeline_key}, page {page})...")
            resp = requests.get(
                f"{GHL_BASE_URL}/opportunities/search",
                headers=headers,
                params=params,
                timeout=30
            )
            resp.raise_for_status()
            data = resp.json()
            opportunities = data.get("opportunities", [])
            all_opportunities.extend(opportunities)

            meta = data.get("meta", {})
            total = meta.get("total", 0)
            if len(all_opportunities) >= total or not opportunities:
                break
            page += 1

        except requests.exceptions.HTTPError as e:
            print(f"  ❌ GHL API error ({pipeline_key}): {e}")
            if e.response:
                print(f"     Response: {e.response.text[:300]}")
            break
        except Exception as e:
            print(f"  ❌ GHL request failed ({pipeline_key}): {e}")
            break

    print(f"  ✅ Got {len(all_opportunities)} opportunities ({pipeline_key})")

    # Map stage IDs to names
    for opp in all_opportunities:
        stage_id = opp.get("pipelineStageId", "")
        opp["_stage_name"] = stages_map.get(stage_id, stage_id)

    return all_opportunities


def _days_since(date_str):
    """Calculate human-friendly days since a date string."""
    if not date_str:
        return ""
    try:
        dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        delta = datetime.now(dt.tzinfo) - dt
        days = delta.days
        if days == 0:
            return " Today"
        elif days == 1:
            return "1 Day "
        else:
            return f"{days} Days "
    except Exception:
        return ""


def save_ghl_csv(opportunities, pipeline_name, client_folder):
    """
    Save GHL opportunities as CSV matching the existing format.
    Pipeline name → {pipeline_name}.csv
    Backwards compatibility: 'leads' → leads.csv, 'clientes' → Clientes.csv
    """
    if not opportunities:
        return None

    # Legacy names for backwards compat; everything else uses pipeline_name.csv
    legacy_names = {"leads": "leads.csv", "clientes": "Clientes.csv"}
    filename = legacy_names.get(pipeline_name, f"{pipeline_name}.csv")
    filepath = client_folder / filename

    rows = []
    for opp in opportunities:
        contact = opp.get("contact", {})
        tags = contact.get("tags", [])
        if isinstance(tags, list):
            tags_str = ",".join(tags)
        else:
            tags_str = str(tags)

        rows.append({
            "Opportunity Name": opp.get("name", ""),
            "Contact Name": contact.get("name", opp.get("name", "")),
            "phone": contact.get("phone", ""),
            "email": contact.get("email", ""),
            "pipeline": pipeline_name.upper(),
            "stage": opp.get("_stage_name", ""),
            "Lead Value": opp.get("monetaryValue", 0),
            "source": opp.get("source", ""),
            "assigned": opp.get("assignedTo", ""),
            "Created on": opp.get("createdAt", ""),
            "Updated on": opp.get("updatedAt", ""),
            "lost reason ID": opp.get("lostReasonId", ""),
            "lost reason name": "",
            "Followers": "",
            "Notes": "",
            "tags": tags_str,
            "Engagement Score": 0,
            "status": opp.get("status", ""),
            "Opportunity ID": opp.get("id", ""),
            "Contact ID": contact.get("id", opp.get("contactId", "")),
            "Pipeline Stage ID": opp.get("pipelineStageId", ""),
            "Pipeline ID": opp.get("pipelineId", ""),
            "Days Since Last Stage Change Date": _days_since(opp.get("lastStageChangeAt", "")),
            "Days Since Last Status Change Date": _days_since(opp.get("lastStatusChangeAt", "")),
            "Days Since Last Updated": _days_since(opp.get("updatedAt", "")),
        })

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=GHL_OPPORTUNITY_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)

    print(f"  💾 Saved: {filename} ({len(rows)} records)")
    return str(filepath)


def _generate_mock_ghl_data(pipeline_key):
    """Generate mock GHL data for dry-run testing."""
    mock_stages = {
        "leads": ["LEAD", "REDES", "AGENDA CLOSER", "NO CUALIFICADO"],
        "clientes": ["ONBOARDING", "ACOMPANAMIENTO", "COMPLETADO"]
    }
    stages = mock_stages.get(pipeline_key, ["STAGE_1"])
    opportunities = []
    for i in range(15):
        stage = stages[i % len(stages)]
        opportunities.append({
            "id": f"mock_opp_{i}",
            "name": f"Mock Contact {i+1}",
            "contact": {
                "id": f"mock_contact_{i}",
                "name": f"Mock Contact {i+1}",
                "phone": f"+1555000{i:04d}",
                "email": f"mock{i+1}@example.com",
                "tags": ["mock_tag", "lead_registro_vsl"]
            },
            "pipelineId": "MOCK_PIPELINE",
            "pipelineStageId": f"stage_{stage}",
            "_stage_name": stage,
            "status": "open",
            "monetaryValue": 5000 if pipeline_key == "clientes" else 0,
            "source": "VSL Mentoria",
            "assignedTo": "",
            "createdAt": (datetime.now() - timedelta(days=i*2)).isoformat() + "Z",
            "updatedAt": (datetime.now() - timedelta(days=i)).isoformat() + "Z",
            "lastStageChangeAt": (datetime.now() - timedelta(days=i)).isoformat() + "Z",
            "lastStatusChangeAt": (datetime.now() - timedelta(days=i)).isoformat() + "Z",
            "lostReasonId": "",
        })
    return opportunities


# ─────────────────────────────────────────────────────────────
# SUMMARY / KPI GENERATION
# ─────────────────────────────────────────────────────────────

def generate_kpi_summary(meta_data, leads_data, clients_data, client_name, date_str, client_folder):
    """
    Generate a JSON summary of key KPIs for the client.
    This is the file that /create-growth-strategy reads for quick analysis.
    """
    summary = {
        "client": client_name,
        "extraction_date": date_str,
        "extraction_timestamp": datetime.now().isoformat(),
        "meta_ads": {},
        "pipeline": {},
        "kpis": {}
    }

    # ── Meta Ads KPIs ──
    if meta_data:
        for period in ["7d", "30d"]:
            records = meta_data.get(period, [])
            if records:
                total_spend = sum(float(r.get("spend", 0)) for r in records)
                total_impressions = sum(int(r.get("impressions", 0)) for r in records)
                total_reach = sum(int(r.get("reach", 0)) for r in records)
                total_clicks = sum(int(r.get("clicks", 0)) for r in records)
                total_leads = sum(
                    _parse_meta_actions(r.get("actions"), "offsite_conversion.fb_pixel_complete_registration")
                    for r in records
                )
                total_purchases = sum(
                    _parse_meta_actions(r.get("actions"), "offsite_conversion.fb_pixel_purchase")
                    for r in records
                )

                avg_cpl = total_spend / total_leads if total_leads > 0 else 0
                avg_ctr = (total_clicks / total_impressions * 100) if total_impressions > 0 else 0

                summary["meta_ads"][period] = {
                    "total_spend_usd": round(total_spend, 2),
                    "total_impressions": total_impressions,
                    "total_reach": total_reach,
                    "total_clicks": total_clicks,
                    "total_leads": int(total_leads),
                    "total_purchases": int(total_purchases),
                    "avg_cpl_usd": round(avg_cpl, 2),
                    "avg_ctr_pct": round(avg_ctr, 2),
                    "num_active_ads": len(records),
                }

    # ── Pipeline KPIs (dynamic — supports any pipeline names) ──
    # pipelines_data is a dict: {"pipeline_key": [opportunities_list], ...}
    # Backwards compatible: also accepts leads_data/clients_data as positional args
    if isinstance(leads_data, dict):
        # New format: leads_data is actually all_pipelines_data dict
        all_pipelines = leads_data
    else:
        # Legacy format: separate leads_data and clients_data
        all_pipelines = {}
        if leads_data is not None:
            all_pipelines["leads"] = leads_data
        if clients_data is not None:
            all_pipelines["clientes"] = clients_data

    total_all_opps = 0
    total_all_value = 0
    for pipe_key, pipe_data in all_pipelines.items():
        if pipe_data is None:
            continue
        by_stage = {}
        for opp in pipe_data:
            stage = opp.get("_stage_name", "Unknown")
            by_stage[stage] = by_stage.get(stage, 0) + 1
        pipe_value = sum(float(opp.get("monetaryValue", 0) or 0) for opp in pipe_data)
        summary["pipeline"][pipe_key] = {
            "total": len(pipe_data),
            "by_stage": by_stage,
            "total_pipeline_value": pipe_value,
        }
        total_all_opps += len(pipe_data)
        total_all_value += pipe_value

    # ── Combined KPIs ──
    # For backwards compat: use 'leads' and 'clientes' if they exist, otherwise sum all
    total_leads = summary.get("pipeline", {}).get("leads", {}).get("total", 0)
    total_clients = summary.get("pipeline", {}).get("clientes", {}).get("total", 0)
    if total_leads == 0 and total_clients == 0:
        # No legacy 'leads'/'clientes' keys — use totals across all pipelines
        total_leads = total_all_opps
        total_clients = 0  # Can't determine without knowing which pipeline is "clients"
    conversion_rate = (total_clients / total_leads * 100) if total_leads > 0 else 0

    summary["kpis"] = {
        "total_leads_in_pipeline": total_leads if total_leads > 0 else total_all_opps,
        "total_active_clients": total_clients,
        "lead_to_client_conversion_pct": round(conversion_rate, 2),
        "total_pipeline_value": total_all_value,
        "total_opportunities": total_all_opps,
        "meta_cpl_7d": summary.get("meta_ads", {}).get("7d", {}).get("avg_cpl_usd", 0),
        "meta_spend_30d": summary.get("meta_ads", {}).get("30d", {}).get("total_spend_usd", 0),
    }

    # ── Compare with previous weeks (last 2) ──
    docs_folder = client_folder / "06_docs"
    previous_files = sorted(docs_folder.glob("metricas_semanales_*.json"), reverse=True)

    # Load up to 2 previous weeks
    prev_weeks = []
    for pf in previous_files[:2]:
        try:
            with open(pf) as f:
                prev_weeks.append(json.load(f))
        except Exception as e:
            print(f"  ⚠️  Could not load {pf.name}: {e}")

    # Week 1 ago (most recent previous)
    if len(prev_weeks) >= 1:
        prev = prev_weeks[0]
        prev_kpis = prev.get("kpis", {})
        summary["deltas"] = {}
        for key in ["total_leads_in_pipeline", "total_active_clients", "meta_cpl_7d", "meta_spend_30d"]:
            current_val = summary["kpis"].get(key, 0)
            prev_val = prev_kpis.get(key, 0)
            if prev_val > 0:
                delta_pct = round(((current_val - prev_val) / prev_val) * 100, 1)
                summary["deltas"][key] = {
                    "previous": prev_val,
                    "current": current_val,
                    "delta_pct": delta_pct,
                    "direction": "↑" if delta_pct > 0 else ("↓" if delta_pct < 0 else "→")
                }
        # Include full previous week snapshot for the report
        summary["week_1_ago"] = {
            "extraction_date": prev.get("extraction_date"),
            "kpis": prev_kpis,
            "meta_ads": prev.get("meta_ads", {}),
            "pipeline": prev.get("pipeline", {}),
        }
        print(f"  📊 Week -1: {prev.get('extraction_date', '?')}")

    # Week 2 ago
    if len(prev_weeks) >= 2:
        prev2 = prev_weeks[1]
        summary["week_2_ago"] = {
            "extraction_date": prev2.get("extraction_date"),
            "kpis": prev2.get("kpis", {}),
            "meta_ads": prev2.get("meta_ads", {}),
            "pipeline": prev2.get("pipeline", {}),
        }
        # Calculate 2-week delta
        prev2_kpis = prev2.get("kpis", {})
        summary["deltas_2w"] = {}
        for key in ["total_leads_in_pipeline", "total_active_clients", "meta_cpl_7d", "meta_spend_30d"]:
            current_val = summary["kpis"].get(key, 0)
            prev2_val = prev2_kpis.get(key, 0)
            if prev2_val > 0:
                delta_pct = round(((current_val - prev2_val) / prev2_val) * 100, 1)
                summary["deltas_2w"][key] = {
                    "two_weeks_ago": prev2_val,
                    "current": current_val,
                    "delta_pct": delta_pct,
                    "direction": "↑" if delta_pct > 0 else ("↓" if delta_pct < 0 else "→")
                }
        print(f"  📊 Week -2: {prev2.get('extraction_date', '?')}")

    # Save
    docs_folder.mkdir(exist_ok=True)
    filepath = docs_folder / f"metricas_semanales_{date_str}.json"
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    print(f"  💾 Saved: 06_docs/metricas_semanales_{date_str}.json")
    return summary


# ─────────────────────────────────────────────────────────────
# MAIN ORCHESTRATOR
# ─────────────────────────────────────────────────────────────

def extract_client(config, client_key, dry_run=False, days=7):
    """Run full extraction for a single client."""
    client_config = config["clients"][client_key]
    client_name = client_config["name"]
    folder_name = client_config["folder"]
    base_path = Path(config["base_clients_path"])
    client_folder = base_path / folder_name

    date_str = datetime.now().strftime("%Y-%m-%d")

    # For dry-run, use a temp folder so we never touch production files
    if dry_run:
        output_folder = Path("/tmp/extract_client_dry_run") / folder_name
        output_folder.mkdir(parents=True, exist_ok=True)
        (output_folder / "03_ads").mkdir(exist_ok=True)
        (output_folder / "06_docs").mkdir(exist_ok=True)
    else:
        output_folder = client_folder

    print(f"\n{'='*60}")
    print(f"  🚀 Extracting data for: {client_name}")
    print(f"  📅 Date: {date_str}")
    print(f"  📂 Folder: {client_folder}")
    if dry_run:
        print(f"  🔸 MODE: DRY RUN (mock data → /tmp/)")
    print(f"{'='*60}\n")

    if not client_folder.exists():
        print(f"  ❌ Client folder not found: {client_folder}")
        return None

    # Backup existing CSVs before overwrite (only in real mode)
    pipeline_ids = client_config.get("pipeline_ids", {})
    if not dry_run:
        import shutil
        archive_folder = client_folder / "_archivados"
        archive_folder.mkdir(exist_ok=True)
        # Backup legacy files + any dynamic pipeline CSVs
        legacy_names = {"leads": "leads.csv", "clientes": "Clientes.csv"}
        csv_names = set(legacy_names.values()) | {f"{k}.csv" for k in pipeline_ids}
        for csv_file in csv_names:
            src = client_folder / csv_file
            if src.exists():
                backup_name = f"{csv_file.replace('.csv', '')}_{date_str}.csv"
                shutil.copy2(src, archive_folder / backup_name)
                print(f"  📦 Backed up: {csv_file} → _archivados/{backup_name}")

    # 1. Extract Meta Ads
    print("  ── META ADS ──")
    meta_data = extract_meta_ads(config, client_config, days=days, dry_run=dry_run)
    if meta_data:
        save_meta_csv(meta_data, output_folder, date_str)
    print()

    # 2. Extract ALL GHL Pipelines (dynamic — iterates all pipeline_ids from config)
    all_pipelines_data = {}
    for pipe_key, pipe_id in pipeline_ids.items():
        pipe_label = pipe_key.upper().replace("_", " ")
        print(f"  ── GHL PIPELINE: {pipe_label} ──")
        pipe_data = extract_ghl_opportunities(client_config, pipe_key, dry_run=dry_run)
        if pipe_data is not None:
            save_ghl_csv(pipe_data, pipe_key, output_folder)
            all_pipelines_data[pipe_key] = pipe_data
        print()

    # 3. Generate KPI Summary (pass all pipelines as dict)
    print("  ── KPI SUMMARY ──")
    summary = generate_kpi_summary(
        meta_data, all_pipelines_data, None,
        client_name, date_str, output_folder
    )
    print()

    # 4. Print summary to terminal
    kpis = summary.get("kpis", {})
    pipelines_summary = summary.get("pipeline", {})
    print(f"  ╔══════════════════════════════════════════╗")
    print(f"  ║  📊 RESUMEN — {client_name:<26} ║")
    print(f"  ╠══════════════════════════════════════════╣")
    for pk, pv in pipelines_summary.items():
        label = pk.upper().replace("_", " ")
        count = pv.get('total', 0)
        value = pv.get('total_pipeline_value', 0)
        if value > 0:
            print(f"  ║  {label:<20} {count:>5} (${value:>10,.0f})  ║")
        else:
            print(f"  ║  {label:<20} {count:>5} opps            ║")
    print(f"  ╠══════════════════════════════════════════╣")
    print(f"  ║  Total opps:         {kpis.get('total_opportunities', 'N/A'):>17}  ║")
    print(f"  ║  Pipeline value:      ${kpis.get('total_pipeline_value', 0):>16,.0f}  ║")
    print(f"  ║  CPL (7d):           ${kpis.get('meta_cpl_7d', 'N/A'):>16}  ║")
    print(f"  ║  Spend (30d):        ${kpis.get('meta_spend_30d', 'N/A'):>16}  ║")
    print(f"  ╚══════════════════════════════════════════╝")

    deltas = summary.get("deltas", {})
    if deltas:
        print(f"\n  📈 Deltas vs semana anterior:")
        for key, d in deltas.items():
            label = key.replace("_", " ").replace("total ", "").replace("meta ", "")
            print(f"     {d['direction']} {label}: {d['previous']} → {d['current']} ({d['delta_pct']:+.1f}%)")

    print(f"\n  ✅ Extraction complete for {client_name}", file=sys.stderr)
    print(f"  → Now run: /create-growth-strategy for {client_name}", file=sys.stderr)
    return summary


def main():
    parser = argparse.ArgumentParser(
        description="Sales Velocity — Weekly Client Data Extraction",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 extract_client_data.py --client walter_pagano
  python3 extract_client_data.py --client walter_pagano --dry-run
  python3 extract_client_data.py --all
  python3 extract_client_data.py --all --days 14
        """
    )
    parser.add_argument("--client", type=str, help="Client key from config (e.g. walter_pagano)")
    parser.add_argument("--all", action="store_true", help="Extract data for all enabled clients")
    parser.add_argument("--dry-run", action="store_true", help="Use mock data instead of API calls")
    parser.add_argument("--days", type=int, default=7, help="Number of days for Meta Ads lookback (default: 7)")
    parser.add_argument("--json-output", action="store_true", help="Output results as JSON to stdout (for N8N integration)")
    args = parser.parse_args()

    if not args.client and not args.all:
        parser.print_help()
        sys.exit(1)

    config = load_config()

    # When --json-output, redirect progress to stderr so stdout is clean JSON
    real_stdout = sys.stdout
    if args.json_output:
        sys.stdout = sys.stderr

    print("╔══════════════════════════════════════════════════╗")
    print("║  ⚡ SALES VELOCITY — Data Extraction Engine     ║")
    print(f"║  📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S'):<44} ║")
    print("╚══════════════════════════════════════════════════╝")

    clients_to_extract = []
    if args.all:
        clients_to_extract = [
            key for key, cfg in config["clients"].items()
            if cfg.get("enabled", False)
        ]
        if not clients_to_extract:
            print("\n  ⚠️  No enabled clients found in config.")
            sys.exit(1)
        print(f"\n  🎯 Extracting for {len(clients_to_extract)} client(s): {', '.join(clients_to_extract)}")
    else:
        if args.client not in config.get("clients", {}):
            print(f"\n  ❌ Client '{args.client}' not found in config.")
            print(f"  Available clients: {', '.join(config.get('clients', {}).keys())}")
            sys.exit(1)
        clients_to_extract = [args.client]

    results = {}
    summaries = {}
    for client_key in clients_to_extract:
        summary = extract_client(config, client_key, dry_run=args.dry_run, days=args.days)
        results[client_key] = "✅" if summary else "❌"
        if summary:
            summaries[client_key] = summary

    if len(results) > 1:
        print(f"\n{'='*60}")
        print("  📋 RESULTS SUMMARY:")
        for key, status in results.items():
            name = config["clients"][key]["name"]
            print(f"     {status} {name}")
        print(f"{'='*60}")

    # Output JSON to stdout for N8N integration
    if args.json_output and summaries:
        sys.stdout = real_stdout  # Restore real stdout for JSON
        output = {
            "extraction_date": datetime.now().strftime("%Y-%m-%d"),
            "clients": summaries
        }
        print(json.dumps(output, indent=2, ensure_ascii=False, default=str))


if __name__ == "__main__":
    main()
