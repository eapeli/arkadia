import sys
import os
import tempfile
import pytest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

os.environ.setdefault("DAMON_HOME", str(REPO_ROOT / ".damon" / "test-home"))


@pytest.fixture()
def repo_root():
    return REPO_ROOT


@pytest.fixture()
def tmp_damon_home(tmp_path):
    home = tmp_path / "damon-home"
    home.mkdir(parents=True, exist_ok=True)
    (home / "skills").mkdir(parents=True, exist_ok=True)
    (home / "plugins").mkdir(parents=True, exist_ok=True)
    old_env = os.environ.get("DAMON_HOME")
    os.environ["DAMON_HOME"] = str(home)
    try:
        yield home
    finally:
        if old_env is None:
            os.environ.pop("DAMON_HOME", None)
        else:
            os.environ["DAMON_HOME"] = old_env
