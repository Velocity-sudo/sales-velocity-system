---
name: Skool Manager
description: Skill para diseñar, lanzar, estructurar y monetizar comunidades Skool para clientes de marca personal / coaching / network marketing.
---

# Skool Manager — Monetización de Marca via Comunidad

> **Objetivo:** Ayudar a clientes a crear, estructurar y monetizar una comunidad Skool desde cero. Generar un plan completo listo para ejecutar.

## Knowledge Base

Este skill se alimenta del notebook de NotebookLM **"Skool Growth & Monetization 2026"** (ID: `abf0e307-c1ea-419b-8d65-1dbb3ee29031`), con **37 fuentes** (23 videos + 14 artículos/guías).

Siempre consultar el notebook antes de generar outputs para obtener datos actualizados.

---

## Archivos Incluidos

| Archivo | Propósito |
|---------|-----------|
| `templates/TEMPLATE_COMMUNITY_BLUEPRINT.md` | Blueprint completo de la comunidad: estructura, canales, classroom, gamificación, Auto-DMs |
| `templates/TEMPLATE_LAUNCH_PLAN.md` | Plan de lanzamiento de 30 días con fases, contenido diario, métricas y DM scripts |
| `templates/TEMPLATE_MONETIZATION_STRATEGY.md` | Estrategia de monetización con 10 modelos, pricing, funnels y matemática de ventas |

---

## Cómo Usar

### Paso 1: Copiar templates al proyecto del cliente

```bash
cp -r ~/.agent/skills/skool-manager/templates/ /path/to/client/skool/
```

### Paso 2: Recopilar información del cliente

Antes de llenar los templates, recopilar estos datos:

#### Datos del Cliente
| Variable | Descripción | Ejemplo |
|----------|-------------|---------|
| `{{NOMBRE_CLIENTE}}` | Nombre completo | Antonio Martínez |
| `{{NICHO}}` | Nicho/industria | Network Marketing |
| `{{PROBLEMA_PRINCIPAL}}` | Problema #1 que resuelve | "No sé cómo monetizar mi marca personal" |
| `{{RESULTADO_PRINCIPAL}}` | Resultado que promete | "Tu primer $5K/mes con tu comunidad" |
| `{{NOMBRE_COMUNIDAD}}` | Nombre de la comunidad Skool | Rock Star Academy |
| `{{PRECIO_MENSUAL}}` | Precio tier pagado | $97/mes |
| `{{PRECIO_ANUAL}}` | Precio anual (si aplica) | $797/año |
| `{{LEAD_MAGNET}}` | Recurso gratuito de entrada | "Checklist: 5 Pasos Para Lanzar Tu Skool" |
| `{{URL_SKOOL}}` | URL de la comunidad | skool.com/rockstar-academy |
| `{{REDES_SOCIALES}}` | Canales de tráfico principales | Instagram, YouTube, TikTok |

### Paso 3: Consultar NotebookLM

Antes de llenar los templates, hacer estas consultas al notebook:

1. **Monetización:** "¿Cuáles son las mejores estrategias de monetización para una comunidad de [NICHO]?"
2. **Estructura:** "¿Cuál es la estructura ideal de comunidad Skool para [NICHO]?"
3. **Growth:** "¿Cómo crecer de 0 a 1000 miembros en [NICHO] sin audiencia previa?"

### Paso 4: Generar outputs

Una vez llenas las plantillas:

1. **Community Blueprint** (`COMMUNITY_BLUEPRINT.md`): Llenar todas las `{{VARIABLES}}` con la info del cliente
2. **Launch Plan** (`LAUNCH_PLAN.md`): Personalizar el plan de 30 días
3. **Monetization Strategy** (`MONETIZATION_STRATEGY.md`): Seleccionar los modelos relevantes al nicho del cliente

---

## 📊 Top 10 Modelos de Monetización (Referencia Rápida)

| # | Modelo | Precio | Conversión | Revenue Potencial |
|---|--------|--------|------------|-------------------|
| 1 | Paid Challenge (5-21 días) | $97-$197 | 70-80% completación, 1:6 → high-ticket | $36K/cohorte |
| 2 | Course Bundle Reframe | $400/año | 9% upgrade de free | $9K→$30K/mes |
| 3 | Self-Liquidating Offer (SLO) | $17-$29/año | CAC = $0 (ads se pagan solos) | ∞ backend |
| 4 | Pin Post Rental | $250-$500/slot | N/A | Revenue pasivo |
| 5 | B2C → B2B Pivot | $208+/mes | Alto LTV | $335K/mes (caso real) |
| 6 | Reverse Ladder (High-Ticket First) | $2K-$5K one-time | Pequeño grupo | $20K/mes en 18 días |
| 7 | Internal Affiliate Army | 30-50% comisión recurrente | Viral | $600-$900/mes pasivo |
| 8 | 7/11/4 Trust Flow | N/A (framework) | 8.3% free→paid | $3K/mes (60 días) |
| 9 | Micro-Upsells "Buy Now" | $9-$27 one-time | Alta en free groups | Identificar buyers |
| 10 | Free-to-Paid Fishbowl | $97-$297/mes | 24% join rate | Escalable |

