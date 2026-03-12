---
description: Sales Velocity System workflow to create GHL pipeline communications (internal + external) for each stage. Generates a dynamic HTML document with tabbed navigation ready for copy-paste into GoHighLevel workflows.
---

# /create-ghl-communications — Create GHL Pipeline Communications

## 🎯 Purpose
Create the **exact communication copy** for every stage of a client's GoHighLevel pipeline. This covers:
- **Internal communications** (to the client's team): Slack, Email, SMS alerts with escalating urgency
- **External communications** (to the client's end-customers): SMS, Email, WhatsApp nurturing and follow-ups

This is a **critical deliverable** in the Sales Velocity System — it directly impacts lead response time, follow-up consistency, and conversion rates.

---

## 📥 Required Inputs (MUST have before starting)

### 1. Client Knowledge Base (MANDATORY)
The client **must** already have a `base_de_conocimiento.md` in `~/Desktop/Clientes/[Client Name]/`. This gives:
- Business context, tone, and voice
- Service details and pricing
- Target audience and their pain points
- Compliance requirements (if any)

> ⚠️ **If the knowledge base doesn't exist, DO NOT proceed.** Run `/client-onboarding` first.

### 2. Brand Manual (MANDATORY)
The client **must** have a `BRAND_MANUAL.html` in `~/Desktop/Clientes/[Client Name]/brand-assets/`. This is the **single source of truth** for:
- **Color palette** (primary, secondary, accent colors with exact hex codes)
- **Typography** (font family, weights, import URL)
- **Visual identity** (gradients, backgrounds, card styles, border treatments)
- **Tone & voice** (how the brand communicates)

The generated HTML **must** use the client's brand colors, fonts, and design language — NOT generic styles. Extract the following from the brand manual:
- Primary background color (e.g., `#0A0E1A`)
- Accent color for CTAs/highlights (e.g., `#F27A30`)
- Secondary color for info/links (e.g., `#00AEEF`)
- Font family and Google Fonts import (e.g., `Outfit`)
- Card/surface styling (glassmorphism, borders, backdrop-filter)

> ⚠️ **If the brand manual doesn't exist, DO NOT proceed.** Run `/create-brand-manual` first.

### 3. Pipeline Diagram (MANDATORY)
The user must provide a visual representation of the pipeline. Accepted formats:
- **Miro board** (screenshot or link)
- **Canva design** (screenshot or export)
- **PDF export** from Miro/Canva
- **Photos/screenshots** of a whiteboard or existing GHL pipeline
- **Text description** of stages with communication requirements

The diagram must show:
- Each **stage name** in the pipeline (in order)
- What **communications** happen at each stage (internal and/or external)
- **Timing** of each communication (0H, 24H, 48H, etc.)
- **Channels** used at each stage (Slack, Email, SMS, WhatsApp)

### 4. Configuration Parameters (ASK if not provided)
Before writing any copy, confirm these with the user:

| Parameter | Default | Ask? |
|---|---|---|
| **Language** | Spanish (both internal and external) | Only if client serves non-Spanish market |
| **Internal channels** | Slack + Email + SMS | Confirm which the client actually uses |
| **External channels** | SMS + Email + WhatsApp | Confirm which the client has enabled in GHL |
| **Escalation pattern** | 0H → 2H → 4H → 24H → 48H → 72H → 96H | Confirm; may vary for appointment reminders (-24H, -1H, -10min) or long-cycle stages (7D, 14D, 21D) |
| **Auto-action timeout** | 96H → move to "No Sigue" / "Inacción" | Confirm terminal behavior and timeout per stage |
| **Tag nomenclature** | `[Category] Detail` (e.g., `[Status] Inacción - Sin Llamada 1`) | Ask if client has existing tag conventions in GHL |
| **Internal recipients** | Client's operations person (e.g., "Jefferson") | Get the name(s) of who receives internal alerts |
| **Business name for signatures** | From knowledge base | Confirm exact name used in SMS/Email signatures |
| **GHL merge fields** | Standard set (see below) | Confirm if client uses custom fields |

**Standard GHL Merge Fields:**
```
{{contact.first_name}}    {{contact.last_name}}     {{contact.phone}}
{{contact.email}}         {{contact.source}}        {{contact.date_created}}
{{contact.contact_link}}  {{contact.tags}}          {{opportunity.name}}
{{opportunity.pipeline_stage}}
{{appointment.date}}      {{appointment.time}}      {{appointment.calendar_link}}
{{custom_values.payment_link}}                      {{custom_values.secure_system_link}}
```

---

## 🔄 Execution Steps

### Step 1: Load Context
// turbo
1. Read the client's `base_de_conocimiento.md`
2. Read the client's `brand-assets/BRAND_MANUAL.html` — extract color palette, fonts, and design tokens
3. Check for any existing GHL-related files in the client folder (pipeline diagrams, architecture docs, previous communications)
4. Load the pipeline diagram provided by the user (image, PDF, or description)

### Step 2: Analyze Pipeline
1. **Identify all stages** from the diagram — list them in order with their names
2. **Map communications per stage** — for each stage, identify:
   - Internal notifications (who, when, what channel)
   - External communications (when, what channel, what action to drive)
   - Auto-actions / timeouts (what happens if no action is taken)
3. **Present the stage map to the user** for confirmation before writing copy. **MUST include exact message count and timing per stage:**

```
| # | Stage | Int. Messages (count × timing) | Ext. Messages (count × timing) | Auto-Action |
|---|-------|-------------------------------|-------------------------------|-------------|
| 1 | [Name] | 7 msgs: 0H, 1H, 12H, 24H, 48H, 72H, 96H | 0 (solo interna) | 96H → Inacción |
| 2 | [Name] | 3 msgs: 0H, 24H, 48H | 5 msgs: 0H, 24H, 48H, 72H, 96H | 96H → Inacción |
```

> ⚠️ **Wait for user confirmation** of timing and message counts before proceeding to copy writing.

### Step 3: Write Communication Copy
For EACH stage, write the exact copy for every notification following these rules:

> 🚨 **MANDATORY MULTI-CHANNEL RULE — NO EXCEPTIONS:**
> Every single message at every timing point MUST be written in ALL required channel formats.
> Delivering a message in only one channel is **NOT acceptable** and will be rejected.

#### ⚡ Channel Format Obligation (STRICT)

**INTERNAL — Every notification MUST have BOTH:**
1. **Slack / GHL App** — Direct, urgent, emoji-driven. Include: name, phone, contact link, clear action.
2. **Email (Gmail)** — Subject line (with emojis + merge fields) + structured body with recipient name, all contact data, context, deadline, contact link. Sign off: `— Notificación automática GHL`

**Example Internal (0H):**
```
Slack: 🚨 *NUEVO LEAD — LLAMAR AHORA* 🚨 ¡Laura! Entró un nuevo Lead... 📞 {{contact.phone}} 👉 {{contact.contact_link}}
Email: Asunto: 🚨 NUEVO LEAD — {{contact.first_name}} {{contact.last_name}} — LLAMAR AHORA | Cuerpo: Laura, entró un nuevo lead... — Notificación automática GHL
```

**EXTERNAL — Every notification MUST have ALL THREE:**
1. **WhatsApp** — Conversational, use formatting (*bold*, _italic_). Emojis okay. Clear CTA with link.
2. **SMS** — Under 160 chars. Friendly but direct. Always include business name signature. Include link.
3. **Email** — Subject line + warm body. Clear CTA with link. Professional signature: `— Equipo [Business Name]`

**Example External (0H Confirmación):**
```
WA: 🎉 *¡Gracias por registrarte!* Ya agendamos tu llamada... {{appointment.calendar_link}}
SMS: 🎉 ¡Gracias {{contact.first_name}}! Tu llamada está confirmada. — Equipo [Business]
Email: Asunto: 🎉 ¡Tu llamada está confirmada! | Cuerpo: Hola {{contact.first_name}}... — Equipo [Business]
```

> ⚠️ **EXCEPTIONS (must be explicit):** If a stage has NO external comms (e.g., Registro = solo interna), mark it clearly as `ext: []` and note "Sin comunicaciones externas" in the stage map.

#### Internal Communication Copy Rules:
- **Slack**: Direct, urgent, emoji-driven. Include: name, phone, contact link, clear action.
- **Email**: Subject line (with emoji + merge fields for name) + structured body. Include: recipient name (e.g., "Laura"), all contact data, context, deadline, contact link. Always end with `— Notificación automática GHL`.
- **Auto-actions**: Clearly state the tag applied, the stage moved to, and whether it's terminal. These do NOT need multi-channel — they are system actions, not notifications.

#### External Communication Copy Rules:
- **WhatsApp**: Conversational, use formatting (*bold*, _italic_). Include emojis. Clear CTA.
- **SMS**: Friendly but professional. Under 160 chars. Always include business name signature.
- **Email**: Subject line + warm body. Clear CTA with link. Professional signature.
- **All external**: NEVER sound robotic. Match the client's brand voice from the knowledge base.

#### Urgency Escalation Visual System:
- **✅ OK** (green) — Confirmations, positive updates
- **ℹ️ Info** (blue) — Standard notifications, reminders
- **⚠️ Warning** (amber) — Escalation, approaching deadline
- **🚨 Critical** (red) — Final warnings, risk of losing lead
- **⚡ Auto** (purple) — Automated system actions

#### Merge Fields:
- Always use GHL merge fields for personalization
- Include `{{contact.contact_link}}` in EVERY internal notification so the team can act with one click
- Include relevant custom value links in external communications (payment, docs, calendar)

### Step 4: Generate HTML Output
Create a single HTML file with the following architecture:

```
comunicaciones_pipeline.html
├── Header (client name + pipeline title — branded with client colors)
├── Merge Fields Reference (quick reference for GHL fields used)
├── DUAL NAVIGATION SYSTEM:
│   ├── Primary: Tab bar (sticky, one tab per pipeline stage)
│   └── Secondary: Sub-tabs WITHIN each stage (🔒 Interna / 📣 Externa)
│
│   ├── Tab 0: [Stage Name]
│   │   ├── Stage info (trigger, tags, auto-actions)
│   │   ├── Sub-tab: 🔒 Interna (Equipo)
│   │   │   ├── Notification cards (Slack/Email/SMS with timing + urgency)
│   │   │   └── Auto-action cards
│   │   └── Sub-tab: 📣 Externa (Cliente)
│   │       └── Notification cards (SMS/Email/WhatsApp with timing)
│   ├── Tab 1: [Stage Name]
│   │   └── ...
│   └── Tab N: [Stage Name]
└── Footer
```

**CRITICAL — Dual Navigation UX:**
The user MUST be able to:
1. **Select a pipeline stage** via the sticky top tab bar
2. **Toggle between Internal and External** communications via sub-tabs within each stage
This means TWO levels of navigation, NOT just one. The Internal/External toggle is a sub-tab WITHIN each stage panel, not a separate global filter.

**Technical Implementation:**
- Use **vanilla HTML + CSS + JS** (no frameworks)
- Use a **data-driven JS approach**: define all notifications as a JS data array and render dynamically (keeps file size manageable)
- Use the client's **brand font** from the Brand Manual (e.g., `Outfit`, `Plus Jakarta Sans`)
- Use the client's **brand color palette** for the header, active tabs, badges, and accents
- Color-code by channel: Slack (purple), Email (red), SMS (green), WhatsApp (green)
- Cards show: channel badge, timing badge, urgency badge, message body with highlighted merge fields
- Sub-tabs toggle between Internal/External within each stage
- Tab bar should be **sticky** for easy navigation
- Design must be **premium** and match the client's brand identity

**Reference implementation:** See `/Users/niko/Desktop/Clientes/Jorge Vergara/proceso GHL/comunicaciones_pipeline.html` as the gold standard.

### Step 5: Save Output
// turbo
1. Create folder if it doesn't exist: `~/Desktop/Clientes/[Client Name]/proceso GHL/`
2. Save HTML file as: `~/Desktop/Clientes/[Client Name]/proceso GHL/comunicaciones_pipeline.html`
3. Open the file in the browser for the user to review

### Step 6: Optional — Deploy to Shareable URL
If the user wants to share with the client:
1. Suggest **Tiiny.host** (https://tiiny.host) — user uploads the HTML and gets a shareable link
2. Alternative: **Netlify Drop** (https://app.netlify.com/drop) — drag and drop for instant URL
3. Alternative: **Surge.sh** — `npx -y surge [folder] [domain].surge.sh`

---

## ✅ Quality Checklist (before delivering)

### Channel Format Compliance (CRITICAL — check FIRST)
- [ ] **Every internal notification has BOTH Slack AND Email variants** — no single-channel messages
- [ ] **Every external notification has ALL THREE: WA, SMS, AND Email** — no missing channels
- [ ] **Message count per stage matches the confirmed stage map** from Step 2
- [ ] Stages with no external comms are clearly marked as `ext: []`

### Content Quality
- [ ] Every stage from the pipeline diagram has a tab
- [ ] Every notification has the correct channel badge (Slack = purple, Email = red, SMS = green, WA = green)
- [ ] Every internal notification includes `{{contact.contact_link}}` for one-click access
- [ ] Every internal Email includes subject line with emoji + merge fields
- [ ] Every external notification includes the business name in the signature
- [ ] Every external Email has a subject line and professional sign-off
- [ ] Urgency levels escalate properly within each stage (OK → Info → Warning → Critical)
- [ ] Auto-actions clearly state the tag, destination stage, and whether terminal
- [ ] All merge fields use correct GHL syntax

### Technical
- [ ] Tab navigation works and sub-tabs toggle correctly
- [ ] HTML renders correctly in browser (no JS errors)
- [ ] File saved in the correct client folder
- [ ] Tone matches client's brand voice from knowledge base

---

## 📂 File Convention
```
~/Desktop/Clientes/[Client Name]/
└── proceso GHL/
    ├── comunicaciones_pipeline.html    ← Main deliverable
    ├── Funnel [Client Name].pdf        ← Input diagram (if provided as PDF)
    └── [other GHL-related files]
```

---

## 💡 Tips
- **Start simple**: If the user only has a rough diagram, first create the stage map (Step 2), get confirmation, then write the copy.
- **Iterate**: The user may want to adjust timing, add stages, or change tone. The data-driven HTML makes this easy to modify.
- **Cross-reference**: Always check the knowledge base for specific terminology, pricing, deadlines, or compliance requirements that should be reflected in the copy.
- **Appointment reminders**: Use negative timing (-24H, -1H, -10min) for pre-appointment notifications.
- **Long cycles**: Some stages (like document collection, payment) may need longer intervals (3D, 7D, 14D, 21D).
