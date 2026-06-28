# Damon Agent - Plano de Implementação v1.0 (Produção)

## Visão Geral
Transformar o fork atual em produto profissional com:
- Sincronização com Hermes Agent v0.17.0 (The Reach Release)
- Sistema de licenciamento próprio (chaves + assinatura mensal)
- Instaladores Windows/macOS/Linux prontos
- Dashboard Web robusto + API backend
- Segurança enterprise-grade
- Pronto para distribuição comercial

---

## 1. Sincronização com Upstream (Hermes Agent v0.17.0)

### Novos recursos a integrar:
- **iMessage via Photon** - plataforma nativa sem Mac relay
- **Desktop App nativo** - Tauri/React para macOS, Linux, Windows
- **Subagentes assíncronos** - background delegation
- **Image Gen Editing** - geração + edição de imagens
- **Cursor Composer / xAI Grok** - novos provedores
- **Dashboard Profile Builder** - UI para perfis
- **Skills Hub Browser** - descoberta de skills
- **Memory Tool Upgrade** - recall melhorado
- **Curator Optimization** - menos gasto de aux model
- **300+ fixes de segurança/bugs**

### Arquivos críticos para merge:
- `agent/` - refatorado (run_agent.py → 14 módulos)
- `apps/desktop/` - app Tauri nativo
- `gateway/platforms/photon/` - iMessage
- `tools/image_generation_tool.py` - edição
- `damon_cli/subcommands/desktop.py` - CLI desktop
- `ui-tui/` - TUI Ink melhorado

---

## 2. Sistema de Licenciamento Profissional

