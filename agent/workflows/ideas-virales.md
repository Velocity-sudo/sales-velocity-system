---
description: Genera un banco de ideas de contenido viral para un cliente. Crea 15 ideas por línea conversacional con título viral + estrategia de atención + score de viralidad. Output en Notion como child page del cliente. Alimenta al workflow /guiones-virales.
---

# 🔥 Workflow: Ideas Virales (`/ideas-virales`)

> **Activar con:** `/ideas-virales [nombre del cliente]`
> **Resultado:** Una página en Notion **"🔥 IDEAS DE CONTENIDO VIRAL - [Cliente]"** con 15 ideas por línea conversacional — cada una con título viral, estrategia de atención, y score de viralidad.
> **Downstream:** Las ideas generadas se convierten en guiones completos con `/guiones-virales`.

---

## FASE 0 — Prerrequisitos & Carga de Skills ⏱ ~2 min

// turbo
### 0.1 Cargar el Skill de Contenido Viral
- Leer: `~/.agent/skills/copy-viral/SKILL.md`
- Internalizar las metodologías: Víctor Heras (Regla 5/50, Convergencia Viral, Método On/Off), Hormozi (Tweet-to-Video), Brendan Kane (Hook Point, CTA al 75%), Paddy Galloway (CCN, Pre-producción > Producción), Chris Do, Russell Brunson, Dan Kennedy
- Tener claras las 9 categorías de títulos (ver Fase 3)

// turbo
### 0.2 Cargar el Skill de Notion
- Leer: `~/.agent/skills/managing-notion/SKILL.md`
- Tener claras las rutas canónicas y el protocolo de "Client Context First"

---

## FASE 1 — Context & Briefing ⏱ ~3 min

### 1.1 Localizar al Cliente en Notion

- Buscar en **Procesos de Clientes** (DB: `2f7e0f37-6c6d-81b6-9cba-df48640f2afe`)
- Obtener el `page_id` del cliente
- Si no se encuentra, preguntar al usuario

### 1.2 Leer el Plan Maestro del Cliente

- Listar child pages del cliente → buscar **"PLAN MAESTRO - [Cliente]"**
- Leer su contenido, especialmente:
  - **Sección CONTEXTO**: Nicho, audiencia, tono
  - **Sección ESTRATEGIA**: Diferencial del cliente, posicionamiento
  - **Sección de Contenido Orgánico**: Líneas conversacionales existentes
- Si el Plan Maestro tiene sub-páginas de contenido tipo "LÍNEA X: [TEMA]" → extraer como líneas conversacionales

### 1.3 Leer Deliverables Existentes (Contexto Profundo)

- **OFERTA 100M** del cliente (si existe) → entender promesa, mecanismo, avatar
- **VSL** del cliente (si existe) → entender argumentos de venta, terminología
- **Brand Manual** (si existe) → entender tono de voz

### 1.4 Confirmar Briefing con el Usuario

Presentar al usuario:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 BRIEFING DE IDEAS VIRALES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

👤 Cliente: [Nombre]
🎯 Nicho: [Extraído del Plan Maestro]
👥 Audiencia: [Extraído del Plan Maestro]
🎭 Tono: [Extraído del Plan Maestro / Brand Manual]

🔥 LÍNEAS CONVERSACIONALES DETECTADAS:
  1. [Línea 1 — ej: "Acciones y Bolsa de Valores"]
  2. [Línea 2 — ej: "Economía Mundial"]  
  3. [Línea 3 — ej: "Finanzas Personales"]
  
