#!/usr/bin/env python3
"""
Sales Velocity — Daily Slack Task Alerts
Queries Notion Tasks DB and sends formatted summaries to Slack each morning.

Usage:
    python3 daily_task_alerts.py
    python3 daily_task_alerts.py --dry-run
    python3 daily_task_alerts.py --person "Valeria"
"""

import argparse
import json
import os
import smtplib
import sys
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

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
LOG_DIR = SCRIPT_DIR.parent / "logs"

NOTION_API_VERSION = "2022-06-28"
NOTION_BASE_URL = "https://api.notion.com/v1"

# Tasks DB ID (hardcoded as backup — also in config)
TASKS_DB_ID = "2f7e0f37-6c6d-811e-8086-ff5ac19e8f3c"

# Procesos de Clientes DB for resolving project names
PROCESOS_DB_ID = "2f7e0f37-6c6d-81e4-981c-dd4d8c2f47ca"


def load_config():
    """Load configuration from JSON file."""
    if not CONFIG_PATH.exists():
        print(f"❌ Config file not found at: {CONFIG_PATH}")
        sys.exit(1)
    with open(CONFIG_PATH) as f:
        return json.load(f)


def get_notion_headers():
    """Get Notion API headers using NOTION_API_KEY env var."""
    token = os.environ.get("NOTION_API_KEY", "")
    if not token:
        print("❌ NOTION_API_KEY environment variable not set.")
        sys.exit(1)
    return {
        "Authorization": f"Bearer {token}",
        "Notion-Version": NOTION_API_VERSION,
        "Content-Type": "application/json",
    }


# ─────────────────────────────────────────────────────────────
# NOTION QUERIES
# ─────────────────────────────────────────────────────────────

def fetch_all_pending_tasks(headers):
    """Fetch all non-Done tasks from the Tasks DB."""
    url = f"{NOTION_BASE_URL}/databases/{TASKS_DB_ID}/query"
    payload = {
        "filter": {
            "property": "Status",
            "status": {"does_not_equal": "Done"}
        },
        "page_size": 100
    }

    all_tasks = []
    has_more = True
    start_cursor = None

    while has_more:
        if start_cursor:
            payload["start_cursor"] = start_cursor

        resp = requests.post(url, headers=headers, json=payload, timeout=30)
        resp.raise_for_status()
        data = resp.json()

        all_tasks.extend(data.get("results", []))
        has_more = data.get("has_more", False)
        start_cursor = data.get("next_cursor")

    return all_tasks


def resolve_project_names(headers, project_ids):
    """Resolve Notion page IDs to project names."""
    names = {}
    for pid in project_ids:
        if pid in names:
            continue
        try:
            resp = requests.get(
                f"{NOTION_BASE_URL}/pages/{pid}",
                headers=headers, timeout=10
            )
            resp.raise_for_status()
            page = resp.json()
            title_prop = page.get("properties", {}).get("Project Name", {})
            title_arr = title_prop.get("title", [])
            names[pid] = title_arr[0]["plain_text"] if title_arr else "Sin proyecto"
        except Exception:
            names[pid] = "Sin proyecto"
    return names


# ─────────────────────────────────────────────────────────────
# TASK CLASSIFICATION
# ─────────────────────────────────────────────────────────────

