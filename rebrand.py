#!/usr/bin/env python3
"""
Comprehensive rebrand: Damon → Damon
Handles: directory renames, file renames, content replacement, import updates
"""
import os
import re
import shutil
from pathlib import Path

ROOT = Path("/home/ubuntu/damon")

# Directories to rename
DIR_RENAMES = {
    "damon_cli": "damon_cli",
    ".damon": ".damon",
}

# Files to rename
FILE_RENAMES = {
    "damon_logging.py": "damon_logging.py",
    "damon_constants.py": "damon_constants.py",
    "damon_state.py": "damon_state.py",
    "damon_time.py": "damon_time.py",
    "damon_bootstrap.py": "damon_bootstrap.py",
    "damon": "damon",  # executable
    "damon-already-has-routines.md": "damon-already-has-routines.md",
}

# Text replacements (order matters - longer/more specific first)
REPLACEMENTS = [
    # Package/module imports (most specific first)
    ("damon_cli.", "damon_cli."),
    ("damon_cli", "damon_cli"),
    ("damon_agent", "damon_agent"),
    
    # Constants / env vars
    ("DAMON_HOME", "DAMON_HOME"),
    ("DAMON_CONFIG", "DAMON_CONFIG"),
    ("DAMON_", "DAMON_"),
    
    # Class/function names
    ("DamonAgent", "DamonAgent"),
    ("DamonConfig", "DamonConfig"),
    ("DamonLogger", "DamonLogger"),
    ("DamonState", "DamonState"),
    ("DamonTime", "DamonTime"),
    ("DamonBootstrap", "DamonBootstrap"),
    ("damon_home", "damon_home"),
    ("damon_config", "damon_config"),
    ("damon_logging", "damon_logging"),
    ("damon_constants", "damon_constants"),
    ("damon_state", "damon_state"),
    ("damon_time", "damon_time"),
    ("damon_bootstrap", "damon_bootstrap"),
    
    # CLI command references
    ("damon ", "damon "),
    (" damon", " damon"),
    ("'damon'", "'damon'"),
    ('"damon"', '"damon"'),
    ("`damon`", "`damon`"),
    
    # Paths
    ("~/.damon", "~/.damon"),
    (".damon/", ".damon/"),
    ("/damon/", "/damon/"),
    
    # General brand references
    ("Damon Agent", "Damon Agent"),
    ("Damon agent", "Damon agent"),
    ("Damon", "Damon"),
    ("damon", "damon"),
    ("DAMON", "DAMON"),
]

# Files to SKIP (binary, generated, or external)
SKIP_PATTERNS = [
    "node_modules",
    ".git",
    "__pycache__",
    "*.egg-info",
    "*.png", "*.jpg", "*.jpeg", "*.gif", "*.ico", "*.woff2", "*.svg",
    "*.pyc", "*.pyo", "*.so", "*.dll", "*.dylib",
    "*.lock", "*.sum",
    "dist/", "build/",
    ".venv/", "venv/", "env/",
]

def should_skip(path: Path) -> bool:
    path_str = str(path)
    for pattern in SKIP_PATTERNS:
        if pattern.endswith("/"):
            if pattern[:-1] in path_str.split(os.sep):
                return True
        elif "*" in pattern:
            ext = pattern[1:]
            if path_str.endswith(ext):
                return True
        elif pattern in path_str:
            return True
    return False

def rename_directories():
    """Rename directories"""
    for old, new in DIR_RENAMES.items():
        old_path = ROOT / old
        new_path = ROOT / new
        if old_path.exists() and not new_path.exists():
            print(f"  Renaming dir: {old} → {new}")
            shutil.move(str(old_path), str(new_path))
        elif new_path.exists():
            print(f"  Dir {new} already exists, skipping {old}")

def rename_files():
    """Rename files"""
    for old, new in FILE_RENAMES.items():
        old_path = ROOT / old
        new_path = ROOT / new
        if old_path.exists() and not new_path.exists():
            print(f"  Renaming file: {old} → {new}")
            shutil.move(str(old_path), str(new_path))
        elif new_path.exists():
            print(f"  File {new} already exists, skipping {old}")

