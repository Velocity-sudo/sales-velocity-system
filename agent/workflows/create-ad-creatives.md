---
description: Sales Velocity System workflow to create Meta Ads static image creatives. Generates 9 campaign-ready images (3 angles × 3 formats) with embedded copy, plus a captions file with recommended post copy. Uses the creating-ad-creatives skill.
---

# OBJECTIVE
Generate a complete set of static Meta Ads image creatives for a client, including campaign-ready images with embedded persuasive copy and a `captions.md` file with post copy, hashtags, and campaign setup recommendations.

# REQUIRED INPUTS
1. **Client Name** — The exact name of the client (must exist in Procesos de Clientes in Notion).
2. **Campaign Objective** (optional) — What the ads drive to (VSL, Webinar, etc.). Default: VSL views.
3. **Custom Angles** (optional) — Override the default 3 angles (Error Común, Emocional, Urgencia).

# PREREQUISITES
The client MUST already have in Notion:
- ✅ **OFERTA 100M** (provides avatar, pain, mechanism, promise)
- ✅ **Brand Manual or brand colors** (in local folder or knowledge base)

If these don't exist, run the prerequisite skills first via the Orchestrator.

# EXECUTION STEPS

## Step 1: Load the Skill
// turbo
Read the `creating-ad-creatives` SKILL.md file at:
```
~/.agent/skills/creating-ad-creatives/SKILL.md
```
OR
```
/Users/niko/Desktop/AntiGravity /Proyecto Agentes Sales Velocity/.agent/skills/creating-ad-creatives/SKILL.md
```

## Step 2: Gather Client Context (via `managing-notion`)
1. Search for the client in Procesos de Clientes database (`2f7e0f37-6c6d-81b6-9cba-df48640f2afe`).
2. Read the client's **OFERTA 100M** child page — extract: Avatar, Pain, Mechanism, Promise.
3. Read the client's **Brand Manual** from `~/Desktop/Clientes/[Client Name]/` — extract: Primary color, Accent color, Dark color, Font.
4. Read the client's **ADS QUE CONVIERTEN** child page if it exists — for messaging alignment.

## Step 3: Generate Copy for 3 Angles
Follow the SKILL.md instructions for **Step 2: Generate Copy for 3 Angles**.
Create the exact text that will go INSIDE the images:
- **Ángulo 1: Error Común** — Headlines, sub-lines, CTAs
- **Ángulo 2: Emocional** — Headlines, sub-lines, CTAs
- **Ángulo 3: Urgencia** — Headlines, sub-lines, CTAs

Present the copy to the user for approval BEFORE generating images.

## Step 4: Generate 9 Images
Using the `generate_image` tool, create 9 images following the SKILL.md prompt template:

| # | Angle | Format | Filename |
|---|-------|--------|----------|
| 1 | Error Común | 1:1 | `error_comun_1x1.webp` |
| 2 | Error Común | 4:5 | `error_comun_4x5.webp` |
| 3 | Error Común | 9:16 | `error_comun_9x16.webp` |
| 4 | Emocional | 1:1 | `emocional_1x1.webp` |
| 5 | Emocional | 4:5 | `emocional_4x5.webp` |
| 6 | Emocional | 9:16 | `emocional_9x16.webp` |
| 7 | Urgencia | 1:1 | `urgencia_1x1.webp` |
| 8 | Urgencia | 4:5 | `urgencia_4x5.webp` |
| 9 | Urgencia | 9:16 | `urgencia_9x16.webp` |

Generate in parallel where possible (3 at a time per angle).

## Step 5: Create `captions.md`
Follow the SKILL.md template for the captions file. Include:
- Summary table of all creatives
- Post copy (100-150 words) for each angle
- Hashtags per angle
- Platform-specific notes
- Campaign A/B test structure
- Budget recommendations

## Step 6: Organize & Deliver
1. Create the folder structure:
```
~/Desktop/Clientes/[Client Name]/ad_creatives/
├── 1x1/
├── 4x5/
├── 9x16/
└── captions.md
```
2. Move/copy all images to the correct format subfolders.
3. Save `captions.md` in the root of `ad_creatives/`.

## Step 7: Notify the User
Present a summary:
- Total images generated: 9 (or more if custom angles)
- Angles covered with brief descriptions
- Path to `captions.md`
- Reminder to review images before uploading to Meta Ads Manager
- Suggest running `/ads-launch-prep` for a full campaign audit

# OUTPUT
- **9 images** (3 angles × 3 formats) in `~/Desktop/Clientes/[Client Name]/ad_creatives/`
- **1 captions.md** file with post copy, hashtags, and campaign setup notes
