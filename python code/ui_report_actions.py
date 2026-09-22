"""Report and export actions for the main application window."""

from tkinter import messagebox

from translations import T


class ReportExportMixin:
    """Methods for printing and exporting data snapshots."""

    def export_client_log(self):
        messagebox.showinfo(T("Export Clients Log"), T("Export action is available in the dedicated report windows."))

    def export_task_log(self):
        messagebox.showinfo(T("Export Task Log"), T("Task export is wired through the report windows."))

    def open_payment_report_window(self):
        messagebox.showinfo(T("Payment Report"), T("The payment report window is managed in the dedicated UI module."))

    def open_transactions_window(self):
        messagebox.showinfo(T("Transactions"), T("The transactions window is managed in the dedicated UI module."))
