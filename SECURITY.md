# Segurança do Damon Agent

<p align="center">
  <a href="README.md"><img src="https://img.shields.io/badge/Lang-Portugu%C3%AAs-blue?style=for-the-badge" alt="Português"></a>
  <a href="SECURITY.en.md"><img src="https://img.shields.io/badge/Lang-English-blue?style=for-the-badge" alt="English"></a>
</p>

---

## 🔐 Visão Geral

O **Damon Agent** é um agente de IA local-first e autônomo criado por **Elisabete Alves**, com código base derivado do [Hermes Agent](https://github.com/NousResearch/damon-agent) (MIT, by Nous Research).

Esta página documenta as práticas de segurança, como reportar vulnerabilidades e o que está em escopo para correções.

---

## 📋 Escopo de Segurança

### Em escopo

- Vazamento de credenciais, segredos ou chaves de API no código, logs ou configurações padrão
- Injeção de comandos ou comandos arbitrários via gateway, CLI, skills ou MCPs
- Bypass de permissões ou aprovação de comandos (`write_approval`, pairing DM)
- Acesso não autorizado a memória persistente (`DAMON_HOME`)
- Execução arbitrária de código em backends remotos (SSH, Docker, Singularity, Modal, Daytona)
- XSS, CSRF ou injeção em painel web/dashboard
- Vulnerabilidades em dependências Python/Node com CVSS >= 7.0 confirmado

### Fora de escopo

- Comportamento do modelo LLM (alucinações, jailbreak direcionado a modelos de terceiros)
- Configurações inseguras escolhidas pelo usuário (ex: chaves expostas em `.env` compartilhado)
- Ataques a infraestrutura do usuário (VPS, servidor físico) não causados pelo Damon
- Issues de segurança em dependências com nível de severidade baixa sem exploit conhecido

---

## 🛡️ Medidas de Segurança Implementadas

| Recurso | Descrição |
|---------|-----------|
| **Aprovação de comandos** | Comandos destrutivos (`rm`, `curl`, `pip install`, etc.) exigem confirmação explícita do usuário antes da execução |
| **DM Pairing** | Acesso remoto via gateway requer pareamento prévio por DM — sem exposição pública acidental |
| **Sandbox de execução** | Suporte a execução isolada em containers Docker e Singularity |
| **Secret Prompt** | Chaves de API são coletadas via prompt seguro, sem armazenamento em plaintext por padrão |
| **Permissões refinadas** | Módulos e skills operam com princípio de menor privilégio |
| **Auditoria e Logs** | Comandos, erros e eventos são registrados para revisão em `damon logs` |
| **Security Audit** | Ferramenta `damon security audit` verifica configurações inseguras |
| **OSV Scanner** | CI/CD integrado com `osv-scanner` para detectar vulnerabilidades em dependências |

---

## 🚨 Reportando uma Vulnerabilidade

Se você encontrou uma vulnerabilidade de segurança, **não abra uma issue pública**.

1. **Envie um e-mail** para: `security@damon-agent.nousresearch.com`
2. **Assunto**: `[SECURITY] Descrição curta`
3. **Corpo**:
   - Passos para reproduzir
   - Impacto potencial
   - Versão do Damon afetada
   - Configuração relevante (sanitizada, sem chaves)

Responderemos em até **72 horas** com status de validação e plano de correção.

---

## 🔄 Divulgação Responsável

Solicitamos **90 dias** de janela de correção antes de qualquer divulgação pública. Isso protege usuários enquanto atualizações são preparadas.

- Crítico (RCE, vazamento massivo): alvo de 7 dias
- Alto (bypass de segurança significativo): alvo de 30 dias
- Médio/Baixo: alvo de 90 dias ou na próxima release planejada

---

## 🌿 Base de Código: Hermes Agent

Partes significativas do código-base do Damon derivam do **Hermes Agent** da Nous Research, licenciado sob MIT. Reconhecemos:

- Todos os termos da licença MIT original são preservados
- Modificações feitas por Elisabete Alves são marcadas em commits e créditos
- O projeto mantém a atribuição ao código original Hermes em `docs/author.md`, `LICENSE` e arquivos de manifesto

Veja [LICENSE](LICENSE) e [docs/author.md](docs/author.md) para detalhes de atribuição.

---

## 📅 Releases e Suporte

| Versão | Status | Segurança |
|--------|--------|-----------|
| `main` (HEAD) | Active Development | Patches contínuos |
| v0.1.x | Stable | Correções de segurança backported |
| <= v0.0.x | End of Life | Sem suporte — atualize |

---

> **Nota**: Esta documentação reflete as práticas de segurança do **Damon Agent** como projeto mantido por Elisabete Alves. A base Hermes (Nous Research) mantém suas próprias políticas em https://github.com/nousresearch/hermes-agent?tab=security-ov-file.
