---
description: Sales Velocity System workflow to build and deploy a client website (landing page) to GitHub Pages. Creates a premium HTML landing page, deploys it to GitHub Pages under the Velocity-sudo account, and delivers a shareable public link as a client deliverable.
---

# /deploy-website — Build & Deploy Client Website

## Overview
This workflow builds a premium, single-purpose landing page for a client and deploys it to **GitHub Pages** under the `Velocity-sudo` GitHub account. The result is a live, shareable URL that serves as a permanent client deliverable.

**Output:** `https://velocity-sudo.github.io/[client-slug]/`

---

## Pre-requisites
Before running this workflow, ensure:
1. ✅ Client has a **Brand Manual** (run `/create-brand-manual` first if missing)
2. ✅ Client has a **knowledge base** at `~/Desktop/Clientes/[Client Name]/base_de_conocimiento_*.md`
3. ✅ `gh` CLI is authenticated (`gh auth status`)
4. ✅ Git is installed and configured

---

## Step 1: Gather Context

Read the following client files to extract brand tokens, copy, and assets:

```
~/Desktop/Clientes/[Client Name]/brand-assets/BRAND_MANUAL.md    → Colors, typography, voice & tone
~/Desktop/Clientes/[Client Name]/base_de_conocimiento_*.md       → Avatar, offer, pain points, key phrases
~/Desktop/Clientes/[Client Name]/brand-assets/BRAND_MANUAL.html  → Design reference
```

**Extract and confirm:**
- [ ] Brand color palette (CSS variables)
- [ ] Typography (font families)
- [ ] Voice & tone guidelines
- [ ] Key phrases / sales copy
- [ ] Primary CTA (what action do we want visitors to take?)
- [ ] CTA destination URL (e.g., Amazon link, GHL form, calendar link)
- [ ] Hero image or book cover (if applicable)
- [ ] Client name and tagline

**ASK the user:**
> "¿Cuál es el objetivo principal de esta página? (ej: vender un libro, agendar una llamada, registrarse a un webinar)"
> "¿Cuál es el link del CTA principal?"

---

## Step 2: Define Website Sections

Based on the client's offer and objective, propose a section index. Here is the **standard template** (adjust per client):

| # | Section | Purpose |
|---|---|---|
| 01 | **Nav** | Brand name + fixed CTA button |
| 02 | **Hero** | Headline + subheadline + hero image/book cover + primary CTA + social proof stats |
| 03 | **Pain / Revelation** | Cards exposing pain points or provocative questions that build curiosity |
| 04 | **Big Quote** | Emotional pull quote from client/brand + CTA |
| 05 | **What You'll Get** | Numbered list of benefits/discoveries/transformations |
| 06 | **Scrolling Quotes** | Infinite-scroll strip with key brand phrases |
| 07 | **About / Author** | Origin story + credentials + trust signals |
| 08 | **Big Quote #2** | Second emotional quote to break up content |
| 09 | **Social Proof / Numbers** | Key stats (pages, years, clients, etc.) |
| 10 | **Formats / Pricing** | Product variants with individual CTA links |
| 11 | **FAQ** | Accordion FAQ to handle objections |
| 12 | **Final CTA** | Closing emotional headline + main CTA button |
| 13 | **Footer** | Copyright + location |
| 14 | **Sticky CTA (Mobile)** | Fixed bottom bar on mobile with CTA |

**Present the proposed index to the user for approval before building.**

---

## Step 3: Build the Landing Page

Create the HTML file at:
```
~/Desktop/Clientes/[Client Name]/website/index.html
```

### Design Standards (MANDATORY):
- **Single HTML file** — all CSS inline in `<style>`, all JS inline in `<script>`
- **Dark premium aesthetic** — use brand manual colors, no generic defaults
- **Dual typography** — Display font (Playfair Display, etc.) for headings + Sans-serif (Inter, Outfit) for body
- **Micro-animations** — `fade-in` on scroll using Intersection Observer
- **Glassmorphism nav** — `backdrop-filter: blur()` on scroll
- **Gold/accent gradients** — for CTA buttons
- **Mobile-first responsive** — `@media (max-width: 900px)` and `(max-width: 600px)` breakpoints
- **Sticky CTA on mobile** — fixed bottom bar with primary CTA
- **FAQ accordion** — vanilla JS, no dependencies
- **Scrolling quote strip** — CSS `@keyframes` infinite animation
- **No external dependencies** — no React, no Tailwind, no frameworks. Pure HTML/CSS/JS
- **SEO meta tags** — title, description, Open Graph

### Image Handling:
- Copy all required images to `~/Desktop/Clientes/[Client Name]/website/assets/`
- Use relative paths (`./assets/image.jpg`) — NOT parent directory paths
- Optimize filenames (no spaces, no special characters)

