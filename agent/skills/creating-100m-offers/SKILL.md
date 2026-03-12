---
name: creating-100m-offers
description: Genera ofertas Grand Slam de $100M siguiendo la metodología de Alex Hormozi. Se activa cuando el usuario pide crear una oferta, diseñar una oferta 100M, aplicar Hormozi, o generar una Grand Slam Offer para un cliente. Requiere transcripciones de llamadas y/o cuestionarios como input.
---

# Offer Architect — Creador de Ofertas $100M

Skill que crea ofertas irresistibles siguiendo la metodología de Alex Hormozi ($100M Offers). Integra NotebookLM como cerebro de conocimiento y genera el documento final en Notion.

## When to Use This Skill

- "Crea una oferta de 100 millones para [cliente]"
- "Diseña una Grand Slam Offer"
- "Aplica la metodología Hormozi"
- "Genera una oferta para [cliente] con base en sus transcripciones"
- Cualquier solicitud que involucre crear/diseñar una oferta de alto valor

## Inputs Requeridos

Antes de empezar, SIEMPRE necesitas:

1. **Transcripciones de llamadas** del cliente (texto, Notion page, o archivo)
2. **Cuestionario inicial** del cliente (texto, Notion page, o datos directos)

> [!IMPORTANT]
> Si no tienes AMBOS inputs, pídelos al usuario. Sin esta información el output será genérico y no personalizado.

### Datos Clave a Extraer del Input

Del cuestionario y transcripciones, extraer:

| Dato | Pregunta Clave |
|------|---------------|
| **Nombre** | ¿Quién es el cliente? |
| **Industria** | ¿En qué sector opera? |
| **Servicio actual** | ¿Qué vende hoy? |
| **Avatar/Cliente ideal** | ¿A quién le vende? |
| **Problema principal** | ¿Qué dolor resuelve? |
| **Objetivo** | ¿Qué quiere lograr? |
| **Oferta actual** | ¿Cómo está empaquetado su servicio hoy? |
| **Precio actual** | ¿Cuánto cobra? |
| **Diferenciador** | ¿Qué lo hace único? |
| **Resultados** | ¿Qué resultados ha generado? |

## Workflow

```
[ ] 1. Validar permisos y acceso a Notion
[ ] 2. Recolectar datos del cliente (con fallback)
[ ] 3. Consultar NotebookLM (metodología Hormozi)
[ ] 4. Analizar y mapear datos al framework
[ ] 5. Generar la oferta completa
[ ] 6. Validar estructura de bloques
[ ] 7. Escribir documento en Notion (con retry)
[ ] 8. Verificar creación exitosa
[ ] 9. Notificar al usuario
```

> [!IMPORTANT]
> El workflow ahora incluye validaciones y manejo de errores en cada paso crítico para prevenir que el proceso se quede parado.

---

## Paso 0: Validar Permisos y Acceso

**CRÍTICO**: Antes de empezar, validar que tenemos acceso a Notion.

### Validar Parent Page con MCP

Usar la herramienta MCP para verificar acceso:

**Tool:** `mcp_notion-mcp-server_API-retrieve-a-page`

**Parámetros:**
```json
{
  "page_id": "[parent_page_id proporcionado por el usuario]"
}
```

### Manejo de Errores

**Si la llamada falla:**

- **Error 403 / Permission denied**: La integración no tiene acceso a la página
  - Usar `notify_user` para pedir al usuario que comparta la página con la integración de Notion
  - Mensaje: "No tengo permisos para acceder a esta página. Por favor comparte la página con la integración de Notion."
  
- **Error 404 / Not found**: El page_id no existe o es inválido
  - Usar `notify_user` para pedir un page_id válido
  - Mensaje: "La página con este ID no existe. Por favor verifica el page_id."

- **Timeout o error de red**: Problema temporal
  - Reintentar 1 vez después de 2 segundos
  - Si falla nuevamente, `notify_user`: "Error de conexión con Notion. Por favor intenta nuevamente."

**Si la llamada es exitosa:**
- Confirmar que tenemos acceso y continuar al Paso 1

---

## Paso 1: Recolectar Datos del Cliente