📱 Formato principal: Video corto (Reels/TikTok/Shorts)
📊 Ideas por línea: 15 (total: ~45)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
¿Confirmas? ¿Quieres ajustar alguna línea?
```

**Reglas:**
- Si el Plan Maestro tiene líneas conversacionales definidas → extraerlas y confirmar
- Si NO tiene → proponer 3 basadas en el nicho/oferta del cliente y preguntar
- Si tiene menos de 3 → proponer líneas adicionales que tengan alto potencial viral en el nicho
- Si el usuario quiere modificar alguna → ajustar antes de continuar
- **NUNCA avanzar sin confirmación del usuario**

---

## FASE 2 — Motor de Fuentes & Investigación ⏱ ~8 min

> **PRINCIPIO**: Las ideas NO salen del aire. Salen de fuentes reales, confiables, y de largo alcance. El workflow cruza 4 capas de investigación para garantizar ideas con sustancia.

### 2.1 CAPA 1 — NotebookLM: Metodología & Frameworks

**Notebook:** `99dcc172-3185-4ba7-b5ac-0b3eaf06ac25`

Ejecutar estas queries en secuencia:

**Query 1 — Fórmulas de Títulos:**
> "¿Cuáles son las mejores fórmulas de títulos virales para videos cortos en [NICHO]? Dame 15 fórmulas con ejemplos concretos. Incluye: curiosity gap, datos numéricos, contrarian hooks, revelaciones, y 'si hubieras...' según Víctor Heras y Brendan Kane."

**Query 2 — Temas Estrella:**
> "¿Cuáles son los temas estrella que SIEMPRE generan views y retención en el nicho de [NICHO]? ¿Qué categorías de contenido tienen la mayor probabilidad de viralizar? Dame temas concretos, no abstractos."

**Query 3 — Técnicas de Atención:**
> "¿Cuáles son las mejores técnicas para RETENER atención en los primeros 3 segundos de un video corto? Dame técnicas específicas de pattern interrupt y curiosity loops según Heras, Kane y Galloway."

---

### 2.2 CAPA 2 — Noticias Reales de Fuentes Confiables

Usar `mcp_firecrawl_firecrawl_search` y/o `mcp_firecrawl_firecrawl_scrape` para extraer noticias recientes y de alto impacto.

#### 📰 Fuentes Universales (para CUALQUIER nicho)

| Fuente | URL / Query | Qué aporta |
|---|---|---|
| **Google News** | `site:news.google.com "[NICHO]"` | Noticias agregadas, las más relevantes del momento |
| **Reuters** | `site:reuters.com "[TEMA]"` | Noticias internacionales de peso, datos verificados |
| **AP News** | `site:apnews.com "[TEMA]"` | Fuente global de referencia, cobertura amplia |
| **BBC Mundo** | `site:bbc.com/mundo "[TEMA]"` | Noticias en español, audiencia LATAM |
| **El País** | `site:elpais.com "[TEMA]"` | Periodismo de largo alcance, datos + opinión |
| **Reddit** | `site:reddit.com "[NICHO] viral OR trending"` | Pulse real de lo que la gente está discutiendo AHORA |
| **X/Twitter Trends** | `site:x.com "[NICHO]" trending OR viral` | Tendencias en tiempo real, debates calientes |

#### 💰 Fuentes por Nicho — FINANZAS / TRADING / INVERSIONES

| Fuente | URL / Query | Qué aporta |
|---|---|---|
| **Bloomberg** | `site:bloomberg.com "[TEMA]"` | Datos financieros de peso, mercados globales |
| **CNBC** | `site:cnbc.com "[TEMA]"` | Noticias de mercados, opiniones de Wall Street |
| **Financial Times** | `site:ft.com "[TEMA]"` | Análisis profundo, economía global |
| **MarketWatch** | `site:marketwatch.com "[TEMA]"` | Datos de mercado, acciones, tendencias |
| **Yahoo Finance** | `site:finance.yahoo.com "[TEMA]"` | Accesible, datos en tiempo real |
| **Investing.com** | `site:investing.com "[TEMA]"` | Datos técnicos, calendarios económicos |
| **Expansión (MX)** | `site:expansion.mx "[TEMA]"` | Economía y finanzas enfocada en LATAM |
| **El Economista** | `site:eleconomista.com.mx "[TEMA]"` | Noticias económicas México/LATAM |
| **CoinDesk** | `site:coindesk.com "[TEMA]"` | Si el nicho incluye crypto |
| **r/wallstreetbets** | `site:reddit.com/r/wallstreetbets` | Pulso de retail investors, memes financieros virales |
| **r/investing** | `site:reddit.com/r/investing` | Discusiones serias de inversión |

#### 💪 Fuentes por Nicho — FITNESS / SALUD / COACHING

| Fuente | URL / Query | Qué aporta |
|---|---|---|
| **PubMed / NIH** | `site:pubmed.ncbi.nlm.nih.gov "[TEMA]"` | Estudios científicos para respaldar claims |
| **Men's Health / Women's Health** | `site:menshealth.com OR womenshealth.com` | Tendencias fitness mainstream |
| **Healthline** | `site:healthline.com "[TEMA]"` | Contenido salud verificado, muy buscado |
| **r/fitness** | `site:reddit.com/r/fitness` | Debates reales de la comunidad |
| **Muscle & Fitness** | `site:muscleandfitness.com "[TEMA]"` | Contenido fitness aspiracional |

#### 🧠 Fuentes por Nicho — COACHING / DESARROLLO PERSONAL / NEGOCIOS

| Fuente | URL / Query | Qué aporta |
|---|---|---|
| **Harvard Business Review** | `site:hbr.org "[TEMA]"` | Autoridad en negocios, datos de estudios |
| **Inc. Magazine** | `site:inc.com "[TEMA]"` | Emprendimiento, startups, liderazgo |
| **Forbes** | `site:forbes.com "[TEMA]"` | Rankings, wealth, negocios globales |
| **Entrepreneur** | `site:entrepreneur.com "[TEMA]"` | Emprendimiento, marketing, monetización |
| **Psychology Today** | `site:psychologytoday.com "[TEMA]"` | Respaldo psicológico para coaching |
| **r/Entrepreneur** | `site:reddit.com/r/Entrepreneur` | Experiencias reales de founders |

#### 🎨 Fuentes por Nicho — BELLEZA / MODA / LIFESTYLE

| Fuente | URL / Query | Qué aporta |
|---|---|---|
| **Vogue** | `site:vogue.com "[TEMA]"` | Tendencias de moda y belleza |
| **Allure** | `site:allure.com "[TEMA]"` | Productos, skincare, beauty trends |
| **Glamour** | `site:glamour.com "[TEMA]"` | Lifestyle y tendencias |
| **r/SkincareAddiction** | `site:reddit.com/r/SkincareAddiction` | Productos virales, rutinas |

#### ⚖️ Fuentes por Nicho — LEGAL / IMPUESTOS / MIGRACIÓN

| Fuente | URL / Query | Qué aporta |
|---|---|---|
| **IRS News** | `site:irs.gov "[TEMA]"` | Cambios fiscales oficiales |
| **USCIS** | `site:uscis.gov "[TEMA]"` | Noticias de inmigración |
| **Nolo** | `site:nolo.com "[TEMA]"` | Legal explicado para el público general |
| **r/tax** | `site:reddit.com/r/tax` | Preguntas reales de contribuyentes |

**📋 Instrucciones de búsqueda:**
1. Seleccionar las 3-5 fuentes más relevantes según el nicho del cliente
2. Ejecutar `mcp_firecrawl_firecrawl_search` con las queries: `"[TEMA de línea conversacional] latest OR breaking OR trending"` + el `site:` de cada fuente
3. De cada resultado, extraer: **titular, dato clave, y ángulo** para convertir en idea viral
4. Las noticias de las últimas 72 horas tienen prioridad (newsjacking)
5. Las noticias con datos numéricos impactantes tienen prioridad (formato Dato Numérico)

---

### 2.3 CAPA 3 — Herramientas de Tendencias

Consultar estas herramientas para detectar qué temas están explotando AHORA:

| Herramienta | URL para Scrape/Search | Qué buscar |
|---|---|---|
| **TikTok Creative Center** | `https://ads.tiktok.com/business/creativecenter/inspiration/popular/hashtag/pc/en` | Hashtags trending del nicho, videos top |
| **Google Trends** | `mcp_firecrawl_firecrawl_search` → `"google trends [NICHO] [PAÍS]"` | Temas en ascenso, búsquedas breakout |
| **Exploding Topics** | `mcp_firecrawl_firecrawl_scrape` → `https://explodingtopics.com/topic/[TEMA]` | Temas pre-virales, tendencias emergentes |
| **Answer Socrates** | `mcp_firecrawl_firecrawl_scrape` → `https://answersocrates.com/q/[TEMA]` | Preguntas reales que la gente hace (People Also Ask) |
| **YouTube Trending** | `mcp_firecrawl_firecrawl_search` → `"[NICHO] youtube viral esta semana"` | Videos que están rompiendo en el nicho |

