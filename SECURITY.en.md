# Damon Agent Security

<p align="center">
  <a href="SECURITY.md"><img src="https://img.shields.io/badge/Lang-Portugu%C3%AAs-blue?style=for-the-badge" alt="Português"></a>
</p>

---

## 🔐 Overview

**Damon Agent** is a personal, local-first and autonomous AI agent created by **Elisabete Alves**, with codebase derived from [Hermes Agent](https://github.com/nousresearch/hermes-agent) (MIT, by Nous Research).

This page documents security practices, how to report vulnerabilities, and what is in scope for fixes.

---

## 📋 Security Scope

### In scope

- Leakage of credentials, secrets, or API keys in code, logs, or default configurations
- Command injection or arbitrary command execution via gateway, CLI, skills, or MCPs
- Bypass of command approval or DM pairing permissions
- Unauthorized access to persistent memory (`DAMON_HOME`)
- Arbitrary code execution on remote backends (SSH, Docker, Singularity, Modal, Daytona)
- XSS, CSRF, or injection in web dashboard
- Python/Node dependency vulnerabilities with confirmed CVSS >= 7.0

### Out of scope

- LLM model behavior (hallucinations, jailbreak attempts directed at third-party models)
- Insecure configurations chosen by the user (e.g., keys exposed in a shared `.env`)
- Attacks on user infrastructure (VPS, physical server) not caused by Damon
- Security issues in low-severity dependencies without a known exploit

---

## 🛡️ Implemented Security Measures

| Feature | Description |
|---------|-------------|
| **Command approval** | Destructive commands (`rm`, `curl`, `pip install`, etc.) require explicit user confirmation before execution |
| **DM Pairing** | Remote access via gateway requires prior DM pairing — no accidental public exposure |
| **Execution sandbox** | Support for isolated execution in Docker and Singularity containers |
| **Secret Prompt** | API keys are collected via secure prompt, not stored in plaintext by default |
| **Fine-grained permissions** | Modules and skills operate on least-privilege |
| **Auditing and logs** | Commands, errors, and events are logged for review in `damon logs` |
| **Security Audit** | `damon security audit` tool checks for insecure configurations |
| **OSV Scanner** | CI/CD integrated with `osv-scanner` to detect dependency vulnerabilities |

---

## 🚨 Reporting a Vulnerability

If you found a security vulnerability, **do not open a public issue**.

1. **Send an email** to: `security@damon-agent.nousresearch.com`
2. **Subject**: `[SECURITY] Short description`
3. **Body**:
   - Steps to reproduce
   - Potential impact
   - Affected Damon version
   - Relevant configuration (sanitized, no keys)

We will respond within **72 hours** with validation status and a fix plan.

---

## 🔄 Responsible Disclosure

We request **90 days** of fix window before any public disclosure. This protects users while updates are prepared.

- Critical (RCE, massive leak): 7-day target
- High (significant security bypass): 30-day target
- Medium/Low: 90-day target or in the next planned release

---

## 🌿 Codebase: Hermes Agent

Significant portions of Damon's codebase derive from **Hermes Agent** by Nous Research, MIT licensed. We acknowledge:

- All terms of the original MIT license are preserved
- Modifications by Elisabete Alves are marked in commits and credits
- The project maintains attribution to the original Hermes code in `docs/author.md`, `LICENSE`, and manifest files

See [LICENSE](LICENSE) and [docs/author.md](docs/author.md) for attribution details.

---

## 📅 Releases and Support

| Version | Status | Security |
|---------|--------|----------|
| `main` (HEAD) | Active Development | Continuous patches |
| v0.1.x | Stable | Security fixes backported |
| <= v0.0.x | End of Life | No support — please update |

---

> **Note**: This documentation reflects the security practices of **Damon Agent** as maintained by Elisabete Alves. The Hermes base (Nous Research) maintains its own policies at https://github.com/nousresearch/hermes-agent?tab=security-ov-file.
