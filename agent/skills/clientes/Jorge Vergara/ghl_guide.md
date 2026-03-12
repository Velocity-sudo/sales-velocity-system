# Guía de Implementación en GoHighLevel: Jorge Vergara Taxes 2026

Esta guía detalla cómo montar la landing page mobile-first, las páginas puente de redirección para tracking y configurar todo en GoHighLevel (GHL).

## 1. Crear la Landing Page en GHL

1.  Ve a **Sites > Funnels** y crea un nuevo Funnel llamado `Jorge Taxes 2026 - VSL`.
2.  Añade un **New Step** llamado `Landing`. Path: `/` o `/impuestos`.
3.  Haz clic en **Edit** para abrir el builder.
4.  **IMPORTANTE**: Para asegurar que el diseño sea perfecto y sin conflictos con estilos de GHL, usaremos un elemento "Custom HTML" para todo el contenido.
    *   Añade una **Section** (Full Width).
    *   Añade una **1 Column Row**.
    *   Añade el elemento **Custom JS/HTML**.
    *   Pega **TODO** el código del archivo `final_landing_page.html` dentro de este elemento.
5.  **Reemplaza los PLACEHOLDERS** en el código antes de guardar:
    *   `[VSL_EMBED_URL_AQUI]`: Pega la URL del video (Youtube/Vimeo/Wistia). Asegúrate que sea la URL "Embed" (ej: `https://www.youtube.com/embed/VIDEO_ID`).
    *   `[GHL_BASE_URL_AQUI]`: Tu dominio conectado en GHL (ej: `https://asesoriajorge.com`).
    *   `[LOGO_O_FOTO_URL_AQUI]`: Sube la foto de Jorge a GHL Media y pega el link aquí.

## 2. Crear las Páginas Puente (Redirects)

Para medir clicks internos sin usar Google Tag Manager complejo, usaremos páginas intermedias en GHL.

### Página: /go/book (Click en Agendar)
1.  Crea un **New Step** en el funnel llamado `Go Book`.
2.  Path: `/go/book`
3.  Edita la página.
4.  Añade un elemento **Code** o script en el Header (Settings > Tracking Code > Header Code) con este Javascript:
    ```html
    <script>
      // 1. Opcional: Disparar evento a Facebook Pixel
      // fbq('track', 'InitiateCheckout'); 
      
      // 2. Redirigir al Calendario
      // Preservar UTMs si existen
      const params = window.location.search;
      const calendarUrl = "https://link.al.calendario/widget/booking" + params; 
      
      setTimeout(function(){
        window.location.href = calendarUrl;
      }, 300); // Pequeño delay para asegurar que el pixel dispare si se usa
    </script>
    ```
    *Nota: Si prefieres usar la herramienta nativa de GHL, simplemente pon el elemento "Calendar" en esta página en lugar de redirigir, pero el redirect es más limpio para tracking.*

### Página: /go/watch (Click en Video - Opcional)
Si quieres medir cuánta gente hace click para activar el sonido o play (si no es autoplay), necesitarías un overlay custom.
*Para esta versión simplificada, asumimos que el video está embebido directamente en la home.*

## 3. Configuración de UTMs

Tu campaña de anuncios debe usar estos parámetros en el link del anuncio:

`https://tudominio.com/?utm_source=instagram&utm_medium=paid&utm_campaign=jorge_taxes_2026`

El script incluido en la Landing Page (`final_landing_page.html`) tomará estos parámetros y se asegurará de que cuando la persona haga click en "Agendar", pasen a la página de agendamiento.

## 4. Verificación y Pruebas

1.  Abre la página en tu celular en modo Incógnito con parámetros de prueba:
    `.../impuestos?utm_source=test&utm_medium=me`
2.  Verifica que el **Video** se vea completo sin hacer scroll (o con muy poco scroll).
3.  Haz scroll hacia abajo. Verifica que aparezca el **Botón Flotante (Sticky CTA)** en la parte inferior.
4.  Haz click en "Agendar". Verifica que la URL de destino tenga `?utm_source=test...`.

---
**Nota sobre Estilos**: El código lleva su propio CSS reset y diseño. No necesitas configurar tipografías ni colores en el menú "Settings" del editor de GHL, ya que el código HTML es autosuficiente.
