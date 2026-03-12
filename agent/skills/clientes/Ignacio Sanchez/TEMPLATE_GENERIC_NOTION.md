# VSL HIGH TICKET - MASTER TEMPLATE

📋 **INSTRUCCIONES CLAVE PARA LA IA / ESTRATEGA**
Esta plantilla está estructurada en **TRES PARTES OBLIGATORIAS** que debes seguir secuencialmente para generar los entregables perfectos de un cliente, basándote en su "Oferta 100M".

---

# [default] PARTE 1: GUIÓN VSL (EL TEXTO HABLADO)
> Instrucciones para la IA / Estratega:
> Aquí vamos a estructurar el guión exacto que el cliente va a **leer frente a la cámara (teleprompter)**.
> **REGLA ESTRICTA:** Extrae ÚNICAMENTE el diálogo puro. Elimina indicaciones de cámara, acotaciones de tiempos (ej. "[0:00]"), o direcciones técnicas. El output debe ser texto corrido listo para leerse en voz alta, organizado en los siguientes 6 bloques:

## [blue] 1.1 Hook + Promesa + Prueba
> Instrucciones para la IA / Estratega:
> **Objetivo:** Capturar atención inmediata en los primeros 45 segundos.
> • Promesa audaz: "Lograremos [Resultado X] o no pagas".
> • Prueba inmediata: Relatar resultados tangibles rápidos.
> • Diferenciación: Abordar la objeción más obvia de su nicho.

[Reemplaza con el texto hablado del Hook...]

## [yellow] 1.2 Autoridad y Casos de Éxito
> Instrucciones para la IA / Estratega:
> **Objetivo:** Contaminar la percepción del usuario con múltiples testimonios para construir autoridad irrefutable rápida.
> • Nombres + resultados específicos de clientes previos.
> • Mención de marcas o credenciales relevantes.

[Reemplaza con el texto hablado de la Autoridad...]

## [red] 1.3 El Filtro (Anti-Selling)
> Instrucciones para la IA / Estratega:
> **Objetivo:** Definir para quién NO es este servicio, construyendo exclusividad.
> • Aclarar que no es mágico, que requiere estatus o experiencia previa, alejando a los novatos o sin presupuesto.

[Reemplaza con el texto hablado del Filtro...]

## [default] 1.4 El Plan / Mecanismo
> Instrucciones para la IA / Estratega:
> **Objetivo:** Explicar el "Vehículo" lógico.
> • Dar la "receta" a grandes rasgos. Explicar el sistema "Hecho Contigo" o metodología propia paso a paso.

[Reemplaza con el texto hablado del Mecanismo...]

## [green] 1.5 Manejo de Objeciones
> Instrucciones para la IA / Estratega:
> **Objetivo:** Desarmar dudas antes de que ocurran.
> • Abordar precio ("lo barato sale caro"), tiempo de implementación, o seguridad del proceso.

[Reemplaza con el texto hablado de Objeciones...]

## [blue] 1.6 Call To Action (CTA)
> Instrucciones para la IA / Estratega:
> **Objetivo:** Invitar a agendar una sesión diagnóstica, cero presión.
> • Indicar el siguiente paso (llenar formulario debajo).
> • Mencionar la escasez real (cupos limitados).

[Reemplaza con el texto hablado del CTA...]

---
---

# [yellow] PARTE 2: ESTRUCTURA COPY LANDING PAGE
> Instrucciones para la IA / Estratega:
> Ahora, toma el guión del VSL y los datos de la Oferta 100M para destilar el **Copy de la Landing Page**. Completa exactamente esta estructura de 5 secciones:

## 1️⃣ Hero / Above the Fold
- **Top Badge / Eyebrow:** 🔴 CLASE GRATUITA EN VIVO / o [Puesto de Autoridad]
- **Headline (H1):** [Promesa Específica + Tiempo + Garantía]
- **Subheadline (H2):** 2-3 líneas desarrollando el H1.
- **Botón CTA Principal:** [Texto orientado a la acción]
- **Micro-copy del CTA:** Beneficios o garantía anti-fricción.

## 2️⃣ Prueba Social (Grid)
- **Headline:** Más de [X] profesionales ya lograron [Resultado]
- **Casos de Éxito:** [Viñetas con Nombre + Métrica Tangible]

## 3️⃣ El Formulario (Filtro)
- **Headline:** Solicita Tu Acceso
- **Texto:** Solo trabajamos con postulantes serios y calificados...
- **Campos Indispensables:** Nombre, Email, Ingresos Mensuales, Capital Dispuesto a Invertir.

## 4️⃣ FAQ (Manejo de Objeciones)
- **Pregunta 1:** [Respuesta...]
- **Pregunta 2:** [Respuesta...]
- **Pregunta 3:** [Respuesta...]

## 5️⃣ Cierre Final
- **Headline Final:** [Frase de escasez o empuje final]
- **Botón CTA Final:** [Acción]

[Reemplaza con el documento final de Copy rellenado con los datos del cliente...]

---
---

# [green] PARTE 3: PROMPT ANTIGRAVITY (Handoff a Desarrollo)
> Instrucciones para la IA / Estratega:
> Esta es la fase de desarrollo web real. **Copia el macro-prompt que está en el bloque de código abajo** y suminístraselo a Antigravity (junto con el Guión y Copy generados arriba) para que él programe la página, los CSS y te dé las instrucciones exactas para implementarlo en GoHighLevel.

```text
Actúa como un Full Stack Developer, CRO Specialist y Web Designer premium (mobile-first), especializado en VSLs de alta conversión para servicios high ticket ($5K-$100K+).

# OBJETIVO
Convertir el Guión VSL (INPUT 1) y la Estructura de Landing Page (INPUT 2) y la OFERTA DEL CLIENTE (INPUT 3) en código HTML/CSS/JS funcional y listo para implementar en Go High Level.
Debes entregar:
1) Snippet HTML unificado para Go High Level (listo para Custom HTML element)
2) Archivo index.html local standalone para previsualizaciones rápidas
3) Guía de pasos a implementar en GHL (Configurar URLs, forms, UTMs)

---
# INPUT 1: GUIÓN VSL (PARTE 1)
[Pegar aquí el guión VSL completo generado en la PARTE 1]

---
# INPUT 2: ESTRUCTURA LANDING PAGE (PARTE 2)
[Pegar aquí el copy exacto desarrollado en la PARTE 2]

---
# INPUT 3: CONTEXTO / OFERTA 100M DEL CLIENTE
[Pegar aquí la data del cliente o ecosistema general]

---
# REQUISITOS CLAVE DE GOHIGHLEVEL (UX / CONVERSIÓN / UI)
- Mobile-first absoluto. 
- Above the fold optimizado donde el Hero sea visible entero en móviles. 
- Formulario de calificación GHL con JS vanilla (Validaciones frontend).
- Acordeones FAQ suaves y responsivos en vanilla JS.
- Inyectar TODO el `CSS` dentro de la etiqueta `<style>` global y no usar archivos externos para que sea un copy/paste directo en GHL.
- Crear una Estética Premium: Elige tú mismo una paleta de colores aspiracionales basada en la industria del cliente (Nada genérico. Ej. usar Charcoal dark mode con Golden Accents o Deep Blue con Emerald). 
- Usa Glassmorphism inteligentemente donde aplique.
- Utiliza fuentes modernas vía Google Fonts (Inter, Montserrat, Outfit).
```
