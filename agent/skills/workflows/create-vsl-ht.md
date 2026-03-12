---
description: Sales Velocity System workflow to create high-converting High Ticket VSLs and Landing Pages.
---

# 🚀 Workflow: Create VSL High Ticket (`/create-vsl-ht`)

Este workflow orquesta la creación de Video Sales Letters (VSLs) de alta conversión para ofertas *High Ticket*, integrando la oferta Grand Slam, la base de conocimiento del cliente y estructurando la salida tanto en local como en Notion.

## 📋 Requisitos Previos (Contexto Necesario)
Antes de iniciar, el Agente debe confirmar que tiene en contexto:
1. El **nombre del cliente**.
2. La **Oferta 100M** (Grand Slam Offer) desarrollada para el cliente.
3. La **Base de Conocimiento** general del cliente.

*(Si falta algo, el Agente debe pedirlo o buscarlo proactivamente utilizando sus capacidades de búsqueda local / Notion).*

---

## 🛠 Ejecución Paso a Paso

1. **Lectura de la Plantilla Maestra en Notion**
   - Utiliza tus herramientas de acceso a Notion / Web para leer detalladamente la [Plantilla Maestra VSL High Ticket](https://www.notion.so/VSL-HIGH-TICKET-Nombre-del-Cliente-303e0f376c6d81dbaa2af73cb6acac1f).
   - Asimila las instrucciones exclusivas de esta plantilla para la estructura del Guión, el Copy de la Landing, y cómo se debe formatear el Prompt de Antigravity (que debe ir estrictamente en un bloque de código).

2. **Generación del Contenido (Activando el skill `creating-vsl`)**
   - Aplica el conocimiento del skill global `creating-vsl` e intégralo con las instrucciones que obtuviste de la plantilla de Notion en el paso 1.
   - Usa la oferta 100M y el conocimiento del cliente para redactar el contenido exacto requerido:
     - **Parte 1:** El Guión del VSL High Ticket (Estructurado para lectura en teleprompter / formato VSL).
     - **Parte 2:** La Estructura del Copy y la Landing Page.
     - **Parte 3:** El Prompt de Antigravity, configurado con las variables del cliente y contenido generado, enmarcado en un `code block`.

// turbo
3. **Creación del Archivo Local Markdown**
   - Combina las 3 partes generadas en un único archivo Markdown limpio y bien formateado.
   - Crea el archivo guardándolo obligatoriamente en la carpeta local del CRM del cliente:
     `~/Desktop/Clientes/[Nombre del Cliente]/VSL-HT.md`
   - *(Si el directorio del cliente no existe, usa la terminal para crearlo con `mkdir -p "~/Desktop/Clientes/[Nombre del Cliente]"` antes de escribir el archivo).*

4. **Creación de la Página Definitiva en Notion**
   - Apóyate en el skill `managing-notion` para interactuar con la API de Notion.
   - Busca la página principal / base de datos del cliente correspondiente en el espacio de trabajo.
   - **Crea una sub-página nueva** (Title: `VSL HIGH TICKET - [Nombre del Cliente]`) que sea hija de la página del cliente.
   - Inserta el contenido estructurado como bloques de Notion, replicando fielmente el formato estético e instruccional de la Plantilla Maestra original.

5. **Entrega de Resultados (Handoff)**
   - Imprime en el chat un mensaje de "Éxito" confirmando que el workflow ha terminado.
   - Proporciona el enlace local clickeable para abrir el archivo MD en VSCode/Cursor (`VSL-HT.md`).
   - Proporciona el enlace directo a la nueva página creada en Notion.