def parse_tasks(raw_tasks, headers):
    """Parse raw Notion tasks into structured dicts with classification."""
    today = datetime.now().date()
    week_end = today + timedelta(days=7)

    # Collect all project IDs for batch resolution
    project_ids = set()
    for task in raw_tasks:
        props = task.get("properties", {})
        relations = props.get("Project", {}).get("relation", [])
        for rel in relations:
            project_ids.add(rel["id"])

    # Resolve project names
    project_names = resolve_project_names(headers, project_ids) if project_ids else {}

    parsed = []
    for task in raw_tasks:
        props = task.get("properties", {})

        # Title
        title_arr = props.get("Task Name", {}).get("title", [])
        title = title_arr[0]["plain_text"].strip() if title_arr else "Sin título"

        # Status
        status_obj = props.get("Status", {}).get("status", {})
        status = status_obj.get("name", "Unknown") if status_obj else "Unknown"

        # Priority
        priority_obj = props.get("Priority Level", {}).get("select", {})
        priority = priority_obj.get("name", "") if priority_obj else ""

        # Due date
        date_obj = props.get("Due Date", {}).get("date", {})
        due_date = None
        due_str = ""
        if date_obj and date_obj.get("start"):
            due_str = date_obj["start"]
            try:
                due_date = datetime.strptime(due_str[:10], "%Y-%m-%d").date()
            except ValueError:
                pass

        # Assigned to
        people = props.get("Assigned To", {}).get("people", [])
        assigned = [p.get("name", "Sin nombre") for p in people] if people else ["Sin asignar"]

        # Project
        relations = props.get("Project", {}).get("relation", [])
        projects = [project_names.get(r["id"], "Sin proyecto") for r in relations] if relations else []

        # Icon
        icon_obj = task.get("icon", {})
        icon = ""
        if icon_obj:
            if icon_obj.get("type") == "emoji":
                icon = icon_obj.get("emoji", "")

        # Classification
        if due_date and due_date < today:
            category = "overdue"
        elif due_date and due_date == today:
            category = "today"
        elif due_date and due_date <= week_end:
            category = "this_week"
        elif due_date is None:
            category = "no_date"
        else:
            category = "later"

        # Notion URL
        page_id = task["id"].replace("-", "")
        notion_url = f"https://www.notion.so/{page_id}"

        parsed.append({
            "title": title,
            "status": status,
            "priority": priority,
            "due_date": due_date,
            "due_str": due_str,
            "assigned": assigned,
            "projects": projects,
            "icon": icon,
            "category": category,
            "notion_url": notion_url,
        })

    return parsed


def group_by_person(tasks, team_members=None):
    """Group tasks by assigned person, optionally filtering to team only."""
    groups = {}
    # Normalize team_members for case-insensitive matching
    team_lower = [m.lower() for m in team_members] if team_members else None

    for task in tasks:
        for person in task["assigned"]:
            # Filter to team members only
            if team_lower and person.lower() not in team_lower:
                continue
            if person not in groups:
                groups[person] = []
            groups[person].append(task)
    return groups


# ─────────────────────────────────────────────────────────────
# SLACK MESSAGE BUILDER
# ─────────────────────────────────────────────────────────────

CATEGORY_EMOJI = {
    "overdue": "🔴",
    "today": "🟡",
    "this_week": "📋",
    "no_date": "⚪",
    "later": "📌",
}

CATEGORY_LABEL = {
    "overdue": "VENCIDAS",
    "today": "HOY",
    "this_week": "ESTA SEMANA",
    "no_date": "SIN FECHA",
    "later": "PENDIENTES",
}

PRIORITY_EMOJI = {"ALTA": "🔴", "MEDIA": "🟡", "BAJA": "🟢"}


def build_slack_message(groups, today_str, config=None):
    """Build a clean, readable Slack Block Kit message."""
    # Count totals for the intro
    total_all = sum(len(tasks) for tasks in groups.values())
    total_overdue = sum(
        1 for tasks in groups.values()
        for t in tasks if t["category"] == "overdue"
    )
    total_today = sum(
        1 for tasks in groups.values()
        for t in tasks if t["category"] == "today"
    )

    # Friendly intro
    intro = f"Buenos días equipo ☀️\n\nAquí está el resumen de tareas pendientes de hoy."
    if total_overdue > 0:
        intro += f" Tenemos *{total_overdue} vencida{'s' if total_overdue != 1 else ''}* que necesitan atención."
    if total_today > 0:
        intro += f" Hay *{total_today}* que deben quedar listas hoy."
    intro += "\nAsegúrense de revisar las que sí o sí tienen que quedar listas hoy. ¡Aprovechemos el día! 💪"

    blocks = [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": f"📋 Tareas — {today_str}",
                "emoji": True
            }
        },
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": intro}
        },
    ]

    # Client alerts (special attention notes from config)
    client_alerts = (config or {}).get("client_alerts", {})
    if client_alerts:
        alert_lines = ["🚨 *Atención especial:*"]
        for client, note in client_alerts.items():
            alert_lines.append(f"  • *{client}* — {note}")
        blocks.append({
            "type": "section",
            "text": {"type": "mrkdwn", "text": "\n".join(alert_lines)}
        })

    blocks.append({"type": "divider"})

    # Sort: prioritize people with overdue tasks
    def person_sort_key(person_name):
        person_tasks = groups[person_name]
        has_overdue = any(t["category"] == "overdue" for t in person_tasks)
        return (0 if has_overdue else 1, person_name)

    for person in sorted(groups.keys(), key=person_sort_key):
        person_tasks = groups[person]

        # Count by category
        counts = {}
        for t in person_tasks:
            cat = t["category"]
            counts[cat] = counts.get(cat, 0) + 1

        # Show all categories including later
        relevant_cats = ["overdue", "today", "this_week", "no_date", "later"]
        relevant = sum(counts.get(c, 0) for c in relevant_cats)
        if relevant == 0:
            continue

        # Build compact task list for this person
        overdue_count = counts.get("overdue", 0)
        alert = " ⚠️" if overdue_count > 0 else ""
        lines = [f"*{person}*{alert}"]

        for cat in relevant_cats:
            cat_tasks = [t for t in person_tasks if t["category"] == cat]
            if not cat_tasks:
                continue

            emoji = CATEGORY_EMOJI[cat]
            label = CATEGORY_LABEL[cat]
            lines.append(f"{emoji} _{label}_")

            for t in cat_tasks:
                project_tag = f" · {', '.join(t['projects'])}" if t["projects"] else ""
                due_tag = ""
                if cat == "overdue" and t["due_date"]:
                    days_late = (datetime.now().date() - t["due_date"]).days
                    due_tag = f" · `{days_late}d tarde`"
                elif cat in ("this_week", "later") and t["due_str"]:
                    due_tag = f" · {t['due_str'][5:10]}"

                lines.append(f"  → <{t['notion_url']}|{t['title']}>{project_tag}{due_tag}")

        blocks.append({
            "type": "section",
            "text": {"type": "mrkdwn", "text": "\n".join(lines)}
        })

    # Footer
    blocks.append({"type": "divider"})
    blocks.append({
        "type": "context",
        "elements": [{
            "type": "mrkdwn",
            "text": f"📊 {total_all} tareas pendientes · <https://www.notion.so/2f7e0f376c6d811e8086ff5ac19e8f3c|Ver todas en Notion>"
        }]
    })

    return {"blocks": blocks}


