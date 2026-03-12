# 📘 Manual de Marca — {{NOMBRE_CLIENTE}}

{{IF_LOGO_START}}
![Logo {{NOMBRE_CLIENTE}}]({{URL_LOGO}})
{{IF_LOGO_END}}

---

## 🎯 Identidad de Marca

| Elemento | Valor |
|----------|-------|
| **Nombre** | {{NOMBRE_CLIENTE}} |
| **Tagline** | *"{{TAGLINE}}"* |
| **Industria** | {{INDUSTRIA}} |
| **Personalidad** | {{RASGOS_PERSONALIDAD}} (ej: Cálida, inspiradora, elegante, empoderada, auténtica) |
| **Handle** | @{{HANDLE_IG}} |
| **Web** | {{SITIO_WEB}} |
| **Email** | {{EMAIL_CONTACTO}} |
| **Ubicación** | {{CIUDAD}}, {{PAIS}} |

### Pilares de Marca

| Pilar | Esencia |
|-------|---------|
| **{{PILAR_1}}** | {{DESCRIPCION_PILAR_1}} |
| **{{PILAR_2}}** | {{DESCRIPCION_PILAR_2}} |
| **{{PILAR_3}}** | {{DESCRIPCION_PILAR_3}} |

> 💡 **Nota:** Definir 3 pilares de marca que representen los valores fundamentales del cliente. Estos se usan en toda la comunicación, contenido, y diseño.

---

## 🎨 Paleta de Colores

### Colores Primarios

| Color | Hex | RGB | Uso |
|-------|-----|-----|-----|
| **Color Base Oscuro** | `#{{HEX_OSCURO}}` | {{RGB_OSCURO}} | Textos principales, fondos hero, bordes |
| **Color Base Claro** | `#{{HEX_CLARO}}` | {{RGB_CLARO}} | Fondos de secciones, texto sobre fondos oscuros |
| **Color de Texto** | `#{{HEX_TEXTO}}` | {{RGB_TEXTO}} | Cuerpo de texto en secciones claras |

### Colores Secundarios

| Color | Hex | Uso |
|-------|-----|-----|
| **Gris Medio** | `#{{HEX}}` | Subtítulos, labels, texto secundario |
| **Gris Suave** | `#{{HEX}}` | Labels de categoría |
| **Off-White** | `#{{HEX}}` | Fondo de tarjetas (cards) |
| **Gris Humo** | `#{{HEX}}` | Fondo alternativo de secciones |

### Color de Acento

| Color | Hex | RGB | Uso |
|-------|-----|-----|-----|
| **Acento Principal** | `#{{HEX_ACENTO}}` | {{RGB_ACENTO}} | Acento principal: bordes hover, líneas decorativas, gradientes |
| **Acento Claro** | `#{{HEX_ACENTO_CLARO}}` | {{RGB}} | Fondos suaves de acento, badges, highlights |
| **Acento Profundo** | `#{{HEX_ACENTO_OSCURO}}` | {{RGB}} | Hover intenso, CTAs, gradiente oscuro |

> **Regla de uso:** El color de acento es un *acento*, no un color dominante. Máximo 10-15% de presencia visual. Úsalo para detalles que "respiran" — líneas hover, bordes sutiles, gradientes secundarios.

### Colores de Superposición (Overlays)

| Overlay | Valor | Uso |
|---------|-------|-----|
| **Hero Overlay** | `rgba(0, 0, 0, 0.40)` | Sobre imágenes hero principales |
| **Vision Overlay** | `rgba(0, 0, 0, 0.45)` | Sobre secciones visual-interlude |
| **Footer Overlay** | `rgba(0, 0, 0, 0.40)` | Sobre sección de cierre |

### Principio de Color

> **{{PRINCIPIO_COLOR}}.** Describir en una oración el principio rector de la paleta de colores del cliente. Ejemplo: "Monocromático con alma — base blanco y negro con un toque de púrpura pastel que aporta feminidad."