---

## 🏗️ Estructura de Comunidad Skool (Referencia)

### Canales Recomendados
1. **📢 Announcements** (Admin Only) — Updates, replays, noticias
2. **👋 Start Here / Introductions** — Presentaciones de nuevos miembros
3. **💬 General Discussion** — Preguntas y conversación principal
4. **🏆 Wins** — Logros y resultados de miembros
5. **📚 Resources / FAQ** — Material de apoyo y preguntas frecuentes

### Classroom (Curso "Start Here")
| Módulo | Contenido | Objetivo |
|--------|-----------|----------|
| 1 | Misión y Bienvenida | Video + cultura/expectativas |
| 2 | Gamificación Explicada | Cómo funciona puntos → rewards |
| 3 | Preséntate | Template de intro → canal Introductions |
| 4 | Setup App + Pin | Descargar app Skool + pin community |
| 5 | Tu Primer Win | CTA → booking call / lead magnet / curso pagado |

### Gamificación (Niveles)
| Level | Nombre Ejemplo | Unlock |
|-------|---------------|--------|
| 1 | Rookie / Nuevo | Start Here course |
| 2 | Player / Activo | Chat DMs + posting |
| 3 | Starter / Avanzado | Masterclass bonus |
| 4 | Pro / VIP | 1-on-1 call access |
| 5+ | Legend / Elite | Archived calls + exclusives |

### Auto-DM Script
```
"Hey {{NOMBRE}}, ¡bienvenido/a a {{NOMBRE_COMUNIDAD}}! 🎉

Pregunta rápida: ¿cuál es el resultado #1 que buscas con {{NICHO}}?

Mientras tanto → Ve a Classroom → 'Start Here' y completa la Lección 1 hoy.

¡Nos vemos adentro! 💪"
```

### 3 Pinned Posts Estratégicos
1. **TOP:** "¡Bienvenido! Empieza aquí →" (link a Start Here course)
2. **MIDDLE:** "¿Dónde estás hoy?" (Poll: Principiante / Intermedio / Avanzado)
3. **BOTTOM:** "Agenda tu llamada de estrategia GRATIS" (CTA a agendar)

---

## 📆 Plan de Contenido Semanal (Referencia)

| Día | Tipo de Contenido | Propósito |
|-----|-------------------|-----------|
| Lun | Challenge / Mini-tarea | Acción inmediata |
| Mar | Poll / Encuesta | Engagement bajo fricción |
| Mié | Highlight de Wins | Prueba social |
| Jue | Value Post / Framework | Enseñanza |
| Vie | Recurso / Throwback | Resurface contenido valioso |
| Sáb | Community Ritual | Conexión personal |

---

## 🎯 DM Scripts de Conversión

### Script 1: Auto-DM (Welcome)
> "Hey {{NOMBRE}}, ¡bienvenido/a! ¿Cuál es tu reto #1 con {{NICHO}}? Ve a Classroom → Start Here para empezar hoy."

### Script 2: Poll Follow-Up
> "Hey {{NOMBRE}}, vi que votaste que estás batallando con [Problema X]. Tengo un recurso sobre eso, ¿te lo mando?"

### Script 3: Hand Raiser (Pre-venta)
> Post: "Estoy pensando en crear un workshop de [Tema]. ¿Quién le entra?"
> DM: "Hey {{NOMBRE}}, vi que te interesa [Tema]. ¿Lo quieres para [Razón A] o [Razón B]?"

---

## 🔗 Referencia de Clientes Completados

| Cliente | Nicho | Comunidad | Precio | Status |
|---------|-------|-----------|--------|--------|
| *Ninguno aún* | — | — | — | — |

---

## Quick Formula: Free → Paid Funnel

```
Lead Magnet (Checklist/SOP)
    ↓ "Descarga gratis en mi comunidad"
Comunidad FREE (Skool)
    ↓ Auto-DM + Start Here + 7/11/4 Trust Flow
    ↓ Polls + Loom videos + Wins
Paid Tier ($97-$297/mes)
    ↓ Desbloquear cursos avanzados + calls 1-on-1
    ↓ Challenge pagado ($97-$197)
High-Ticket ($2K-$5K)
    ↓ Coaching grupal / Bootcamp / Done-for-you
Affiliate Army (30-50% recurring)
    → Tus miembros reclutan nuevos miembros
```
