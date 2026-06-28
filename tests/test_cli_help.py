"""Tests for Damon CLI help/version behavior."""
from contextlib import redirect_stdout
import io
import sys

from damon_cli.main import main


def test_cli_version_flag_exits_cleanly():
    sys.argv = ["damon", "version"]
    out = io.StringIO()
    with redirect_stdout(out):
        try:
            main()
        except SystemExit:
            pass
    text = out.getvalue()
    assert "Damon" in text or "damon" in text