**📋 Instrucciones:**
1. Buscar trending hashtags en TikTok Creative Center para el nicho
2. Consultar Google Trends para las líneas conversacionales → obtener "Related Queries" y "Breakout" topics
3. Si hay un tema en Exploding Topics con crecimiento >100% → es idea candidata de alto score
4. Las preguntas de Answer Socrates/People Also Ask → ideas de formato Tutorial Express o Secreto/Revelación

---

### 2.4 CAPA 4 — Cuentas de Referencia Viral (Benchmark)

Scraper las cuentas más virales del nicho para ver **qué títulos y formatos están funcionando AHORA**.

#### 📱 Cómo buscar cuentas de referencia:
```
mcp_firecrawl_firecrawl_search → "mejores cuentas [NICHO] instagram tiktok viral [AÑO]"
mcp_firecrawl_firecrawl_search → "top [NICHO] creators tiktok reels viral"
mcp_firecrawl_firecrawl_search → "[NICHO] influencers más seguidos [PAÍS/LATAM]"
```

#### 💰 Cuentas de Referencia — FINANZAS / TRADING / INVERSIONES

| Cuenta | Plataforma | Por qué es referencia |
|---|---|---|
| **@morgarfinanzas** | TikTok/IG | Trading accesible, títulos numéricos, alto engagement LATAM |
| **@finanzasconluisdd** | TikTok | Rankings de inversiones, formato ranking/comparación |
| **@ignaciosancheztrading** | IG/TikTok | (Si es cliente, estudiar competencia directa) |
| **@humphreytalks** | TikTok | Finanzas en inglés, formato viral probado, datos impactantes |
| **@calltoinvest** | IG | Acciones, noticias de mercado, formato dato + opinión |
| **@margaritapasos** | TikTok | Mentoría y mentalidad de negocios, LATAM massive reach |
| **@wallstmemes** | IG/TikTok | Memes financieros, lenguaje retail investor |

