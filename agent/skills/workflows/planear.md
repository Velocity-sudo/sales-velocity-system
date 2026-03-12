---
description: Planear un proyecto antes de ejecutarlo. Usa /planear [nombre] para activar. SIEMPRE planear antes de construir.
---

# 📐 Workflow: Planear Proyecto

> **Regla #1:** NO se ejecuta nada hasta que el usuario apruebe el plan.
> Este workflow se activa con `/planear [nombre del proyecto]` y produce un plan de implementación antes de tocar cualquier archivo.

---

## Fase 1 — DEFINIR (2 min)

Presenta al usuario un resumen claro respondiendo estas preguntas:

```
📌 PROYECTO: [Nombre]
🎯 OBJETIVO: ¿Qué vamos a lograr? (1 oración)
📦 ENTREGABLE: ¿Qué se entrega al final? (archivos, skills, páginas, etc.)
👤 PARA QUIÉN: ¿Cliente específico o uso interno?
⏱ COMPLEJIDAD: 🟢 Simple (< 30 min) | 🟡 Medio (1-3 hrs) | 🔴 Complejo (> 3 hrs)
```

**Si falta información, PREGUNTA antes de continuar.**

---

## Fase 2 — INVESTIGAR (5-10 min)

Antes de planear los pasos, investiga qué ya existe:

1. **Revisar Knowledge Items (KIs):** ¿Ya hay trabajo previo sobre este tema?
2. **Revisar `conocimiento/proyectos.md`:** ¿Hay un proyecto relacionado activo o completado?
3. **Revisar Skills existentes:** ¿Hay un skill en `~/.agent/skills/` que aplique?
4. **Revisar Workflows existentes:** ¿Hay un workflow en `~/.agent/workflows/` que ya cubra esto?
5. **Revisar NotebookLM:** ¿Hay un notebook con conocimiento relevante?
6. **Revisar Notion:** ¿Hay datos del cliente o proyecto en Notion?
7. **Web research (si aplica):** ¿Necesitamos información externa? (Firecrawl, búsqueda web)

**Reportar al usuario:**
```
🔍 INVESTIGACIÓN:
- Ya existe: [qué encontramos]
- No existe: [qué hay que crear desde cero]
- Reutilizable: [qué podemos aprovechar]
```

---

## Fase 3 — DESGLOSAR (5 min)

Divide el proyecto en fases claras con mini-entregables. Usa este formato:

```
📋 PLAN DE IMPLEMENTACIÓN
━━━━━━━━━━━━━━━━━━━━━━━━

Fase 1: [Nombre] ⏱ ~[tiempo estimado]
  □ Paso 1.1: [Acción concreta]
  □ Paso 1.2: [Acción concreta]
  → Entregable: [qué se produce]

Fase 2: [Nombre] ⏱ ~[tiempo estimado]
  □ Paso 2.1: [Acción concreta]
  □ Paso 2.2: [Acción concreta]
  → Entregable: [qué se produce]

Fase 3: [Nombre] ⏱ ~[tiempo estimado]
  □ Paso 3.1: [Acción concreta]
  → Entregable: [qué se produce]

━━━━━━━━━━━━━━━━━━━━━━━━
⏱ TIEMPO TOTAL ESTIMADO: [suma]
```

---

## Fase 4 — DEPENDENCIAS Y RIESGOS (2 min)

Identifica qué puede bloquear o complicar el proyecto:

```
⚡ DEPENDENCIAS:
- [ ] [Lo que necesitamos ANTES de empezar — accesos, datos, aprobaciones]

⚠️ RIESGOS:
- [Qué podría salir mal y cómo lo mitigamos]

🔧 TOOLS QUE VAMOS A USAR:
- [Lista de herramientas/MCPs/skills que necesitamos]
```

---

## Fase 5 — PRESENTAR PLAN (Checkpoint de Aprobación)

Presenta el plan completo al usuario con este formato:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📐 PLAN: [NOMBRE DEL PROYECTO]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 Objetivo: [1 oración]
📦 Entregables: [lista]
⏱ Tiempo estimado: [total]
🔧 Tools: [lista]

📋 FASES:
[El desglose de la Fase 3]

⚡ DEPENDENCIAS:
[De la Fase 4]

⚠️ RIESGOS:
[De la Fase 4]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
¿Apruebas el plan? (Sí / Ajustar / Cancelar)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**ESPERAR la respuesta del usuario.**
- **Sí** → Continuar a Fase 6
- **Ajustar** → Modificar según feedback y volver a presentar
- **Cancelar** → No ejecutar nada

---

## Fase 6 — EJECUTAR CON CHECKPOINTS

Una vez aprobado, ejecuta fase por fase:

1. **Antes de cada fase:** Anuncia qué vas a hacer
   ```
   ▶️ Ejecutando Fase [N]: [Nombre]...
   ```

2. **Después de cada fase:** Reporta qué se completó
   ```
   ✅ Fase [N] completada:
   - [Lo que se hizo]
   - [Archivos creados/modificados]
   ```

3. **Al terminar todo:** Presenta resumen final
   ```
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   ✅ PROYECTO COMPLETADO: [NOMBRE]
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   
   📦 Entregables:
   - [Lista de archivos/recursos creados]
   
   📍 Ubicaciones:
   - [Dónde quedó cada cosa]
   
   📝 Siguiente paso sugerido:
   - [Qué viene después, si aplica]
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   ```

4. **Actualizar `conocimiento/proyectos.md`** con el resultado del proyecto

---

## 🔑 Reglas del Workflow

1. **NUNCA ejecutar sin plan aprobado** — Si el usuario pide algo grande, activa este workflow automáticamente
2. **Mantener al usuario informado** — Cada fase tiene un checkpoint visible
3. **Investigar antes de crear** — No reinventar lo que ya existe
4. **Adaptarse** — Si a mitad de ejecución aparece un blocker, pausar y re-planear
5. **Documentar** — Al final, actualizar proyectos.md y hacer commit/push

---

## 📎 Cuándo Activar Este Workflow

| Tipo de tarea | ¿Planear? |
|---|---|
| Crear un skill nuevo | ✅ Sí |
| Setup de cliente nuevo | ✅ Sí |
| Proyecto multi-fase | ✅ Sí |
| Investigación profunda | ✅ Sí |
| Corrección rápida / bug fix | ❌ No, ejecutar directo |
| Pregunta de información | ❌ No, responder directo |
| Edición menor de un archivo | ❌ No, ejecutar directo |
| Tarea con > 3 pasos | ✅ Sí |

> **Regla de oro:** Si el proyecto tiene más de 3 pasos o toca más de 2 archivos/sistemas → PLANEAR PRIMERO.
