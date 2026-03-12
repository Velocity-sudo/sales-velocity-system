---
description: Sales Velocity System workflow to build a custom GoHighLevel premium funnel.
---
# OBJECTIVE
Pass from validated copy to a fully styled, premium GoHighLevel landing page / funnel. This workflow converts text and brand manuals into exact GHL-compatible CSS, JS, and HTML snippets.

# REQUIRED INPUTS
1. The validated copy (e.g., VSL script, page structure).
2. The client's Brand Manual (`BRAND_MANUAL.md`) to establish the color palette, typography, and styling rules.

# EXECUTION STEPS
1. **Design System Abstraction**: Review the Brand Manual and establish the core CSS variables (`:root`) for colors, fonts, and spacing.
2. **Component Breakdown**: Translate the page copy into standard GHL sections (Hero, VSL, Guarantee, Offer).
3. **Generate GHL-Specific Codes**:
   - Provide the **[Custom CSS]** block (to be pasted in Page Settings). It MUST use high-end aesthetics: glassmorphism (`backdrop-filter: blur(10px)`), smooth hover transitions, premium typography imports (`@import`), and robust structural overrides for GHL forms (`.ghl-form-wrap`, etc.).
   - Provide the **[Tracking Code - Header/Footer]** blocks if custom scripts or tracking are required.
   - Provide the **[Custom HTML Element]** snippets for anything that GHL's native builder cannot natively support (e.g., specific micro-animations, complex gradients, or embedded custom widgets).
4. **Mobile Responsiveness**: Specifically target and fix common GHL mobile breakpoints via `@media (max-width: 480px)`.

# OUTPUT
Output the code blocks clearly labeled with EXACT instructions on where they should be pasted inside the GoHighLevel Page Builder. Do not assume the user knows; be perfectly explicit. 
