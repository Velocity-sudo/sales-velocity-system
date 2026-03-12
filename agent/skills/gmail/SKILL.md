---
name: gmail
description: Send emails instantly via Gmail SMTP. Use this instead of browser automation for all email tasks.
metadata:
  {
    "openclaw":
      { "emoji": "📧", "requires": { "env": ["GMAIL_USER", "GMAIL_APP_PASSWORD"] }, "primaryEnv": "GMAIL_USER" },
  }
---

# Gmail Email Skill

Send emails **instantly** via SMTP (~1 second) instead of browser automation (~5 minutes).

## Setup
Credentials in `~/.openclaw/.env`:
- `GMAIL_USER` — Gmail address (e.g. niko@luchobranding.com)
- `GMAIL_APP_PASSWORD` — App Password from Google (no spaces)

## How to Send Email

Run the script at `~/.openclaw/scripts/send-email.py`:

```bash
# Simple email
python3 ~/.openclaw/scripts/send-email.py \
  --to "recipient@email.com" \
  --subject "Subject line" \
  --body "Email body text"

# With CC
python3 ~/.openclaw/scripts/send-email.py \
  --to "main@email.com" \
  --cc "copy@email.com" \
  --subject "Subject" \
  --body "Body"

# With HTML formatting
python3 ~/.openclaw/scripts/send-email.py \
  --to "recipient@email.com" \
  --subject "Subject" \
  --html "<h1>Hello</h1><p>This is HTML email</p>"

# Multiple recipients
python3 ~/.openclaw/scripts/send-email.py \
  --to "one@email.com,two@email.com" \
  --subject "Subject" \
  --body "Body"

# Custom sender name
python3 ~/.openclaw/scripts/send-email.py \
  --to "recipient@email.com" \
  --subject "Subject" \
  --body "Body" \
  --from-name "Sales Velocity"

# Body from file
python3 ~/.openclaw/scripts/send-email.py \
  --to "recipient@email.com" \
  --subject "Subject" \
  --body-file /path/to/content.txt
```

## All Options

| Flag | Required | Description |
|---|---|---|
| `--to` | ✅ | Recipient(s), comma-separated |
| `--subject` | ✅ | Email subject |
| `--body` | One of body/html | Plain text body |
| `--html` | One of body/html | HTML body |
| `--body-file` | Optional | Read body from file |
| `--cc` | Optional | CC recipients |
| `--bcc` | Optional | BCC recipients |
| `--from-name` | Optional | Sender display name (default: "Niko AI") |
| `--reply-to` | Optional | Reply-to address |

## ⚠️ Important Rules

1. **ALWAYS use this script** for sending emails — NEVER use browser automation for email
2. The email sends from `niko@luchobranding.com` (Google Workspace)
3. Sender name can be customized per email via `--from-name`
4. If the script returns `❌ Authentication failed`, the App Password needs to be regenerated at https://myaccount.google.com/apppasswords
