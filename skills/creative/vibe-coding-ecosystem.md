---
name: vibe-coding-ecosystem
description: "Comprehensive skill for vibe coding ecosystem: UI library curation, Hermes essential integrations, vibe vs no-code vs low-code framework, and Composio integration for Hermes/OpenClaw"
version: "1.0.0"
author: "Damon"
tags:
  - vibe-coding
  - ui-libraries
  - damon-integrations
  - composio
  - openclaw
  - no-code
  - low-code
---

# Vibe Coding Ecosystem Skill

Unified skill covering the complete vibe coding stack: UI component libraries, essential Hermes integrations, methodology comparison (vibe vs no-code vs low-code), and Composio/OpenClaw integration.

## 1. UI Library Curation for Vibe Coding

### Tier 1: The Vibe Coding Standard Stack
| Library | Base | Strength | Best For |
|---------|------|----------|----------|
| **shadcn/ui** | React + Tailwind + Radix | Copy-paste ownership, accessible, 50+ components | Default choice for React/Next.js vibe coding |
| **Radix UI** | Headless primitives | Unstyled, fully accessible, composition | Building custom design systems |
| **Base UI** | Headless (Radix successor) | Zero dependencies, smaller bundle | Performance-critical apps |

### Tier 2: Specialized Libraries
| Library | Focus | Vibe Coding Fit |
|---------|-------|-----------------|
| **Tailwind UI** | Pre-built pages/sections | Fast prototyping, marketing sites |
| **Headless UI** | Unstyled accessible components | When you need full control + accessibility |
| **React Aria / Adobe Spectrum** | Hook-based, framework-agnostic | Complex interactions, multi-framework |
| **Ark UI** | Headless, state machine driven | Advanced stateful components |
| **Park UI** | Styled components (Panda CSS) | Alternative to Tailwind stack |

### Tier 3: Component Marketplaces (Copy-Paste Ready)
- **shadcn Studio** — 1000+ blocks, templates, themes
- **Magic UI** — Animated components, 3D effects
- **Aceternity UI** — Modern, animated components
- **HyperUI** — Free Tailwind components
- **Flowbite** — Open-source component library
- **daisyUI** — Semantic component classes
- **Mantine** — Full React ecosystem (hooks, forms, core)

### Vibe Coding UI Prompt Pattern
```markdown
> Use shadcn/ui + Tailwind + Radix. Create [Feature] with:
> - Component: [Name] (accessible, typed with TypeScript)
> - State: [Zustand/Redux/Context] with persistence
> - Tests: Vitest + React Testing Library + Playwright E2E
> - Storybook: stories for all variants
> - Dark mode: CSS variables, next-themes
> - Animations: Framer Motion / Tailwind animate
> - Responsive: mobile-first, container queries
> - A11y: ARIA, keyboard nav, focus management
> - Output: PR-ready diff, no placeholders
```

## 2. 8 Essential Integrations for Hermes Agent

### Messaging Platforms (Core)
| # | Platform | Use Case | Setup Complexity |
|---|----------|----------|------------------|
| 1 | **Telegram** | Primary bot interface, groups, channels | Easy (BotFather) |
| 2 | **Discord** | Community, voice, rich embeds | Medium (Intents) |
| 3 | **WhatsApp** | Personal/business comms | Medium (Baileys bridge) |
| 4 | **Slack** | Team workflows, slash commands | Medium (OAuth) |

### Productivity & Knowledge (High Value)
| # | Integration | Capability | Auth Type |
|---|-------------|------------|-----------|
| 5 | **Notion** | Knowledge base, tasks, databases | OAuth / Internal Integration |
| 6 | **GitHub** | Code, PRs, issues, CI, releases | OAuth / PAT |
| 7 | **Google Workspace** | Gmail, Calendar, Drive, Docs, Sheets | OAuth |
| 8 | **Linear / Jira** | Issue tracking, sprints, roadmaps | OAuth / API Key |

