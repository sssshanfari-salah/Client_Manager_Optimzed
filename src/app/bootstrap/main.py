"""Application entry point for the staged Client Manager package layout.

This keeps the repository compatible with the refactor while preserving the
legacy "python code" tree as a rollback-safe fallback.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
SRC_ROOT = PROJECT_ROOT / "src"

for candidate in (str(SRC_ROOT),):
    if candidate not in sys.path:
        sys.path.insert(0, candidate)


def launch_reservation_form():
    from app.ui.windows.ui_reservation_contract import ShopReservationForm

    form = ShopReservationForm()
    form.mainloop()
    return form


def main(argv=None):
    parser = argparse.ArgumentParser(description="Starco Client Manager")
    parser.add_argument(
        "--reservation-form",
        "--contract-form",
        action="store_true",
        dest="reservation_form",
        help="Open the reservation contract form instead of the main dashboard.",
    )
    args = parser.parse_args(argv)

    if args.reservation_form:
        launch_reservation_form()
        return 0

    from app.ui.windows.clients_progress_ui import safe_main

    safe_main()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
