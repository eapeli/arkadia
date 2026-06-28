"""Shared constants for Damon Agent.

Import-safe module with no dependencies — can be imported from anywhere
without risk of circular imports.
"""

import os
import sys
import sysconfig
from contextvars import ContextVar, Token
from pathlib import Path


_profile_fallback_warned: bool = False
_UNSET = object()
_DAMON_HOME_OVERRIDE: ContextVar[str | object] = ContextVar(
    "_DAMON_HOME_OVERRIDE", default=_UNSET
)


def set_damon_home_override(path: str | Path | None) -> Token:
    value: str | object = _UNSET if path is None else str(path)
    return _DAMON_HOME_OVERRIDE.set(value)


def reset_damon_home_override(token: Token) -> None:
    _DAMON_HOME_OVERRIDE.reset(token)


def get_damon_home_override() -> str | None:
    override = _DAMON_HOME_OVERRIDE.get()
    if override is _UNSET or not override:
        return None
    return str(override)


def _get_platform_default_damon_home() -> Path:
    if sys.platform == "win32":
        local_appdata = os.environ.get("LOCALAPPDATA", "").strip()
        base = Path(local_appdata) if local_appdata else Path.home() / "AppData" / "Local"
        return base / "damon"
    return Path.home() / ".damon"


def get_damon_home() -> Path:
    override = get_damon_home_override()
    if override:
        return Path(override)

    val = os.environ.get("DAMON_HOME", "").strip()
    if val:
        return Path(val)

    global _profile_fallback_warned
    if not _profile_fallback_warned:
        try:
            fallback_home = _get_platform_default_damon_home()
            active_path = fallback_home / "active_profile"
            active = active_path.read_text().strip() if active_path.exists() else ""
        except (UnicodeDecodeError, OSError):
            active = ""
        if active and active != "default":
            _profile_fallback_warned = True
            msg = (
                f"[DAMON_HOME fallback] DAMON_HOME is unset but active "
                f"profile is {active!r}. Falling back to {fallback_home}, which "
                f"is the DEFAULT profile — not {active!r}. Any data this "
                f"process writes will land in the wrong profile. The "
                f"subprocess spawner should pass DAMON_HOME explicitly "
                f"(see issue #18594)."
            )
            try:
                sys.stderr.write(msg + "\n")
                sys.stderr.flush()
            except Exception:
                pass

    return _get_platform_default_damon_home()


def get_default_damon_root() -> Path:
    native_home = _get_platform_default_damon_home()
    env_home = os.environ.get("DAMON_HOME", "")
    if not env_home:
        return native_home
    env_path = Path(env_home)
    try:
        env_path.resolve().relative_to(native_home.resolve())
        return native_home
    except ValueError:
        pass
    if env_path.parent.name == "profiles":
        return env_path.parent.parent
    return env_path


def _get_packaged_data_dir(name: str) -> Path | None:
    candidates = []
    for scheme in ("data", "purelib", "platlib"):
        raw = sysconfig.get_path(scheme)
        if raw:
            candidates.append(Path(raw) / name)
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def get_optional_skills_dir(default: Path | None = None) -> Path:
    override = os.getenv("DAMON_OPTIONAL_SKILLS", "").strip()
    if override:
        return Path(override)
    packaged = _get_packaged_data_dir("optional-skills")
    if packaged is not None:
        return packaged
    if default is not None:
        return default
    return get_damon_home() / "optional-skills"


def get_optional_mcps_dir(default: Path | None = None) -> Path:
    override = os.getenv("DAMON_OPTIONAL_MCPS", "").strip()
    if override:
        return Path(override)
    packaged = _get_packaged_data_dir("optional-mcps")
    if packaged is not None:
        return packaged
    if default is not None:
        return default
    return get_damon_home() / "optional-mcps"


def get_bundled_skills_dir(default: Path | None = None) -> Path:
    override = os.getenv("DAMON_BUNDLED_SKILLS", "").strip()
    if override:
        return Path(override)
    packaged = _get_packaged_data_dir("skills")
    if packaged is not None:
        return packaged
    if default is not None:
        return default
    return get_damon_home() / "skills"