def build_dry_run_output(groups, today_str):
    """Build a plain-text version for --dry-run."""
    lines = [f"\n📋 TAREAS DEL EQUIPO — {today_str}\n{'='*50}\n"]

    for person, tasks in sorted(groups.items()):
        relevant = [t for t in tasks if t["category"] in ("overdue", "today", "this_week", "no_date")]
        if not relevant:
            continue

        lines.append(f"\n👤 {person} ({len(relevant)} pendientes)")
        lines.append("-" * 40)

        for cat in ["overdue", "today", "this_week", "no_date"]:
            cat_tasks = [t for t in tasks if t["category"] == cat]
            if not cat_tasks:
                continue
            emoji = CATEGORY_EMOJI[cat]
            label = CATEGORY_LABEL[cat]
            lines.append(f"\n  {emoji} {label}:")
            for t in cat_tasks:
                icon = t["icon"] or "•"
                priority = f" [{t['priority']}]" if t["priority"] else ""
                project = f" ({', '.join(t['projects'])})" if t["projects"] else ""
                due = ""
                if t["due_str"]:
                    due = f" — {t['due_str'][:10]}"
                lines.append(f"    {icon} {t['title']}{project}{due}{priority}")

    return "\n".join(lines)


# ─────────────────────────────────────────────────────────────
# SEND TO SLACK
# ─────────────────────────────────────────────────────────────

def send_to_slack(webhook_url, message):
    """Send message payload to Slack webhook."""
    resp = requests.post(webhook_url, json=message, timeout=15)
    if resp.status_code == 200 and resp.text == "ok":
        print("  ✅ Slack message sent successfully!")
        return True
    else:
        print(f"  ❌ Slack error: {resp.status_code} — {resp.text}")
        return False


# ─────────────────────────────────────────────────────────────
# EMAIL
# ─────────────────────────────────────────────────────────────