### Arquitetura:
```
┌─────────────────────────────────────────────────────────────┐
│                    License Server (Backend)                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │  API Keys   │  │ Subscriptions│ │  Webhooks/Events    │  │
│  │  Management │  │  (Stripe)    │  │  (usage, renewals)  │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      Client SDK (Python)                    │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │ License Key │  │  Token      │  │  Feature Gates      │  │
│  │ Validation  │  │  Refresh    │  │  (pro/enterprise)   │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### Componentes:
1. **License Server** - FastAPI + PostgreSQL + Redis
2. **Client SDK** - `damon_license` package
3. **CLI Integration** - `damon license activate/validate/status`
4. **Feature Gates** - `pro`, `enterprise`, `team` tiers
5. **Offline Support** - cache assinado (JWT RS256)
6. **Trial System** - 14 dias, machine-bound

### Planos:
| Feature | Free | Pro (R$49/mês) | Enterprise |
|---------|------|----------------|------------|
| CLI/TUI | ✓ | ✓ | ✓ |
| Gateway (1 platform) | ✓ | ✓ | ✓ |
| Gateway (unlimited) | ✗ | ✓ | ✓ |
| Desktop App | ✗ | ✓ | ✓ |
| Skills Hub | ✗ | ✓ | ✓ |
| Subagents | ✗ | 3/concurrent | Unlimited |
| Memory Providers | Local only | Cloud + Local | All |
| Team Workspaces | ✗ | ✗ | ✓ |
| SSO/SAML | ✗ | ✗ | ✓ |
| Audit Logs | ✗ | 30 dias | 1 ano |
| Support | Community | Email (24h) | Dedicated |

---

## 3. Instaladores Finais

### Windows (Tauri + NSIS)
- **Arquivo**: `Damon-Setup-x64.exe` (assinado)
- **Recursos**: Auto-update, desktop shortcut, PATH entry, uninstaller
- **Assinatura**: Azure Code Signing (EV cert)
- **Requisitos**: Windows 10/11, x64/ARM64

### macOS (Tauri + DMG)
- **Arquivo**: `Damon-Setup-universal.dmg` (notarizado)
- **Recursos**: App bundle, Sparkle updates, Gatekeeper ready
- **Notarização**: Apple Developer ID

### Linux (AppImage + DEB + RPM)
- **AppImage**: `Damon-Setup-x86_64.AppImage` (portável)
- **DEB**: `damon-setup_amd64.deb` (apt repo)
- **RPM**: `damon-setup.x86_64.rpm` (dnf/yum repo)
- **Assinatura**: GPG + cosign/keyless

### Script Universal (curl | bash)
- `install.sh` - Linux/macOS/Termux
- `install.ps1` - Windows PowerShell
- Detecta OS, arquitetura, instala dependências, configura license

---

## 4. Frontend/Backend Robusto

### Backend (FastAPI + WebSocket)
```
damon-server/
├── app/
│   ├── api/v1/
│   │   ├── auth.py          # JWT, license validation
│   │   ├── agents.py        # Agent management
│   │   ├── sessions.py      # Session CRUD
│   │   ├── skills.py        # Skill marketplace
│   │   ├── memory.py        # Memory providers
│   │   ├── gateway.py       # Messaging platforms
│   │   ├── billing.py       # Stripe webhooks
│   │   └── admin.py         # Admin panel
│   ├── core/
│   │   ├── config.py        # Settings
│   │   ├── security.py      # Crypto, JWT, rate limit
│   │   ├── database.py      # SQLAlchemy + asyncpg
│   │   └── cache.py         # Redis
│   ├── models/              # SQLModels
│   ├── services/            # Business logic
│   └── websocket/           # Real-time updates
├── tests/
├── Dockerfile
├── docker-compose.yml
└── pyproject.toml
```

### Frontend (React + TypeScript + Vite)
```
damon-dashboard/
├── src/
│   ├── pages/
│   │   ├── Dashboard.tsx      # Overview
│   │   ├── Agents.tsx         # Agent list/control
│   │   ├── Sessions.tsx       # Chat history
│   │   ├── Skills.tsx         # Marketplace
│   │   ├── Gateway.tsx        # Platform config
│   │   ├── Memory.tsx         # Memory explorer
│   │   ├── Billing.tsx        # Subscription mgmt
│   │   ├── Settings.tsx       # Config
│   │   └── Admin.tsx          # Admin panel
│   ├── components/
│   │   ├── AgentCard.tsx
│   │   ├── SessionList.tsx
│   │   ├── SkillCard.tsx
│   │   ├── LogViewer.tsx
│   │   └── MetricsCharts.tsx
│   ├── hooks/
│   │   ├── useWebSocket.ts
│   │   ├── useAuth.ts
│   │   └── useLicense.ts
│   ├── store/                 # Zustand/nanostores
│   ├── api/                   # Axios + types
│   └── styles/                # TailwindCSS
├── package.json
├── vite.config.ts
└── Dockerfile
```

### Integração CLI ↔ Server
- `damon serve` - inicia backend local
- `damon dashboard` - abre frontend
- WebSocket para updates real-time
- IPC para comunicação com agent core

---

## 5. Security Hardening (Baseado na Auditoria)

### Correções Imediatas (Médio):
1. **mcp_catalog.py:367** - Substituir `shell=True` por `shlex.split()`
2. **tools_config.py:813** - `curl | sh` → download + verify hash + execute
3. **transcription_tools.py:1236** - Validar/sanitizar comando antes de `shell=True`

### Melhorias Estruturais:
1. **Bandit/ruff security rules** no CI
2. **pip-audit** + **OSV-Scanner** weekly
3. **Supply chain**: pin all deps com upper bounds
4. **Secrets scanning**: TruffleHog no PR
5. **SBOM generation**: CycloneDX no build
6. **Runtime**: seccomp profile, capability drop
7. **Audit logging**: todas operações sensíveis

### Novos Controles:
- **License enforcement** - feature gates criptografados
- **Telemetry opt-in** - GDPR compliant
- **Audit trail** - immutable logs (append-only)
- **Key rotation** - automatic JWT key rotation

---

## 6. CI/CD Pipeline Completo

### GitHub Actions Workflows:
```
.github/workflows/
├── ci.yml                    # Testes, lint, typecheck
├── security.yml              # Bandit, pip-audit, osv, trufflehog
├── build-windows.yml         # Tauri Windows + sign
├── build-macos.yml           # Tauri macOS + notarize
├── build-linux.yml           # AppImage/DEB/RPM + sign
├── build-server.yml          # Backend Docker image
├── build-dashboard.yml       # Frontend Docker image
├── release.yml               # Tag → build all → GitHub Release
├── license-server-deploy.yml # Deploy license server
└── dependency-update.yml     # Dependabot + auto-merge
```

### Release Process:
1. `git tag v1.0.0` → trigger release workflow
2. Build all platforms in parallel (matrix)
3. Sign artifacts (Windows EV, macOS notarize, Linux GPG)
4. Generate SBOM + provenance (SLSA Level 3)
5. Create GitHub Release com todos artifacts
6. Update Homebrew/Scoop/Chocolatey/AUR formulas
7. Publish to PyPI (`damon-agent` package)
8. Notify Discord/email subscribers

---

## 7. Estrutura Final do Projeto

```
damon-agent/
├── .github/workflows/        # 10+ workflows
├── agent/                    # Core agent (synced upstream)
├── damon_cli/                # CLI principal
├── damon_license/            # NOVO: License SDK
├── damon_server/             # NOVO: Backend API
├── damon_dashboard/          # NOVO: Frontend React
├── apps/
│   ├── bootstrap-installer/  # Tauri installer
│   └── desktop/              # Tauri desktop app
├── gateway/                  # Messaging gateway
├── plugins/                  # Plugin system
├── scripts/
│   ├── install.sh            # Universal installer
│   ├── install.ps1           # Windows installer
│   └── release.py            # Release automation
├── tests/                    # Unit + integration + e2e
├── docs/                     # Documentação completa
├── docker/
│   ├── Dockerfile.server
│   ├── Dockerfile.dashboard
│   └── docker-compose.yml
├── pyproject.toml
├── package.json              # Root workspace
├── Cargo.toml                # Tauri workspace
├── SECURITY.md
├── LICENSE.md
└── README.md
```

---

## Cronograma Estimado

| Fase | Duração | Entregáveis |
|------|---------|-------------|
| **1. Sync Upstream** | 3 dias | Código base v0.17.0 integrado |
| **2. License System** | 5 dias | Server + SDK + CLI + Billing |
| **3. Installers** | 4 dias | Windows/macOS/Linux assinados |
| **4. Backend API** | 5 dias | FastAPI + WebSocket + Auth |
| **5. Frontend Dashboard** | 5 dias | React + TS + Real-time |
| **5. Security Hardening** | 3 dias | Todos fixes + CI security |
| **6. CI/CD + Release** | 3 dias | Pipeline completo |
| **7. Testes + Docs** | 3 dias | Coverage >80%, docs completas |
| **TOTAL** | **~31 dias** | **Produto v1.0 Pronto** |

---

## Próximos Passos Imediatos

1. **Criar branch `feat/production-v1`** 
2. **Implementar `damon_license` package** (core do negócio)
3. **Setup License Server** (FastAPI + Stripe)
4. **Integrar CLI com license validation**
5. **Finalizar Tauri installer** (build + sign)
6. **Desenvolver Backend + Frontend** em paralelo
7. **Hardening segurança** baseado na auditoria
8. **CI/CD completo** com assinatura
9. **Release v1.0.0** → GitHub + PyPI + Homebrew

---

## Notas Técnicas Importantes

- **Offline-first**: License cache assinado (7 dias), sync quando online
- **Machine binding**: HWID + TPM quando disponível
- **Graceful degradation**: Free features sempre funcionam
- **Audit trail**: Todas validações logadas (sem PII)
- **Key rotation**: RS256 keys rotacionadas a cada 90 dias
- **Compliance**: LGPD/GDPR ready, data export/delete APIs