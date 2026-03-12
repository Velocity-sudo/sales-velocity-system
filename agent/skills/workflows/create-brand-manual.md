---
description: Sales Velocity System workflow to create a complete Brand Manual (HTML + PDF) using the brand-designer skill.
---

# 🎨 Create Brand Manual Workflow (`/create-brand-manual`)

Este workflow está especializado en crear el manual de marca para los clientes de Sales Velocity de manera automatizada. Su objetivo es entregar un HTML funcional y un PDF optimizado con el manual de marca del cliente, listo para usarse como base en GHL y diseño de comunicaciones. Utiliza el skill `brand-designer`.

## Paso 1: Inicialización y Auditoría Inicial (Brainstorming)
Identifica la cuenta del cliente en la que vas a trabajar.
Revisa el contexto actual del cliente en su carpeta (ej. `/Users/niko/Desktop/Clientes/[Nombre]/`):
1. Revisa de inmediato si el cliente ya tiene información suficiente para el manual:
   - ¿Ya tiene una página web de referencia?
   - ¿Existen referencias clave, pilares definidos, un tagline, o paletas de colores en sus documentos y assets?
2. Si **hay referencias**, extrae y organiza esta información automáticamente. Preséntala como un resumen para validar antes de empezar la construcción.
3. Si **NO hay referencias** ni información, inicia una sesión de **Brainstorming**. Haz preguntas guiadas para definir:
   - Nombre principal y Tagline.
   - Industria principal y personalidad de la marca (cálida, empoderada, elegante, disruptiva, etc.).
   - Preferencias de paletas de color y tipografía (o propón unas usando estética Premium como base).
   - Los 3 Pilares de su marca.

## Paso 2: Ejecución e Inserción de Configuración
1. Lee detenidamente las directrices del skill: `~/.agent/skills/brand-designer/SKILL.md`.
2. Lee las plantillas requeridas si son necesarias y úsalas como base:
   - `~/.agent/skills/brand-designer/templates/TEMPLATE_BRAND_MANUAL.md`
   - `~/.agent/skills/brand-designer/templates/TEMPLATE_BRAND_MANUAL.html`
   - Si no puedes leerlas, usa CUALQUIER OTRA plantilla de manual de marca existente en tu contexto y adáptala para generar un manual similar. Analiza otros clientes exitosos (ej. Joana Cueva, Cristian Fones, Antonio Martínez, Jorge Vergara) para inspirarte.
3. Asegúrate de aplicar principios de diseño Premium, utilizando tipografías modernas (Inter/Outfit), combinando el contenido con un *dark-mode* si ayuda a resaltar la propuesta visual, y elementos *glassmorphism* u organizados de forma limpia.

## Paso 3: Generación de Archivos y PDF de Salida
1. Genera los archivos en la estructura deseada para el cliente: `[Ruta del Cliente]/brand-assets/`.
2. Genera las salidas locales:
   - Escribe el HTML: `[Ruta del Cliente]/brand-assets/BRAND_MANUAL.html`. Asegúrate de que el archivo sirva como base completa, con variables de color bien establecidas (`--brand-accent`, etc.).
   - Escribe el Markdown: `[Ruta del Cliente]/brand-assets/BRAND_MANUAL.md`.
3. **Conversión a PDF Exclusiva:** 
   - Genera inmediatamente el PDF asociado (`BRAND_MANUAL.pdf`) usando las herramientas del sistema (ej. Puppeteer desde JS, wkhtmltopdf, pdfkit en Python, o tu navegador subagente, según tu capacidad y las librerías activadas).
   - Ejemplo: Escribe y ejecuta un script de NodeJS `generate_pdf.js` usando `puppeteer` en la carpeta para lograr la conversión limpia con el fondo incluido (`printBackground: true`). Si no tienes dependencias y necesitas ayuda, usa bash commands instalando temporalmente con npm en local el `puppeteer` exportarlo y generar el `BRAND_MANUAL.pdf`.
4. Borra el script temporal generador luego del éxito.
5. NO modifiques ni actualices información relacionada a Notion (Este workflow es 100% offline y local tras su ejecución).

## Paso 4: Finalización y Confirmación
1. Verifica por última vez la disponibilidad de archivos (MD, HTML, PDF) en `[Ruta del Cliente]/brand-assets/`.
2. Notifica el cierre del proceso.