---

## 🔤 Tipografía

### Fuente Principal

**{{FUENTE_PRINCIPAL}}** — [Google Fonts](https://fonts.google.com/specimen/{{FUENTE_PRINCIPAL}})

```css
@import url('https://fonts.googleapis.com/css2?family={{FUENTE_URL}}&display=swap');

font-family: '{{FUENTE_PRINCIPAL}}', sans-serif;
```

### Escala Tipográfica

| Peso | Valor | Uso |
|------|-------|-----|
| Light | `font-weight: 300` | Cuerpo de texto, descripciones |
| Regular | `font-weight: 400` | Headlines editoriales |
| Medium | `font-weight: 500` | Nav links, texto destacado |
| SemiBold | `font-weight: 600` | Títulos (h1, h2, h3), botones |
| Bold | `font-weight: 700` | Énfasis máximo |

### Tamaños (Desktop → Mobile)

| Elemento | Desktop | Mobile (≤768px) |
|----------|---------|-----------------|
| **Hero Title** | 5rem | 1.6rem |
| **Headlines (h1)** | 3.5rem | 1.6rem |
| **Section Titles (h2)** | 1.8rem | 1.4rem |
| **Body Text** | 1.1rem | 0.92rem |
| **Labels** | 0.65rem | 0.6rem |
| **Buttons** | 0.9rem | 0.75rem |

### Atributos Tipográficos Clave

```css
/* Headlines — tracking apretado */
letter-spacing: -0.02em;

/* Subtitles — tracking abierto, uppercase */
letter-spacing: 0.15em;
text-transform: uppercase;

/* Body — line-height generoso */
line-height: 1.7;
```

### Fuente Alternativa

`{{FUENTE_FALLBACK}}` (solo si la fuente principal no carga)

---

## 📐 Espaciado y Layout

| Principio | Valor |
|-----------|-------|
| **Max-width contenido** | 800px |
| **Max-width body text** | 600px |
| **Padding lateral** | 5% |
| **Sección (desktop)** | 100px top/bottom |
| **Sección (mobile)** | 40px top/bottom |
| **Border-radius cards** | 20px |

---

## 🧩 Componentes de Diseño

### 1. Botones

```css
/* Botón Base */
.editorial-button {
    display: inline-block;
    padding: 16px 32px;
    font-size: 0.9rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    text-decoration: none;
    transition: all 0.3s ease;
    border: 1px solid currentColor;
    cursor: pointer;
}

/* Variante Dark (sobre fondos claros) */
.editorial-button.dark {
    color: {{COLOR_OSCURO}};
    border-color: {{COLOR_OSCURO}};
    background: transparent;
}

/* Variante Accent (CTAs destacados) */
.editorial-button.accent {
    color: {{COLOR_ACENTO_OSCURO}};
    border-color: {{COLOR_ACENTO}};
    background: transparent;
}

/* Variante Light (sobre fondos oscuros) */
.editorial-button.light {
    color: #fff;
    border-color: #fff;
    background: rgba(255, 255, 255, 0.1);
}
```

### 2. Tarjetas (Cards)

```css
.card {
    background: {{COLOR_CARD_BG}};
    border: 1px solid rgba(0, 0, 0, 0.08);
    border-radius: 20px;
    padding: 40px 32px;
    transition: all 0.4s ease;
}

.card:hover {
    transform: translateY(-6px);
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.08);
}
```

### 3. Pricing Cards

```css
.package-card {
    background: #fff;
    border: 1px solid rgba(0, 0, 0, 0.08);
    border-radius: 20px;
    padding: 48px 32px;
}

.package-card.featured {
    background: {{COLOR_OSCURO}};
    color: #fff;
    transform: scale(1.03);
}
```

---

## 🖼️ Dirección de Fotografía

| Atributo | Descripción |
|----------|-------------|
| **Iluminación** | {{ESTILO_ILUMINACION}} |
| **Mood** | {{MOOD_VISUAL}} |
| **Composición** | {{COMPOSICION}} |
| **Color fotográfico** | {{PALETA_FOTOS}} |
| **Pose/Estilo** | {{ESTILO_POSE}} |

### Tratamiento de Imágenes Web

```css
background-size: cover;
background-position: center;

/* Overlay oscuro obligatorio */
.overlay {
    background: rgba(0, 0, 0, 0.40–0.55);
}

/* Text shadow para legibilidad */
text-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
```

---

## ✍️ Tono de Voz

| Atributo | Descripción |
|----------|-------------|
| **Idioma** | {{IDIOMA_PRINCIPAL}} |
| **Tono** | {{TONO}} (ej: Inspirador, personal, directo) |
| **Perspectiva** | {{PERSPECTIVA}} (ej: Primera persona, tercera persona) |
| **Energía** | {{ENERGIA}} (ej: Positiva, empoderada, inclusiva) |

### Frases Clave

- *"{{FRASE_1}}"*
- *"{{FRASE_2}}"*
- *"{{FRASE_3}}"*

### Qué decir (Dos) vs Qué no decir (Don'ts)

| ✅ Sí decir (Dos) | ❌ No decir (Don'ts) |
|-----------|-----------|
| {{DOS_1}} | {{DONTS_1}} |
| {{DOS_2}} | {{DONTS_2}} |
| {{DOS_3}} | {{DONTS_3}} |
| {{DOS_4}} | {{DONTS_4}} |

---

## 🎨 Design Tokens (CSS Variables)

```css
:root {
    /* ── Colores ── */
    --brand-black: {{COLOR_OSCURO}};
    --brand-white: {{COLOR_CLARO}};
    --brand-gray-dark: {{COLOR_TEXTO}};
    --brand-gray-mid: {{COLOR_SECUNDARIO_1}};
    --brand-off-white: {{COLOR_CARD_BG}};

    /* ── Acento ── */
    --brand-accent: {{COLOR_ACENTO}};
    --brand-accent-light: {{COLOR_ACENTO_CLARO}};
    --brand-accent-deep: {{COLOR_ACENTO_OSCURO}};
    --brand-accent-gradient: linear-gradient(135deg, {{COLOR_ACENTO}}, {{COLOR_ACENTO_OSCURO}});

    /* ── Overlays ── */
    --brand-overlay-hero: rgba(0, 0, 0, 0.40);
    --brand-overlay-strong: rgba(0, 0, 0, 0.55);

    /* ── Tipografía ── */
    --brand-font: '{{FUENTE_PRINCIPAL}}', sans-serif;

    /* ── Espaciado ── */
    --brand-radius: 20px;
    --brand-max-content: 800px;
    --brand-transition: all 0.3s ease;
    --brand-shadow-card: 0 20px 60px rgba(0, 0, 0, 0.08);
}
```

---

## ❌ Usos Incorrectos

| No hacer | Por qué |
|----------|---------|
| 🚫 Usar colores de acento no autorizados | Solo el color de acento definido arriba |
| 🚫 Usar el acento como color dominante | Máx 10-15%, es un acento sutil |
| 🚫 Tipografías no autorizadas | Solo la fuente principal |
| 🚫 Border-radius pequeño en cards | El look es redondeado (20px) |
| 🚫 Imágenes sin overlay oscuro | El texto necesita contraste |
| 🚫 Texto centrado sin max-width | Pierde legibilidad |

---

## 📥 Archivos de Referencia

| Archivo | Ubicación |
|---------|-----------|
| Foto Hero | `hero.jpg` |
| Foto Visión | `vision.jpg` |
| Foto Contacto | `contact.jpg` |
| Landing Page | `index.html` |
| Pricing Page | `ghl-pricing.html` |

---

*Manual de Marca v1.0 — {{NOMBRE_CLIENTE}} — {{MES}} {{AÑO}}*
