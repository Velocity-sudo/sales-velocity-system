# 🚀 PLAN DE EJECUCIÓN META ADS — JORGE VERGARA TAXES 2026

**Fecha:** 18 de Febrero 2026  
**Plataforma:** Meta Ads (Instagram + Facebook)  
**Servicio:** Preparación de Impuestos (Tax Prep)  
**Objetivo:** Sistema de adquisición pagado, medible y repetible  
**Landing Page:** GHL Funnel "Jorge Taxes 2026 - VSL"  
**Activos listos:** VSL A (15 min), VSL B (7 min), 3 Ads cortos

---

## 📊 RESUMEN EJECUTIVO

### El Sistema Completo

```
META ADS (Reels + Estáticos)
    ↓
LANDING PAGE en GHL (VSL + CTA)
    ↓
PÁGINA PUENTE /go/book (Tracking)
    ↓
CALENDARIO GHL (Agendamiento)
    ↓
AUTOMATIZACIÓN GHL (Confirmación + Recordatorio)
    ↓
CITA 1-a-1 CON JORGE (Cierre)
```

### Métricas Objetivo (90 días)

| Métrica | Meta |
|---------|------|
| Registros totales | 100 |
| Citas calificadas | 10+ |
| Primera venta | Semana 3-4 |
| CPL (Costo por Lead) | < $15 |
| Show Rate | > 60% |
| Tasa de cierre | > 20% |
| ROAS mínimo | 3x |

---

## 🏗️ PARTE 1: CONFIGURACIÓN EN GO HIGH LEVEL (Antes de lanzar ads)

### 1.1 Funnel en GHL

El funnel ya existe: **"Jorge Taxes 2026 - VSL"**

**Verificar que estén listos:**

- [ ] Landing page con VSL embebido (archivo `final_landing_page.html` en Custom HTML)
- [ ] Video VSL subido a YouTube/Vimeo/Wistia (URL embed reemplazada en `[VSL_EMBED_URL_AQUI]`)
- [ ] Logo/foto de Jorge subido a GHL Media
- [ ] Dominio conectado (ej: `asesoriajorge.com`)
- [ ] Página puente `/go/book` con redirect al calendario
- [ ] Calendario configurado con horarios disponibles de Jorge/Ana
- [ ] Sticky CTA funcionando en mobile

### 1.2 Pixel de Meta en GHL

**Configuración obligatoria antes de lanzar:**

1. **Instalar Meta Pixel** en GHL:
   - Ve a **Settings > Business Profile > Integrations > Facebook**
   - Conecta tu cuenta de Business Manager
   - Selecciona el Pixel ID correcto

2. **Meta Conversions API (CAPI)**:
   - En GHL: **Settings > Integrations > Facebook Conversions API**
   - Conectar para tracking server-side (indispensable para iOS 14+)
   - Esto duplica señales: Pixel (browser) + CAPI (server) = mejor data

3. **Eventos a configurar:**

| Evento Meta | Dónde se dispara | Propósito |
|-------------|------------------|-----------|
| `PageView` | Landing page (auto) | Medir tráfico total |
| `ViewContent` | Landing page (auto por Pixel) | Medir interés |
| `Lead` | Cuando agenda cita en calendario | Medir conversiones |
| `InitiateCheckout` | Página `/go/book` (opcional) | Medir clicks en CTA |
| `Schedule` | Confirmación de cita | Evento custom para optimizar |

4. **Verificar dominio:**
   - En Business Manager → **Brand Safety > Domains** → Verificar `asesoriajorge.com`
   - Agregar meta tag en GHL Settings > Custom Code > Head

5. **Configurar eventos agregados:**
   - En Events Manager → **Aggregated Event Measurement**
   - Priorizar: `Lead` > `ViewContent` > `PageView`

### 1.3 UTMs Estandarizados

**Estructura de UTMs para TODAS las campañas:**

```
https://asesoriajorge.com/impuestos?utm_source=facebook&utm_medium=paid&utm_campaign={{campaign.name}}&utm_content={{ad.name}}&utm_term={{adset.name}}
```

**Parámetros dinámicos de Meta:**