Obtener y leer las transcripciones y cuestionarios.

### 1.1 Leer la Página Principal del Cliente

**Tool:** `mcp_notion-mcp-server_API-retrieve-a-page`

**Parámetros:**
```json
{
  "page_id": "[client_page_id]"
}
```

**Output esperado:** Propiedades de la página (título, metadata, etc.)

### 1.2 Leer el Contenido de la Página

**Tool:** `mcp_notion-mcp-server_API-get-block-children`

**Parámetros:**
```json
{
  "block_id": "[client_page_id]",
  "page_size": 100
}
```

**Output esperado:** Array de bloques con el contenido de la página

### 1.3 Leer Páginas de Meetings/Transcripciones

Si la página tiene sub-páginas (meetings, transcripciones):

1. Identificar los IDs de las sub-páginas en los bloques
2. Para cada sub-página, repetir las llamadas de 1.1 y 1.2

### Error Handling con Graceful Degradation

**Si falla el acceso a Notion:**

1. **Primera opción**: Pedir al usuario que comparta las páginas
2. **Segunda opción**: Pedir al usuario que pegue el contenido directamente
3. **Tercera opción**: Proceder con datos parciales y marcar secciones como `[DATOS FALTANTES]`

**Llamada a notify_user si falla:**
```
"No puedo acceder a los datos en Notion. Opciones:
1. Comparte la página [page_id] con la integración de Notion
2. Pega el contenido de las transcripciones y cuestionario aquí
3. Procedo con datos parciales (marcará secciones incompletas)

¿Qué prefieres?"
```

Extraer los datos clave de la tabla anterior.

---

## Paso 2: Consultar NotebookLM

**Notebook ID:** `b0072d73-ee7b-459c-ac58-ccf50155e994`
**Nombre:** Oferta 100M - Grand Slam Offers (32 fuentes)

Hacer estas 3 queries al notebook para obtener la metodología:

### Query 1 — Framework Core
```
¿Cuáles son los pasos principales de la metodología de Alex Hormozi para crear una oferta de $100 millones? Incluye: cómo definir el nicho, la promesa, el mecanismo de entrega, la ecuación de valor, las garantías, los bonus, el naming y el one-liner.
```

### Query 2 — Ecuación de Valor + Garantías
```
Explica en detalle la Ecuación de Valor de Hormozi (Value Equation) con sus 4 palancas: Dream Outcome, Perceived Likelihood of Achievement, Time Delay, Effort & Sacrifice. Además, describe los 4 tipos de garantías (incondicional, condicional, anti-garantía, rendimiento) con ejemplos.
```

### Query 3 — Naming + Bonus Stacking
```
Explica la fórmula MAGIC de Hormozi para nombrar ofertas (Magnetic, Avatar, Goal, Interval, Container) y las mejores prácticas para crear un value stack con bonos. ¿Cómo se debe apilar valor para que la discrepancia precio-valor sea inmensa?
```

> [!TIP]
> No siempre necesitas hacer las 3 queries. Si ya tienes contexto de la metodología de una sesión previa, puedes omitir queries redundantes.

---

## Paso 3: Analizar y Mapear

Con los datos del cliente + la metodología de NotebookLM, construir:

1. **Nicho específico**: Cruzar el avatar del cliente con los 4 criterios de Hormozi (dolor masivo, poder adquisitivo, fácil de localizar, en crecimiento)
2. **Promesa (Dream Outcome)**: Articular la transformación que el avatar desea — EN PALABRAS SIMPLES
3. **Value Equation aplicada**: Llenar las 4 palancas con datos reales del cliente
4. **Problemas → Soluciones**: Listar obstáculos del avatar y convertirlos en soluciones entregables
5. **Guarantía**: Escoger el tipo más adecuado para el cliente
6. **Bonus stack**: Diseñar 3-5 bonos de bajo costo / alto valor percibido
7. **Naming atractivo**: Crear un nombre irresistible para la oferta (ver reglas de naming abajo)
8. **One-liner**: "Ayudo a [X] a lograr [Y] a través de [Z] sin [W]"

---

## Principios de Contenido (OBLIGATORIOS)