#### 💪 Cuentas de Referencia — FITNESS / SALUD

| Cuenta | Plataforma | Por qué es referencia |
|---|---|---|
| **@charliejohnsonfitness** | IG | 500K+, fitness business coach, contenido de posicionamiento |
| **@jeffnippard** | YT/IG | Fitness basado en ciencia, datos + estudio |
| **@gennofit** | IG | "Anyone can do this" — formato replicable, accesible |
| **@doctorunmute** | TikTok | Médico + fitness, formato mito vs realidad |

#### 🧠 Cuentas de Referencia — COACHING / NEGOCIOS / DESARROLLO PERSONAL

| Cuenta | Plataforma | Por qué es referencia |
|---|---|---|
| **@garyvee** | Todas | El estándar de contenido de valor masivo |
| **@alexhormozi** | Todas | Negocios + offers + contenido educativo viral |
| **@dariodeoli** | TikTok | Emprendimiento joven, LATAM, confesión/personal |
| **@iman.gadzhi** | IG/YT | Agency + marca personal, Gen Z biz content |
| **@davemeltzer** | IG | Motivación empresarial, frases virales |

#### 🎨 Cuentas de Referencia — BELLEZA / LIFESTYLE

| Cuenta | Plataforma | Por qué es referencia |
|---|---|---|
| **@hylobeauty** | TikTok/IG | Skincare viral, formato "POV" + producto |
| **@doctorly** | TikTok | Dermatólogos + skincare, educativo + controversia |
| **@johannacueva_** | IG | (Si es cliente, estudiar posicionamiento personal) |

