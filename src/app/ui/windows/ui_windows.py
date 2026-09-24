"""Compatibility shim for the legacy ui_windows module.

This stays intentionally thin while the real window implementations are moved into
src/app/ui/windows and migrated to app.* imports. It ensures older callers keep
working during the staged refactor without forcing a single-step rewrite.
"""

from app.ui.windows.ui_main_app import *  # noqa: F401,F403
from app.ui.windows.ui_client_windows import *  # noqa: F401,F403
from app.ui.windows.ui_task_windows import *  # noqa: F401,F403
from app.ui.windows.ui_report_windows import *  # noqa: F401,F403
from app.ui.windows.ui_reservation_contract import *  # noqa: F401,F403
from app.ui.windows.clients_progress_ui import *  # noqa: F401,F403
