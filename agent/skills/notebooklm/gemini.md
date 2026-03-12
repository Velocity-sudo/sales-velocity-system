# 📜 NotebookLM Skill - Project Constitution

> **Status:** ✅ Phase 2 Complete - Installation & Configuration Done
> **Last Updated:** 2026-02-08
> **Account:** marca@luchobranding.com

---

## 🎯 North Star
NotebookLM será el **cerebro** de los agentes de Sales Velocity. Cada agente tendrá acceso a notebooks específicos con conocimiento especializado.

---

## 🔗 Integraciones
- **N8N:** Orquestación de workflows
- **Notion:** Fuente primaria de datos de clientes
- **Google Drive:** Almacenamiento de documentos
- **NotebookLM:** Base de conocimiento de agentes

---

## 📍 Source of Truth
- **Clientes:** Notion
- **Conocimiento:** NotebookLM notebooks

---

## 📦 Delivery Payload
El agente consultará NotebookLM y escribirá el resultado en Notion (Entregables).

---

## 📊 Data Schema

### Input Schema
```json
{
  "notebook_id": "string (from notebook list)",
  "query": "string (question to ask the notebook)"
}
```

### Output Schema
```json
{
  "response": "string (AI-generated answer)",
  "sources": ["array of source citations"]
}
```

---

## ⚖️ Behavioral Rules
1. Consultar el notebook correcto según el tipo de entregable
2. Siempre citar las fuentes del notebook
3. Responder en español (70% clientes hispanohablantes)

---

## 🏛️ Architectural Invariants

1. NotebookLM no tiene API oficial - usa browser cookies
2. Autenticación guardada en `~/.notebooklm-mcp-cli/profiles/default`
3. MCP Server: `/opt/homebrew/bin/notebooklm-mcp`

---

## 📝 Maintenance Log

| Date | Change | Reason |
|------|--------|--------|
| 2026-02-08 | Created project constitution | Protocol 0 initialization |
| 2026-02-08 | Installed notebooklm-mcp-cli | Phase 2: Link |
| 2026-02-08 | Authenticated with Google | 47 cookies extracted |
| 2026-02-08 | Added to mcp_config.json | MCP server configured |


---

## 🏛️ Architectural Invariants

1. NotebookLM is a Google product for AI-powered research
2. Cannot be accessed via API (as of Feb 2026)
3. Interaction must be through browser automation or manual workflows

---

## 📝 Maintenance Log

| Date | Change | Reason |
|------|--------|--------|
| 2026-02-08 | Created project constitution | Protocol 0 initialization |