> [!IMPORTANT]
> Estos principios aplican a TODA la oferta. El documento final debe ser tan claro que cualquier persona — sin importar su nivel técnico — lo entienda en la primera lectura.

### 1. Lenguaje Simple y Directo

- **PROHIBIDO** usar tecnicismos de marketing, ventas o negocios (Revenue, ROI, KPI, funnel, pipeline, churn, LTV, CAC, etc.)
- **PROHIBIDO** usar anglicismos innecesarios cuando existe una palabra en español clara
- **SIEMPRE** escribir como si le explicaras a un amigo inteligente que NO sabe de marketing
- Usar frases cortas. Si una oración tiene más de 20 palabras, partirla en dos
- Preferir verbos concretos sobre sustantivos abstractos ("te ayudamos a vender más" > "optimización de conversiones")
- **ENFOQUE EN RESULTADOS ESPECÍFICOS Y CLAROS:** Evita usar términos poéticos o corporativos abstractos (Ej. "Construir tu patrimonio financiero"). Usa expectativas y promesas directas, numéricas y tangibles (Ej. "Ganar de 25% a 45% de rentabilidad garantizada invirtiendo de forma personalizada"). La sencillez extrema (estilo Hormozi) siempre gana.


**Ejemplos de corrección:**

| ❌ Tecnicismo | ✅ Lenguaje simple |
|---|---|
| "Optimizar tu pipeline de ventas" | "Conseguir más clientes que paguen" |
| "Incrementar tu LTV" | "Que cada cliente te compre más veces" |
| "Funnel de alta conversión" | "Un sistema que convierte visitantes en compradores" |
| "Mecanismo de entrega DFY" | "Nosotros lo hacemos todo por ti" |
| "Reducir tu CAC" | "Gastar menos para conseguir cada cliente" |
| "Escalar tu revenue" | "Aumentar tus ingresos" |

### 2. Oferta Irresistible

- La oferta debe sonar tan buena que el lector piense: "Sería tonto NO aceptar esto"
- Cada sección debe responder preguntas que el cliente ya tiene en su cabeza
- El valor percibido debe ser OBVIO — no requiere explicación
- Las garantías deben eliminar todo el riesgo del cliente
- Los precios deben crear un contraste claro: "esto vale $X, pero tú pagas $Y"

### 3. Naming Atractivo (Solo Interno)

> El nombre atractivo de la oferta es para USO INTERNO del sistema (headings, referencias). El cliente final ve descripciones simples.

**Reglas de naming:**
- Si el cliente ya tiene un nombre para su servicio → usarlo y hacerlo más atractivo sin complicarlo
- Si NO tiene nombre → crear uno que sea: corto (2-4 palabras), memorable, que evoque el resultado
- **NO** usar fórmulas complicadas tipo "MAGIC" — simplemente buscar un nombre que suene bien
- El nombre debe funcionar en una conversación casual: "¿Has oído del [Nombre]?"

**Buenos ejemplos:** "Método Hipoteca Fácil", "Sistema 30 Clientes", "Programa Ventas Sin Frío"
**Malos ejemplos:** "The Accelerated Revenue Maximizer 3.0", "Framework CLAVE de Monetización"

### 4. Desagregar Sin Complicar

- Cada sección debe desglosar la información en puntos específicos y concretos
- Usar bullets cortos (1 idea = 1 bullet)
- Cada bullet debe ser auto-contenido — se entiende sin leer los demás
- Incluir números y datos concretos siempre que sea posible
- Los resúmenes (bold+italic) deben capturar la esencia en UNA línea

**Ejemplo de desagregación correcta:**

```
✅ Bien:
• Conseguimos 15 clientes nuevos en 30 días
• Sin gastar en publicidad
• Solo con contenido orgánico en Instagram

❌ Mal:
• Implementación de estrategia multi-canal de adquisición orgánica 
  con optimización de contenido para maximizar el engagement 
  y la conversión en plataformas sociales
```

---

## Paso 4: Generar la Oferta Completa

Seguir la plantilla en `resources/offer-template.md` para generar cada sección. La oferta tiene **11 secciones obligatorias** (Gold Standard verificado contra la plantilla maestra).

