# 🔧 NotebookLM MCP Server - Guía de Instalación

## Paso 1: Instalar el paquete

**Con uv (recomendado):**
```bash
uv tool install notebooklm-mcp-cli
```

**Con pip (alternativa):**
```bash
pip install notebooklm-mcp-cli
```

---

## Paso 2: Autenticación con Google

> ⚠️ **Importante:** Cierra sesión de Chrome en todos los navegadores antes de este paso.

```bash
nlm login
```

Esto abrirá Chrome automáticamente para que inicies sesión en tu cuenta de Google.

---

## Paso 3: Verificar instalación

```bash
nlm notebooks list
```

Deberías ver una lista de tus notebooks de NotebookLM.

---

## Paso 4: Configurar MCP

Una vez autenticado, agregar a tu `mcp_config.json`:

```json
{
  "mcpServers": {
    "notebooklm": {
      "command": "notebooklm-mcp",
      "args": []
    }
  }
}
```

---

## Ubicaciones comunes del archivo MCP config:
- `~/.config/opencode/opencode.json`
- `~/.cursor/mcp.json`
- `~/.vscode/mcp.json`

---

## Troubleshooting

**Si falla la autenticación:**
```bash
rm -rf ~/.notebooklm-mcp-cli
nlm login
```

**Verificar estado de auth:**
```bash
nlm login --check
```
