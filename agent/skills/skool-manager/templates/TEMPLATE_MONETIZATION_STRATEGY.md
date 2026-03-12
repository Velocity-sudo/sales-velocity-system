# Estrategia de Monetización — {{NOMBRE_COMUNIDAD}}

> **Cliente:** {{NOMBRE_CLIENTE}}
> **Nicho:** {{NICHO}}
> **Fecha:** {{FECHA}}
> **Meta Revenue:** {{META_REVENUE_MENSUAL}}/mes en {{PLAZO_MESES}} meses

---

## 1. Resumen del Modelo de Negocio

### Value Ladder (Escalera de Valor)

```
GRATIS                    BAJO                    MEDIO                   ALTO
──────────────────────────────────────────────────────────────────────────────
Lead Magnet          →    Micro-Upsell       →    Membresía Pagada    →    High-Ticket
{{LEAD_MAGNET}}           ${{PRECIO_MICRO}}        ${{PRECIO_MENSUAL}}/mes   ${{PRECIO_HIGH_TICKET}}
                          one-time                 recurring                one-time / programa
```

### Revenue Projection

| Mes | Free Members | Paid Members | Conv. Rate | Revenue |
|-----|-------------|--------------|------------|---------|
| 1 | {{MES1_FREE}} | {{MES1_PAID}} | {{MES1_CONV}}% | ${{MES1_REV}} |
| 3 | {{MES3_FREE}} | {{MES3_PAID}} | {{MES3_CONV}}% | ${{MES3_REV}} |
| 6 | {{MES6_FREE}} | {{MES6_PAID}} | {{MES6_CONV}}% | ${{MES6_REV}} |
| 12 | {{MES12_FREE}} | {{MES12_PAID}} | {{MES12_CONV}}% | ${{MES12_REV}} |

---

## 2. Modelos de Monetización Seleccionados

> Seleccionar los modelos más relevantes al nicho del cliente. No es necesario implementar los 10 — elegir 3-4 que se complementen.

---

### Modelo A: Paid Challenge (Recomendado como primer revenue)

**Qué es:** Un challenge de 5-21 días con tareas diarias y una línea de meta sincronizada. La urgencia y el formato de cohorte generan alta conversión.

| Parámetro | Valor |
|-----------|-------|
| **Nombre** | {{NOMBRE_CHALLENGE}} |
| **Duración** | {{DURACION_CHALLENGE}} días |
| **Precio** | ${{PRECIO_CHALLENGE}} |
| **Entregable** | {{ENTREGABLE_CHALLENGE}} |
| **Formato** | Tareas diarias via Skool + WhatsApp/DM |
| **Upsell al final** | {{UPSELL_CHALLENGE}} (${{PRECIO_UPSELL}}) |

**Matemática:**
- 50 participantes × ${{PRECIO_CHALLENGE}} = ${{REVENUE_CHALLENGE}}
- 78% completan → 39 finishers
- 1:6 ratio upsell → ~8 compran {{UPSELL_CHALLENGE}} = 8 × ${{PRECIO_UPSELL}} = ${{REVENUE_UPSELL}}
- **Total por cohorte: ${{REVENUE_TOTAL_CHALLENGE}}**

**Frecuencia:** {{FRECUENCIA_CHALLENGE}} (mensual / trimestral)

---

### Modelo B: Free-to-Paid Fishbowl Funnel

**Qué es:** Comunidad gratuita como "fishbowl" para construir confianza. Monetizar via DMs, calls de estrategia, y upgrades al tier pagado.

| Parámetro | Valor |
|-----------|-------|
| **Tier Free** | $0 — Feed + Start Here + Gamificación |
| **Tier Paid** | ${{PRECIO_MENSUAL}}/mes — Cursos + calls + DMs |
| **Tier Annual** | ${{PRECIO_ANUAL}}/año — Todo incluido + descuento |