### Secciones Obligatorias (Gold Standard)

| # | Sección | Color heading_1 |
|---|---------|------------------|
| 1 | **CONTEXTO** — Quién es, qué hace, situación actual | `default` |
| 2 | **A QUIÉN AYUDA** — Nicho, avatar, dolor, deseo | `yellow_background` |
| 3 | **A QUÉ LO AYUDA** — Resultado, promesa, transformación | `blue_background` |
| 4 | **CÓMO LO AYUDA** — Mecanismo, entregables, formato | `red_background` |
| 5 | **PRECIOS / ESCALERA DE VALOR** — Pricing, anclaje | `default` |
| 6 | **PRUEBA / CREDIBILIDAD** — Casos, testimonios, prueba social | `default` |
| 7 | **OFERTA (one liner)** — Fórmula "Ayudo a..." | `green_background` |
| 8 | **ECUACIÓN DE VALOR** — Las 4 palancas de Hormozi | `default` |
| 9 | **GATILLOS MENTALES Y GARANTÍAS** — Urgencia, escasez, garantía | `default` |
| 10 | **OFERTA IRRESISTIBLE (one liner)** — Promesa + mecanismo + garantía | `green_background` |
| 11 | **CÓMO COMUNICARLA (en cada canal)** — Redes, email, ads, landing, ventas 1:1 | `green_background` |

---

## Paso 5: Validar Estructura de Bloques

Antes de enviar a Notion, validar que todos los bloques tienen la estructura correcta.

### Validación de Bloques

```python
for block in blocks:
    try:
        NotionMCPHelper.validate_block_structure(block)
    except NotionValidationError as e:
        logger.error(f"Bloque inválido: {e}")
        # Corregir o notificar al usuario
```

### Checklist de Validación

- [ ] Cada bloque tiene campo `type`
- [ ] Cada bloque tiene campo con el nombre de su tipo
- [ ] Rich text arrays están formateados correctamente
- [ ] No hay campos vacíos requeridos
- [ ] Los emojis son válidos

---

## Paso 6: Escribir en Notion

Crear la página de oferta usando llamadas MCP directas.

### 6.1 Crear la Página

**Tool:** `mcp_notion-mcp-server_API-post-page`

**Parámetros:**
```json
{
  "parent": {
    "page_id": "[parent_page_id]"
  },
  "icon": {
    "emoji": "🎯"
  },
  "properties": {
    "title": [
      {
        "text": {
          "content": "🎯 Oferta del Agente - [Nombre del Cliente]"
        }
      }
    ]
  }
}
```

**Output esperado:** Objeto con `id` de la página creada

**Guardar el `page_id` para el siguiente paso.**

### 6.2 Añadir Contenido a la Página

**Tool:** `mcp_notion-mcp-server_API-patch-block-children`

**Parámetros:**
```json
{
  "block_id": "[page_id del paso 6.1]",
  "children": [
    // Array de bloques generados en Paso 4
  ]
}
```

**Bloques Permitidos (Gold Standard):**

> [!CAUTION]
> El template Gold Standard usa SOLO estos tipos de bloque. NO usar `callout`, `quote`, `heading_2`, `heading_3`, `numbered_list_item`, ni `code`.

- `heading_1` — Secciones principales (siempre `bold: true`, con color según tabla de secciones)
- `paragraph` — Contenido normal, bold (sub-labels), bold+italic (resúmenes), o vacío (separador)
- `bulleted_list_item` — Listas dentro de cada sub-sección
- `divider` — Separador entre secciones principales

**Referencia completa:** Ver `resources/offer-template.md`

### 6.3 Retry Manual

Si alguna llamada falla:

1. **Primer intento falla**: Esperar 2 segundos y reintentar
2. **Segundo intento falla**: Esperar 4 segundos y reintentar  
3. **Tercer intento falla**: Notificar al usuario con `notify_user`

### Manejo de Errores

**Error 403 (Permission Denied):**
```
notify_user(
  "❌ No tengo permisos para crear páginas en esta ubicación.",
  "Por favor verifica que la integración de Notion tenga acceso a la página padre."
)
```

