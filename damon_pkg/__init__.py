"""Damon Agent - Core utilities and constants."""

# Re-export root-level modules for backward compatibility
from . import constants as damon_constants
from . import utils
from . import model_tools
from . import toolsets

# Common imports for convenience
from .constants import (
    get_damon_home,
    DAMON_HOME,
    DEFAULT_CONFIG_DIR,
    DEFAULT_DATA_DIR,
    DEFAULT_LOG_DIR,
    DEFAULT_SESSIONS_DIR,
    DEFAULT_SKILLS_DIR,
    DEFAULT_MEMORY_DIR,
    DEFAULT_CRON_DIR,
    DEFAULT_STATE_FILE,
    DEFAULT_SOUL_FILE,
    DEFAULT_PERSONA_FILE,
)

from .utils import (
    atomic_replace,
    atomic_yaml_write,
    atomic_json_write,
    base_url_hostname,
    base_url_host_matches,
    model_forces_max_completion_tokens,
    env_int,
    env_var_enabled,
    is_truthy_value,
)

__version__ = "0.1.0"
__all__ = [
    "damon_constants",
    "utils",
    "model_tools",
    "toolsets",
    "get_damon_home",
    "DAMON_HOME",
    "DEFAULT_CONFIG_DIR",
    "DEFAULT_DATA_DIR",
    "DEFAULT_LOG_DIR",
    "DEFAULT_SESSIONS_DIR",
    "DEFAULT_SKILLS_DIR",
    "DEFAULT_MEMORY_DIR",
    "DEFAULT_CRON_DIR",
    "DEFAULT_STATE_FILE",
    "DEFAULT_SOUL_FILE",
    "DEFAULT_PERSONA_FILE",
    "atomic_replace",
    "atomic_yaml_write",
    "atomic_json_write",
    "base_url_hostname",
    "base_url_host_matches",
    "model_forces_max_completion_tokens",
    "env_int",
    "env_var_enabled",
    "is_truthy_value",
]