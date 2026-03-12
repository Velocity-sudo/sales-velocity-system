---
description: Genera guiones virales teleprompter-ready dentro de las sub-páginas de ideas de contenido en Notion. Lee las ideas del Plan Maestro del cliente y escribe el guión listo para grabar.
---

# 🎬 Workflow: Guiones Virales (`/guiones-virales`)

Convierte las **sub-páginas de ideas de contenido** en **guiones completos listos para teleprompter**.

> **Fuente de ideas**: Busca PRIMERO en la página **"🔥 IDEAS DE CONTENIDO VIRAL - [Cliente]"** (generada por `/ideas-virales`). Si no existe, busca en el Plan Maestro del cliente como fallback.

---

## 📋 Requisitos Previos

Antes de iniciar, el Agente debe confirmar que tiene:

1. **Nombre del cliente** — Para buscar sus páginas en Notion.
2. **Página de Notion con las ideas** — Buscar en este orden de prioridad:
   - **OPCIÓN A (Preferida):** Página **"🔥 IDEAS DE CONTENIDO VIRAL - [Cliente]"** → child page del cliente, generada por `/ideas-virales`. Contiene sub-páginas por línea conversacional, cada una con sub-páginas de ideas que incluyen score de viralidad y estrategia.
   - **OPCIÓN B (Fallback):** Sección dentro del **Plan Maestro** que contiene sub-páginas de ideas (ej: "LÍNEA 1: ACCIONES Y BOLSA DE VALORES").
3. **Base de Conocimiento del cliente** — Para entender su tono, nicho, audiencia y nivel de expertise.

*(Si no existe ninguna fuente de ideas, sugerir al usuario ejecutar `/ideas-virales [Cliente]` primero para generar el banco de ideas.)*

---

## 🛠 Ejecución Paso a Paso

### 1. Cargar el skill de Contenido Viral

- Leer el skill completo: `~/.agent/skills/copy-viral/SKILL.md`
- Internalizar las metodologías: Victor Heras, Hormozi, Brendan Kane, Paddy Galloway
- Tener claros los frameworks de hooks, curiosity loops, y técnicas de retención

### 2. Investigar en NotebookLM (si disponible)

- Usar `mcp_notebooklm-mcp_notebook_query` con el notebook `99dcc172-3185-4ba7-b5ac-0b3eaf06ac25`
- Query sugerido: *"¿Cuáles son los mejores hooks y estructuras de retención para [TEMA] en el nicho de [NICHO]?"*
- Si NotebookLM no responde, proceder con la metodología del skill cargado

### 3. Identificar las sub-páginas de ideas en Notion

**Búsqueda en orden de prioridad:**

**3A. Buscar en "IDEAS DE CONTENIDO VIRAL" (Fuente preferida):**
- Listar child pages del cliente en `Procesos de Clientes`
- Si existe una página que contenga **"IDEAS DE CONTENIDO VIRAL"** en el título:
  - Listar sus child pages → serán las **líneas conversacionales** (ej: "📂 LÍNEA 1: ACCIONES Y BOLSA DE VALORES")
  - Dentro de cada línea, las child pages son las **ideas individuales** con título viral, score y estrategia
  - **Ventaja**: Cada idea ya tiene score de viralidad → priorizar las 🔴🔴🔴 (alto) primero
  - Obtener los `block_id` de las sub-páginas y listarlas con su score

**3B. Buscar en Plan Maestro (Fallback):**
- Si NO existe la página de IDEAS DE CONTENIDO VIRAL:
  - Buscar el **Plan Maestro** del cliente
  - Dentro, localizar la sección de contenido orgánico (ej: "2 - COMENZAR A GRABAR CONTENIDO ORGÁNICO")
  - Obtener los `block_id` de las sub-páginas de tipo `child_page` que representan las ideas

**3C. Sin ideas existentes:**
- Si no se encuentran ideas en ninguna fuente:
  - Informar al usuario: *"No encontré ideas de contenido para [Cliente]. ¿Quieres que ejecute `/ideas-virales [Cliente]` primero para generar el banco de ideas?"*
  - No continuar hasta tener ideas

- Listar las ideas encontradas y confirmar con el usuario cuáles quiere que se escriban (o todas)
- Si vienen del banco de IDEAS VIRALES, mostrar el score de viralidad para ayudar a priorizar

### 4. Para CADA sub-página de idea, escribir el guión

El Agente debe limpiar el contenido existente de la sub-página y escribir el siguiente formato:

#### Estructura del contenido en Notion:

```
📎 Ref: [referencia si existe — cuenta de IG, video viral, fuente]
📹 Formato: [Reel / Story / Directo a cámara — duración — estilo]

───────────────────── (divider)

🎣 HOOK                  ← etiqueta gris sutil (gray_background)

[2-3 frases máximo. Cortas. Detienen el scroll.]

💬 CONTEXTO              ← etiqueta gris sutil

[3-5 frases. Rompe creencia falsa. Abre curiosity loop.]

💎 VALOR                 ← etiqueta gris sutil

[El contenido principal. Datos, nombres, números.
 Frases cortas (máx 8-10 palabras).
 Cada párrafo separado = pausa de medio segundo.
 Palabras en MAYÚSCULAS = énfasis vocal.
 Información dosificada — de a poco, no de golpe.
 Datos que den ganas de GUARDAR y COMPARTIR.]

📣 CTA                   ← etiqueta gris sutil

[2-3 frases. Suave si viral / Directo si conversión.]
```

#### Reglas de escritura del guión:

- **NO poner H1 con el título** — El título de la página YA es el título del video
- Las etiquetas de sección (`🎣 HOOK`, `💬 CONTEXTO`, `💎 VALOR`, `📣 CTA`) van como **párrafos con fondo gris** (`gray_background`), **bold**, **italic**, **color gray** — sutiles, no interrumpen la lectura
- El guión se lee de CORRIDO como teleprompter
- Frases CORTAS — máximo 8-10 palabras por frase
- Cada `paragraph` block de Notion = una frase
- Párrafos vacíos entre secciones para respirar
- Datos numéricos y nombres propios en **bold**
- Palabras de énfasis en MAYÚSCULAS (no poner bold, solo mayúsculas en el texto)
- Sin emojis dentro del guión (solo en las etiquetas de sección)
- Sin instrucciones de edición ni notas de producción dentro del guión
- Usar curiosity loops: "Y el último es el que nadie te cuenta..."
- Incluir datos aspiracionales: "$500/mes → $500K en 20 años"
- Social proof: "Warren Buffett recomienda esto"

### 5. Formato de las etiquetas de sección en Notion API

Las etiquetas de sección deben crearse así en la API:

```json
{
  "type": "paragraph",
  "paragraph": {
    "color": "gray_background",
    "rich_text": [{
      "type": "text",
      "text": { "content": "🎣 HOOK" },
      "annotations": {
        "bold": true,
        "italic": true,
        "color": "gray"
      }
    }]
  }
}
```

### 6. Formato de la referencia y formato de grabación

Compactos, en gris, en la parte superior antes del divider:

```json
[
  {
    "type": "paragraph",
    "paragraph": {
      "rich_text": [
        { "type": "text", "text": { "content": "📎 Ref: " }, "annotations": { "bold": true, "color": "gray" } },
        { "type": "text", "text": { "content": "@cuenta — descripción de referencia" }, "annotations": { "italic": true, "color": "gray" } }
      ]
    }
  },
  {
    "type": "paragraph",
    "paragraph": {
      "rich_text": [
        { "type": "text", "text": { "content": "📹 Formato: " }, "annotations": { "bold": true, "color": "gray" } },
        { "type": "text", "text": { "content": "Reel — Directo a cámara — 45-60 seg" }, "annotations": { "color": "gray" } }
      ]
    }
  }
]
```

// turbo
### 7. Ejecución en lote

- Procesar las ideas una por una
- Para cada idea:
  1. Leer el título de la sub-página (es la idea del video)
  2. Borrar cualquier contenido existente dentro de la sub-página
  3. Generar el guión según la metodología del skill
  4. Escribir el contenido en la sub-página usando `mcp_notion-mcp-server_API-patch-block-children`
- Confirmar con el usuario cada 5 guiones (o al finalizar)

// turbo
### 8. Entrega de resultados

- Imprimir un resumen con la lista de guiones creados
- Incluir los links directos a cada sub-página en Notion
- Indicar cuántas sub-páginas faltan (si no se procesaron todas)

---

## 📊 Adaptaciones por Línea de Contenido

| Línea | Tono | Formato típico | CTA |
|---|---|---|---|
| **Acciones y Bolsa** | Experto, datos duros, confianza | Reel directo a cámara, 60-90s | Guarda / Comparte / Sígueme |
| **Economía Mundial** | Informativo, opinion de experto, urgencia sutil | Reel con datos de noticias, 60-120s | Sígueme para estar al día |
| **Finanzas Personales** | Cercano, práctico, aspiracional | Reel educativo, 60-90s | Guarda este video / Comparte |