def get_damon_dir(new_subpath: str, old_name: str) -> Path:
    home = get_damon_home()
    old_path = home / old_name
    if old_path.exists():
        return old_path
    return home / new_subpath


def display_damon_home() -> str:
    home = get_damon_home()
    try:
        return "~/" + str(home.relative_to(Path.home()))
    except ValueError:
        return str(home)


def secure_parent_dir(path: Path) -> None:
    parent = path.parent.resolve()
    if parent == Path("/") or len(parent.parts) < 3:
        return
    try:
        os.chmod(parent, 0o700)
    except OSError:
        pass


def _norm_home_path(path: str | None) -> str:
    raw = (path or "").strip()
    if not raw:
        return ""
    try:
        return os.path.normcase(os.path.abspath(os.path.expanduser(raw)))
    except Exception:
        return os.path.normcase(raw)


def _profile_home_path(env: dict[str, str] | None = None) -> str | None:
    damon_home = get_damon_home_override() or (env or {}).get("DAMON_HOME") or os.getenv("DAMON_HOME")
    if not damon_home:
        return None
    profile_home = os.path.join(damon_home, "home")
    if os.path.isdir(profile_home):
        return profile_home
    return None


def _is_profile_home(candidate: str | None, profile_home: str | None) -> bool:
    return bool(candidate and profile_home and _norm_home_path(candidate) == _norm_home_path(profile_home))


def _iter_real_home_candidates(env: dict[str, str] | None = None) -> list[str]:
    env = env or {}
    candidates: list[str] = []
    explicit = str(env.get("DAMON_REAL_HOME") or os.getenv("DAMON_REAL_HOME", "")).strip()
    if explicit:
        candidates.append(explicit)
    home = str(env.get("HOME") or os.getenv("HOME", "")).strip()
    if home:
        candidates.append(home)
    try:
        import pwd

        pw_home = pwd.getpwuid(os.getuid()).pw_dir.strip()
        if pw_home:
            candidates.append(pw_home)
    except Exception:
        pass
    userprofile = str(env.get("USERPROFILE") or os.getenv("USERPROFILE", "")).strip()
    if userprofile:
        candidates.append(userprofile)
    drive = str(env.get("HOMEDRIVE") or os.getenv("HOMEDRIVE", "")).strip()
    path = str(env.get("HOMEPATH") or os.getenv("HOMEPATH", "")).strip()
    if drive and path:
        candidates.append(f"{drive}{path}" if path.startswith(("\\", "/")) else os.path.join(drive, path))
    expanded = os.path.expanduser("~")
    if expanded and expanded != "~":
        candidates.append(expanded)
    return candidates


def get_real_home(env: dict[str, str] | None = None) -> str:
    profile_home = _profile_home_path(env)
    seen: set[str] = set()
    for candidate in _iter_real_home_candidates(env):
        key = _norm_home_path(candidate)
        if not key or key in seen:
            continue
        seen.add(key)
        if not _is_profile_home(candidate, profile_home):
            return candidate
    return "/tmp"


def get_subprocess_home(env: dict[str, str] | None = None) -> str | None:
    env = env or {}
    profile_home = _profile_home_path(env)
    mode = str(env.get("TERMINAL_HOME_MODE") or os.getenv("TERMINAL_HOME_MODE", "auto")).strip().lower() or "auto"
    if mode in {"isolated", "profile_home", "profile-home"}:
        mode = "profile"
    if mode in {"host", "user", "real_home", "real-home"}:
        mode = "real"

    if mode == "profile":
        return profile_home

    real_home = get_real_home(env)
    current_home = str(env.get("HOME") or os.getenv("HOME", "")).strip()
    if mode == "real":
        return real_home if _norm_home_path(real_home) != _norm_home_path(current_home) else None

    if profile_home and is_container():
        return profile_home
    if _is_profile_home(current_home, profile_home):
        return real_home if _norm_home_path(real_home) != _norm_home_path(current_home) else None
    return None


def apply_subprocess_home_env(env: dict[str, str]) -> None:
    real_home = get_real_home(env)
    if real_home:
        env["DAMON_REAL_HOME"] = real_home
    home = get_subprocess_home(env)
    if home:
        env["HOME"] = home