**📋 Instrucciones:**
1. Identificar 3-5 cuentas del nicho del cliente (usar las de arriba como punto de partida)
2. Buscar sus videos más recientes y/o más virales:
   ```
   mcp_firecrawl_firecrawl_search → "site:tiktok.com @[cuenta] viral"
   mcp_firecrawl_firecrawl_search → "[cuenta] viral reel instagram"
   ```
3. De cada video viral detectado, extraer: **título/hook + formato + tema**
4. NO copiar — ADAPTAR al estilo y nicho del cliente
5. Documentar la referencia en la idea: `📎 Ref: @cuenta — "[título del video similar]"`

---

### 2.5 Registro de Fuentes por Cliente

Al ejecutar el workflow, documentar qué fuentes se usaron para poder repetir y mejorar:

```
━━━━━━━━━━━━━━━━━━━━━
📡 FUENTES CONSULTADAS
━━━━━━━━━━━━━━━━━━━━━
📰 Noticias: [listar fuentes usadas]
📈 Tendencias: [herramientas consultadas]
📱 Cuentas benchmark: [listar cuentas escaneadas]
🧠 NotebookLM: Queries 1-3 ejecutados
━━━━━━━━━━━━━━━━━━━━━
```

**REGLA FUNDAMENTAL**: Las ideas NO se generan del vacío. Cada idea debe poder rastrearse a al menos UNA de estas fuentes:
- Una noticia real (newsjacking)
- Un trending topic verificado (dato numérico, tendencia)
- Un video viral de referencia (adaptación)
- Una fórmula del skill copy-viral (metodología)
- Un tema evergreen del nicho validado por NotebookLM

---

## FASE 3 — Generación de Ideas ⏱ ~10 min

### 3.1 Categorías de Títulos (Distribución para 15 ideas por línea)

| Categoría | Cantidad | Fórmula Base | Ejemplo |
|---|---|---|---|
| **🔢 Dato Numérico** | 3-4 | "[Número impactante] + contexto" | "El 94% de los day traders pierde dinero. El 6% hace esto." |
| **⏪ Si Hubieras...** | 2 | "Si hubieras hecho X hace Y, hoy tendrías Z" | "Si hubieras metido $500 en Bitcoin en 2019..." |
| **🔄 Contrarian** | 2 | "Por qué [creencia popular] está MAL" | "Deja de ahorrar dinero. En serio." |
| **🔓 Secreto/Revelación** | 2 | "Lo que X no quiere que sepas" | "Lo que los bancos NO te cuentan sobre tu cuenta de ahorros" |
| **📋 Lista/Ranking** | 2 | "3 [cosas] que [autoridad] hace y tú no" | "3 acciones que Buffett compró en silencio este mes" |
| **📰 Newsjacking** | 1-2 | "[Evento actual] + tu perspectiva" | "La Fed acaba de hacer algo que no hacía desde 2008" |
| **😤 Polémico** | 1-2 | "La verdad incómoda sobre X" | "Las crypto están muertas. Y aquí está la prueba." |
| **💬 Confesión/Personal** | 1 | "Cometí este error y perdí $X" | "Perdí $30,000 por no entender ESTO" |

### 3.2 Reglas de Generación

1. **TODOS los títulos deben pasar el Test 5/50 de Víctor Heras:**
   - ¿Un niño de 5 años entiende el concepto?
   - ¿Al menos 50 de 100 personas en la calle querrían verlo?

2. **Framework CCN de Paddy Galloway** — Cada idea debe atraer a:
   - **Core**: Fans fieles del nicho (profundidad)
   - **Casual**: Conocen el tema (relevancia)  
   - **New**: No saben nada (accesibilidad)

3. **Convergencia Viral de Heras** — Los mejores títulos viven en la intersección entre:
   - **NICHO** (específico del cliente) + **SECTOR GENERAL** (tema masivo que conecta con todos)
   - Ejemplo: "Trading" (nicho) + "Dinero" (masivo) = "Si hubieras invertido $100 hace 5 años..."

