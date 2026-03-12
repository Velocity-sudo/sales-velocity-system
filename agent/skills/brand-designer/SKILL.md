---
name: Brand Designer
description: Genera un manual de marca completo y un plan de acción/facturación para cualquier cliente nuevo usando plantillas probadas.
---

# Brand Designer Skill

Este skill contiene dos plantillas universales probadas con clientes reales. Se usan para crear materiales profesionales de marca y plan de facturación para cualquier cliente nuevo.

## Archivos incluidos

| Archivo | Propósito |
|---------|-----------|
| `templates/TEMPLATE_BRAND_MANUAL.md` | Manual de marca completo con identidad, colores, tipografía, componentes CSS, tono de voz, design tokens |
| `templates/TEMPLATE_BRAND_MANUAL.html` | Versión visual HTML del manual — dark-mode, swatches vivos, demos de componentes, design tokens en código |
| `templates/TEMPLATE_PLAN_ACCION.md` | Plan de facturación con matemática de ventas, lista de marcas, plan diario, técnicas ROPE/Dream Pitch, templates DM |

## Cómo usar

### Paso 1: Copiar las plantillas a la carpeta del nuevo cliente

```bash
# Crear carpeta del cliente
mkdir -p "/Users/niko/Desktop/{{NOMBRE_CLIENTE}}/brand-assets"
mkdir -p "/Users/niko/Desktop/{{NOMBRE_CLIENTE}}/templates"

# Copiar plantillas
cp "/Users/niko/.agent/skills/brand-designer/templates/TEMPLATE_BRAND_MANUAL.md" "/Users/niko/Desktop/{{NOMBRE_CLIENTE}}/brand-assets/BRAND_MANUAL.md"
cp "/Users/niko/.agent/skills/brand-designer/templates/TEMPLATE_BRAND_MANUAL.html" "/Users/niko/Desktop/{{NOMBRE_CLIENTE}}/brand-assets/BRAND_MANUAL.html"
cp "/Users/niko/.agent/skills/brand-designer/templates/TEMPLATE_PLAN_ACCION.md" "/Users/niko/Desktop/{{NOMBRE_CLIENTE}}/Plan_Dinero_1_Semana.md"
```

### Paso 2: Recolectar información del cliente

Antes de llenar las plantillas, necesitas:

**Para el Manual de Marca:**
1. Nombre completo del cliente
2. Tagline / frase clave
3. Industria / nicho
4. 3 pilares de marca
5. Colores existentes (o definir paleta nueva)
6. Fuente preferida (o elegir de Google Fonts)
7. Fotos profesionales (hero, visión, contacto)
8. Tono de voz (idioma, perspectiva, energía)
9. Frases clave / vocabulario de marca

**Para el Plan de Acción:**
1. Precios reales de paquetes/servicios
2. Meta mensual de ingresos ($X – $Y USD)
3. Caso de éxito existente (marca que ya pagó — con números)
4. Nicho y ubicación (para seleccionar marcas target)
5. Handle de redes sociales

### Paso 3: Llenar las variables

Ambas plantillas usan el formato `{{VARIABLE}}`. Busca y reemplaza cada variable con la información real del cliente:

```
{{NOMBRE_CLIENTE}} → Diego Páramo
{{TAGLINE}} → "Tu consultor de negocios digitales"
{{COLOR_ACENTO}} → #FF6B35
...etc
```

### Paso 4: Generar outputs

Una vez llenas las plantillas:

1. **Brand Manual Markdown** (`BRAND_MANUAL.md`): Llenar todas las `{{VARIABLES}}` con la info del cliente
2. **Brand Manual HTML** (`BRAND_MANUAL.html`): **OBLIGATORIO** — Llenar la plantilla HTML con las mismas variables. El HTML incluye swatches de colores vivos, demos interactivos de componentes, tipografía renderizada y design tokens en bloque de código
3. **Plan de Acción PDF:** Generar versión PDF del plan de acción
4. **GHL Snippets:** Crear las páginas web (landing, pricing, linktree, thank you) basadas en el manual de marca

> ⚠️ **IMPORTANTE:** La versión HTML del manual es un entregable obligatorio. Siempre generar ambos: `.md` y `.html`.

## Ejemplos de referencia

| Cliente | Carpeta | Archivos clave |
|---------|---------|----------------|
| **Johanna Cueva** | `/Users/niko/Desktop/Johanna Cueva /` | `brand-assets/BRAND_MANUAL.md`, `brand-assets/BRAND_MANUAL.html` |
| **Christian Funes** | `/Users/niko/Desktop/Christian Funes/` | `brand-assets/BRAND_MANUAL.md`, `brand-assets/BRAND_MANUAL.html` |
| **Antonio Martínez** | `/Users/niko/Desktop/Antonio Martinez /` | `brand-assets/BRAND_MANUAL.md`, `brand-assets/BRAND_MANUAL.html` |

> 💡 **Tip:** Revisa los HTML existentes como referencia de estilo. Cada uno adapta la plantilla base al estilo visual único del cliente (colores, fuentes, dark/light mode).

## Variables principales

### Manual de Marca
`{{NOMBRE_CLIENTE}}`, `{{TAGLINE}}`, `{{INDUSTRIA}}`, `{{HANDLE_IG}}`, `{{SITIO_WEB}}`, `{{PILAR_1}}` a `{{PILAR_3}}`, `{{HEX_OSCURO}}`, `{{HEX_CLARO}}`, `{{COLOR_ACENTO}}`, `{{FUENTE_PRINCIPAL}}`, `{{PRINCIPIO_COLOR}}`

### Plan de Acción
`{{META_MIN}}`, `{{META_MAX}}`, `{{PAQUETE_1_NOMBRE}}` a `{{PAQUETE_3_NOMBRE}}`, `{{PAQUETE_1_PRECIO}}` a `{{PAQUETE_3_PRECIO}}`, `{{NUM_EMPRESAS}}`, `{{CATEGORIA_1}}` a `{{CATEGORIA_5}}`, `{{MARCA_1}}` a `{{MARCA_14}}`

## Fórmula del embudo (para referencia rápida)

```
META_MENSUAL ÷ PRECIO_PROMEDIO = Deals necesarios
Deals × 2 = Llamadas necesarias
Llamadas ÷ 0.4 = Respuestas necesarias
Respuestas ÷ 0.15 = Empresas a contactar
Empresas ÷ 4 semanas ÷ 5 días = DMs por día
```
