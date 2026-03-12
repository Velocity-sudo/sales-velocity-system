# Security Hardening Guide (3-Tier Model)

## Threat Model

OpenClaw has access to your file system, APIs, and messaging channels. Threats include:
- **Prompt injection** via inbound messages (malicious text to hijack agent)
- **Skill poisoning** via ClawHub (~15% potentially malicious)
- **Data exfiltration** via tool abuse (agent sends private data externally)
- **Remote code execution** via unconstrained shell access
- **Credential theft** via exposed API keys or OAuth tokens

---

## Tier 1: Basic Protection (Minimum Viable)

**Goal: Isolation and access control**

### Network
- Bind Gateway to `127.0.0.1` (never `0.0.0.0`)
- Use Tailscale or SSH tunnels for remote access
- Set firewall: `ufw default deny incoming`

### Authentication
- Set `dmPolicy: "pairing"` (requires code for new users)
- Better: `dmPolicy: "allowlist"` (blocks all unknown users)
- **NEVER** use `dmPolicy: "open"`

### File System
- Restrict to workspace directory only
- Deny: `~/.ssh`, `~/.aws`, `~/.env`, `/etc/passwd`
- Use `security.sandbox.allowedPaths` / `deniedPaths`

### Deployment
- Run on **VPS** (Hetzner $4/mo, DigitalOcean $6/mo), NOT personal machine
- Keep OS and Node.js updated
- Use dedicated user account (non-root)

---

## Tier 2: Standard Protection (Recommended)

**Goal: Principle of least privilege**

### Tool Control
- **Allowlist** tools instead of denylist (attackers bypass denylists)
- Only allow: `ls`, `grep`, `cat`, `node`, specific binaries
- Block: `curl`, `wget`, `ssh`, `nc`, `python` (unless needed)

### MCP Security
- Pin versions: `"version": "0.3.0"`, `autoUpdate: false`
- Disable `filesystem` and `shell` MCP servers
- Audit all enabled servers quarterly

### OAuth Scoping
- Grant minimal scopes (e.g., `gmail.readonly` not `gmail.full`)
- Review OAuth consents quarterly
- Revoke unused integrations

### Monitoring
```bash
# Weekly audit script example
#!/bin/bash
echo "=== Suspicious prompts ==="
grep -ri "IGNORE PREVIOUS" ~/.openclaw/sessions/ | tail -20
echo "=== Unauthorized ports ==="
ss -tlnp | grep -v "127.0.0.1"
echo "=== Modified skills ==="
find ~/.openclaw/skills -mtime -7 -name "*.md"
```

---

## Tier 3: Advanced Protection (Defense-in-Depth)

**Goal: Contain blast radius of compromise**

### Container Sandboxing
- Run OpenClaw in Docker or rootless Podman
- No external internet from OpenClaw container
- All API traffic routes through LiteLLM proxy

```yaml
# docker-compose.yml sketch
services:
  openclaw:
    image: openclaw/openclaw:latest
    network_mode: "none"  # no internet
    volumes:
      - ./workspace:/workspace
    environment:
      - ANTHROPIC_API_KEY=proxy-token

  litellm:
    image: ghcr.io/berriai/litellm:main-latest
    ports:
      - "4000:4000"
    # This container has internet, proxies API calls
```

### Egress Filtering
- Deploy Squid proxy with domain allowlist
- Only allow: `api.anthropic.com`, `api.openai.com`, `generativelanguage.googleapis.com`
- Block all other outbound traffic

### Credential Brokering
- Agent never sees real API keys
- LiteLLM holds actual keys, agent gets proxy token
- Rotate proxy tokens monthly
- Log all API calls through proxy

---

## Security Checklist

- [ ] Gateway bound to loopback (`127.0.0.1`)
- [ ] dmPolicy set to `pairing` or `allowlist`
- [ ] File system sandboxed (allowedPaths/deniedPaths)
- [ ] Running on VPS (not personal machine)
- [ ] Tools allowlisted (not defaulting to all)
- [ ] MCP servers version-pinned
- [ ] `enableAllProjectMcpServers: false`
- [ ] OAuth scopes minimized
- [ ] Weekly audit script running
- [ ] API keys in env vars (not in openclaw.json)
