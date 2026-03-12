---
name: creating-vsl
description: Generates high-converting Video Sales Letter scripts and landing page copy based on proven frameworks from Russell Brunson, Alex Hormozi, Alex Cattoni, and Jon Benson. Use when the user mentions VSL, video sales letter, landing page copy, sales funnel, conversion optimization, or wants to create persuasive video scripts.
---

# VSL Creator - Video Sales Letter & Landing Page Copy Generator

## When to Use This Skill

Use this skill when the user wants to:
- Create a Video Sales Letter (VSL) script
- Generate landing page copy for a VSL
- Optimize conversion rates for video funnels
- Apply proven copywriting frameworks (PAS, BAB, etc.)
- Create hooks, headlines, or CTAs for sales videos
- Adapt messaging to different awareness levels

## Workflow

### Step 1: Gather Client Information

Collect the following information from the user:

```markdown
**Product/Service Information:**
- [ ] What are you selling?
- [ ] What is the price point? (Low-ticket <$100, High-ticket >$1000)
- [ ] What is the dream outcome for the customer?

**Avatar Information:**
- [ ] Who is your ideal customer?
- [ ] What is their main pain point?
- [ ] What level of awareness are they at?
  - Unaware (don't know they have a problem)
  - Problem Aware (know the problem, not the solution)
  - Solution Aware (know solutions exist, not yours specifically)
  - Product Aware (know your product, need convincing)
  - Most Aware (ready to buy, just need a nudge)

**Supporting Elements:**
- [ ] Do you have testimonials or proof of results?
- [ ] What guarantee can you offer?
- [ ] What makes your solution unique? (Mechanism)
- [ ] What are the main objections customers have?
```

If the user doesn't provide all information, query NotebookLM for best practices on that specific element.

### Step 2: Query NotebookLM for Framework Guidance

Consult the **"VSL High Ticket - Copy & Conversión"** notebook (ID: `b2a2dc71-04e6-4c93-af5a-7549fe00d1ff`) with these queries:

**Query 1 - Framework Selection:**
```
Para un [tipo de producto/servicio] dirigido a audiencia [nivel de consciencia], con precio [X], ¿qué framework de VSL recomiendas (PAS, BAB, o Checklist Oferta Caliente)? Dame la estructura específica paso a paso.
```

**Query 2 - Hook Generation:**
```
Para un VSL sobre [producto/servicio] con avatar [descripción] y dolor principal [dolor específico], genera 3-5 hooks efectivos usando técnicas comprobadas (pregunta de identificación, declaración fuerte, "cómo lograr X sin Y", advertencia, curiosidad).
```

**Query 3 - Objection Handling:**
```
¿Cuáles son las objeciones más comunes para ofertas de [tipo] a precio [X] y cómo se manejan en el guión del VSL? Dame el FAQ sequencing recomendado.
```

### Step 3: Generate VSL Script

Using the framework recommended by NotebookLM, create a complete VSL script following this 8-phase structure:

#### **Phase 1: The Hook (0-30 seconds)**
- Choose hook type based on avatar and awareness level
- Front-load: Name pain + Promise + Proof in first 30 seconds
- See [hooks-library.md](resources/hooks-library.md) for templates

#### **Phase 2: Problem & Rapport**
- Describe their current "hell" 
- Use Epiphany Bridge technique (storytelling)
- Make them feel understood ("You're not alone")

#### **Phase 3: Agitation**
- Intensify the pain emotionally
- Describe consequences in all life areas
- "Pour salt in the wound" technique