### CTA Links:
- Replace ALL `href="#"` placeholders with the real CTA URL
- Ensure `target="_blank"` on external links (Amazon, calendars, etc.)
- Internal scroll links use `href="#section-id"` with `scroll-behavior: smooth`

---

## Step 4: Local Preview & Verification

// turbo
Open the HTML file in the browser and verify:
```bash
open ~/Desktop/Clientes/[Client\ Name]/website/index.html
```

**Verify checklist:**
- [ ] Hero loads correctly with image
- [ ] All sections render properly
- [ ] CTA buttons have correct links
- [ ] FAQ accordion works
- [ ] Mobile responsive (resize window)
- [ ] Animations fire on scroll
- [ ] No broken images or missing fonts

---

## Step 5: Deploy to GitHub Pages

### 5a. Initialize Git repo
// turbo
```bash
cd ~/Desktop/Clientes/[Client\ Name]/website
git init
git add -A
git commit -m "🚀 Landing page: [Client Name] — [Page Title]"
```

### 5b. Create GitHub repo
**Naming convention:** `Velocity-sudo/[client-slug]`
- Lowercase
- Hyphens instead of spaces
- No special characters

Examples:
- Roy Roby → `roy-roby`
- Jorge Vergara → `jorge-vergara`
- Ignacio Sánchez → `ignacio-sanchez`

```bash
cd ~/Desktop/Clientes/[Client\ Name]/website
gh repo create Velocity-sudo/[client-slug] \
  --public \
  --description "Landing page — [Client Name]" \
  --source . \
  --push
```

### 5c. Enable GitHub Pages
```bash
gh api repos/Velocity-sudo/[client-slug]/pages \
  -X POST \
  --input - <<'EOF'
{
  "source": {
    "branch": "main",
    "path": "/"
  },
  "build_type": "legacy"
}
EOF
```

### 5d. Wait for deployment
// turbo
```bash
sleep 30
gh api repos/Velocity-sudo/[client-slug]/pages --jq '{status, html_url}'
```

Expected output: `"status": "built"`

If status is `"building"`, wait 30 more seconds and check again.

---

## Step 6: Verify Live Site

Open the live URL in the browser and take screenshots to verify:
```
https://velocity-sudo.github.io/[client-slug]/
```

**Verify:**
- [ ] Page loads on the public URL
- [ ] All images display correctly
- [ ] CTA links work and open in new tab
- [ ] HTTPS is active (green padlock)

---

## Step 7: Deliver to Client

### 7a. Save the link in the client's local folder
Create a `DELIVERABLES.md` file:

```markdown
# Entregables — [Client Name]

## 🌐 Sitio Web (Landing Page)
- **URL Live:** https://velocity-sudo.github.io/[client-slug]/
- **Repositorio:** https://github.com/Velocity-sudo/[client-slug]
- **Última actualización:** [date]
- **Objetivo:** [purpose of the page]
- **CTA Principal:** [destination URL]
```

Save at: `~/Desktop/Clientes/[Client Name]/DELIVERABLES.md`

### 7b. (Optional) Connect custom domain
If the client has a custom domain (e.g., royroby.com):

1. Add a `CNAME` file in the website folder:
```bash
echo "royroby.com" > ~/Desktop/Clientes/[Client\ Name]/website/CNAME
git add CNAME && git commit -m "🌐 Add custom domain" && git push
```

2. Configure DNS at the domain registrar:
   - Add a CNAME record: `www` → `velocity-sudo.github.io`
   - Or A records pointing to GitHub IPs:
     - `185.199.108.153`
     - `185.199.109.153`
     - `185.199.110.153`
     - `185.199.111.153`

3. Enable in GitHub:
```bash
gh api repos/Velocity-sudo/[client-slug]/pages -X PUT -f "cname=royroby.com"
```

---

## Updating the Site (Future Changes)

When you need to update the site after deployment:

// turbo-all
```bash
cd ~/Desktop/Clientes/[Client\ Name]/website
# Make your changes to index.html...
git add -A
git commit -m "✨ [Description of change]"
git push
# Site auto-updates in ~30-60 seconds
```

---

## Quick Reference

| Item | Value |
|---|---|
| **GitHub Account** | `Velocity-sudo` |
| **Repo Pattern** | `Velocity-sudo/[client-slug]` |
| **URL Pattern** | `https://velocity-sudo.github.io/[client-slug]/` |
| **Local Path** | `~/Desktop/Clientes/[Client Name]/website/` |
| **Deliverables File** | `~/Desktop/Clientes/[Client Name]/DELIVERABLES.md` |
| **Tech Stack** | Vanilla HTML + CSS + JS (single file, no frameworks) |
| **Design Standard** | Premium dark, brand manual colors, micro-animations |
