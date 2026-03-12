---
description: Sales Velocity System workflow to create the Master Plan (Plan Maestro) for a client. Consolidates context, objectives, strategy, and tasks into a single Notion page.
---

# 🔥 Workflow: Create Master Plan (`/create-master-plan`)

Este workflow crea el **PLAN MAESTRO** del cliente — el documento estratégico central que consolida contexto, objetivos, paso a paso, estrategia y tareas tanto para el equipo como para el cliente.

> **El Plan Maestro es el PRIMER entregable visible al cliente.** Es la hoja de ruta completa del proyecto.

---

## 📋 Requisitos Previos

Antes de iniciar, el Agente debe confirmar:
1. El **nombre del cliente**.
2. Acceso a la **Base de Conocimiento** del cliente (transcripciones de onboarding, cuestionario inicial, reuniones).
3. Si existen: la **OFERTA 100M** y el **VSL High Ticket** ya creados.

*(Si falta información crítica, el Agente DEBE preguntarle a Niko antes de proceder. NO inventar datos.)*

---

## 🛠 Ejecución Paso a Paso

### Paso 1: Activar `managing-notion` — Localizar al Cliente
- Buscar la página del cliente en **Procesos de Clientes** (`2f7e0f37-6c6d-8148-94ce-ca5cc5d53b9d`).
- Obtener el `page_id` del cliente.
- Listar las sub-páginas hijas del cliente para identificar entregables existentes:
  - ¿Tiene `OFERTA 100M - [Cliente]`? → Si sí, leer su contenido completo.
  - ¿Tiene `VSL HIGH TICKET - [Cliente]`? → Si sí, leer su contenido completo.
  - ¿Tiene `ADS QUE CONVIERTEN - [Cliente]`? → Si sí, leer su contenido completo.
  - ¿Tiene `Base de Conocimiento`? → Buscar en sub-páginas o en el directorio local `~/Desktop/Clientes/[Cliente]/`.

### Paso 2: Recopilar y Sintetizar el Contexto del Cliente
Con toda la información recopilada, extraer:
- **CONTEXTO**: ¿Quién es el cliente? ¿A quién sirve? ¿Situación actual? ¿Ventaja competitiva? ¿Por qué contrató a Sales Velocity?
- **OBJETIVOS**: 2-4 objetivos concretos y medibles (validación, métricas, orgánico, escala).
- **ESTRATEGIA**: 3 párrafos (Oferta Diferenciada, Sistema de Ventas, Sistema de Adquisición).
- **PASO A PASO**: El pipeline estándar de Sales Velocity (Oferta → Sistema de Ventas → Sistema de Adquisición), vinculando los entregables existentes.
- **TAREAS DEL CLIENTE**: Tareas operativas que el cliente debe completar (Grabar VSL, Grabar Ads, Recopilar Casos de Éxito).
- **TAREAS SECUNDARIAS**: Accesos e insumos que el cliente debe proveer (Meta Ads, GHL, Logo, Slack, etc.).

> ⚠️ **REGLA CRÍTICA**: Si un dato no está disponible, escribir `[PENDIENTE — consultar con Niko o con el cliente]`. NUNCA inventar datos.

### Paso 3: Verificar Información Faltante (Checkpoint)
Antes de crear el documento, revisar si hay campos marcados como `[PENDIENTE]`:
- Si hay **más de 3 campos pendientes críticos** (contexto + objetivos), **PAUSAR** y preguntarle a Niko qué datos puede proveer.
- Si son campos menores (tareas secundarias como accesos), proceder y marcarlos como pendientes.

// turbo
### Paso 4: Crear el Archivo Local Markdown
- Crear el archivo en la carpeta local del cliente:
  `~/Desktop/Clientes/[Nombre del Cliente]/plan_maestro_[nombre_del_cliente].md`
- *(Si el directorio no existe, crearlo con `mkdir -p`).*
- Formato: Markdown limpio con todas las secciones del Plan Maestro.

### Paso 5: Leer la Plantilla Maestra de Notion
- Leer la estructura y bloques de la **Plantilla PLAN MAESTRO** en Notion:
  - Template ID: `313e0f37-6c6d-801c-aa64-e59ff3a534e8`
  - URL: https://www.notion.so/PLAN-MAESTRO-Nombre-del-cliente-313e0f376c6d801caa64e59ff3a534e8
- Asimilar las instrucciones de cada bloque azul (INSTRUCCIONES PARA LA IA) para replicar la estructura exacta.

### Paso 6: Crear la Página del Plan Maestro en Notion
- Utilizar el skill `managing-notion` para crear una **página hija** dentro de la página principal del cliente.
- **Título**: `🔥 PLAN MAESTRO - [Nombre del Cliente]`
- **Icono**: 🔥
- **Estructura de bloques** (replicar EXACTAMENTE la plantilla):

  1. **H2**: `🔍 CONTEXTO` (gray_background)
     - Quote block azul con instrucciones de la IA (copiar de la plantilla)
     - Párrafos en gris itálica con el contenido real del cliente

  2. **Divider**

  3. **H2**: `🎯 OBJETIVOS` (yellow_background)
     - Quote block azul con instrucciones de la IA
     - Numbered list con los objetivos del cliente

  4. **H2**: `📝 PASO A PASO A SEGUIR` (green_background)
     - Quote block azul con instrucciones de la IA
     - Numbered list con los pasos del pipeline, vinculando entregables existentes con @mentions

  5. **H2**: `💡 ESTRATEGIA` (purple_background)
     - Quote block azul con instrucciones de la IA
     - 3 párrafos de estrategia personalizada

  6. **Divider**

  7. **H2**: `✅ TUS TAREAS` (orange_background)
     - Quote block azul con instrucciones de la IA
     - Sub-páginas de tareas: `1 - GRABAR VSL y TY Page`, `2 - GRABAR ADS`, `3 - RECOPILAR CASOS DE ÉXITO`

  8. **H2**: `📋 TUS TAREAS SECUNDARIAS` (orange_background)
     - Quote block azul con instrucciones de la IA
     - Checklist (to_do blocks) con los accesos pendientes

  9. **Callout** (🤖 red_background): Instrucciones maestras para la IA (copiar de la plantilla)

### Paso 7: Entrega de Resultados (Handoff)
- Confirmar con mensaje de éxito:
  - ✅ Enlace al archivo local `.md`
  - ✅ Enlace directo a la nueva página en Notion
  - ✅ Lista de campos marcados como `[PENDIENTE]` que requieren acción

---

## 🚨 Reglas Críticas

1. **NO inventar datos**. Si no está en la base de conocimiento, es PENDIENTE.
2. **NO copiar de otro cliente**. Cada Plan Maestro es 100% único.
3. **Los bloques azules de instrucciones** de la IA se mantienen en la plantilla. Se replican tal cual.
4. **El Plan Maestro vive como página hija** de la página principal del cliente en Procesos de Clientes.
5. **Los textos en gris itálica** se reemplazan con contenido real del cliente.
6. **Siempre vincular** (con @mention) los entregables que ya existan (Oferta 100M, VSL, Ads).

---

## 📐 Referencia Rápida — IDs de Notion

| Recurso | ID |
|---|---|
| Procesos de Clientes | `2f7e0f37-6c6d-8148-94ce-ca5cc5d53b9d` |
| Clientes Database | `2f7e0f37-6c6d-81b6-9cba-df48640f2afe` |
| Plantilla Plan Maestro | `313e0f37-6c6d-801c-aa64-e59ff3a534e8` |
| Plantillas de Presentación | `303e0f37-6c6d-80be-9628-e919582f3b46` |