def build_email_html(person, tasks, today_str):
    """Build a clean personal HTML email for a team member."""
    # Classify
    overdue = [t for t in tasks if t["category"] == "overdue"]
    today_tasks = [t for t in tasks if t["category"] == "today"]
    this_week = [t for t in tasks if t["category"] == "this_week"]
    no_date = [t for t in tasks if t["category"] == "no_date"]
    later = [t for t in tasks if t["category"] == "later"]

    relevant = overdue + today_tasks + this_week + no_date + later
    if not relevant:
        return None

    first_name = person.split()[0] if person != "LuchoBranding" else "Lucho"

    def task_row(t, badge_color=None, badge_text=None):
        """Build one task row."""
        proj_names = ", ".join(t["projects"])
        project = f'<span style="color:#888"> · {proj_names}</span>' if t["projects"] else ""
        badge = ""
        if badge_color and badge_text:
            badge = f' <span style="background:{badge_color};color:#fff;padding:2px 8px;border-radius:10px;font-size:11px;font-weight:600">{badge_text}</span>'
        url = t["notion_url"]
        title = t["title"]
        return f'<tr><td style="padding:8px 12px;border-bottom:1px solid #f0f0f0"><a href="{url}" style="color:#1a73e8;text-decoration:none">{title}</a>{project}{badge}</td></tr>'

    sections_html = ""

    if overdue:
        rows = ""
        for t in overdue:
            days = (datetime.now().date() - t["due_date"]).days
            rows += task_row(t, "#e74c3c", f"{days}d tarde")
        sections_html += f'''
        <div style="margin-bottom:20px">
            <div style="font-size:13px;font-weight:700;color:#e74c3c;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:6px">🔴 Vencidas</div>
            <table width="100%" cellpadding="0" cellspacing="0" style="background:#fff;border-radius:8px;border:1px solid #fde2e2">{rows}</table>
        </div>'''

    if today_tasks:
        rows = "".join(task_row(t, "#f39c12", "Hoy") for t in today_tasks)
        sections_html += f'''
        <div style="margin-bottom:20px">
            <div style="font-size:13px;font-weight:700;color:#f39c12;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:6px">🟡 Para hoy</div>
            <table width="100%" cellpadding="0" cellspacing="0" style="background:#fff;border-radius:8px;border:1px solid #fef3cd">{rows}</table>
        </div>'''

    if this_week:
        rows = ""
        for t in this_week:
            date_label = t["due_str"][5:10] if t["due_str"] else ""
            rows += task_row(t, "#6c757d", date_label)
        sections_html += f'''
        <div style="margin-bottom:20px">
            <div style="font-size:13px;font-weight:700;color:#6c757d;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:6px">📋 Esta semana</div>
            <table width="100%" cellpadding="0" cellspacing="0" style="background:#fff;border-radius:8px;border:1px solid #e9ecef">{rows}</table>
        </div>'''

    if no_date:
        rows = "".join(task_row(t) for t in no_date)
        sections_html += f'''
        <div style="margin-bottom:20px">
            <div style="font-size:13px;font-weight:700;color:#adb5bd;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:6px">⚪ Sin fecha</div>
            <table width="100%" cellpadding="0" cellspacing="0" style="background:#fff;border-radius:8px;border:1px solid #e9ecef">{rows}</table>
        </div>'''

    if later:
        rows = ""
        for t in later:
            date_label = t["due_str"][5:10] if t["due_str"] else ""
            rows += task_row(t, "#6c757d", date_label)
        sections_html += f'''
        <div style="margin-bottom:20px">
            <div style="font-size:13px;font-weight:700;color:#6c757d;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:6px">📌 Pendientes</div>
            <table width="100%" cellpadding="0" cellspacing="0" style="background:#fff;border-radius:8px;border:1px solid #e9ecef">{rows}</table>
        </div>'''

    # Urgency line
    urgency = ""
    if overdue:
        urgency = f'<p style="color:#e74c3c;font-weight:600">Tienes {len(overdue)} tarea{"s" if len(overdue) != 1 else ""} vencida{"s" if len(overdue) != 1 else ""}. Por favor dale prioridad.</p>'
    elif today_tasks:
        urgency = f'<p style="color:#f39c12;font-weight:600">Tienes {len(today_tasks)} tarea{"s" if len(today_tasks) != 1 else ""} para hoy.</p>'

    html = f'''<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"></head>
<body style="margin:0;padding:0;background:#f7f8fa;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif">
<div style="max-width:560px;margin:0 auto;padding:30px 20px">
    <div style="text-align:center;margin-bottom:24px">
        <div style="font-size:24px;font-weight:700;color:#1a1a2e">📋 Tus tareas de hoy</div>
        <div style="font-size:13px;color:#888;margin-top:4px">{today_str}</div>
    </div>

    <div style="background:#fff;border-radius:12px;padding:24px;box-shadow:0 1px 3px rgba(0,0,0,0.08)">
        <p style="color:#333;margin-top:0">Hola {first_name} 👋</p>
        <p style="color:#555">Aquí está tu resumen de tareas pendientes. Revisa las que deben quedar listas hoy y aprovechemos el día.</p>
        {urgency}
    </div>

    <div style="margin-top:20px">
        {sections_html}
    </div>

    <div style="text-align:center;margin-top:24px">
        <a href="https://www.notion.so/2f7e0f376c6d811e8086ff5ac19e8f3c" style="display:inline-block;background:#1a73e8;color:#fff;padding:10px 28px;border-radius:8px;text-decoration:none;font-weight:600;font-size:14px">Ver todas en Notion →</a>
    </div>

    <div style="text-align:center;margin-top:20px;font-size:11px;color:#aaa">
        Sales Velocity · LuchoBranding
    </div>
</div>
</body>
</html>'''

    return html


