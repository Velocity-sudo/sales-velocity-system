---
name: Notion Automation
description: Best practices and patterns for working with Notion API efficiently, including page creation, block management, and performance optimization
---

# Notion Automation Skill

Este skill contiene las mejores prácticas para trabajar eficientemente con la API de Notion.

## Principios Fundamentales

### 1. **Crear Nueva Página vs. Borrar Bloques Existentes**

**REGLA DE ORO: Si borrar bloques se demora más de 10 segundos, CREA UNA PÁGINA NUEVA.**

#### ❌ Enfoque Lento (Evitar)
```typescript
// Borrar todos los bloques de una página existente
async function deleteAllBlocks(pageId: string) {
    const { results } = await notion.blocks.children.list({ block_id: pageId });
    for (const block of results) {
        await notion.blocks.delete({ block_id: block.id });
    }
}
// Esto puede tomar MINUTOS si la página tiene muchos bloques
```

#### ✅ Enfoque Rápido (Preferido)
```typescript
// Crear una nueva página en su lugar
const newPage = await notion.pages.create({
    parent: { page_id: PARENT_PAGE_ID },
    properties: {
        title: {
            title: [{ text: { content: 'Título de la Página Nueva' } }]
        }
    }
});
// Esto toma SEGUNDOS, no minutos
```

#### Cuándo usar cada enfoque:

| Situación | Acción |
|-----------|--------|
| Actualización menor (< 10 bloques) | ✅ Puedes borrar y recrear |
| Actualización completa de página | ✅ Crear nueva página |
| Script se demora > 10 segundos borrando | ✅ Cancela y crea nueva página |
| Necesitas mantener el mismo ID de página | ⚠️ Borrar (pero advierte al usuario) |

### 2. **Batch Processing para Bloques**

Siempre agrupa bloques en batches de 100 (límite de Notion):

```typescript
async function appendBlocks(pageId: string, blocks: any[]) {
    const BATCH_SIZE = 100;
    for (let i = 0; i < blocks.length; i += BATCH_SIZE) {
        const batch = blocks.slice(i, i + BATCH_SIZE);
        await notion.blocks.children.append({ 
            block_id: pageId, 
            children: batch 
        });
        console.log(`Batch ${Math.floor(i / BATCH_SIZE) + 1} agregado`);
    }
}
```

### 3. **Rich Text Builders (Helpers Reutilizables)**

```typescript
// Helper para crear rich text
const rt = (content: string, bold = false, italic = false) => ({
    type: 'text' as const,
    text: { content },
    annotations: { 
        bold, italic, 
        strikethrough: false, 
        underline: false, 
        code: false, 
        color: 'default' 
    }
});

// Helper para párrafos
const p = (...parts: ReturnType<typeof rt>[]) => ({
    object: 'block' as const,
    type: 'paragraph' as const,
    paragraph: { rich_text: parts, color: 'default' as const }
});

// Uso:
blocks.push(p(
    rt('Texto normal '),
    rt('texto en negrita', true),
    rt(' y algo en ', false),
    rt('cursiva', false, true)
));
```

### 4. **Block Builders Comunes**

```typescript
// Heading 1
const h1 = (text: string, bold = true) => ({
    object: 'block' as const,
    type: 'heading_1' as const,
    heading_1: {
        rich_text: [{ 
            type: 'text' as const, 
            text: { content: text }, 
            annotations: { bold, italic: false, strikethrough: false, underline: false, code: false, color: 'default' } 
        }],
        is_toggleable: false,
        color: 'default' as const
    }
});

// Heading 3
const h3 = (text: string, bold = true) => ({
    object: 'block' as const,
    type: 'heading_3' as const,
    heading_3: {
        rich_text: [{ 
            type: 'text' as const, 
            text: { content: text }, 
            annotations: { bold, italic: false, strikethrough: false, underline: false, code: false, color: 'default' } 
        }],
        is_toggleable: false,
        color: 'default' as const
    }
});

// Divider
const divider = () => ({
    object: 'block' as const,
    type: 'divider' as const,
    divider: {}
});

// Empty paragraph
const empty = () => ({
    object: 'block' as const,
    type: 'paragraph' as const,
    paragraph: { rich_text: [], color: 'default' as const }
});

// Bullet list item
const bullet = (text: string) => ({
    object: 'block' as const,
    type: 'bulleted_list_item' as const,
    bulleted_list_item: { 
        rich_text: [rt(text)], 
        color: 'default' as const 
    }
});

// Numbered list item
const numbered = (...parts: ReturnType<typeof rt>[]) => ({
    object: 'block' as const,
    type: 'numbered_list_item' as const,
    numbered_list_item: { 
        rich_text: parts, 
        color: 'default' as const 
    }
});
```

