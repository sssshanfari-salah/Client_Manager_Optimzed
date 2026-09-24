"""Simple compatibility launcher for the staged app bootstrap package."""

from __future__ import annotations

from app.bootstrap.main import main


if __name__ == "__main__":
    raise SystemExit(main())
