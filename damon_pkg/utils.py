"""Damon utilities (core helpers used across damon_cli/gateway/etc)."""
from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path


def atomic_replace(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_path = tempfile.mkstemp(dir=str(dst.parent), suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(src.read_text(encoding="utf-8"))
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp_path, dst)
    except BaseException:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise


def atomic_yaml_write(path: Path, data, *, sort_keys: bool = False) -> None:
    import yaml

    dumped = yaml.safe_dump(
        data,
        sort_keys=sort_keys,
        allow_unicode=True,
        default_flow_style=False,
    )
    tmp = path.parent / f".{path.name}.tmp"
    tmp.write_text(dumped, encoding="utf-8")
    atomic_replace(tmp, path)


def atomic_json_write(path: Path, data, **kwargs) -> None:
    dumped = json.dumps(data, ensure_ascii=False, **kwargs)
    tmp = path.parent / f".{path.name}.tmp"
    tmp.write_text(dumped, encoding="utf-8")
    atomic_replace(tmp, path)


def env_int(name: str, default: int = 0) -> int:
    value = os.getenv(name)
    if value is None:
        return default
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def env_var_enabled(name: str, default: str = "false") -> bool:
    value = os.getenv(name, default)
    if isinstance(value, str):
        return value.strip().lower() not in {"0", "false", "no", "off", ""}
    return bool(value)


def is_truthy_value(value) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, int):
        return value != 0
    if isinstance(value, str):
        return value.strip().lower() not in {"0", "false", "no", "off", ""}
    return bool(value)


def base_url_hostname(base_url: str) -> str:
    """Return the lowercased hostname for a base URL, or ``\"\"`` if absent.

    Use exact-hostname comparisons against known provider hosts
    (``api.openai.com``, ``api.x.ai``, ``api.anthropic.com``) instead of
    substring matches on the raw URL. Substring checks treat attacker- or
    proxy-controlled paths/hosts like ``https://api.openai.com.example/v1``
    or ``https://proxy.test/api.openai.com/v1`` as native endpoints, which
    leads to wrong api_mode / auth routing.
    """
    from urllib.parse import urlparse
    raw = (base_url or "").strip()
    if not raw:
        return ""
    parsed = urlparse(raw if "://" in raw else f"//{raw}")
    return (parsed.hostname or "").lower().rstrip(".")


def model_forces_max_completion_tokens(model: str) -> bool:
    """Return True for model families that require ``max_completion_tokens``.

    OpenAI's newer families reject ``max_tokens`` on /v1/chat/completions with
    HTTP 400 ``unsupported_parameter`` -- the caller must send
    ``max_completion_tokens`` instead. This covers:

    - ``gpt-4o`` / ``gpt-4o-mini`` / ``gpt-4o-*``
    - ``gpt-4.1`` / ``gpt-4.1-*``
    - ``gpt-5`` / ``gpt-5.x`` / ``gpt-5-*``
    - ``o1`` / ``o1-*``
    - ``o3`` / ``o3-*``
    - ``o4`` / ``o4-*``

    Handles vendor prefixes like ``openai/gpt-5.4`` by stripping to the tail.
    The URL-based check (``base_url_hostname == "api.openai.com"``) misses
    third-party OpenAI-compatible endpoints (custom OpenAI gateways,
    OpenRouter) that front these models and enforce the same parameter
    constraint, so name-based detection is required as a fallback.
    """
    m = (model or "").strip().lower()
    if not m:
        return False
    if "/" in m:
        m = m.rsplit("/", 1)[-1]
    return (
        m.startswith("gpt-4o")
        or m.startswith("gpt-4.1")
        or m.startswith("gpt-5")
        or m.startswith("o1")
        or m.startswith("o3")
        or m.startswith("o4")
    )


def base_url_host_matches(base_url: str, domain: str) -> bool:
    """Return True when the base URL's hostname is ``domain`` or a subdomain.

    Safer counterpart to ``domain in base_url``, which is the substring
    false-positive class documented on ``base_url_hostname``. Accepts bare
    hosts, full URLs, and URLs with paths.

        base_url_host_matches("https://api.moonshot.ai/v1", "moonshot.ai") == True
        base_url_host_matches("https://moonshot.ai", "moonshot.ai")        == True
        base_url_host_matches("https://evil.com/moonshot.ai/v1", "moonshot.ai") == False
        base_url_host_matches("https://moonshot.ai.evil/v1", "moonshot.ai")     == False
    """
    hostname = base_url_hostname(base_url)
    if not hostname:
        return False
    domain = (domain or "").strip().lower().rstrip(".")
    if not domain:
        return False
    return hostname == domain or hostname.endswith("." + domain)