VALID_REASONING_EFFORTS = ("minimal", "low", "medium", "high", "xhigh")


def parse_reasoning_effort(effort: str) -> dict | None:
    if not effort or not effort.strip():
        return None
    effort = effort.strip().lower()
    if effort == "none":
        return {"enabled": False}
    if effort in VALID_REASONING_EFFORTS:
        return {"enabled": True, "effort": effort}
    return None


def is_termux() -> bool:
    prefix = os.getenv("PREFIX", "")
    return bool(os.getenv("TERMUX_VERSION") or "com.termux/files/usr" in prefix)


_wsl_detected: bool | None = None


def is_wsl() -> bool:
    global _wsl_detected
    if _wsl_detected is not None:
        return _wsl_detected
    try:
        with open("/proc/version", "r", encoding="utf-8") as f:
            _wsl_detected = "microsoft" in f.read().lower()
    except Exception:
        _wsl_detected = False
    return _wsl_detected


_container_detected: bool | None = None


def is_container() -> bool:
    global _container_detected
    if _container_detected is not None:
        return _container_detected
    if os.path.exists("/.dockerenv"):
        _container_detected = True
        return True
    if os.path.exists("/run/.containerenv"):
        _container_detected = True
        return True
    if os.getenv("KUBERNETES_SERVICE_HOST"):
        _container_detected = True
        return True
    try:
        with open("/proc/1/cgroup", "r", encoding="utf-8") as f:
            cgroup = f.read()
            if any(token in cgroup for token in ("docker", "podman", "/lxc/", "kubepods")):
                _container_detected = True
                return True
    except OSError:
        pass
    try:
        with open("/proc/self/mountinfo", "r", encoding="utf-8") as f:
            mountinfo = f.read()
            if any(token in mountinfo for token in ("overlay", "containerd")):
                _container_detected = True
                return True
    except OSError:
        pass
    _container_detected = False
    return False


# ─── Well-Known Paths ─────────────────────────────────────────────────────────


def get_config_path() -> Path:
    return get_damon_home() / "config.yaml"


def get_skills_dir() -> Path:
    return get_damon_home() / "skills"


def get_env_path() -> Path:
    return get_damon_home() / ".env"


# ─── Network Preferences ─────────────────────────────────────────────────────


def apply_ipv4_preference(force: bool = False) -> None:
    if not force:
        return
    import socket

    if getattr(socket.getaddrinfo, "_damon_ipv4_patched", False):
        return
    _original_getaddrinfo = socket.getaddrinfo

    def _ipv4_getaddrinfo(host, port, family=0, type=0, proto=0, flags=0):
        if family == 0:
            try:
                return _original_getaddrinfo(
                    host, port, socket.AF_INET, type, proto, flags
                )
            except socket.gaierror:
                return _original_getaddrinfo(host, port, family, type, proto, flags)
        return _original_getaddrinfo(host, port, family, type, proto, flags)

    _ipv4_getaddrinfo._damon_ipv4_patched = True  # type: ignore[attr-defined]
    socket.getaddrinfo = _ipv4_getaddrinfo  # type: ignore[assignment]


# ─── Streaming Response Constants ────────────────────────────────────────────

PARTIAL_STREAM_STUB_ID = "partial-stream-stub"
FINISH_REASON_LENGTH = "length"

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
OPENROUTER_MODELS_URL = f"{OPENROUTER_BASE_URL}/models"

DAMON_HOME = get_damon_home()
DEFAULT_CONFIG_DIR = get_damon_home() / "config"
DEFAULT_DATA_DIR = get_damon_home() / "data"
DEFAULT_LOG_DIR = get_damon_home() / "logs"
DEFAULT_SESSIONS_DIR = get_damon_home() / "sessions"
DEFAULT_SKILLS_DIR = get_damon_home() / "skills"
DEFAULT_MEMORY_DIR = get_damon_home() / "memory"
DEFAULT_CRON_DIR = get_damon_home() / "cron"
DEFAULT_STATE_FILE = get_damon_home() / "state.json"
DEFAULT_SOUL_FILE = get_damon_home() / "soul.md"
DEFAULT_PERSONA_FILE = get_damon_home() / "persona.md"
