---
description: Sales Velocity System workflow to create a personalized closing presentation deck and closer's guide. Combines expert techniques (Jeremy Miner, Alex Hormozi, Daniel G, Andy Elliott, Jordan Belfort, Dan Lok, Grant Cardone, Shelby Sapp) adapted to each client's industry and offer type via NotebookLM.
---

# 🎯 Workflow: Create Closing Deck (`/create-closing-deck`)

Este workflow genera una **presentación de cierre de ventas personalizada** y una **guía del closer** para llamadas de cierre, integrando técnicas de los mejores closers del mundo adaptadas a la industria y oferta del cliente.

## 📋 Requisitos Previos

Antes de iniciar, confirmar que el cliente tiene en Notion:
1. ✅ **Base de Conocimiento** (transcripciones, cuestionarios, info del negocio)
2. ✅ **Oferta 100M** (Grand Slam Offer) → Si no existe: ejecutar `/create-100m-offer` primero
3. ✅ **Manual de Marca** (colores, tipografía, tono) → Si no existe: ejecutar `/create-brand-manual` primero

---

## 🛠 Ejecución Paso a Paso

// turbo
0. **Consultar Notebook de Cierre en NotebookLM** 🧠
   - Utiliza `notebook_query` con el notebook ID `8105c0c8-94f4-4f72-8216-02fe7fb55964`
   - **Query 1:** Adaptar estructura de cierre a la industria del cliente:
     *"Dame la estructura de cierre ideal para un servicio de [INDUSTRIA]. Incluye: cómo abrir la llamada, las mejores preguntas NEPQ para este tipo de prospecto, cómo presentar la solución en 3 pilares, y las objeciones más comunes de esta industria con scripts específicos."*
   - **Query 2:** Adaptar pitch al tipo de oferta:
     *"¿Cuál es la mejor forma de presentar una oferta de [TIPO] a precio de $[RANGO]? ¿Cuántos pilares usar? ¿Qué social proof funciona mejor? ¿Cómo manejar el precio? ¿Qué garantía recomienda cada experto?"*
   - Guardar los insights para usarlos en pasos siguientes.

// turbo
1. **Lectura de Base de Conocimiento del Cliente**
   - Activar skill `managing-notion` → buscar el cliente en Procesos de Clientes.
   - Leer la página del cliente: transcripciones, cuestionarios, info del negocio.
   - Cruzar la info del cliente con las recomendaciones del notebook (paso 0).

// turbo
2. **Lectura de Oferta 100M**
   - Leer la child page OFERTA 100M del cliente en Notion.
   - Extraer: Avatar, problema principal, solución, mecanismo, garantía, pricing.
   - Mapear el tipo de oferta (high ticket, webinar, recurrente) a las recomendaciones del notebook.

// turbo
3. **Lectura de Manual de Marca**
   - Leer el Brand Manual del cliente (colores, tipografía, tono de voz, logo).
   - Extraer: paleta de colores HEX, fuentes, estilo visual, tono comunicacional.

4. **🛑 CHECKPOINT 1: Confirmación Pre-Creación**
   - Presentar al usuario un resumen completo con:
     1. Cliente, Industria/Nicho
     2. Avatar principal y Problema #1
     3. Solución/Servicio y Mecanismo
     4. Pricing y Garantía
     5. Identidad visual (colores, fuente, estilo)
     6. Insights del Notebook (técnicas recomendadas para esta industria)
     7. Preguntas NEPQ propuestas (8-10 personalizadas)
   - **ESPERAR APROBACIÓN antes de continuar.**
   - Si hay ajustes → aplicarlos y volver a presentar.

// turbo
5. **Generación de Entregables (Activando skill `creating-closing-deck`)**
   - Con el contexto confirmado + insights del notebook:
     - **Entregable 1: Guía del Closer** (HTML premium):
       - 6 fases de la llamada con scripts personalizados
       - Checklist pre-llamada
       - Tips de tonalidad y manejo de objeciones
       - Diseño con identidad visual del cliente
     - **Entregable 2: Slide Deck de Ventas** (HTML interactivo):
       - 10 slides (5 internos + 5 externos)
       - Contenido 100% personalizado a la oferta y avatar
       - Diseño premium alineado con brand manual

6. **🛑 CHECKPOINT 2: Revisión Post-Creación**
   - Presentar ambos entregables generados al usuario.
   - El usuario revisa contenido, diseño, scripts y preguntas.
   - Si hay ajustes → corregir antes de guardar.
   - Si está aprobado → proceder al paso final.

// turbo
7. **Guardado Local**
   - Crear el directorio si no existe: `mkdir -p ~/Desktop/Clientes/[Nombre del Cliente]/`
   - Guardar `guia_closer.html` y `closing_deck.html` en la carpeta del cliente.

8. **Creación de Página en Notion**
   - Activar skill `managing-notion` para interactuar con la API de Notion.
   - Buscar la página del cliente en Procesos de Clientes.
   - Crear sub-página nueva: `PRESENTACIÓN DE CIERRE — [Nombre del Cliente]`
   - Insertar contenido estructurado como bloques de Notion.

// turbo
9. **Deploy a GitHub Pages (si se requiere link compartible)**
   - Crear/actualizar repo en `Velocity-sudo/[client-slug]`
   - Push archivos HTML al repo
   - Actualizar `DELIVERABLES.md` con links públicos

10. **Entrega de Resultados (Handoff)**
    - Confirmar que todo está guardado exitosamente.
    - Proporcionar:
      - 📁 Enlace local a los archivos HTML
      - 📝 Enlace a la nueva página en Notion
      - 🌐 Link de GitHub Pages (si aplica)

---

## 📦 Entregables Finales

| Entregable | Formato | Ubicación |
|------------|---------|-----------|
| **Guía del Closer** | HTML premium (1-2 pags) | Local + Notion + GitHub Pages |
| **Slide Deck de Ventas** | HTML interactivo (10 slides) | Local + Notion + GitHub Pages |

## 🧠 Notebook de Referencia

**Sales Closing Mastery** — 59 fuentes de:
Jeremy Miner, Alex Hormozi, Daniel G, Andy Elliott, Jordan Belfort, Dan Lok, Grant Cardone, Shelby Sapp, Daniel Iles
