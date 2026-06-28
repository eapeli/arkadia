"""Resolve HERMES_HOME for standalone skill scripts.

Skill scripts may run outside the Hermes process (e.g. system Python,
nix env, CI) where ``damon_constants`` is not importable.  This module
provides the same ``get_damon_home()`` and ``display_damon_home()``
contracts as ``damon_constants`` without requiring it on ``sys.path``.

When ``damon_constants`` IS available it is used directly so that any
future enhancements (profile resolution, Docker detection, etc.) are
picked up automatically.  The fallback path replicates the core logic
from ``damon_constants.py`` using only the stdlib.

All scripts under ``google-workspace/scripts/`` should import from here
instead of duplicating the ``HERMES_HOME = Path(os.getenv(...))`` pattern.
"""

from __future__ import annotations

import os
from pathlib import Path

try:
    from damon_pkg.constants import display_damon_home as display_damon_home
    from damon_pkg.constants import get_damon_home as get_damon_home
except (ModuleNotFoundError, ImportError):

    def get_damon_home() -> Path:
        """Return the Hermes home directory (default: ~/.hermes).

        Mirrors ``damon_constants.get_damon_home()``."""
        val = os.environ.get("HERMES_HOME", "").strip()
        return Path(val) if val else Path.home() / ".hermes"

    def display_damon_home() -> str:
        """Return a user-friendly ``~/``-shortened display string.

        Mirrors ``damon_constants.display_damon_home()``."""
        home = get_damon_home()
        try:
            return "~/" + str(home.relative_to(Path.home()))
        except ValueError:
            return str(home)