| Parámetro | Valor Dinámico Meta | Propósito |
|-----------|-------------------|-----------|
| `utm_source` | `facebook` o `instagram` | Plataforma |
| `utm_medium` | `paid` | Tipo de tráfico |
| `utm_campaign` | `{{campaign.name}}` | Nombre campaña |
| `utm_content` | `{{ad.name}}` | ID del anuncio específico |
| `utm_term` | `{{adset.name}}` | Nombre del ad set |

> **⚠️ IMPORTANTE:** El script en `final_landing_page.html` ya toma estos UTMs y los pasa al calendario cuando el usuario hace click en "Agendar". Esto permite trackear qué anuncio generó cada lead en GHL.

### 1.4 Automatizaciones GHL

**Workflow 1: Confirmación de Cita**
- **Trigger:** Appointment Scheduled
- **Acciones:**
  1. SMS inmediato: "¡Listo! Tu evaluación con Jorge está confirmada para [FECHA]. Guarda este mensaje."
  2. Email de confirmación con instrucciones (lugar tranquilo, documentos a tener a la mano)
  3. Tag: `meta-ads-lead`
  4. Tag por UTM: `campaign-[nombre_campaña]`

**Workflow 2: Recordatorio Pre-Cita**
- **Trigger:** 24 horas antes de la cita
- **Acciones:**
  1. SMS: "Mañana tienes tu evaluación fiscal con Jorge a las [HORA]. ¿Todo listo? Responde SÍ para confirmar."
  2. Si no confirma: SMS 2 horas antes como último recordatorio

**Workflow 3: No-Show Recovery**
- **Trigger:** Cita marcada como No-Show
- **Acciones:**
  1. SMS a los 30 min: "Vimos que no pudiste conectar. ¿Quieres reagendar? Usa este link: [CALENDAR_LINK]"
  2. Email con reagendamiento 24h después
  3. Tag: `no-show`

**Workflow 4: Lead Nurturing (No agendó)**
- **Trigger:** Contact visitó landing pero NO agendó (pixel event sin Lead event en 48h)
- **Acciones:**
  1. Email con value (guía PDF de deducciones comunes)
  2. SMS sutil 3 días después: "¿Tienes preguntas sobre tus impuestos? Responde aquí y te ayudo."

---

## 📢 PARTE 2: ESTRUCTURA DE CAMPAÑAS EN META ADS

### 2.1 Arquitectura de Campañas

Se organizan en **3 capas** (Cold → Warm → Hot):

```
🔵 CAPA 1: PROSPECTING (Tráfico Frío - 70% del presupuesto)
│
├── Campaña 1: "JV-TAXES-PROSPECTING-1099"
│   ├── Ad Set: Broad-1099-FL-TX-CA
│   ├── Ad Set: Interest-GigEconomy
│   └── Ads: 1 variante (Reel ángulo 1099)
│
├── Campaña 2: "JV-TAXES-PROSPECTING-W2"
│   ├── Ad Set: Broad-W2-Empleados
│   ├── Ad Set: Interest-Finance-W2
│   └── Ads: 1 variante (Reel ángulo W2)
│
└── Campaña 3: "JV-TAXES-PROSPECTING-EMPRESA"
    ├── Ad Set: Broad-Empresarios
    ├── Ad Set: Interest-SmallBiz
    └── Ads: 1 variante (Reel ángulo Empresas)

🟡 CAPA 2: RETARGETING WARM (20% del presupuesto)
│
└── Campaña 4: "JV-TAXES-RETARGET-WARM"
    ├── Ad Set: Video-Viewers-50%+ (últimos 30 días)
    ├── Ad Set: IG-Engagement (últimos 30 días)
    └── Ads: VSL teaser + Testimonios + Urgencia

🔴 CAPA 3: RETARGETING HOT (10% del presupuesto)
│
└── Campaña 5: "JV-TAXES-RETARGET-HOT"
    ├── Ad Set: Landing-Visitors-No-Lead (últimos 14 días)
    └── Ads: Oferta directa + Caso de éxito + Urgencia temporal
```

### 2.2 Configuración Detallada de Cada Campaña

---

#### 🔵 CAMPAÑA 1: JV-TAXES-PROSPECTING-1099

