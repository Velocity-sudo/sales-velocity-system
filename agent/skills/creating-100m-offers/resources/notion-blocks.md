# Referencia de Bloques Notion API — Oferta $100M

Guía rápida para construir la página de oferta en Notion usando la API. Cada sección mapea a bloques específicos.

## Patrón General

Todas las páginas de oferta siguen esta secuencia de bloques:

```
callout (blue) → heading_1 → paragraphs → divider → heading_1 → ...
```

## Crear la Página

```json
{
  "parent": { "page_id": "[PAGE_ID_DEL_PROYECTO_DEL_CLIENTE]" },
  "icon": { "emoji": "🎯" },
  "properties": {
    "title": [{
      "text": { "content": "🎯 Oferta del Agente - [Nombre] ([Descripción])" }
    }]
  }
}
```

## Bloques por Sección

### Callout Header (Sistema)

```json
{
  "type": "callout",
  "callout": {
    "rich_text": [{
      "type": "text",
      "text": { "content": "Este documento fue generado por el Offer Architect Agent usando los frameworks de Alex Hormozi ($100M Offers, Money Models, Leads)." }
    }],
    "icon": { "type": "emoji", "emoji": "🤖" },
    "color": "blue_background"
  }
}
```

### Heading 1 (Secciones principales)

```json
{
  "type": "heading_1",
  "heading_1": {
    "rich_text": [{
      "text": { "content": "🎯 CONTEXTO DEL CLIENTE" }
    }]
  }
}
```

### Párrafo con Label Bold

```json
{
  "type": "paragraph",
  "paragraph": {
    "rich_text": [
      {
        "type": "text",
        "text": { "content": "Cliente: " },
        "annotations": { "bold": true }
      },
      {
        "type": "text",
        "text": { "content": "[Nombre del cliente]" }
      }
    ]
  }
}
```

### Quote (para copys, scripts, garantías)

```json
{
  "type": "quote",
  "quote": {
    "rich_text": [{
      "type": "text",
      "text": { "content": "Valor = (Dream Outcome × Probabilidad) / (Tiempo × Esfuerzo)" }
    }]
  }
}
```

### Heading 2 (Subsecciones)

```json
{
  "type": "heading_2",
  "heading_2": {
    "rich_text": [{
      "text": { "content": "↑ Dream Outcome (MAXIMIZAR)" }
    }]
  }
}
```

### Bullet List Item

```json
{
  "type": "bulleted_list_item",
  "bulleted_list_item": {
    "rich_text": [{
      "type": "text",
      "text": { "content": "[Elemento de la lista]" }
    }]
  }
}
```

### Numbered List Item (Stack de Bonos)

```json
{
  "type": "numbered_list_item",
  "numbered_list_item": {
    "rich_text": [
      {
        "type": "text",
        "text": { "content": "Nombre del Bono" },
        "annotations": { "bold": true }
      },
      {
        "type": "text",
        "text": { "content": " - Valor $X\n(Descripción del bono)" }
      }
    ]
  }
}
```

### Callout de Oferta (green_background)

```json
{
  "type": "callout",
  "callout": {
    "rich_text": [{
      "type": "text",
      "text": { "content": "\"Nombre de la Oferta Aquí\"" },
      "annotations": { "bold": true }
    }],
    "icon": { "type": "emoji", "emoji": "🤖" },
    "color": "green_background"
  }
}
```

### Divider (entre secciones)

```json
{
  "type": "divider",
  "divider": {}
}
```

### Callout Footer (yellow)

```json
{
  "type": "callout",
  "callout": {
    "rich_text": [
      {
        "type": "text",
        "text": { "content": "NOTA DEL SISTEMA: " },
        "annotations": { "bold": true }
      },
      {
        "type": "text",
        "text": { "content": "Esta oferta fue generada automáticamente basada en la información del cuestionario/transcripciones del cliente. Todos los elementos siguen los frameworks de $100M Offers de Alex Hormozi." }
      }
    ],
    "icon": { "type": "emoji", "emoji": "📝" },
    "color": "yellow_background"
  }
}
```

## Secuencia Completa de Bloques

1. `callout` (blue, 🤖) — Header del sistema
2. `heading_1` — 🎯 CONTEXTO DEL CLIENTE
3. `paragraph` × 7 — Datos del cliente (bold label + valor)
4. `divider`
5. `heading_1` — 💰 VALUE EQUATION APLICADA
6. `quote` — Fórmula
7. `heading_2` + `paragraph` — ↑ Dream Outcome
8. `heading_2` + `bulleted_list_item` × N — ↑ Probabilidad Percibida
9. `heading_2` + `bulleted_list_item` × N — ↓ Tiempo de Espera
10. `heading_2` + `bulleted_list_item` × N — ↓ Esfuerzo y Sacrificio
11. `divider`
12. `heading_1` — 🏆 GRAND SLAM OFFER
13. `heading_2` + contenido — Nicho Específico
14. `heading_2` + `quote` — Promesa Central
15. `heading_2` + `callout` (green) — Nombre (MAGIC)
16. `heading_2` + `paragraph` + `quote` — Garantía
17. `heading_2` + `numbered_list_item` × 5 — Stack de Bonos
18. `heading_2` + `quote` — Precio y Anclaje
19. `divider`
20. `heading_1` — 📝 ONE-LINER
21. `callout` (green) — El one-liner
22. `divider`
23. `heading_1` — 📱 BIO PARA REDES SOCIALES
24. `heading_2` + `quote` — Instagram
25. `heading_2` + `quote` — LinkedIn
26. `heading_2` + `quote` — Twitter/X
27. `divider`
28. `heading_1` — 🌐 SECCIÓN LANDING PAGE
29. `heading_2` + `callout` (blue) — Hero Headline
30. `heading_2` + `paragraph` — Subheadline
31. `heading_2` + `bulleted_list_item` × 5 — Bullets de Beneficios
32. `heading_2` + `callout` — CTA
33. `heading_2` + `quote` — Garantía Visual
34. `divider`
35. `heading_1` — 📣 OUTPUTS ADAPTADOS
36. `heading_2` + `quote` — Hook para Ads
37. `heading_2` + `quote` — Email de Seguimiento
38. `heading_2` + `quote` — Script de Cierre
39. `divider`
40. `callout` (yellow, 📝) — Footer del sistema
