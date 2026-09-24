"""Public UI facade that re-exports the split window modules.

The app's window classes are now organized by concern into smaller dedicated files,
while this module keeps the legacy import surface stable for older code paths.
"""

from ui_shared import APP_ICON, WelcomeWindow, build_startup_splash, open_overview_window, open_welcome_home, safe_main
from ui_main_app import ProgressApp
from ui_client_windows import AllClientsProgressWindow, ClientDetailsWindow
from ui_task_windows import (
    ClientPaymentReportWindow,
    ClientTransactionsWindow,
    ContractDetailsWindow,
    ReservationContractWindow,
    TaskDetailsWindow,
)
from ui_report_windows import (
    ClientLogPreviewWindow,
    ClientReviewsLogWindow,
    ExportClientsLogWindow,
    ExportReviewLogWindow,
    ExportTaskLogWindow,
)

__all__ = [
    "APP_ICON",
    "WelcomeWindow",
    "ProgressApp",
    "TaskDetailsWindow",
    "ContractDetailsWindow",
    "ReservationContractWindow",
    "ClientDetailsWindow",
    "AllClientsProgressWindow",
    "ClientLogPreviewWindow",
    "ClientPaymentReportWindow",
    "ClientTransactionsWindow",
    "ExportClientsLogWindow",
    "ExportTaskLogWindow",
    "ExportReviewLogWindow",
    "ClientReviewsLogWindow",
    "build_startup_splash",
    "open_overview_window",
    "open_welcome_home",
    "safe_main",
]
