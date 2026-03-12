---
description: Crea un motor de noticias virales diario en N8N para cualquier cliente. Genera guiones para teleprompter listos para grabar.
---

# 📰 Workflow: Motor de Noticias Virales (N8N)

> **Activar con:** `/viral-news [nombre del cliente]`
> **Resultado:** Un workflow de N8N importable que cada mañana busca noticias del sector del cliente, las analiza con IA, genera guiones virales completos para teleprompter, y los envía por email.

---

## Fase 1 — Briefing del Cliente ⏱ ~5 min

**ANTES DE CREAR NADA, obtener esta información. SI FALTA ALGO, PREGUNTAR.**

```
📌 BRIEFING DE NOTICIAS VIRALES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

👤 Cliente: [Nombre]
🎯 Nicho: [Ej: Finanzas, Fitness, Real Estate, Coaching, Tech]
🔑 Keywords principales (5-10): [Ej: S&P 500, acciones, ETFs, inversiones]
🔑 Keywords de engagement (5-10): [Ej: Warren Buffett, market crash, Bitcoin]
🌐 Fuentes de noticias preferidas: [Ej: Yahoo Finance, Bloomberg, TechCrunch]
🗣 Tono: [Ej: Informativo con opinión, polémico, educativo]
👥 Público objetivo: [Ej: Personas 25-50 que quieren invertir]
📣 CTA destino: [Ej: Clase gratuita, link en bio, WhatsApp]
📧 Email de entrega: [Ej: marca@luchobranding.com]
⏰ Hora de envío: [Ej: 7:00 AM hora Colombia]
📅 Días: [Ej: Lunes a Viernes]
```

---

## Fase 2 — Generar el Workflow JSON ⏱ ~15 min

Usar como base el archivo de referencia:
```
/Users/niko/Desktop/AntiGravity /N8N - Viral news content /workflow-viral-news-ignacio.json
```

### Estructura del flujo N8N (8 nodos):

```
⏰ Schedule Trigger
    │
    ├──→ 📰 RSS Feed 1 (Google News — keywords del nicho)
    │                                                     ──→ 🔀 Merge
    └──→ 📰 RSS Feed 2 (Fuentes específicas del cliente)  ──→   │
                                                                 ▼
                                                          🧹 Code: Parse RSS + Prompt
                                                                 │
                                                          🤖 HTTP Request → OpenAI
                                                                 │
                                                          📋 Code: Formatear Email
                                                                 │
                                                          📧 Gmail / Email
```

### Configuración de cada nodo:

**1. ⏰ Schedule Trigger**
- Expresión cron según la hora del cliente (convertir a UTC)
- Ejemplo: 7AM Colombia = `0 12 * * 1-5` (12:00 UTC, Lun-Vie)

**2. 📰 RSS Feed 1 — Google News (keywords del nicho)**
- URL base: `https://news.google.com/rss/search?q=KEYWORDS+when%3A7d&hl=en&gl=US&ceid=US:en`
- Separar keywords con `+OR+`
- Frases exactas entre `%22` (comillas URL-encoded)
- Response format: `text`

**3. 📰 RSS Feed 2 — Fuentes específicas**
- URL base: `https://news.google.com/rss/search?q=site%3AFUENTE1+OR+site%3AFUENTE2+KEYWORDS+when%3A7d&hl=en&gl=US&ceid=US:en`
- Usar `site%3A` para filtrar por dominio

**4. 🔀 Merge**
- Mode: `append`

**5. 🧹 Code: Parse + Prompt**
- Parsea XML de ambas fuentes RSS
- Elimina duplicados
- Construye el request body de OpenAI con el prompt personalizado
- **VER FASE 3 para el prompt completo**

**6. 🤖 HTTP Request → OpenAI**
- Method: POST
- URL: `https://api.openai.com/v1/chat/completions`
- Authentication: None
- Headers: `Content-Type: application/json` + `Authorization: Bearer SK-API-KEY`
- Body: `{{ JSON.stringify($json) }}`
- Timeout: 120000ms
- **IMPORTANTE:** El usuario debe poner su propia API key

**7. 📋 Code: Formatear Email**
- Extrae `choices[0].message.content` de la respuesta
- Formatea con fecha y nombre del cliente

**8. 📧 Gmail**
- Destinatario: email del cliente/equipo
- Subject: `Contenido Viral — [Cliente] — [Fecha]`
- Body: contenido generado

---

## Fase 3 — El Prompt (CRÍTICO) ⏱ ~10 min

Este es el corazón del sistema. El prompt debe personalizarse para cada cliente pero SIEMPRE mantener estas reglas de formato de entrega:

### System Prompt (personalizar los campos entre [BRACKETS]):

