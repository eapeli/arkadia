# Security Audit Report - Damon Agent

**Date:** 2026-06-28
**Auditor:** Kilo Code Assistant

## Executive Summary

The Damon Agent codebase demonstrates strong security practices overall. The project has comprehensive supply-chain protection workflows (OSV-Scanner, supply-chain-audit), uses SafeLoader for YAML parsing, has env var denylist protection for the dashboard, and follows the " Footprint Ladder" principle minimizing core tool surface. However, several instances of `shell=True` in subprocess calls were identified that warrant attention.

## Findings

### 🔴 High Severity

None found.

### 🟡 Medium Severity

#### 1. `shell=True` in subprocess calls (3 locations)

| File | Line | Context | Risk |
|------|------|---------|------|
| `damon_cli/mcp_catalog.py` | 367 | Bootstrap commands run through shell for `&&` support | Command injection if catalog manifest is compromised |
| `damon_cli/tools_config.py` | 813 | cua-driver install via `curl | sh` pattern | Supply chain if upstream compromised |
| `tools/transcription_tools.py` | 1236 | Run command with shell=True for shell features | Command injection if user input reaches this path |

**Mitigation:** These are either:
- Internal bootstrap commands (mcp_catalog) - limited to catalog maintainers
- Hardcoded install commands (tools_config) - not user-controlled
- Explicit user commands (transcription_tools) - requires user to invoke

**Recommendation:** 
- For `mcp_catalog.py`: Consider using `shlex.split()` for simple commands, or validate bootstrap commands are static
- For `tools_config.py`: The `curl | sh` pattern is standard for uv/Node installers; consider pinning to specific versions
- For `transcription_tools.py`: This appears to be a user-facing tool; ensure proper input validation

### 🟢 Low Severity / Informational

#### 2. YAML Loading (Safe)

- `agent/skill_utils.py:84` - Uses `CSafeLoader` or `SafeLoader` ✓
- `damon_cli/xai_retirement.py:207` - Uses ruamel.yaml's safe loader ✓

#### 3. Pickle Usage (Opt-in only)

- `optional-skills/research/darwinian-evolver/scripts/show_snapshot.py` - Gated by `--i-trust-this-file` flag, opt-in skill ✓

#### 4. exec()/eval() (Test/Optional only)

- `optional-skills/security/godmode/scripts/*.py` - Red-teaming skills, opt-in ✓
- `damon_ui/__init__.py:676` - Qt's `app.exec()` event loop, not Python eval ✓

#### 5. Existing Security Controls (Good)

- **OSV-Scanner** (`.github/workflows/osv-scanner.yml`) - Weekly CVE scans on lockfiles
- **Supply Chain Audit** (`.github/workflows/supply-chain-audit.yml`) - PR scanning for .pth files, base64+exec, encoded subprocess, install hooks
- **Dependency Bounds Check** - Enforces `<next_major` upper bounds on PyPI deps
- **MCP Catalog Review** - Requires explicit maintainer label for MCP changes
- **Env Var Denylist** (`damon_cli/config.py:210`) - Blocks dangerous vars from dashboard writes
- **uv.lock / package-lock.json pinning** - Full dependency pinning with hashes

## Recommendations

1. **Immediate (Medium)**
   - Review `transcription_tools.py:1236` - ensure command arg is validated/sanitized
   - Consider replacing `shell=True` in `mcp_catalog.py` with explicit command arrays where possible

2. **Short-term**
   - Add semgrep/bandit to CI for static analysis
   - Consider adding `pip-audit` to CI for runtime dependency scanning

3. **Long-term**
   - Audit all `subprocess.run` calls for `shell=True` usage
   - Consider a linting rule to flag new `shell=True` introductions

## Compliance

- ✅ No hardcoded secrets found in codebase
- ✅ API keys only in `.env` (not committed)
- ✅ Dependency pinning policy enforced
- ✅ Supply chain attack patterns scanned in PRs
- ✅ YAML parsing uses safe loaders
- ✅ Pickle usage gated and opt-in

---

**Next Steps:** Create missing macOS and Ubuntu installer workflows to complete distribution pipeline.