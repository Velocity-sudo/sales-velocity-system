---
description: Sales Velocity System — Daily Slack task alerts. Sends morning summary of pending tasks to the team via Slack.
---

# /daily-alerts — Daily Task Alerts (Slack + Email)

Sends a Slack summary + individual emails every morning at 8:00 AM with pending tasks grouped by team member.

## What It Does

1. Queries Notion Tasks DB for all non-Done tasks
2. Classifies: 🔴 Overdue, 🟡 Today, 📋 This Week, ⚪ No Date
3. Groups by Assigned To person (filtered to team_members in config)
4. Highlights clients needing special attention (configurable in client_alerts)
5. **Slack**: Sends Block Kit message to #operaciones with full team summary
6. **Email**: Sends personalized HTML email to each team member with THEIR tasks only

## Prerequisites

- **Slack Webhook URL** in `~/Desktop/Clientes/LuchoBranding/config/clients_config.json` → `slack_webhook_url`
- **SMTP Config** in config → `smtp_config` (host, port, username, app_password)
- **Team Emails** in config → `team_emails` (name → email mapping)
- **NOTION_API_KEY** environment variable set
- **LaunchAgent** loaded: `com.salesvelocity.daily-alerts`

## Manual Execution

// turbo-all

### Dry Run (preview without sending)
```bash
cd ~/Desktop/Clientes/LuchoBranding
python3 scripts/daily_task_alerts.py --dry-run
```

### Send Both Slack + Email
```bash
cd ~/Desktop/Clientes/LuchoBranding
python3 scripts/daily_task_alerts.py
```

### Slack Only (no emails)
```bash
python3 scripts/daily_task_alerts.py --no-email
```

### Email Only (no Slack)
```bash
python3 scripts/daily_task_alerts.py --no-slack
```

### Filter by Person
```bash
python3 scripts/daily_task_alerts.py --dry-run --person "Valeria"
```

## Configuration

### team_members (in clients_config.json)
List of names to filter. Only tasks assigned to these people are included.
```json
"team_members": ["LuchoBranding", "Esteban Celis", "Valeria Bolivar", "Johanna Cueva", "Carolina"]
```

### client_alerts (in clients_config.json)
Clients needing special attention — shown as a highlight at the top of the Slack message.
```json
"client_alerts": {
  "Luis Corona": "Onboarding brand manual this week"
}
```

### team_emails (in clients_config.json)
Maps team member names (as they appear in Notion) to their email addresses.

### smtp_config (in clients_config.json)
```json
"smtp_config": {
  "host": "smtp.gmail.com",
  "port": 587,
  "username": "marca@luchobranding.com",
  "app_password": "[APP_PASSWORD]"
}
```

## Setup (First Time)

### 1. Create Slack Webhook
1. Go to https://api.slack.com/apps
2. Create New App → From scratch → Name: "Sales Velocity Alerts" → Select workspace
3. Incoming Webhooks → Toggle ON → Add New Webhook to Workspace → Select channel
4. Copy the webhook URL

### 2. Add to Config
```bash
nano ~/Desktop/Clientes/LuchoBranding/config/clients_config.json
```

### 3. Load LaunchAgent
```bash
launchctl load ~/Library/LaunchAgents/com.salesvelocity.daily-alerts.plist
```

### 4. Test
```bash
python3 ~/Desktop/Clientes/LuchoBranding/scripts/daily_task_alerts.py --dry-run
```

## Automation

- **LaunchAgent:** `~/Library/LaunchAgents/com.salesvelocity.daily-alerts.plist`
- **Schedule:** Daily at 8:00 AM
- **If Mac is asleep/off:** Runs automatically on wake (once per day)

## Logs

- Stdout: `~/Desktop/Clientes/LuchoBranding/logs/daily_alerts.log`
- Stderr: `~/Desktop/Clientes/LuchoBranding/logs/daily_alerts_error.log`

## Troubleshooting

- **"NOTION_API_KEY not set"** → Check LaunchAgent has the key in EnvironmentVariables
- **"Slack webhook URL not configured"** → Add the URL to `clients_config.json`
- **"Slack error: 404"** → Webhook URL is wrong or channel was deleted
- **"SMTP not configured"** → Add `smtp_config` to `clients_config.json`
- **Emails not arriving** → Check Gmail App Password is valid, check spam folder
- **No message received** → Check `launchctl list | grep salesvelocity` to verify agent is loaded