### 🎚️ Duración dinámica (variedad obligatoria)

NO todos los guiones deben tener la misma duración, pero NINGUNO debe ser menor a 60 segundos. Un video corto no permite desarrollar bien la noticia, incluir datos concretos ni posicionar al experto.

**Rangos de duración:**
- **ESTÁNDAR** (60-75s): Noticias unidimensionales — un solo evento, una sola causa, un solo takeaway. Aún así debe tener contexto y datos.
- **DESARROLLADO** (75-90s): Noticias con contexto — hay que explicar el "por qué", conectar 2 eventos, dar una opinión más profunda. Incluir comparaciones históricas y cifras.
- **PROFUNDO** (90-120s): Noticias complejas — múltiples causas, impacto en varias regiones/sectores, requiere explicar mecanismos (cómo X causa Y causa Z), incluye pasos accionables y múltiples datos de soporte.

**Criterios de selección (la lógica para decidir):**

| Pregunta | Si la respuesta es SÍ → sube de nivel |
|---|---|
| ¿La noticia tiene UNA sola causa clara? | Si no → DESARROLLADO o PROFUNDO |
| ¿Necesito explicar el mecanismo (cómo funciona)? | Si sí → DESARROLLADO mínimo |
| ¿Afecta a más de una región/sector/tipo de inversionista? | Si sí → PROFUNDO |
| ¿Hay pasos accionables que el viewer puede tomar? | Si sí → PROFUNDO (para incluirlos) |
| ¿Hay datos/cifras comparativas que hacen la historia más fuerte? | Si sí → subir duración para incluir los datos |
| ¿El potencial viral es 🔴🔴🔴? | Si sí → darle más espacio, mínimo DESARROLLADO |

**Distribución sugerida en un lote de 10:**
- 3-4 guiones **ESTÁNDAR** (60-75s)
- 4-5 guiones **DESARROLLADO** (75-90s)
- 1-2 guiones **PROFUNDO** (90-120s)

Marcar la duración sugerida en la línea de `📹 Formato:` de cada guión.

### 📊 Regla de datos y cifras (OBLIGATORIO)

**SIEMPRE respaldar ideas con números concretos.** Los guiones financieros SIN datos son genéricos y pierden credibilidad. Esta regla aplica a TODOS los guiones, sin excepción.

**Qué incluir siempre que sea posible:**
- 💰 **Cifra actual:** "El oro tocó los $5,000 por onza"
- 📉 **Comparación histórica:** "Hace 10 años costaba $1,200"
- 📊 **Porcentaje de cambio:** "Subió un 316% en una década"
- ⏰ **Temporalidad:** "En los últimos 6 meses aumentó un 40%"
- 🏛️ **Contexto institucional:** "JP Morgan maneja $3.7 TRILLONES en activos"
- 👥 **Escala humana:** "Esto afecta a 330 millones de personas en EE.UU."

**Formato en el guión:** Los números van en el TEXTO del guión como se hablarían natural:
- ✅ "Pasó de mil doscientos a CINCO MIL dólares."
- ✅ "Eso es un aumento del 316 POR CIENTO."
- ❌ NO poner tablas ni bullet points con datos — todo narrado en conversación.

**Dónde investigar los datos:** Antes de redactar cada guión, usar `mcp_firecrawl_firecrawl_search` o fuentes de referencia para obtener cifras verificables y actualizadas. Si no hay datos disponibles, usar frases con rangos ("entre X y Y") en lugar de inventar.

---

## ⚠️ Lo que NO debe hacer el workflow

- ❌ No inventar datos financieros — usar fuentes reales o datos genéricos verificables
- ❌ No poner CTA de venta directa en contenido viral — solo engagement (guarda/comparte/sígueme)
- ❌ No escribir párrafos largos — cada frase es un bloque de párrafo separado
- ❌ No poner instrucciones de producción dentro del guión (ángulos de cámara, B-roll, etc.)
- ❌ No repetir el título del video como H1 dentro de la página
- ❌ No poner timestamps (0:00-0:03) — solo las etiquetas de sección sutiles
- ❌ No escribir guiones sin cifras/datos concretos — el contenido financiero SIN números es genérico
- ❌ No hacer guiones menores a 60 segundos — un video corto no permite desarrollar la noticia ni posicionar al experto
