---
description: Sales Velocity System workflow to build GoHighLevel workflows and automations.
---
# OBJECTIVE
Structure a comprehensive automation system in GoHighLevel to capture, nurture, and notify high-intent leads using the Sales Velocity System methodology. Ensure no lead acts without consequence.

# REQUIRED INPUTS
1. The objective of the automation (e.g., Webinar Registration, VSL Opt-In, Lead Magnet Download, No-Show Follow-up).
2. The specific target audience and offer details from the client's Knowledge Base (`base_de_conocimiento.md`).

# EXECUTION STEPS
1. **Trigger Definition**: Specify the exact trigger in GHL (e.g., `Form Submitted` or `Opportunity Stage Changed`).
2. **Tag Nomenclature System**: Identify the strict tags to add or remove at the beginning of the sequence (e.g., `+ [Status] Registered`, `- [Status] Cold Lead`).
3. **Omnichannel Communication Flow**:
   - Provide a sequential list of actions incorporating Email, SMS, and WhatsApp (if applicable).
   - Specify the wait times/delays required (`Wait 5 minutes`, `Wait 1 Day`).
   - For every communication, draft the copy in a direct, persuasive format. Give exact text. Include placeholders like `{{contact.first_name}}` and `{{custom_values.link}}`.
   - Ensure the copy aligns with the brand's tone of voice and directly drives the desired CTA (e.g., "Join the Webinar", "Book a Call").
4. **Internal Notifications**: Include the logic for notifying the internal sales team/closers (via Slack or GHL App) when a high-intent action occurs, specifying what the notification should say.
5. **Pipeline Structuring**: Define what Opportunity Pipeline this flow belongs to, stage mapping, and lead score adjustments.

# OUTPUT
Output the entire GHL Automation flow visually as a step-by-step numbered list, with all the draft texts ready to be copied and pasted directly into GHL's action nodes.
