---
description: Sales Velocity System workflow for daily handoff and logging.
---
# OBJECTIVE
Ensure absolute continuity of context. This workflow summarizes daily progress, pinpoints current blocker locations, and explicitly details the next atomic steps across the entire system.

# SYSTEM TRIGGERS & CONTEXT
This should be the **final step** executed at the end of a session or before switching contexts/clients.

# EXECUTION STEPS
1. **Analyze Session History**: Review all files touched, configurations made, assets produced, and strategies formulated in the current session.
2. **Current Deliverables Status**: Identify whether the client is at the Offer phase, VSL creation, GHL Setup, or Ads Launch.
3. **Structured Log Creation**:
   - Synthesize a handoff report named `LOG.md` (or append to an existing `LOG.md` file) within the client's working directory.
   - Format exactly as:
     - `## DATE & TIME`: [Current Date and Timestamp]
     - `### ✅ WHAT WAS ACHIEVED`: Bullet points detailing exact files edited, copies written, or workflows designed.
     - `### 🔴 BLOCKERS / PENDING`: Any missing information from the client (e.g., waiting for video assets, domain credentials) or bugs encountered.
     - `### ➡️ NEXT EXACT STEPS`: Granular, actionable steps for the next session (e.g., "Implement CSS into GHL Footer").

# ACTION
Do not hesitate. Generate the `LOG.md` file immediately upon the user running `/log-session`. If the user provided a summary verbally, incorporate it directly into the report.
