"""Report and export action handlers for the main client manager window."""

from tkinter import messagebox

from app.i18n.translations import T


class ReportActions:
    """Handlers for report and export flows."""

    def export_client_log(self):
        messagebox.showinfo(T("Export Clients Log"), T("Export action is available in the dedicated report windows."))

    def export_task_log(self):
        messagebox.showinfo(T("Export Task Log"), T("Task export is wired through the report windows."))

    def open_payment_report_window(self):
        messagebox.showinfo(T("Payment Report"), T("The payment report window is managed in the dedicated UI module."))

    def open_transactions_window(self):
        messagebox.showinfo(T("Transactions"), T("The transactions window is managed in the dedicated UI module."))
