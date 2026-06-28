"""Compatibility re-export layer.

Imports live symbols from the canonical constants module so legacy
``from damon_pkg.constants import ...`` and ``import damon_constants`` keep
working.
"""

from damon_pkg.constants import (  # noqa: F401
    get_damon_home,
    get_damon_dir,
    display_damon_home,
    is_termux,
    is_wsl,
    is_container,
    apply_subprocess_home_env,
    secure_parent_dir,
    parse_reasoning_effort,
    get_bundled_skills_dir,
    get_optional_skills_dir,
    get_default_damon_root,
    get_config_path,
    get_skills_dir,
    get_env_path,
    apply_ipv4_preference,
    OPENROUTER_BASE_URL,
    OPENROUTER_MODELS_URL,
    PARTIAL_STREAM_STUB_ID,
    FINISH_REASON_LENGTH,
    VALID_REASONING_EFFORTS,
)

HERMES_HOME = get_damon_home()

__all__ = [
    "get_damon_home",
    "HERMES_HOME",
    "get_damon_dir",
    "display_damon_home",
    "is_termux",
    "is_wsl",
    "is_container",
    "apply_subprocess_home_env",
    "secure_parent_dir",
    "parse_reasoning_effort",
    "get_bundled_skills_dir",
    "get_optional_skills_dir",
    "get_default_damon_root",
    "OPENROUTER_BASE_URL",
    "OPENROUTER_MODELS_URL",
    "PARTIAL_STREAM_STUB_ID",
    "FINISH_REASON_LENGTH",
    "VALID_REASONING_EFFORTS",
]

get_hermes_home = get_damon_home
get_hermes_dir = get_damon_dir
display_hermes_home = display_damon_home

_container_detected = None
_profile_fallback_warned = False