| Setting | Valor |
|---------|-------|
| **Objetivo** | Leads (o Conversiones > Lead event) |
| **Tipo** | Advantage+ Campaign Budget (CBO) |
| **Presupuesto diario** | $15-20/día |
| **Optimización** | Conversiones > Evento Lead |
| **Atribución** | 7-day click, 1-day view |
| **Placements** | Advantage+ (dejar que Meta optimice) |
| **Schedule** | Correr 24/7 (no limitar horarios la primera semana) |

**Ad Set A: Broad-1099**
| Setting | Valor |
|---------|-------|
| **Ubicación** | Florida, Texas, California, New York, New Jersey, Illinois |
| **Edad** | 25-50 |
| **Género** | Todos |
| **Idioma** | Español (cualquier) |
| **Targeting** | BROAD (sin intereses) — dejar que el algoritmo encuentre |
| **Exclusiones** | Custom Audience de clientes existentes |

**Ad Set B: Interest-GigEconomy**
| Setting | Valor |
|---------|-------|
| **Ubicación** | Mismos estados |
| **Intereses** | Uber, Lyft, DoorDash, Instacart, Freelancing, Self-employment, Construction |
| **Idioma** | Español (cualquier) |
| **Exclusiones** | Custom Audience de clientes existentes |

**Ads (1 variante):**

| # | Nombre del Ad | Formato | Archivo fuente | CTA |
|---|--------------|---------|----------------|-----|
| 1 | `1099-ShockDel1099-ReelA` | Video Reel 15s | VSL+ADS PDF Reel 1 (1099) | "Mira el video" → Landing |

---

#### 🔵 CAMPAÑA 2: JV-TAXES-PROSPECTING-W2

| Setting | Valor |
|---------|-------|
| **Objetivo** | Leads (o Conversiones > Lead event) |
| **Tipo** | Advantage+ Campaign Budget (CBO) |
| **Presupuesto diario** | $15-20/día |
| **Optimización** | Conversiones > Evento Lead |

**Ad Set A: Broad-W2-Empleados**
| Setting | Valor |
|---------|-------|
| **Ubicación** | FL, TX, CA, NY, NJ, IL |
| **Edad** | 25-45 |
| **Género** | Todos |
| **Idioma** | Español (cualquier) |
| **Targeting** | BROAD |

**Ad Set B: Interest-Finance-W2**
| Setting | Valor |
|---------|-------|
| **Intereses** | TurboTax, H&R Block, Tax preparation, Personal finance, Child tax credit |
| **Idioma** | Español |

**Ads (1 variante):**

| # | Nombre del Ad | Formato | CTA |
|---|--------------|---------|-----|
| 1 | `W2-FalsaSeguridad-ReelA` | Video Reel 15s | "Mira el video" |

---

#### 🔵 CAMPAÑA 3: JV-TAXES-PROSPECTING-EMPRESA

| Setting | Valor |
|---------|-------|
| **Objetivo** | Leads |
| **Tipo** | Advantage+ CBO |
| **Presupuesto diario** | $10-15/día |
| **Optimización** | Conversiones > Lead |

**Ad Set A: Broad-Empresarios**
| Setting | Valor |
|---------|-------|
| **Ubicación** | FL, TX, CA |
| **Edad** | 30-55 |
| **Idioma** | Español |
| **Targeting** | BROAD |

**Ad Set B: Interest-SmallBiz**
| Setting | Valor |
|---------|-------|
| **Intereses** | Small business, LLC, Entrepreneurship, Business owner, QuickBooks |
| **Comportamientos** | Small business owners |

**Ads (1 variante):**

| # | Nombre del Ad | Formato | CTA |
|---|--------------|---------|-----|
| 1 | `EMP-RiesgoAlto-ReelA` | Video Reel 15s | "Mira el video" |

---

#### 🟡 CAMPAÑA 4: JV-TAXES-RETARGET-WARM

| Setting | Valor |
|---------|-------|
| **Objetivo** | Leads |
| **Presupuesto diario** | $8-10/día |
| **Optimización** | Conversiones > Lead |

**Audiencias Custom (crear en Meta):**

| Audiencia | Fuente | Ventana |
|-----------|--------|---------|
| Video Viewers 50%+ | Todos los videos de las campañas 1-3 | 30 días |
| IG Engagers | Engagement con perfil de Instagram de Jorge | 30 días |
| FB Page Engagers | Interacción con página de Facebook | 30 días |