## Workflow Típico

### Crear Nueva Página con Contenido

```typescript
import { Client } from '@notionhq/client';
import dotenv from 'dotenv';

dotenv.config();

const notion = new Client({ auth: process.env.NOTION_API_KEY });

async function main() {
    // 1. Crear la página
    console.log('📝 Creando página...');
    const newPage = await notion.pages.create({
        parent: { page_id: PARENT_PAGE_ID },
        properties: {
            title: {
                title: [{ text: { content: 'Mi Nueva Página' } }]
            }
        }
    });
    
    console.log(`✅ Página creada: ${newPage.id}`);
    
    // 2. Construir bloques
    const blocks = buildAllBlocks();
    console.log(`📦 ${blocks.length} bloques preparados`);
    
    // 3. Agregar bloques en batches
    console.log('📤 Agregando bloques...');
    await appendBlocks(newPage.id, blocks);
    
    console.log('✅ Listo!');
}

main().catch(console.error);
```

## Anti-Patterns (Evitar)

❌ **NO hacer esto:**
```typescript
// Borrar página por página en loop sin batch
for (const block of results) {
    await notion.blocks.delete({ block_id: block.id }); // MUY LENTO
}
```

❌ **NO hacer esto:**
```typescript
// Agregar bloques uno por uno
for (const block of blocks) {
    await notion.blocks.children.append({ 
        block_id: pageId, 
        children: [block] 
    }); // SÚPER LENTO
}
```

## Manejo de Errores

```typescript
try {
    await notion.pages.create({...});
} catch (error) {
    if (error.code === 'object_not_found') {
        console.error('❌ La página padre no existe o no está compartida');
    } else if (error.code === 'unauthorized') {
        console.error('❌ API key inválida o sin permisos');
    } else {
        console.error('❌ Error:', error.message);
    }
}
```

## Variables de Entorno

```bash
# .env
NOTION_API_KEY=secret_xxxxxxxxxxxxx
```

## Testing Rápido

Para verificar que la conexión funciona antes de ejecutar scripts largos:

```typescript
// test-notion.ts
const notion = new Client({ auth: process.env.NOTION_API_KEY });

async function test() {
    const user = await notion.users.me({});
    console.log('✅ Conectado como:', user.name || user.id);
}

test();
```

## Resumen: Decision Tree

```
¿Necesitas actualizar una página?
│
├─ ¿Tiene < 10 bloques?
│  └─ ✅ Borra y recrea
│
├─ ¿Tiene > 10 bloques?
│  └─ ✅ Crea nueva página
│
└─ ¿El borrado se demora > 10 segundos?
   └─ ✅ CANCELA y crea nueva página
```

## Ejemplos en el Proyecto

- `/src/scripts/create_christian_vsl_complete.ts` - Ejemplo COMPLETO de página con 3 partes

## Estructura de Páginas VSL (Best Practice)

Para páginas de VSL High Ticket, siempre incluir estas 3 secciones:

1.  **Guion VSL (Script):** Formato diálogo palabra por palabra.
2.  **Landing Page Copy:** Estructura de ventas (Hero, Prueba Social, Oferta, CTA).
3.  **Prompt Antigravity:** El prompt usado para generar el código, visible para referencia futura.

## Patrón "Strict Prompt" (Prompt Listo para Usar)

Para maximizar la eficiencia, **NO** entregues prompts con placeholders vacíos (ej: `[INSERTAR TEXTO AQUÍ]`).

### El Problema
Entregar un prompt genérico obliga al usuario a:
1. Copiar el prompt.
2. Copiar el VSL Script.
3. Copiar el Landing Page Copy.
4. Unir todo manualmente en el chat del LLM.

### La Solución: "Strict Prompt"
Genera el prompt final **dentro de tu script**, inyectando el contenido generado en las variables correspondientes.

```typescript
// Define el template con variables
const PROMPT_TEMPLATE = `... INPUT 1: {{VSL_SCRIPT}} ...`;

// Inyecta el contenido REAL que acabas de generar
const populatedPrompt = PROMPT_TEMPLATE.replace('{{VSL_SCRIPT}}', finalVslScript);

// Crea un bloque de código con el prompt LISTO
blocks.push(codeBlock(populatedPrompt));
```

### Ventajas
- **Zero Friction:** El usuario solo hace clic en "Copiar" y "Pegar" en Claude/GPT.
- **Single Source of Truth:** El prompt en Notion refleja *exactamente* lo que se usó (o se debe usar) para generar el código, sin errores humanos de copy-paste.


