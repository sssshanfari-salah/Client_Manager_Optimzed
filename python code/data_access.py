"""File and data-access helpers for the client manager app."""

from pathlib import Path
import sys


def resolve_log_output_dir(log_type="general"):
    root_dir = Path(__file__).resolve().parent.parent
    if getattr(sys, "_MEIPASS", None):
        root_dir = Path(sys._MEIPASS)
    output_root = root_dir / "application_outputs"
    target_dir = output_root / str(log_type).strip().strip("/") if str(log_type).strip() else output_root
    target_dir.mkdir(parents=True, exist_ok=True)
    return target_dir


__all__ = ["resolve_log_output_dir"]