**Exclusiones:** Personas que ya agendaron (Custom Audience de leads GHL)

**Ads (3 variantes):**

| # | Nombre del Ad | Formato | Mensaje |
|---|--------------|---------|---------|
| 1 | `RT-WARM-VSLteaser` | Video 30s (extracto VSL B) | "¿Viste el video completo? → Miralo aquí" |
| 2 | `RT-WARM-Testimonio` | Video testimonial 20s | Social proof + CTA agendar |
| 3 | `RT-WARM-Urgencia` | Estático | "Temporada de taxes cierra pronto. Evalúa tu caso gratis." |

---

#### 🔴 CAMPAÑA 5: JV-TAXES-RETARGET-HOT

| Setting | Valor |
|---------|-------|
| **Objetivo** | Leads |
| **Presupuesto diario** | $5-7/día |
| **Optimización** | Conversiones > Lead |

**Audiencias Custom:**

| Audiencia | Fuente | Ventana |
|-----------|--------|---------|
| Landing Visitors No Lead | Pixel > Visitó landing + NO disparó evento Lead | 14 días |

**Ads (2 variantes):**

| # | Nombre del Ad | Formato | Mensaje |
|---|--------------|---------|---------|
| 1 | `RT-HOT-OfertaDirecta` | Estático | "Primera evaluación 100% gratis. Sin compromisos. Agenda ahora." |
| 2 | `RT-HOT-CasoExito` | Video caso real 15s | "Le pagó $100, le costó $6,000. No cometas el mismo error." |

---

## 💰 PARTE 3: PRESUPUESTO POR SEMANA

### Presupuesto Total Recomendado: $1,500 - $2,000 para primer mes

| Semana | Presupuesto/día | Total semanal | Campañas activas | Objetivo |
|--------|----------------|---------------|-------------------|----------|
| **Semana 1** | $30-40/día | $210-280 | Solo Prospecting (1,2,3) | Activar pixel, recolectar data |
| **Semana 2** | $40-50/día | $280-350 | Prospecting + Retarget Warm | Primeros leads, analizar métricas |
| **Semana 3** | $50-60/día | $350-420 | Todas (Prosp + Warm + Hot) | Escalar ganadores, pausar perdedores |
| **Semana 4** | $60-80/día | $420-560 | Ganadores escalados | Primeras ventas cerradas |

**Distribución por campaña (Semana 3 en adelante):**

| Capa | % Presupuesto | $/día |
|------|--------------|-------|
| Prospecting (Cold) | 70% | $35-56 |
| Retarget Warm | 20% | $10-16 |
| Retarget Hot | 10% | $5-8 |

---

## 📅 PARTE 4: PLAN SEMANA POR SEMANA

### ✅ SEMANA 0 — PREPARACIÓN (3-4 días antes del launch)

**Go High Level:**
- [ ] Verificar landing page funcional en mobile (abrir en incógnito con UTMs de prueba)
- [ ] Verificar que el CTA "Agendar" redirige correctamente a `/go/book` → Calendario
- [ ] Probar agendamiento completo (desde click hasta confirmación por SMS)
- [ ] Configurar Workflows 1-4 (confirmación, recordatorio, no-show, nurturing)
- [ ] Crear tags: `meta-ads-lead`, `prospecting-1099`, `prospecting-w2`, `prospecting-empresa`
- [ ] Configurar reportes diarios por email con: contactos nuevos, fuente, agendamientos

**Meta Business Manager:**
- [ ] Verificar dominio en Business Settings
- [ ] Instalar Meta Pixel en GHL (Settings > Tracking)
- [ ] Configurar Conversions API (CAPI) en GHL
- [ ] Configurar Aggregated Event Measurement (priorizar Lead > ViewContent > PageView)
- [ ] Crear Custom Audiences:
  - Clientes actuales (subir lista CSV para exclusión)
  - Lookalike 1% sobre lista de clientes actuales (si hay >100 emails)