def replace_in_file(filepath: Path):
    """Replace text in a single file"""
    try:
        content = filepath.read_text(encoding="utf-8")
        original = content
        
        for old, new in REPLACEMENTS:
            content = content.replace(old, new)
        
        if content != original:
            filepath.write_text(content, encoding="utf-8")
            return True
    except UnicodeDecodeError:
        pass  # Binary file
    except Exception as e:
        print(f"  Error processing {filepath}: {e}")
    return False

def process_all_files():
    """Walk and process all text files"""
    count = 0
    for filepath in ROOT.rglob("*"):
        if filepath.is_file() and not should_skip(filepath):
            if replace_in_file(filepath):
                count += 1
                print(f"  Updated: {filepath.relative_to(ROOT)}")
    return count

def fix_python_imports():
    """Fix Python imports after rename"""
    # Find all .py files
    for py_file in (ROOT / "damon_cli").rglob("*.py"):
        if py_file.is_file():
            try:
                content = py_file.read_text(encoding="utf-8")
                # Fix any remaining damon_cli imports
                content = re.sub(r"from damon_cli\.", "from damon_cli.", content)
                content = re.sub(r"import damon_cli\.", "import damon_cli.", content)
                py_file.write_text(content, encoding="utf-8")
            except Exception as e:
                print(f"  Error fixing imports in {py_file}: {e}")

    for py_file in (ROOT / "agent").rglob("*.py"):
        if py_file.is_file():
            try:
                content = py_file.read_text(encoding="utf-8")
                content = re.sub(r"from damon_cli\.", "from damon_cli.", content)
                content = re.sub(r"import damon_cli\.", "import damon_cli.", content)
                content = re.sub(r"from damon_logging", "from damon_logging", content)
                content = re.sub(r"import damon_logging", "import damon_logging", content)
                content = re.sub(r"from damon_constants", "from damon_constants", content)
                content = re.sub(r"import damon_constants", "import damon_constants", content)
                content = re.sub(r"from damon_state", "from damon_state", content)
                content = re.sub(r"import damon_state", "import damon_state", content)
                content = re.sub(r"from damon_time", "from damon_time", content)
                content = re.sub(r"import damon_time", "import damon_time", content)
                content = re.sub(r"from damon_bootstrap", "from damon_bootstrap", content)
                content = re.sub(r"import damon_bootstrap", "import damon_bootstrap", content)
                py_file.write_text(content, encoding="utf-8")
            except Exception as e:
                print(f"  Error fixing imports in {py_file}: {e}")

    for py_file in ROOT.glob("*.py"):
        if py_file.is_file():
            try:
                content = py_file.read_text(encoding="utf-8")
                content = re.sub(r"from damon_logging", "from damon_logging", content)
                content = re.sub(r"import damon_logging", "import damon_logging", content)
                content = re.sub(r"from damon_constants", "from damon_constants", content)
                content = re.sub(r"import damon_constants", "import damon_constants", content)
                content = re.sub(r"from damon_state", "from damon_state", content)
                content = re.sub(r"import damon_state", "import damon_state", content)
                content = re.sub(r"from damon_time", "from damon_time", content)
                content = re.sub(r"import damon_time", "import damon_time", content)
                content = re.sub(r"from damon_bootstrap", "from damon_bootstrap", content)
                content = re.sub(r"import damon_bootstrap", "import damon_bootstrap", content)
                content = re.sub(r"from damon_cli\.", "from damon_cli.", content)
                content = re.sub(r"import damon_cli\.", "import damon_cli.", content)
                py_file.write_text(content, encoding="utf-8")
            except Exception as e:
                print(f"  Error fixing imports in {py_file}: {e}")

def update_setup_py():
    """Check for setup.py / pyproject.toml / MANIFEST.in"""
    for f in ["setup.py", "pyproject.toml", "MANIFEST.in", "setup.cfg"]:
        p = ROOT / f
        if p.exists():
            print(f"  Found {f} - may need manual review")

def main():
    print("=" * 60)
    print("REBRAND: Damon → Damon")
    print("=" * 60)
    
    print("\n1. Renaming directories...")
    rename_directories()
    
    print("\n2. Renaming files...")
    rename_files()
    
    print("\n3. Replacing text in all files...")
    updated = process_all_files()
    print(f"  Updated {updated} files")
    
    print("\n4. Fixing Python imports...")
    fix_python_imports()
    
    print("\n5. Checking setup files...")
    update_setup_py()
    
    print("\n" + "=" * 60)
    print("REBRAND COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    main()