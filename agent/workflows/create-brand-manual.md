---
description: Sales Velocity System workflow to create a complete Brand Manual (HTML + PDF) using the brand-designer skill. Includes industry research, 5 visual proposals in a single selector doc, user approval, and full manual build.
---

# 🎨 Create Brand Manual Workflow (`/create-brand-manual`)

Workflow completo para crear manuales de marca con **verdadera diferenciación visual** para cada cliente. Tres fases obligatorias antes de construir: investigación de industria, documento selector con 5 acercamientos, y aprobación del usuario.

---

## FASE 1 — Investigación de Industria

Antes de proponer cualquier estética, investiga el ecosistema visual del cliente.

### 1.1 Contexto del Cliente
1. Revisa la carpeta del cliente (`~/Desktop/Clientes/[Nombre]/`) y su base de conocimiento.
2. Extrae:
   - Industria principal y sub-nicho
   - Audiencia(s) objetivo (edad, perfil, aspiraciones)
   - Referencias visuales existentes (sitio web, Instagram, materiales)
   - Personalidad aspiracional de la marca (si está definida)
   - Si opera con sub-marcas o líneas duales, identificarlas

### 1.2 Investigación de Líderes del Nicho
1. Identifica **3-5 líderes/referentes** de la industria del cliente (no necesariamente competidores directos, sino personas/marcas con resultados grandes en el mismo espacio).
2. Usa `firecrawl_scrape` con formato `branding` para extraer la identidad visual de cada uno:
   - Paleta de colores
   - Tipografías
   - Modo visual (dark/light/mix)
   - Estilo general (corporativo, tech, lifestyle, editorial)
3. Documenta los hallazgos en un resumen interno (no se entrega al usuario, es para informar las propuestas).

### 1.3 Inputs del Usuario (antes de proponer)
Pregunta explícitamente al usuario:
- ¿Qué vibe/feeling buscas? (moderno tech / elegante clásico / vibrante lifestyle / minimalista / otro)
- ¿Preferencia de modo? (dark / light / sin preferencia)
- ¿Hay alguna marca o sitio web que admires visualmente?
- ¿Se necesitan sub-marcas / líneas duales?

> **NOTA:** Si el usuario ya proporcionó esta info en el prompt inicial, no vuelvas a preguntar. Úsala directo.

---

## FASE 2 — Documento Selector de Acercamientos

Genera **UN solo documento HTML** (ligero, una sola página) que presente **5 acercamientos visuales** diferentes. Cada acercamiento consiste en:

### Estructura de cada acercamiento:
1. **Nombre del acercamiento** (ej: "Neon Momentum", "Heritage Prestige", "Swiss Minimal")
2. **Muestra visual compacta:** un bloque con:
   - El nombre del cliente renderizado en la tipografía display propuesta
   - 4-6 swatches de color (cuadrados pequeños con hex)
   - Un par tipográfico mostrado (display + body)
3. **Objetivo / Por qué**: 2-3 líneas explicando qué comunica este estilo y por qué funciona para la audiencia del cliente
4. **Arquetipo base**: Indicar cuál arquetipo usa (Tech/Neon, Editorial/Prestige, Swiss/Minimal, Lifestyle/Vibrant, Bento/Dashboard, etc.)

### Reglas para las 5 propuestas:
- **Mínimo 3 arquetipos diferentes** (no puede haber 3 propuestas dark mode tech)
- **Mínimo 2 familias tipográficas display diferentes** (no todo puede ser geometric sans)
- **Mínimo 1 propuesta light mode y 1 dark mode**
- **Cada propuesta debe tener un font pairing único** (display + body, nunca repetir el mismo pairing)
- Los colores deben estar informados por la investigación de industria (Fase 1)

### Pool de Tipografías Disponibles (usar variedad, NO siempre las mismas):

**Display (elegir diferente para cada propuesta):**
- Geometric Sans: Space Grotesk, Syne, Urbanist, Instrument Sans
- Rounded: Plus Jakarta Sans, Nunito, Quicksand  
- Serif: Cormorant Garamond, Playfair Display, DM Serif Display, Lora, Fraunces
- Slab: Roboto Slab, Bitter, Zilla Slab
- Monospace accent: JetBrains Mono, Fira Code, IBM Plex Mono
- Heavy impact: Outfit, Montserrat 900, Bebas Neue, Anton

**Body (complementario al display):**
- DM Sans, Inter, Lato, Source Sans 3, IBM Plex Sans, Manrope, Figtree

