---
name: creating-closing-deck
description: Gold Standard skill for creating premium Sales Closing Decks and Closer Guides. Implements the 6-stage sales process as the universal framework for all high-ticket closing materials.
---

# 🎯 Skill: Creating Closing Deck & Closer Guide

Este es el **estándar dorado** para generar materiales de cierre de ventas. Todo deck y guía que se cree debe seguir esta estructura de **6 etapas** sin excepción.

---

## 📐 Las 6 Etapas del Proceso de Venta (OBLIGATORIAS)

Cada guía de closer y deck de ventas DEBE seguir estas 6 etapas en este orden exacto:

| # | Etapa | Objetivo | Tiempo Ref. | Quién Habla |
|---|-------|----------|-------------|-------------|
| **1** | **Romper el Hielo** | Usar respuestas del formulario + confirmar tomador de decisión | 0–8 min | Closer |
| **2** | **Encontrar el Problema** | Guiar al prospecto a que ÉL encuentre su problema real | 8–18 min | Prospecto (80%) |
| **3** | **Pre-cierre** | "¿Tiene sentido escuchar cómo?" → SÍ → Abrir Deck | 18–22 min | Closer |
| **4** | **El Vehículo (DECK)** | Abrir el deck. Autoridad, casos de éxito, sistema, números | 22–36 min | Closer + Deck |
| **5** | **Pre-cierre del Cierre** | "¿Te hace sentido?" → Confirmar ANTES de ir al precio | 36–38 min | Closer |
| **6** | **Cierre** | Precio, compromiso, garantía. 3 resultados posibles. | 38–50 min | Closer |

### ⚠️ Reglas Críticas del Proceso:
- **NO se salta ninguna etapa.** Si el prospecto no confirma en una etapa, no avanzas.
- **Etapa 1 SIEMPRE inicia con el formulario.** Las respuestas del formulario del cliente son la apertura.
- **Etapa 3 es la puerta al deck.** Sin SÍ lógico, NO se abre el deck.
- **Etapa 5 es el check de temperatura.** Confirma que entiende el valor ANTES de hablar de precio.
- **Etapa 6 usa cierre asumido.** NUNCA preguntar "¿qué opinas?" — siempre asumir la venta y preguntar sobre el siguiente paso.

---

## 📦 Entregable 1: Guía del Closer (HTML Premium)

### Estructura Obligatoria

```
1. Top Bar (logo del cliente + badge "Confidencial")
2. Tabs de Navegación (scrollable, sticky):
   📋 Resumen | 1 · [Etapa 1] | 2 · [Etapa 2] | 3 · [Etapa 3] | 4 · [Etapa 4] | 5 · [Etapa 5] | 6 · [Etapa 6] | ⚡ Objeciones | ✅ Resultados
3. Hero / Overview:
   - Título: "Proceso de Venta"
   - Subtítulo: "6 etapas. Sigue el orden exacto."
   - Grid de 6 cards interactivas (clickeables → navegan a la sección)
4. Vista Rápida "El Flujo Completo":
   - Tabla con las 6 fases, objetivo, y tiempo
   - Diagrama de flujo visual horizontal: 1 → 2 → 3 → 4 → 5 → 6
5. Secciones por cada Fase (1-6):
   - Phase Label ("Fase X")
   - Título + rango de tiempo
   - Scripts literales con formato especial (script-box)
   - Tips (tip-box), Warnings (warn-box)
   - Deck moment (en Fase 3: "AQUÍ ABRES EL DECK")
6. Sección de Objeciones:
   - Top 5-6 objeciones con scripts de respuesta
   - Notas sobre cuáles ya deberían estar resueltas si hiciste bien las fases
7. Sección de Resultados:
   - 3 únicos resultados: Cierre, Seguimiento con Fecha, No quiere
   - Script de seguimiento
   - Post-pago (secuencia de los primeros 7 días)
8. Footer
9. JavaScript de navegación entre tabs
```

### Elementos de UI Reutilizables

| Clase CSS | Uso |
|-----------|-----|
| `.script-box` | Scripts literales del closer (fondo semi-transparente, borde izquierdo accent) |
| `.tip-box` | Tips y momentos clave (fondo verde semi-transparente) |
| `.warn-box` | Warnings y errores comunes (fondo rojo semi-transparente) |
| `.deck-moment` | Momento de abrir/transicionar en el deck (borde naranja, ícono grande) |
| `.preclose-card` | Cards explicativas del pre-cierre (fondo especial) |
| `.form-fields` | Campos del formulario del cliente (para Etapa 1) |
| `.step-row` + `.step-num` | Preguntas numeradas paso a paso |
| `.overview-item` | Cards interactivas del overview (con `data-target`) |

### Reglas de Diseño

1. **Alternancia de fondos:** `section-dark` ↔ `section-light` entre secciones para ritmo visual.
   - Dark: fondo `#0A0E1A` o similar del brand
   - Light: fondo `#FFFFFF` con texto oscuro
2. **Tipografía:** Outfit (Google Fonts) — weights 200-800.
3. **Color accent:** del brand manual del cliente (ej. `#F27A30` para Victor Arroyo).
4. **Responsive:** Max 6 cols en desktop, 3 en tablet (1024px), 3 en mobile (768px) para overview grid.
5. **Navegación interactiva:** Tabs funcionales con JavaScript que muestran/ocultan secciones. Overview cards clickeables.

---

## 📦 Entregable 2: Slide Deck de Ventas (HTML Interactivo)