**Error 400 (Validation Error):**
```
notify_user(
  "❌ Error de validación en los bloques de la oferta.",
  "Esto es un error del sistema. Por favor reporta este problema."
)
```

**Error 500/503 (Server Error):**
```
notify_user(
  "❌ Error temporal de Notion API.",
  "Por favor intenta nuevamente en unos minutos."
)
```

**Error de Timeout:**
```
notify_user(
  "❌ Timeout al conectar con Notion.",
  "Verifica tu conexión e intenta nuevamente."
)
```

---

## Paso 7: Verificar Creación Exitosa

Después de intentar crear la página, verificar que se creó correctamente.

### Checklist de Verificación

1. **Confirmar page_id válido**: El resultado debe tener un page_id
2. **Recuperar página creada**: Intentar `retrieve-a-page` para confirmar
3. **Verificar contenido**: Confirmar que los bloques se añadieron

```python
if page_id:
    try:
        # Verificar que la página existe
        created_page = safe_retrieve_page(mcp_client, page_id)
        logger.info(f"✅ Verificación exitosa: {page_id}")
    except Exception as e:
        logger.warning(f"⚠️ Página creada pero no se pudo verificar: {e}")
else:
    logger.error("❌ No se obtuvo page_id, la creación falló")
```

---

## Paso 8: Notificar al Usuario

Después de crear la página (exitoso o fallido), SIEMPRE notificar al usuario.

### Si fue exitoso:
```python
notify_user(
    f"✅ Oferta creada exitosamente para {client_name}",
    f"Link: https://notion.so/{page_id.replace('-', '')}",
    f"Resumen:",
    f"- Nombre: {offer_name}",
    f"- Nicho: {nicho}",
    f"- Promesa: {promesa}",
    f"- Garantía: {garantia}",
    "¿Quieres hacer ajustes?"
)
```

### Si falló:
```python
notify_user(
    f"❌ No se pudo crear la oferta para {client_name}",
    f"Error: {error_message}",
    "Opciones:",
    "1. Revisar permisos en Notion",
    "2. Intentar con otro page_id padre",
    "3. Proporcionar datos manualmente"
)
```

---

## Ejemplo de Referencia

La plantilla maestra (Gold Standard) de **Diego Páramo** es la referencia para esta skill:
- **Plantilla Maestra:** `303e0f37-6c6d-81f1-bf4b-eeb9c41ba021`
- **Ejemplo Generado (Christian Funes):** `304e0f37-6c6d-81cc-97d3-d37df9fd5eb0` (137 bloques, 11 secciones)
- **Estructura**: CONTEXTO → A QUIÉN AYUDA → A QUÉ LO AYUDA → CÓMO LO AYUDA → PRECIOS → PRUEBA → OFERTA → ECUACIÓN DE VALOR → GATILLOS → OFERTA IRRESISTIBLE → CÓMO COMUNICARLA

## Error Handling Best Practices

### 1. Fail Fast
- Validar inputs al inicio (page_id, datos del cliente)
- No continuar si falta información crítica

### 2. Preserve Context
- Loggear cada paso con contexto relevante
- Incluir detalles en excepciones (page_id, cliente, step)

### 3. Meaningful Messages
- Mensajes claros de error para el usuario
- Explicar qué salió mal Y cómo solucionarlo

### 4. Graceful Degradation
- Siempre tener un plan B (fallback)
- Pedir datos manualmente si Notion falla
- Crear oferta parcial si falta información

### 5. Don't Swallow Errors
- Nunca ignorar excepciones silenciosamente
- Loggear todos los errores
- Notificar al usuario cuando algo falle

## Resources

- [Plantilla de Oferta](resources/offer-template.md) — Estructura completa del documento
- [Bloques Notion](resources/notion-blocks.md) — Referencia de bloques API para construir la página

> [!NOTE]
> El archivo `notion_mcp_helper.py` existe en esta carpeta pero es **solo código de referencia stub**. No se ejecuta. Todas las llamadas a Notion deben hacerse con las herramientas MCP directamente según lo documentado en este SKILL.md.