def send_emails(groups, today_str, config):
    """Send individual HTML emails to each team member via Gmail SMTP."""
    smtp_config = config.get("smtp_config", {})
    team_emails = config.get("team_emails", {})

    if not smtp_config or not smtp_config.get("username"):
        print("  ⚠️  SMTP not configured — skipping emails")
        return False

    if not team_emails:
        print("  ⚠️  No team_emails in config — skipping emails")
        return False

    # Connect to SMTP
    try:
        server = smtplib.SMTP(smtp_config.get("host", "smtp.gmail.com"), smtp_config.get("port", 587))
        server.starttls()
        server.login(smtp_config["username"], smtp_config["app_password"])
    except Exception as e:
        print(f"  ❌ SMTP connection failed: {e}")
        return False

    sent_count = 0
    for person, tasks in groups.items():
        # Find email for this person (case-insensitive match)
        email_addr = None
        for name, addr in team_emails.items():
            if name.lower() == person.lower() and addr:
                email_addr = addr
                break

        if not email_addr:
            print(f"  ⏭️  No email for {person} — skipped")
            continue

        html = build_email_html(person, tasks, today_str)
        if not html:
            continue

        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"📋 Tus tareas de hoy — {datetime.now().strftime('%d/%m')}"
        msg["From"] = f"Sales Velocity <{smtp_config['username']}>"
        msg["To"] = email_addr
        msg.attach(MIMEText(html, "html"))

        try:
            server.sendmail(smtp_config["username"], email_addr, msg.as_string())
            sent_count += 1
            print(f"  📧 {person} → {email_addr} ✓")
        except Exception as e:
            print(f"  ❌ Failed to send to {person}: {e}")

    server.quit()
    print(f"  ✅ {sent_count} email{'s' if sent_count != 1 else ''} sent")
    return True


# ─────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Sales Velocity — Daily Slack Task Alerts"
    )
    parser.add_argument("--dry-run", action="store_true",
                        help="Print to stdout without sending to Slack or email")
    parser.add_argument("--person", type=str,
                        help="Only show tasks for a specific person")
    parser.add_argument("--no-email", action="store_true",
                        help="Skip sending individual emails")
    parser.add_argument("--no-slack", action="store_true",
                        help="Skip sending Slack summary")
    args = parser.parse_args()

    config = load_config()
    webhook_url = config.get("slack_webhook_url", "")
    headers = get_notion_headers()
    today_str = datetime.now().strftime("%A %d de %B, %Y")

    print(f"\n⚡ Sales Velocity — Daily Task Alerts")
    print(f"📅 {today_str}")
    print(f"{'='*50}\n")

    # 1. Fetch tasks
    print("  📡 Querying Notion Tasks DB...")
    raw_tasks = fetch_all_pending_tasks(headers)
    print(f"  ✅ Found {len(raw_tasks)} pending tasks")

    if not raw_tasks:
        print("  🎉 No pending tasks! Nothing to send.")
        return

    # 2. Parse and classify
    print("  🔄 Classifying tasks...")
    parsed = parse_tasks(raw_tasks, headers)

    # 3. Group by person (filtered to team members from config)
    team_members = config.get("team_members", None)
    groups = group_by_person(parsed, team_members=team_members)

    # Filter by specific person if requested via CLI
    if args.person:
        filtered = {k: v for k, v in groups.items() if args.person.lower() in k.lower()}
        if not filtered:
            print(f"  ⚠️  No tasks found for '{args.person}'")
            return
        groups = filtered

    # 4. Output
    if args.dry_run:
        output = build_dry_run_output(groups, today_str)
        print(output)
        print(f"\n  🔸 DRY RUN — no messages sent")
    else:
        # Slack
        if not args.no_slack:
            if webhook_url and not webhook_url.startswith("https://hooks.slack.com/services/XXXX"):
                message = build_slack_message(groups, today_str, config=config)
                print("  📤 Sending to Slack...")
                send_to_slack(webhook_url, message)
            else:
                print("  ⚠️  Slack webhook not configured — skipped")

        # Email
        if not args.no_email:
            print("  📧 Sending individual emails...")
            send_emails(groups, today_str, config)

    print(f"\n  ✅ Done — {len(parsed)} tasks processed for {len(groups)} people")


if __name__ == "__main__":
    main()
