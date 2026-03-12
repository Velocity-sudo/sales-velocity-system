---
description: to create 100m offers for our clients
---

# OBJECTIVE
Analyze the client's Knowledge Base to design, structure, or refine a "$100M Grand Slam Offer" (Alex Hormozi style) tailored perfectly to their dream buyer.

# REQUIRED INPUTS
When running this workflow, please ensure:
1. The client's Knowledge Base file (`base_de_conocimiento_[cliente].md`) is available in context.
2. Any specific ideas, constraints, or price points the user has for this offer are mentioned.

# SKILL INTEGRATION
You MUST automatically activate and strictly follow the exact guidelines from the `creating-100m-offers` skill located in `~/.agent/skills/creating-100m-offers/SKILL.md`.

# EXECUTION STEPS
1. **Context Analysis**: Read the client's knowledge base to deeply understand their Identity, Business Goals, Premium Avatar, and Unique Mechanism.
2. **Offer Blueprint**: Apply the Value Equation framework (Dream Outcome, Perceived Likelihood of Achievement, Time Delay, Effort & Sacrifice) to engineer an irresistible, high-ticket offer.
3. **Local File Generation**: 
   - **CRITICAL**: Verify the EXACT absolute path of the current client's active directory (watch out for trailing spaces in directory names) before creating any files.
   - Create a local markdown file named `oferta_100M_[nombre_del_cliente].md` in that exact verified local directory.
   - Format it with high-end, direct, and aggressive sales copy.
4. **Notion Integration & Sync**: 
   - Use the Notion MCP tools to create a new page for the client's offer in their workspace.
   - The structure MUST strictly follow this exact template: `https://www.notion.so/OFERTA-100M-Nombre-del-Cliente-303e0f376c6d80968dd5d81be5da6766`
   - Map all the generated content from our local `.md` file directly into the newly created Notion blocks (Headers, Bullet points, Callouts).

# OUTPUT EXPECTATIONS
The offer must feel extremely premium, high-ticket, and impossible to say no to. The local `.md` file and the Notion page must serve as identical, synchronized sources of truth. Never deliver a basic offer; it must scream exponential ROI.