**Funnel de Conversión:**
```
Redes Sociales / Content Marketing
    ↓ "Descarga {{LEAD_MAGNET}} gratis en mi comunidad"
    ↓ Join Rate esperado: 24%
Comunidad FREE
    ↓ Auto-DM → Start Here → 7/11/4 Trust Flow
    ↓ Polls → Loom videos → Wins
    ↓ Conv. rate esperada: 5-9%
Upgrade a PAID (${{PRECIO_MENSUAL}}/mes)
    ↓ Cursos completos + calls semanales
    ↓ Acceso a niveles avanzados de gamificación
```

**Matemática:**
- 500 free members × 7% conversión = 35 paid members
- 35 × ${{PRECIO_MENSUAL}} = ${{REVENUE_FISHBOWL}}/mes MRR

---

### Modelo C: Course Bundle Reframe

**Qué es:** En lugar de vender "membresía con cursos bonus", vender un BUNDLE de cursos con "membresía gratis incluida." Este reframe psicológico triplicó revenue en casos documentados.

| Parámetro | Valor |
|-----------|-------|
| **Bundle Name** | {{NOMBRE_BUNDLE}} |
| **Incluye** | {{CURSOS_INCLUIDOS}} |
| **Precio Annual** | ${{PRECIO_BUNDLE}}/año (one-time) |
| **Bonus** | Membresía {{NOMBRE_COMUNIDAD}} incluida gratis |

**Caso referencia:** De $9K/mes a $30K/mes con un solo cambio de framing (9% upgrade rate desde free members).

---

### Modelo D: Self-Liquidating Offer (SLO)

**Qué es:** Membresía anual ultra-barata que cubre el costo de ads. El objetivo NO es ganar dinero aquí, sino adquirir clientes a costo $0 para upsells futuros.

| Parámetro | Valor |
|-----------|-------|
| **Precio Annual** | ${{PRECIO_SLO}}/año ($17-$29 sugerido) |
| **Costo por Lead (ads)** | ~${{CPL}} |
| **Matemática** | Si CPL = $27 y SLO = $27 → CAC = $0 |
| **Backend Upsell** | {{BACKEND_UPSELL}} a ${{PRECIO_BACKEND}} |

**Resultado:** Todo el revenue del backend es 100% profit.

---

### Modelo E: Internal Affiliate Army

**Qué es:** Convertir a tus miembros en tu equipo de marketing. Skool permite comisiones custom por referidos.

| Parámetro | Valor |
|-----------|-------|
| **Comisión** | {{PORCENTAJE_COMISION}}% recurrente |
| **Material** | Links trackables + templates de DM |
| **Incentivo extra** | Top affiliates → acceso a {{INCENTIVO_AFILIADO}} |

**Matemática:**
- 10 affiliates activos × 3 referidos/mes × ${{PRECIO_MENSUAL}} = {{REVENUE_AFILIADOS}}/mes adicional
- Comisión: {{PORCENTAJE_COMISION}}% = ${{COSTO_COMISION}}/mes
- **Net new revenue: ${{NET_AFILIADOS}}/mes**

---

### Modelo F: High-Ticket Reverse Ladder

**Qué es:** En vez de empezar con precios bajos, lanzar primero una oferta high-ticket a un grupo pequeño. Generar cash flow rápido y luego crear el tier más bajo.

| Parámetro | Valor |
|-----------|-------|
| **Nombre** | {{NOMBRE_HIGH_TICKET}} |
| **Precio** | ${{PRECIO_HIGH_TICKET}} one-time |
| **Capacidad** | {{CAPACIDAD_HT}} personas |
| **Incluye** | {{INCLUYE_HT}} |
| **Duración** | {{DURACION_HT}} |

**Matemática:**
- 5 founding members × ${{PRECIO_HIGH_TICKET}} = ${{REVENUE_HT}} en launch
- Timeline: Posible $20K/mes en 18 días

---

### Modelo G: Pin Post Rental (Revenue Pasivo)