### Bonus: Developer Tools
- **Vercel/Netlify** — Deploy previews, logs, analytics
- **Supabase/PlanetScale** — DB, auth, realtime, edge functions
- **Sentry** — Error tracking, performance
- **PostHog** — Analytics, feature flags, session replay
- **Resend/SendGrid** — Transactional email
- **Stripe** — Payments, subscriptions, webhooks

### Hermes Integration Config Pattern
```yaml
# ~/.damon/config.yaml
platforms:
  telegram:
    bot_token: "${TELEGRAM_BOT_TOKEN}"
    allowed_chats: ["-1001234567890"]
  discord:
    bot_token: "${DISCORD_BOT_TOKEN}"
    application_id: "${DISCORD_APP_ID}"
    allowed_guilds: ["1234567890"]
  whatsapp:
    allow_from: ["351913603304@lid"]
    group_allow_from: ["120363427062762522"]
  slack:
    bot_token: "${SLACK_BOT_TOKEN}"
    signing_secret: "${SLACK_SIGNING_SECRET}"
    allowed_channels: ["C1234567890"]

skills:
  - notion
  - github
  - google-workspace
  - linear
```

## 3. Vibe Coding vs No-Code vs Low-Code: Decision Framework

### Comparison Matrix
| Dimension | **Vibe Coding** | **Low-Code** | **No-Code** |
|-----------|-----------------|--------------|-------------|
| **Output** | Real code (React, Python, Go, etc.) | Generated code + visual logic | Config/data only |
| **Ownership** | Full — you own every line | Partial — vendor lock-in risk | None — platform dependent |
| **Flexibility** | Unlimited | Constrained by platform | Highly constrained |
| **Learning Curve** | Medium (prompt engineering) | Low (visual builder) | Lowest |
| **Speed to MVP** | Fast (hours) | Fastest (minutes-hours) | Fastest (minutes) |
| **Scalability** | Unlimited (your architecture) | Platform limits | Platform limits |
| **Technical Debt** | Manageable (refactorable) | Hidden (black box) | Hidden (black box) |
| **Team Collaboration** | Git, PRs, code review | Visual diffs, limited | Config diffs |
| **AI Enhancement** | Native (Copilot, Cursor, Claude) | Bolted on | Bolted on |
| **Cost at Scale** | Infrastructure only | Per-seat + usage | Per-seat + usage |
| **Exportability** | 100% (it's your code) | Partial/None | None |

### When to Choose Each

**→ Vibe Coding When:**
- You need custom logic, complex algorithms, unique UX
- Team knows/learns code; long-term ownership matters
- Integrating with existing codebase/infrastructure
- Compliance/security requires code auditability
- Building developer tools, APIs, complex SaaS

**→ Low-Code When:**
- Standard CRUD apps, admin panels, internal tools
- Business users need to modify logic
- Fast iteration > customization
- Platform (Retool, Power Apps, Appsmith) fits domain
- Legacy integration via connectors

**→ No-Code When:**
- Landing pages, forms, simple workflows
- Zero technical team
- MVP validation in days
- Bubble, Webflow, Framer, Softr cover needs
- Budget/time extremely constrained

### Hybrid Strategy (Recommended)
```
Vibe Coding (core product) + Low-Code (admin/internal) + No-Code (marketing/landing)
```
- Core differentiators → vibe coded (full control)
- Internal tools → Retool/Appsmith (speed)
- Marketing pages → Framer/Webflow (design freedom)
- All connected via APIs/webhooks

## 4. Composio Integration for Hermes & OpenClaw

### What is Composio
- **1000+ pre-built integrations** (GitHub, Notion, Slack, Gmail, Salesforce, HubSpot, etc.)
- **Unified API** — one SDK, consistent auth, automatic token refresh
- **MCP (Model Context Protocol) endpoint** — exposes tools to any compatible agent
- **Managed OAuth** — handles auth flows, scopes, refresh tokens
- **Sandboxed execution** — secure, isolated tool runs

### Architecture: Hermes + Composio
```
┌─────────────┐     ┌──────────────┐     ┌─────────────────┐
│   Hermes    │────▶│  Composio    │────▶│  1000+ Apps     │
│  (Agent)    │ MCP │  MCP Server  │ API │  (GitHub, etc.) │
└─────────────┘     └──────────────┘     └─────────────────┘
       │                    │
       │              ┌────┴────┐
       │              │ OpenClaw│
       │              │ Plugin  │
       │              └─────────┘
       ▼
┌─────────────────┐
│  Local Skills   │
│  (reasoning,    │
│   memory, etc.) │
└─────────────────┘
```

### Setup: Hermes + Composio (via OpenClaw Plugin)

#### 1. Install Composio CLI
```bash
npm install -g @composio/cli
# or
pip install composio
```

#### 2. Configure Composio
```bash
composio login
# Opens browser → authorize → returns API key

composio add github
composio add notion
composio add slack
composio add gmail
# ...add needed apps
```

#### 3. Start Composio MCP Server
```bash
composio mcp serve --port 8000
# Runs on http://localhost:8000/mcp
# Exposes all connected apps as MCP tools
```

#### 4. Configure OpenClaw to Use Composio
```json
// ~/.opencaw/config.json
{
  "mcpServers": {
    "composio": {
      "url": "http://localhost:8000/mcp",
      "transport": "http"
    }
  }
}
```

#### 5. Configure Hermes to Use OpenClaw (via claw plugin)
```yaml
# ~/.damon/config.yaml
plugins:
  - openclaw:
      mcp_servers:
        - name: composio
          url: http://localhost:8000/mcp
          tools: ["github_*", "notion_*", "slack_*", "gmail_*"]
```

#### 6. Alternative: Direct Composio SDK in Hermes Skills
```python
# skills/my-skill/scripts/composio_tool.py
from composio import Composio

composio = Composio(api_key=os.getenv("COMPOSIO_API_KEY"))

# Execute any connected app action
result = composio.execute(
    app="github",
    action="create_issue",
    params={"repo": "owner/repo", "title": "Bug", "body": "..."}
)
```

### Composio vs Native Hermes Integrations

| Factor | Composio | Native Hermes |
|--------|----------|---------------|
| **App Count** | 1000+ | ~20 native |
| **Auth Management** | Automatic (OAuth, refresh) | Manual per platform |
| **Maintenance** | Composio handles breaking changes | You maintain |
| **Latency** | Extra hop (MCP server) | Direct |
| **Cost** | Free tier + paid plans | Free (self-hosted) |
| **Customization** | Limited to exposed actions | Full control |
| **Security** | Sandboxed, scoped tokens | Your implementation |

### Recommended: Hybrid Approach
- **Core messaging (Telegram, Discord, WhatsApp, Slack)** → Native Hermes (low latency, full control)
- **Productivity apps (Notion, GitHub, Linear, Gmail, Calendar)** → Composio via MCP
- **Specialized/SaaS (Salesforce, HubSpot, Jira, Stripe)** → Composio
- **Custom/internal APIs** → Native Hermes skills

## Quick Start Checklist

### For New Vibe Coding Project
- [ ] Choose UI stack: shadcn/ui + Tailwind + Radix (default)
- [ ] Set up Hermes with 4 core messaging platforms
- [ ] Add Notion + GitHub + Google Workspace via Composio
- [ ] Configure ethical-autonomy + self-check-v7 guardrails
- [ ] Create PR template with security checklist

### For Existing Hermes Setup
- [ ] Audit current integrations → migrate to Composio where beneficial
- [ ] Add UI library skill for consistent vibe coding output
- [ ] Document methodology choice (vibe/low/no-code) per project
- [ ] Set up Composio MCP server as systemd service
- [ ] Test OpenClaw ↔ Hermes tool routing

## References
- Microsoft Learn: Introduction to Vibe Coding (9 units)
- Microsoft Learn: GitHub Copilot Agent Mode
- Composio Docs: https://composio.dev/docs
- OpenClaw: https://openclaw.dev
- Hermes Docs: https://damon-agent.nousresearch.com/docs
- shadcn/ui: https://ui.shadcn.com
- Vibe Coding vs No/Low Code: Taskade, MemberStack, Rocket.new comparisons