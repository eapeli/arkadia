import importlib
import pytest


def _try_import(module_name):
    try:
        importlib.import_module(module_name)
        return True
    except Exception as exc:
        return f"{type(exc).__name__}: {exc}"


CORE_MODULES = [
    "agent",
    "agent.agent_init",
    "agent.tool_executor",
    "agent.context_engine",
    "gateway",
    "gateway.run",
    "damon_cli",
    "damon_cli.main",
    "tools.registry",
    "tools.memory_tool",
    "tools.delegate_tool",
    "tools.managed_tool_gateway",
    "providers",
]


@pytest.mark.parametrize("module_name", CORE_MODULES)
def test_core_module_importable(module_name):
    result = _try_import(module_name)
    assert result is True, f"Failed to import {module_name}: {result}"