- [ ] Probar Pixel con [Meta Pixel Helper](https://chrome.google.com/webstore/detail/meta-pixel-helper/) — verificar que dispare PageView en landing

**Creativos:**
- [ ] Subir los 3 videos de ads cortos y el VSL a Meta Ad Account > Media Library
- [ ] Crear imágenes estáticas en Canva (6 diseños por segmento) con identidad visual Jorge (navy, gold, white)
- [ ] Crear carruseles (Deducciones 1099, Créditos W2, Deducciones Empresas)
- [ ] Verificar subtítulos en todos los videos
- [ ] Preparar al menos 2-3 variantes de Primary Text por ad

---

### 🚀 SEMANA 1 — LANZAMIENTO Y APRENDIZAJE

**Día 1-2: Lanzar campañas de Prospecting**

**Acción paso a paso:**

1. **Crear Campaña 1:** `JV-TAXES-PROSPECTING-1099`
   - Objective: Leads
   - Campaign Budget Optimization: ON
   - Daily Budget: $15/día
   - Crear Ad Set Broad (sin intereses) + Ad Set Interest (gig economy)
   - Cargar 1 ad por segmento con UTMs correctos en cada URL
   - URL: `https://asesoriajorge.com/impuestos?utm_source=facebook&utm_medium=paid&utm_campaign=JV-TAXES-PROSPECTING-1099&utm_content={{ad.name}}&utm_term={{adset.name}}`
   - Publicar

2. **Crear Campaña 2:** `JV-TAXES-PROSPECTING-W2`
   - Misma estructura, $15/día
   - 1 ad corto del ángulo W2
   - Publicar

3. **Crear Campaña 3:** `JV-TAXES-PROSPECTING-EMPRESA`
   - Misma estructura, $10/día
   - 1 ad corto del ángulo Empresas
   - Publicar

**Día 3-4: Monitoreo inicial**

- [ ] Verificar que TODOS los ads pasaron revisión de Meta (si alguno se rechaza, ajustar copy)
- [ ] Verificar que el Pixel está disparando correctamente (Events Manager > Test Events)
- [ ] Verificar en GHL que los UTMs llegan correctamente a los contactos
- [ ] NO tocar nada aún — dejar que el algoritmo aprenda

**Día 5-7: Primera revisión de data**

| Qué revisar | Dónde | Decisión |
|-------------|-------|----------|
| Impressions por ad | Ads Manager | ¿Se están gastando parejo entre ads? |
| CTR por ad | Ads Manager | < 1% → candidato a pausar |
| Hook Rate (3s video views / impressions) | Ads Manager | < 25% → hook débil |
| CPM | Ads Manager | Benchmark: $8-20 para hispanos en USA |
| Leads en GHL | GHL Contacts | ¿Están llegando? ¿Con UTMs correctos? |
| Costo por click | Ads Manager | Benchmark: < $2 |

**Regla de Semana 1: NO PAUSAR NADA** a menos que:
- Un ad tenga 0% CTR después de 500+ impresiones
- Haya un error técnico (pixel no dispara, link roto)

---

### 📊 SEMANA 2 — PRIMERAS OPTIMIZACIONES

**Día 8-10: Análisis profundo**

Revisar en Ads Manager por cada campaña:

| Métrica | Acción si mal | Acción si bien |
|---------|--------------|----------------|
| CTR < 1% | Revisar copy y hook del video/estático | Mantener |
| CPL > $25 | Pausar ese ad o ad set | Mantener, considerar escalar |
| CPL < $12 | ¡Ganador! Notar cuál ad/ad set | Escalar presupuesto +20% |
| Hook Rate < 25% | Test nuevo hook (primeros 3 seg) | Mantener |
| Frequency > 2.5 | Ampliar audiencia o refrescar creative | Mantener |

**Día 10: Activar Retargeting Warm**

1. Crear Campaña 4: `JV-TAXES-RETARGET-WARM`
   - Custom Audience: Video Viewers 50%+ (ya deberías tener data de 7+ días)
   - Custom Audience: IG/FB Engagers
   - $8-10/día
   - 3 ads (VSL teaser, testimonio, urgencia)
   - Excluir: Custom Audience de leads existentes

**Día 11-14: Optimización continua**

- [ ] Pausar los 2 ads con peor performance por campaña (dejar los 3 mejores)
- [ ] Revisar en GHL: ¿Los leads que llegan están agendando? ¿Cuál es el % de agenda vs. registro?
- [ ] Si un segmento (ej: 1099) está outperforming a los otros, mover $5/día de presupuesto del peor al mejor
- [ ] A/B test nuevas variantes de Primary Text en los ads ganadores

---

### 💪 SEMANA 3 — ESCALAMIENTO INTELIGENTE

**Acciones clave:**

1. **Activar Retargeting Hot:**
   - Campaña 5: `JV-TAXES-RETARGET-HOT`
   - Custom Audience: Landing visitors sin Lead event
   - $5-7/día
   - 2 ads (oferta directa + caso de éxito)

2. **Escalar ganadores:**
   - Ads con CPL < $15 y CTR > 1.5% → Aumentar presupuesto del ad set 20% cada 3 días
   - **NUNCA** aumentar más de 20-30% de golpe (resetea el aprendizaje del algoritmo)

3. **Matar perdedores:**
   - Ads con > $30 CPL después de 1,000+ impresiones → PAUSAR
   - Ad sets sin leads después de $30+ gastados → PAUSAR
   - Campañas enteras con 0 leads después de $100+ → Revisar landing page y pixel

4. **Reporte a Jorge:**
   - Total leads por segmento (1099/W2/Empresa)
   - CPL promedio
   - Ads ganadores (con screenshots)
   - Agendamientos vs. leads
   - Show rate
   - Ventas cerradas

**Dashboard semanal (enviar cada viernes):**

```
📊 REPORTE SEMANAL - SEMANA [X]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💰 Inversión total: $XXX
👥 Leads nuevos: XX
📅 Citas agendadas: XX
✅ Citas asistidas: XX
💵 Ventas cerradas: XX
📈 Revenue generado: $X,XXX

COSTO POR:
• Lead: $XX
• Cita agendada: $XX
• Cita asistida: $XX

🏆 AD GANADOR: [Nombre del ad]
💀 AD PAUSADO: [Nombre del ad]

NEXT STEPS:
• [Acción 1]
• [Acción 2]
```

---

### 🔥 SEMANA 4+ — ESCALA Y REFINAMIENTO

**Acciones:**

1. **Lookalike Audiences:**
   - Crear Lookalike 1% basado en leads que SÍ agendaron
   - Crear Lookalike 1% basado en leads que SÍ cerraron (cuando haya 25+)
   - Probar estas audiencias en nuevos ad sets dentro de las campañas ganadoras

2. **Nuevos creativos:**
   - Crear 3-5 ads nuevos basados en los hooks que mejor funcionaron
   - Reutilizar la fórmula ganadora con variaciones (diferente ángulo, mismo formato)
   - Probar VSL B (7 min) como ad largo de retargeting

3. **Presupuesto objetivo:**
   - Si ROAS > 3x → Escalar a $80-100/día total
   - Si ROAS 2-3x → Mantener y optimizar
   - Si ROAS < 2x → Pausar, revisar funnel completo (landing → cita → cierre)

4. **Expansión geográfica:**
   - Si FL/TX/CA funcionan bien → Agregar: GA, NC, AZ, NV, CO (alta población latina)

---

## 🎯 PARTE 5: NOMENCLATURA DE CAMPAÑAS (NAMING CONVENTIONS)

Para mantener todo organizado y medible:

```
Patrón: [INICIALES]-[SERVICIO]-[CAPA]-[SEGMENTO]-[DETALLE]
```

**Ejemplos completos:**

| Nivel | Formato | Ejemplo |
|-------|---------|---------|
| **Campaña** | `JV-TAXES-[CAPA]-[SEGMENTO]` | `JV-TAXES-PROSPECTING-1099` |
| **Ad Set** | `[TIPO_AUDIENCIA]-[GEO]-[DETALLE]` | `Broad-FLTXCA-Esp-25-50` |
| **Ad** | `[SEGMENTO]-[TEMA]-[FORMATO]` | `1099-ShockDel1099-ReelA` |

---

## 📋 PARTE 6: CHECKLIST COMPLETO DE LANZAMIENTO

### Pre-Launch (Día -3 a 0)

**GHL:**
- [ ] Landing page live y funcional en mobile
- [ ] Calendario configurado con slots disponibles
- [ ] Workflows de confirmación, recordatorio, no-show activos
- [ ] Tags y UTM tracking verificados
- [ ] Reporte diario por email configurado

**Meta Business Manager:**
- [ ] Pixel instalado y verificando eventos
- [ ] CAPI configurado
- [ ] Dominio verificado
- [ ] Aggregated Event Measurement configurado
- [ ] Custom Audiences creadas (clients exclusión)
- [ ] Medio de pago verificado

**Creativos:**
- [ ] Los 3 ads de prospección creados y aprobados + el VSL subido
- [ ] Subtítulos en todos los videos
- [ ] Estáticos con brand identity correcta
- [ ] Carruseles diseñados
- [ ] UTMs correctos en todas las URLs de destino

### Launch Day

- [ ] Publicar las 3 campañas de Prospecting
- [ ] Verificar que todos los ads pasaron revisión
- [ ] Verificar pixel en Events Manager > Test Events
- [ ] Verificar primer lead de prueba en GHL (con UTMs)
- [ ] Screenshot de los ads publicados y guardar

### Post-Launch (Diario)

- [ ] Revisar Ads Manager 1x al día (no más, no menos)
- [ ] Revisar GHL contacts nuevos y calidad
- [ ] Verificar que workflows disparan correctamente
- [ ] Anotar observaciones en un doc compartido

---

## ⚠️ REGLAS DE ORO — NO ROMPER

1. **No tocar las campañas los primeros 3-4 días** — el algoritmo está aprendiendo
2. **No aumentar presupuesto más de 20% a la vez** — resetea el aprendizaje
3. **Un ad no es perdedor hasta 500+ impresiones** — paciencia con la data
4. **Siempre excluir clientes actuales** — no gastar dinero en gente que ya compró
5. **Verificar pixel CADA SEMANA** — un pixel roto = dinero tirado
6. **Medir desde ventas hacia atrás** — un CPL bajo con 0 ventas no sirve
7. **Reels > Estáticos para cold traffic** — los videos outperforman en prospecting
8. **Estáticos con oferta directa para retargeting** — menos storytelling, más acción
9. **Frequency > 3 = creative fatigue** — cambiar creativos cuando la frecuencia sube
10. **ROAS es la única métrica que importa al final** — todo lo demás es vanidad

---

## 🛡️ COMPLIANCE META ADS (Servicios Financieros)

**Qué SÍ hacer:**
- ✅ Usar "maximizar deducciones legales" (no "pagar menos taxes")
- ✅ Decir "te ayudamos a entender" o "te explicamos"
- ✅ Usar casos generales ("muchas personas", "es común que")
- ✅ Agregar disclaimers: "Resultados varían según situación individual"

**Qué NO hacer:**
- ❌ Prometer ahorros específicos ("te ahorramos $5,000 garantizado")
- ❌ Usar lenguaje alarmista excesivo del IRS
- ❌ Mostrar formularios reales del IRS con datos
- ❌ Claims de ingresos o resultados garantizados
- ❌ Comparar directamente con TurboTax/H&R Block por nombre (solo mencionarlo en contexto educativo)

**Categoría especial:** Los ads de servicios financieros/tax prep pueden requerir la categoría especial "Credit" en algunos casos. Si Meta lo pide, activarla — reduce el targeting pero evita rechazos.

---

## 📞 RESUMEN: LOS 5 PASOS INMEDIATOS

| # | Qué | Cuándo | Quién |
|---|-----|--------|-------|
| 1 | Configurar Pixel + CAPI + Eventos en GHL | Hoy | Lucho/Programador |
| 2 | Subir creativos a Meta Media Library | Hoy/Mañana | Lucho |
| 3 | Crear las 3 campañas de Prospecting | Después de Pixel verificado | Lucho |
| 4 | Verificar funnel completo (ad → landing → cita → SMS) | Antes de publicar | Lucho + Jorge |
| 5 | Publicar y NO TOCAR por 72 horas | Día de lanzamiento | - |

---

**Documento creado por Antigravity para Lucho Branding × Jorge Vergara**  
**Próximo paso:** Aprobar este plan → Convertir a HTML premium → Ejecutar