```
Eres el ghostwriter de [NOMBRE DEL CLIENTE], un experto en [NICHO] que crea contenido viral e informativo en Instagram sobre [TEMA GENERAL].

ESTILO DE [NOMBRE]:
- SIEMPRE abre con un DATO NUMÉRICO IMPACTANTE. Nunca empieza con una pregunta ni con una frase genérica.
  Ejemplos de hooks correctos:
  "[Ejemplo 1 con dato del nicho]"
  "[Ejemplo 2 con dato del nicho]"
  "Si hubieras [acción relevante al nicho] hace [tiempo], hoy tendrías [resultado]."

- Siempre da su POSTURA/OPINIÓN con frases como:
  "En mi opinión, esto representa una oportunidad para..."
  "Si yo estuviera en esta situación, esto es lo que haría..."
  "[NOMBRE] siempre ha dicho que..."

- Usa la perspectiva de RESULTADO/IMPACTO PERSONAL:
  "Si hubieras [acción], hoy [resultado]."
  "Quien [hizo X] hace [tiempo], ahora [resultado]."

- Tono: [TONO DEL CLIENTE]. NO amarillista. NO alarmista. Informativo con opinión fundamentada.
- Idioma: ESPAÑOL. Traduce todo del inglés.

FORMATO — TELEPROMPTER LISTO PARA GRABAR:
Solo escribe las PALABRAS EXACTAS que [NOMBRE] va a decir frente a cámara.
Sin indicaciones de cámara. Sin "[corte a]". Sin notas de producción. Sin emojis en el guión. Solo texto hablado.

ESTRUCTURA (3 partes):

[HOOK]
Una o dos frases que ABREN con un número o dato impactante. Debe ser imposible no seguir escuchando.

[VALOR]
El cuerpo del guión. MÍNIMO 250 palabras. MÁXIMO 450. Aquí va todo el contenido:
- Explica la noticia con datos concretos: porcentajes, cifras, fechas, nombres.
- Pon la noticia en contexto: qué significa para la audiencia.
- Usa al menos UNA VEZ la perspectiva "si hubieras [acción]...".
- Da la opinión de [NOMBRE]: qué opina, qué recomienda, qué haría él.
- RITMO DE FRASES: alterna frases CORTAS (3-5 palabras) con frases MEDIANAS (8-12 palabras) y frases LARGAS (15-20 palabras). Esto es CLAVE para retención.
  Ejemplo del ritmo correcto:
  "El mercado cayó un 3 por ciento esta semana. Tres por ciento. Puede sonar poco. Pero si tienes 50 mil invertidos, perdiste mil quinientos en cinco días. Y la pregunta no es si va a seguir bajando. La pregunta es si estás preparado para aprovechar cuando rebote. Porque siempre rebota."
- El contenido debe dar GANAS de guardar y reenviar. Lleno de datos útiles y perspectiva que no encuentras en otro lado.

[CTA]
Cierre natural, no forzado. Invitar a [CTA DESTINO DEL CLIENTE].

REGLAS INQUEBRANTABLES:
1. Guión COMPLETO. No cortes. No resumas. Escribe CADA palabra.
2. Mínimo 250 palabras en VALOR.
3. SIEMPRE abre el HOOK con un número o cifra.
4. SIEMPRE da la postura/opinión de [NOMBRE].
5. SIEMPRE usa al menos una vez "si hubieras [acción]...".
6. Alterna frases cortas y largas para ritmo y retención.
7. Caption de Instagram: limpio, profesional, máximo 2 emojis. Hashtags al final.
8. Todo en ESPAÑOL.
```

### User Prompt:

```
NOTICIAS DE [SECTOR] DE LA ÚLTIMA SEMANA:

[NOTICIAS PARSEADAS DEL RSS]

---

Selecciona las 3 noticias con más IMPACTO para [AUDIENCIA].
Prioriza: [TEMAS PRIORITARIOS DEL CLIENTE].

Para CADA noticia entrega EXACTAMENTE esto:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
NOTICIA #[N]: [Título en español]
Fuente: [Medio original]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TÍTULOS (3 opciones — todos deben incluir un NÚMERO):
1. [Dato numérico directo]
2. [Perspectiva "si hubieras..."]
3. [Postura/opinión de NOMBRE]

GUIÓN COMPLETO PARA TELEPROMPTER:

[HOOK]
(Abre SIEMPRE con un número. 1-2 frases. Imposible no seguir escuchando.)

[VALOR]
(MÍNIMO 250 palabras. Datos, cifras, "si hubieras...", opinión. Frases cortas y largas alternadas. TODAS las palabras.)

[CTA]
(Cierre natural invitando a [CTA DESTINO].)

CAPTION INSTAGRAM:
(Profesional, limpio, máximo 2 emojis, 5-8 hashtags al final.)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

IMPORTANTE: Cada guión debe estar 100% COMPLETO. Mínimo 250 palabras en VALOR. No cortes NADA.
```