#### **Phase 4: Transition/Hope**
- Create a hope bridge
- Tease that a solution exists (but don't reveal yet)
- "Imagine if you could..." statements

#### **Phase 5: The Solution (Your Offer)**
- Present as a unique mechanism, not just a product
- Explain HOW it works (logic that justifies why it'll work)
- Use "So That" formula for benefits (see template)

#### **Phase 6: Social Proof**
- Specific testimonials with measurable results
- Exact numbers (9,984 not 10,000)
- Testimonials that handle objections

#### **Phase 7: Objection Handling**
- Pre-answer FAQ before they ask
- "Sequence their objections" from sales calls

#### **Phase 8: CTA + Scarcity**
- Clear, single call-to-action
- Guarantee that reverses risk
- Justified urgency/scarcity

**Recommended Length:**
- SaaS/Low-Ticket: 3-5 minutes
- High-Ticket/B2B: 10-15 minutes
- Webinar-style: Up to 30 minutes

Use [vsl-script-template.md](resources/vsl-script-template.md) as your base.

### Step 4: Generate Landing Page Copy

Create landing page copy that supports the VSL (doesn't compete with it):

#### **Above the Fold:**
```
[Eyebrow] <- Audience qualifier or social proof
[Headline] <- Promise + Unique Mechanism
[Subheadline] <- Reinforce offer + next step
[VIDEO PLAYER]
[Primary CTA Button]
```

#### **Benefit Bullets:**
- Use "So That" technique (feature → so that → benefit)
- 3-7 "juicy" benefits
- Focus on emotional & tangible outcomes

#### **Social Proof Section:**
- Strategic testimonial placement
- Logos (if applicable)
- Specific, measurable results

#### **Guarantee:**
- Risk reversal language
- Clear terms (30-day, unconditional, etc.)

#### **Secondary CTA:**
- Reinforcement of primary CTA
- Variant for A/B testing

#### **FAQ/Objections:**
- Pre-empt common doubts

Use [landing-page-template.md](resources/landing-page-template.md) as your base.

### Step 5: Optimize for Conversion

Run the output through [conversion-checklist.md](resources/conversion-checklist.md):

**Critical Checks:**
- [ ] Hook names pain + promise + proof in first 30 sec
- [ ] Benefits use "So That" formula (not just features)
- [ ] CTA reduces anxiety ("Get" vs "Buy")
- [ ] Numbers are specific and exact
- [ ] Guarantee eliminates perceived risk
- [ ] Message match: Ad → Headline congruence
- [ ] Only ONE primary goal (no distracting links)

### Step 6: Deliver Outputs

Provide the user with:
1. **Complete VSL Script** (timestamped by phase)
2. **Landing Page Copy** (structured by section)
3. **CTA Variants** for A/B testing (from [cta-library.md](resources/cta-library.md))
4. **Headline Variants** for A/B testing
5. **Optimization Notes** (what to test first)

### Step 7: Generate Antigravity Landing Page Code (BONUS)

If the user wants production-ready HTML/CSS/JS code for the landing page, use [landing-page-prompt-template.md](resources/landing-page-prompt-template.md) to create a detailed prompt for Antigravity.

**Process:**
1. Fill out the template with all client information gathered in Steps 1-4
2. Select appropriate brand personality and color palette based on niche:
   - **High-Ticket Coaching**: Aspirational/Luxury (dark + gold)
   - **SaaS B2B**: Professional/Trustworthy (white + corporate blue)
   - **Fitness**: Energetic/Bold (white + red/orange)
   - **eCommerce**: Warm/Friendly or Clean/Minimal (depends on brand)
   - **Education**: Clean/Minimal Tech (white + purple/blue)
3. Complete the "INFORMACIÓN ESPECÍFICA DEL CLIENTE" section with:
   - VSL script details (promise, mechanism, testimonials)
   - FAQ from objection handling phase
   - Tracking IDs (Google Analytics, Facebook Pixel)
   - Video URL and CTA destination
4. Copy the complete prompt and send to Antigravity or any AI code generator
5. Receive 3 production-ready files: `index.html`, `styles.css`, `script.js`

**Why this matters:**
- Reduces landing page development from days to minutes
- Ensures mobile-first, conversion-optimized design
- Maintains message match between VSL and landing page
- Includes tracking for analytics out of the box

**Deliverable:** Give the user the customized Antigravity prompt so they can generate the code instantly.

## Best Practices 2024-2025

Auto-apply these modern optimizations:

1. **Front-Loading**: Put strongest message first (not at the end)
2. **Pronoun Swap**: Use "my" instead of "your" in CTAs (+90% conversion)
3. **Exact Numbers**: 9,984 clients (not "10,000")
4. **FAQ Sequencing**: Answer objections before they arise
5. **Message Match**: Ad copy = Landing headline
6. **Specificity**: Avoid vague claims, use concrete data
7. **Authenticity & Natural Language (CRITICAL)**: 
   - Speak directly to the **pain** right from the start (e.g., "If you want to stop trading time for money...").
   - AVOID marketer clichés and exaggerated language entirely (e.g., do not use words like "crack", "ninja", "hacerte millonario", or "pudriéndose en el banco").
   - Ensure the tone is mature, direct, and highly professional. It should sound like a natural, honest conversation.
   - For authority/proof, always mention specific cases: "Person X achieved Y result doing Z."
   - For the mechanism/system, always break it down clearly into actionable steps ("Primero, hacemos X. Segundo, configuramos Y. Tercero, invertimos Z.").
   - Do not explicitly narrate your strategy to the user in the copy (e.g., avoids phrases like "voy a filtrarte rápido"). Integrate the strategy naturally.
8. **Repurposing**: Suggest how to clip long VSL into short ads

## Resources

- [vsl-script-template.md](resources/vsl-script-template.md) - Complete script template
- [landing-page-template.md](resources/landing-page-template.md) - Landing page structure
- [landing-page-prompt-template.md](resources/landing-page-prompt-template.md) - **NEW** Antigravity prompt for HTML/CSS/JS generation
- [frameworks-reference.md](resources/frameworks-reference.md) - PAS, BAB, Oferta Caliente frameworks
- [hooks-library.md](resources/hooks-library.md) - Effective hook formulas
- [cta-library.md](resources/cta-library.md) - Optimized CTA copy
- [conversion-checklist.md](resources/conversion-checklist.md) - Quality assurance checklist

## Example Usage

```
USER: "Create a VSL for my $2,000 coaching program that helps entrepreneurs scale to 7 figures"

AGENT:
1. Gathers missing info (avatar pain points, testimonials, guarantee)
2. Queries NotebookLM for high-ticket coaching VSL structure
3. Generates 15-min VSL script using BAB framework
4. Creates landing page copy with 5 headline variants
5. Runs conversion checklist
6. Delivers complete VSL + Landing copy package
7. BONUS: Generates Antigravity prompt for production-ready HTML/CSS/JS code (mobile-first, tracking included)
```

## Notes

- Always consult NotebookLM before generating to ensure latest strategies
- Adapt framework to awareness level (don't use PAS for "Unaware" audience)
- VSL length should match ticket price and complexity
- Landing page should have ONLY one goal (the video + CTA)