4. **Diversidad de formatos** — Indicar si la idea es mejor para:
   - 📱 Reel (30-60s)
   - 📑 Carrusel (7-10 slides)
   - 🎙 Directo a cámara (60-120s)

### 3.3 Score de Viralidad

Cada idea lleva un score basado en 3 criterios:

| Criterio | Peso | Pregunta |
|---|---|---|
| **Alcance** | 40% | ¿Cuánta gente FUERA del nicho querría ver esto? |
| **Conversación** | 35% | ¿Genera comentarios polarizados, opiniones, debate? |
| **Guardado/Compartido** | 25% | ¿Es tan útil/impactante que la gente lo guarda o lo envía? |

**Escala:**
- 🔴🔴🔴 **Alto** (8-10) → Potencial de romper burbuja del nicho. Grabar PRIMERO.
- 🟡🟡 **Medio** (5-7) → Muy sólido dentro del nicho. Contenido consistente.
- 🟢 **Bajo** (3-4) → Funcional pero predecible. Usar como relleno del calendario.

**REGLA: Apuntar a que al menos 60% de las ideas sean 🔴🔴🔴 o 🟡🟡. Si no, la idea no es lo suficientemente buena — descartarla y generar otra.**

---

## FASE 4 — Creación en Notion ⏱ ~10 min

### 4.1 Verificar si ya existe la página

- Listar child pages del cliente
- Buscar una que contenga **"IDEAS DE CONTENIDO VIRAL"** en el título
- Si existe → modo **ACTUALIZACIÓN** (agregar nuevas ideas sin borrar existentes)
- Si no existe → modo **CREACIÓN**

### 4.2 Crear la Página Principal (solo si es modo CREACIÓN)

Crear como **child page** del cliente:

```
Título: "🔥 IDEAS DE CONTENIDO VIRAL - [Cliente]"
Emoji: 🔥
```

Agregar metadata al inicio:
```
📌 Nicho: [Nicho del cliente]
📌 Audiencia: [Audiencia objetivo]
📌 Última actualización: [DD/MM/AAAA]
📌 Total ideas: [N]

──────── (divider)
```

### 4.3 Crear Sub-Páginas por Línea Conversacional

Para cada línea conversacional, crear una **child_page** dentro de la página de IDEAS:

```
Título: "📂 LÍNEA 1: [NOMBRE DE LA LÍNEA]"
```

Dentro, agregar un header con conteo:
```
Total ideas: 15 | 🔴 Alto: X | 🟡 Medio: Y | 🟢 Bajo: Z
──────── (divider)
```

### 4.4 Crear Cada Idea como Sub-Página

Cada idea es una **child_page** dentro de su línea conversacional:

**Título de la sub-página = El título viral**

Contenido dentro de la sub-página:

```
Bloques de Notion (usando API):

1. Párrafo con fondo de color (callout-style):
   "🎯 VIRALIDAD: 🔴🔴🔴 (9/10) | 📱 Formato: Reel 30-60s"
   → color: según score (red_background / yellow_background / green_background)

2. Divider

3. Heading 3: "🎯 ESTRATEGIA DE ATENCIÓN"

4. Párrafos (gray, italic) con:
   • Técnica: [Curiosity gap / Dato numérico / Contrarian / etc.]
   • Por qué funciona: [1-2 frases explicando la psicología]
   • Audiencia CCN: [Core: X / Casual: Y / New: Z]

5. Divider

6. Heading 3: "💡 DESARROLLO"

7. Párrafos con:
   • Ángulo: [Cómo abordar este tema]
   • Datos clave a incluir: [Cifras, nombres, referencias]
   • Conexión con audiencia: [Cómo esto toca al viewer]
   
8. Divider

9. Heading 3: "📣 CTA SUGERIDO"

10. Párrafo:
    • 🔴 Si viral: "[CTA suave]"
    • 🟢 Si conversión: "[CTA directo]"
```

### 4.5 Formato de Bloques en Notion API