### Estructura de Slides (11 slides estándar)

| Slide | Contenido | Background | Propósito |
|-------|-----------|------------|-----------|
| **1** | Portada | bg-navy | Nombre, marca, tagline |
| **2** | Autoridad | bg-white | Stats reales, credenciales, experiencia |
| **3** | El Problema | bg-accent | Describir el problema (conectar con lo que dijo en Fase 2) |
| **4-5** | Casos de Éxito | bg-white / bg-gradient | Antes/después con ROI real, nombres, fotos |
| **6** | El Sistema | bg-dark | 3 pasos simplificados |
| **7** | La Fórmula | bg-navy | Cómo funciona el apalancamiento / mecanismo |
| **8** | Números Reales | bg-white | Tabla con datos verificables |
| **9** | 🔥 Oportunidades | bg-gradient | 2-3 propiedades/opciones disponibles HOY con desglose de números |
| **10** | Inversión | bg-dark | Pricing claro, qué incluye |
| **11** | CTA | bg-accent | Call to action con urgencia |

### Elementos Clave del Deck

1. **Slide 9 (Oportunidades)** — Es el slide más importante para aterrizar la venta:
   - Mostrar 2-3 opciones REALES disponibles ahora mismo
   - Cada opción con: precio de entrada, financiamiento, costo de construcción, valor de venta, ganancia estimada
   - Usar cards con diseño premium (`.opp-card`)
   - Conectar con el capital del prospecto

2. **Navegación del Deck:**
   - Flechas izquierda/derecha
   - Indicador de dots (puntos)
   - Contador de slides (ej. "3/11")
   - Keyboard arrows
   - Touch swipe en mobile

3. **Reglas de Diseño del Deck:**
   - Slides fullscreen (`100vh x 100vw`)
   - Transiciones suaves (`translateX` con cubic-bezier)
   - Alternancia entre `bg-dark`, `bg-white`, `bg-navy`, `bg-accent`, `bg-gradient`
   - Tipografía: Outfit con tamaños responsivos (`clamp()`)
   - Stats con números grandes y labels pequeños

---

## 🔗 Conexión Guía ↔ Deck

La guía y el deck están **íntimamente conectados**:

- **Fase 3 (Pre-cierre):** La guía indica "AQUÍ ABRES EL DECK DE VENTAS" con visual callout.
- **Fase 4 (Vehículo):** La guía contiene una tabla slide-por-slide con qué decir en cada uno.
- **Fase 5 (Pre-cierre del Cierre):** Transición del deck al cierre. Check de temperatura.
- **Fase 6 (Cierre):** Referencia a slides 10-11 del deck (Inversión + CTA).

---

## 🧠 Personalización por Cliente

### Inputs requeridos:
1. **Formulario del cliente:** Las preguntas que hace en su landing/funnel (para Fase 1)
2. **Oferta 100M:** Avatar, problema, solución, pricing, garantía
3. **Brand Manual:** Colores, tipografía, tono
4. **Casos de éxito reales:** Nombres, números, antes/después
5. **Oportunidades actuales:** Productos/servicios disponibles ahora con números reales
6. **NotebookLM insights:** Técnicas NEPQ adaptadas a la industria

### Adaptación por industria:
- **Real Estate:** Oportunidades = propiedades con desglose financiero
- **Coaching/Consultoría:** Oportunidades = slots disponibles + transformación
- **SaaS/Tech:** Oportunidades = planes con ROI calculado
- **Servicios profesionales:** Oportunidades = capacidad actual + resultados de clientes

---

## 📏 Checklist de Calidad

Antes de entregar, verificar:

### Guía del Closer:
- [ ] 6 etapas numeradas correctamente en: tabs, overview cards, tabla, flow, headers
- [ ] Scripts personalizados con datos reales del cliente
- [ ] Formulario del cliente integrado en Fase 1
- [ ] Tomador de decisión en Fase 1 (OBLIGATORIO)
- [ ] Deck moment en Fase 3
- [ ] Tabla slide-por-slide en Fase 4
- [ ] Pre-cierre del cierre en Fase 5 (check de temperatura)
- [ ] Cierre asumido en Fase 6 (NO "¿qué opinas?")
- [ ] Mínimo 5 objeciones con scripts
- [ ] 3 resultados posibles (Cierre, Seguimiento con Fecha, No)
- [ ] Post-pago secuence
- [ ] Tabs funcionan correctamente (JS)
- [ ] Overview cards clickeables
- [ ] Alternancia dark/light funcional
- [ ] Responsive en mobile
- [ ] Brand colors aplicados

### Deck de Ventas:
- [ ] 11 slides mínimo
- [ ] Slide de Autoridad con stats reales
- [ ] Slide de Oportunidades con 2-3 opciones con números
- [ ] Navegación funcional (flechas, dots, keyboard, touch)
- [ ] Alternancia de backgrounds
- [ ] Responsive
- [ ] Brand colors aplicados

---

## 🏗️ Ejemplo de Referencia (Gold Standard)

**Cliente:** Víctor Arroyo — Nexus Inmobiliario (Real Estate / Florida)
**Archivos:**
- `~/Desktop/Clientes/Victor Arroyo/guia_closer.html` — Guía del Closer completa
- `~/Desktop/Clientes/Victor Arroyo/closing_deck.html` — Deck de Ventas interactivo
- **GitHub Pages:** `https://velocity-sudo.github.io/victor-arroyo/`

Estos archivos son la referencia a seguir para todos los futuros clientes.