### Formato del documento selector:
- HTML single-page con **los 5 acercamientos en vertical**, scroll simple
- Cada acercamiento en un "card" o sección visualmente separada
- El card muestra el nombre del cliente en la tipografía propuesta (cargada via Google Fonts)
- Fondo del card refleja el modo propuesto (dark/light/cream)
- NO es un mini-manual — es solo una muestra visual rápida para decidir

### Entrega:
1. Guarda el documento en `[Ruta del Cliente]/01_marca/BRAND_SELECTOR.html`
2. **Deploy a GitHub Pages** para previsualización compartible:
   - Copia `BRAND_SELECTOR.html` como `selector.html` en `[Ruta del Cliente]/05_deploy/`
   - Crea/actualiza el repo `Velocity-sudo/[client-slug]` y push
   - Activa GitHub Pages → URL live: `https://velocity-sudo.github.io/[client-slug]/selector.html`
   - Presenta el **link live** al usuario para que pueda ver desde cualquier dispositivo
3. Abre en browser y captura screenshots de las 5 opciones
4. **Espera aprobación** — el usuario elige uno, pide ajustes, o mezcla elementos

---

## FASE 3 — Construcción del Manual Completo

Solo se ejecuta **después** de que el usuario apruebe un acercamiento de la Fase 2.

### 3.1 Lectura del Skill
1. Lee las directrices del skill: `~/.agent/skills/brand-designer/SKILL.md`
2. Usa como referencia (NO como template rígido) las plantillas en:
   - `~/.agent/skills/brand-designer/templates/`
   - Otros manuales existentes de clientes como inspiración de contenido (NO de diseño visual)

### 3.2 Construcción del HTML
1. Construye el manual completo usando el **arquetipo visual elegido** por el usuario
2. **REGLA CRÍTICA:** El layout, tipografía, modo visual, estilo de componentes y animaciones **deben corresponder al arquetipo elegido, NO al template default**
3. **REGLA SUB-MARCAS:** Si el cliente tiene múltiples sub-marcas (ej: Socios + Clientes), cada una se muestra de forma **completamente independiente**, lado a lado pero **NUNCA mezcladas**:
   - ❌ NO gradientes que combinen colores de ambas marcas
   - ❌ NO logotipos/nombres con letras de diferentes sub-marcas (ej: "C" azul + "orona" dorado)
   - ❌ NO elementos que fusionen ambas identidades en un solo componente
   - ✅ SÍ secciones side-by-side donde cada panel tiene SU propia paleta completa
   - ✅ SÍ cards separados para cada sub-marca con sus propios colores
4. Secciones mínimas del manual:
   - Hero / Portada
   - Identidad & Filosofía
   - Arquitectura de marca (si hay sub-marcas)
   - Paleta(s) de color con swatches y códigos hex
   - Sistema tipográfico con muestras reales
   - Pilares de marca
   - Voz y tono (con ejemplos DO/DON'T)
   - Componentes UI (botones, badges, cards)
   - Design tokens (spacing, radius, shadows)
   - Footer con versión y fecha
4. Guarda en: `[Ruta del Cliente]/01_marca/BRAND_MANUAL.html`

### 3.3 Verificación Visual
1. Abre el HTML en browser subagent
2. Captura screenshots de al menos 3 secciones clave
3. Verifica que el diseño corresponda al arquetipo elegido (NO al template default)
4. Si hay problemas, itera antes de entregar

---

## FASE 4 — Deploy y Registro

### 4.1 GitHub Pages
1. Copia `BRAND_MANUAL.html` como `index.html` en `[Ruta del Cliente]/05_deploy/`
2. Crea/actualiza el repo en `Velocity-sudo/[client-slug]` (lowercase, hyphens)
3. Push y activa GitHub Pages en branch `main`, path `/`
4. URL final: `https://velocity-sudo.github.io/[client-slug]/`

### 4.2 Notion
1. Busca la página del cliente en "Procesos de Clientes"
2. Crea sub-página: `📘 Brand Manual — [Nombre] v1.0`
3. Agrega callout con link live de GitHub Pages + detalles del arquetipo visual usado

### 4.3 DELIVERABLES.md
1. Actualiza o crea `DELIVERABLES.md` en la raíz del cliente con:
   - Link de GitHub Pages
   - Link del repo
   - Ruta local
   - Link de Notion
2. Copia a `06_docs/DELIVERABLES.md`

### 4.4 Confirmación
Notifica al usuario con:
- ✅ Link live de GitHub Pages
- ✅ Ruta local del HTML
- ✅ Link de Notion