**Score de viralidad (callout al inicio de cada idea):**
```json
{
  "type": "callout",
  "callout": {
    "rich_text": [{
      "type": "text",
      "text": { "content": "VIRALIDAD: 🔴🔴🔴 (9/10) | 📱 Formato: Reel 30-60s" },
      "annotations": { "bold": true }
    }],
    "icon": { "type": "emoji", "emoji": "🎯" },
    "color": "red_background"
  }
}
```

**Usar colores según score:**
- 🔴 Alto → `red_background`
- 🟡 Medio → `yellow_background`
- 🟢 Bajo → `green_background`

**Secciones internas:**
```json
{
  "type": "heading_3",
  "heading_3": {
    "rich_text": [{
      "type": "text",
      "text": { "content": "🎯 ESTRATEGIA DE ATENCIÓN" },
      "annotations": { "bold": true }
    }],
    "color": "default"
  }
}
```

---

## FASE 5 — Entrega & Resumen ⏱ ~2 min

### 5.1 Resumen al Usuario

Imprimir:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ IDEAS VIRALES GENERADAS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📂 LÍNEA 1: [NOMBRE]
   → 15 ideas | 🔴 X alto | 🟡 Y medio | 🟢 Z bajo
   → Top 3: 
     1. "[Título más viral]" (🔴 9/10)
     2. "[Segundo más viral]" (🔴 8/10)
     3. "[Tercero]" (🔴 8/10)

📂 LÍNEA 2: [NOMBRE]
   → 15 ideas | 🔴 X alto | 🟡 Y medio | 🟢 Z bajo
   → Top 3: [...]

📂 LÍNEA 3: [NOMBRE]
   → 15 ideas | 🔴 X alto | 🟡 Y medio | 🟢 Z bajo
   → Top 3: [...]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 Total: [N] ideas generadas
🔗 Notion: [Link a la página de IDEAS DE CONTENIDO VIRAL]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔜 SIGUIENTE PASO:
   Selecciona las ideas que quieras grabar y usa 
   /guiones-virales [Cliente] para generar los guiones completos.
```

### 5.2 Backup Local

Guardar un resumen en:
```
~/Desktop/Clientes/[Nombre del Cliente]/ideas_virales_[fecha].md
```

---

## 🔄 Modo Actualización (Re-ejecución)

Cuando se ejecuta `/ideas-virales [Cliente]` y la página ya existe:

1. **NO borrar ideas existentes**
2. Contar cuántas ideas hay actualmente por línea
3. Agregar 15 NUEVAS ideas por línea (evitando duplicados de títulos)
4. Actualizar metadata (fecha, conteo total)
5. Indicar en el resumen: "Ideas existentes: X | Nuevas: 15 | Total: X+15"

---

## 🔑 Reglas del Workflow

1. **SIEMPRE confirmar briefing con el usuario** antes de generar ideas
2. **SIEMPRE cargar el skill `copy-viral`** antes de generar — las ideas deben usar las metodologías
3. **NUNCA generar ideas genéricas** — cada idea debe pasar el Test 5/50 de Heras
4. **NUNCA avanzar sin las líneas conversacionales confirmadas**
5. **Los títulos son el 80% del éxito** — invertir más tiempo en el título que en el desarrollo
6. **Mínimo 60% de ideas deben ser 🔴🔴🔴 o 🟡🟡** — si no, la idea es débil
7. **Diversificar categorías** — no repetir la misma fórmula más de 4 veces por línea
8. **Si el cliente tiene menos de 3 líneas**, proponer líneas adicionales con alto potencial viral
9. **Re-ejecución es aditiva** — nunca borra ideas existentes, siempre agrega
10. **Guardar siempre backup local** en `~/Desktop/Clientes/[Cliente]/`

---

## 🔗 Workflows Relacionados

| Workflow | Relación |
|---|---|
| `/guiones-virales` | CONSUME las ideas generadas por este workflow → escribe guiones completos |
| `/viral-news` | Complementa con noticias diarias (N8N) → puede alimentar ideas de newsjacking |
| `/copy-viral` | Provee la metodología base (skill `copy-viral`) |

---

## 📎 Clientes Configurados

| Cliente | Líneas Conversacionales | Ideas Generadas | Status |
|---|---|---|---|
| — | — | — | — |