---

## Fase 4 — Formato de Entrega Esperado ⏱ (referencia)

Cada ejecución del workflow debe producir un email con EXACTAMENTE este formato por cada noticia:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
NOTICIA #1: [Título en Español]
Fuente: [Nombre del medio]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TÍTULOS (3 opciones):
1. "[Título con dato numérico]"
2. "[Título con perspectiva de resultado]"
3. "[Título con postura del cliente]"

GUIÓN COMPLETO PARA TELEPROMPTER:

[HOOK]
[Dato numérico impactante que abre el guión. 1-2 frases.
Ejemplo: "NVIDIA acaba de reportar ingresos por 22 mil millones de dólares.
Veintidós mil millones. En un solo trimestre."]

[VALOR]
[Cuerpo del guión — 250 a 450 palabras.
Todo el texto que el cliente va a decir frente a cámara.
Con datos, cifras, contexto, perspectiva "si hubieras invertido...",
y la opinión/postura del cliente.
Alternando frases cortas, medianas y largas para retención.
Sin indicaciones de cámara ni notas de producción.
Solo las palabras exactas a decir.]

[CTA]
[Cierre natural. Ejemplo: "Si quieres aprender a tomar mejores
decisiones con tu dinero, te dejo mi clase gratuita en el link de
mi bio. Y si este contenido te aportó, compártelo con alguien
que necesite escucharlo."]

CAPTION INSTAGRAM:
[Caption limpio, profesional, máximo 2 emojis.
Texto claro que resume el valor del reel.
5-8 hashtags relevantes al final.]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Se repite para Noticia #2 y #3]
```

**Características CLAVE del formato:**
- ❌ Sin emojis en los guiones (solo en caption, máx 2)
- ❌ Sin indicaciones de cámara ("[corte a B-roll]", "[cambio de ángulo]")
- ❌ Sin notas de producción dentro del guión
- ❌ Sin frases genéricas como hook ("¿Sabías que...?", "Hoy te quiero hablar de...")
- ✅ Hook SIEMPRE abre con un número/dato
- ✅ Perspectiva "si hubieras [acción], hoy [resultado]"
- ✅ Opinión/postura del cliente en cada guión
- ✅ Ritmo: frases cortas + medianas + largas alternadas
- ✅ Guiones de 250-450 palabras, COMPLETOS
- ✅ Listo para teleprompter — solo las palabras a decir

---

## Fase 5 — Generar y Entregar ⏱ ~10 min

1. **Generar el workflow JSON** usando el template de referencia, personalizando:
   - Keywords del RSS según el nicho del cliente
   - Fuentes de noticias del cliente
   - System prompt + User prompt con datos del cliente
   - Email de destino
   - Horario del cron

2. **Guardar el JSON** en la carpeta del cliente:
   ```
   /[CARPETA-DEL-CLIENTE]/workflow-viral-news-[nombre].json
   ```

3. **Entregar al usuario con instrucciones:**
   - Cómo importar en N8N
   - Cómo configurar API Key de OpenAI (header Authorization: Bearer sk-...)
   - Cómo configurar Gmail
   - Cómo hacer test manual
   - Cómo activar en producción

---

## Fase 6 — Configuración del Cliente en N8N ⏱ ~15 min

Guiar al usuario paso a paso:

```
SETUP EN N8N:
━━━━━━━━━━━━━
1. Importar: Menú ... → Import from File → seleccionar JSON
2. OpenAI:
   - Nodo 🤖 → Authentication: None
   - Headers → Authorization: Bearer sk-proj-TU-KEY
   - Headers → Content-Type: application/json
3. Gmail:
   - Nodo 📧 → Crear credencial Gmail OAuth2
   - Autorizar cuenta de Google
4. Test: Botón "Test Workflow" → verificar email
5. Activar: Toggle Active → ON
```

---

## 🔑 Reglas del Workflow

1. **SIEMPRE hacer el briefing completo** antes de generar el JSON
2. **SIEMPRE usar el formato de entrega exacto** definido en la Fase 4
3. **NUNCA poner la API key del usuario en el JSON** — usar placeholder `SK-TU-API-KEY-AQUI`
4. **El prompt es el 80% del resultado** — invertir tiempo en personalizarlo bien para cada cliente
5. **Probar antes de entregar** — verificar que el flujo funciona con Test Workflow
6. **Archivo de referencia base:** `/Users/niko/Desktop/AntiGravity /N8N - Viral news content /workflow-viral-news-ignacio.json`

---

## 📎 Clientes Configurados

| Cliente | Nicho | Archivo | Status |
|---|---|---|---|
| Ignacio Sánchez | Finanzas / Inversiones | `workflow-viral-news-ignacio.json` | ✅ Activo |
