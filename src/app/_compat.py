"""Compatibility helpers used during the staged package migration.

The legacy source tree is intentionally kept in place to preserve rollback safety,
while the app package provides a cleaner import surface for the refactor. These
helpers reduce repeated boilerplate without removing the fallback path.
"""

from __future__ import annotations

import sys
from pathlib import Path


def resolve_legacy_dir() -> Path:
    """Find the root-level legacy source directory without relying on fragile parent indexes."""
    start = Path(__file__).resolve().parent
    for candidate in (start, *start.parents):
        legacy_dir = candidate / "python code"
        if legacy_dir.exists() and legacy_dir.is_dir():
            return legacy_dir
    raise FileNotFoundError(
        "Unable to locate the legacy 'python code' directory. "
        "Rollback safety requires that the original source tree remain present."
    )


def ensure_legacy_path() -> Path:
    legacy_dir = resolve_legacy_dir()
    legacy_path = str(legacy_dir)
    if legacy_path not in sys.path:
        sys.path.insert(0, legacy_path)
    return legacy_dir


def reexport_legacy_module(module_name: str):
    """Import the legacy module under the new app namespace while keeping the original tree intact."""
    ensure_legacy_path()
    module = __import__(module_name, fromlist=["*"])
    globals().update({name: getattr(module, name) for name in dir(module) if not name.startswith("__")})
    return module