**Qué es:** Si tu comunidad free tiene 4,000+ miembros, rentar el pinned post slot como "ad space."

| Parámetro | Valor |
|-----------|-------|
| **Precio por slot** | ${{PRECIO_PIN}} por {{DURACION_PIN}} |
| **Requisito** | Mínimo 4,000 miembros activos |
| **Frecuencia** | {{FRECUENCIA_SLOTS}}/mes |

**Revenue potencial:** {{FRECUENCIA_SLOTS}} × ${{PRECIO_PIN}} = ${{REVENUE_PINS}}/mes

---

### Modelo H: Micro-Upsells "Buy Now"

**Qué es:** Vender cursos individuales como one-time purchases dentro de la comunidad free. Identifica "buyers" que luego pueden upgradearse.

| Producto | Precio | Descripción |
|----------|--------|-------------|
| {{MICRO_1}} | ${{PRECIO_MICRO_1}} | {{DESC_MICRO_1}} |
| {{MICRO_2}} | ${{PRECIO_MICRO_2}} | {{DESC_MICRO_2}} |
| {{MICRO_3}} | ${{PRECIO_MICRO_3}} | {{DESC_MICRO_3}} |

---

## 3. Stack de Monetización Recomendado

> Combinación sugerida de modelos para el cliente:

| Prioridad | Modelo | Timeline | Revenue Esperado |
|-----------|--------|----------|-----------------|
| 🥇 Primero | {{MODELO_PRIMERO}} | Mes 1 | ${{REV_PRIMERO}} |
| 🥈 Segundo | {{MODELO_SEGUNDO}} | Mes 2-3 | ${{REV_SEGUNDO}} |
| 🥉 Tercero | {{MODELO_TERCERO}} | Mes 4-6 | ${{REV_TERCERO}} |
| 4 | {{MODELO_CUARTO}} | Mes 6+ | ${{REV_CUARTO}} |

---

## 4. Pricing Cheat Sheet

### Reglas de Pricing
1. **Nunca competir por precio** — competir por resultado
2. **$99/mes es el sweet spot** para membresías de nicho ($97 psicológico)
3. **Annual deals** deben dar 2-3 meses gratis (ej. $97/mes × 12 = $1,164 → cobrar $797-$997/año)
4. **Founding member pricing** = 30-50% descuento SOLO para los primeros 20-50 miembros
5. **Subir precios cada 3 meses** — comunica el incremento 2 semanas antes para crear urgencia

### Pricing para {{NOMBRE_COMUNIDAD}}

| Tier | Precio | Valor Anual | Descuento |
|------|--------|-------------|-----------|
| Free | $0 | $0 | — |
| Monthly | ${{PRECIO_MENSUAL}}/mes | ${{VALOR_ANUAL_MENSUAL}} | — |
| Annual | ${{PRECIO_ANUAL}}/año | ${{PRECIO_ANUAL}} | {{DESCUENTO_ANUAL}}% ahorro |
| Founding | ${{PRECIO_FOUNDING}}/mes | — | Solo primeros {{NUM_FOUNDING}} miembros |

---

## 5. KPIs y Objetivos

| KPI | Meta Mes 1 | Meta Mes 3 | Meta Mes 6 |
|-----|-----------|-----------|-----------|
| MRR (Monthly Recurring Revenue) | ${{MRR_M1}} | ${{MRR_M3}} | ${{MRR_M6}} |
| Free Members | {{FREE_M1}} | {{FREE_M3}} | {{FREE_M6}} |
| Paid Members | {{PAID_M1}} | {{PAID_M3}} | {{PAID_M6}} |
| Free→Paid Conversion | 3-5% | 5-7% | 7-9% |
| Churn Rate (monthly) | <10% | <8% | <5% |
| LTV (Lifetime Value) | — | ${{LTV_M3}} | ${{LTV_M6}} |
| CAC (Costo Adquisición) | $0 (orgánico) | ${{CAC_M3}} | ${{CAC_M6}} |
