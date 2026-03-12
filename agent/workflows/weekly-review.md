---
description: Reporte semanal de tareas pendientes por cliente. Ejecutar cada domingo al mediodía. Genera un resumen organizado de todos los pendientes, lo que se completó y lo que falta.
---
# /weekly-review — Reporte Semanal de Pendientes

## Cuándo ejecutar
Cada **domingo a las 12:00pm**. Lucho abre un chat y escribe `/weekly-review`.

## Pasos

### 1. Obtener todos los clientes activos
// turbo-all
- Query la **Clientes Database** (`2f7e0f37-6c6d-81b6-9cba-df48640f2afe`) para obtener la lista de clientes activos.
- Guardar los IDs y nombres de cada cliente.

### 2. Query la Tasks DB completa
- Query la **Tasks DB** (`2f7e0f37-6c6d-811e-8086-ff5ac19e8f3c`) para obtener TODAS las tareas.
- Filtrar solo tareas que NO están en trash.
- Agrupar por Project (cliente).

### 3. Clasificar tareas por cliente
Para cada cliente, separar las tareas en 3 categorías:
- **✅ Completado esta semana**: Status = `Done` y última edición dentro de los últimos 7 días
- **🔴 Pendiente (vencido)**: Status ≠ `Done` y Due Date < hoy
- **🟡 Pendiente (próximo)**: Status ≠ `Done` y Due Date >= hoy
- **⏳ Sin fecha**: Status ≠ `Done` y sin Due Date

### 4. Generar el reporte
Crear un resumen en formato tabla con esta estructura:

```
# 📋 Reporte Semanal — [Fecha]

## 🔥 Resumen Ejecutivo
- Total tareas activas: X
- Completadas esta semana: X
- Vencidas: X (¡ATENCIÓN!)
- Próximas: X

---

## [Emoji] Cliente 1 — [X pendientes]

### ✅ Completado
| Tarea | Fecha |
|---|---|

### 🔴 Vencido
| Tarea | Due Date | Asignado |
|---|---|---|

### 🟡 Próximo
| Tarea | Due Date | Asignado |
|---|---|---|

---
(Repetir por cada cliente)

## 🏢 Tareas Internas (Lucho Branding)
(Tareas sin proyecto asignado o internas)
```

### 5. Guardar el reporte
- Guardar como `~/Desktop/Clientes/LuchoBranding/reportes_semanales/weekly_review_YYYY-MM-DD.md`
- Si la carpeta `reportes_semanales` no existe, crearla.

### 6. Actualizar tareas si necesario
- Si hay tareas que claramente ya están hechas pero siguen en `To Do`, preguntar a Lucho si marcarlas como `Done`.
- Si hay tareas sin fecha o sin asignado, sugerir asignarlas.

### 7. Presentar al usuario
- Mostrar el resumen ejecutivo directamente en el chat.
- Presentar el reporte completo con `notify_user` adjuntando el archivo .md generado.
- Incluir recomendaciones sobre qué priorizar esta semana.
